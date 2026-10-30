#!/usr/bin/env python3
"""nm000465 fix-20261030: stop-signal task events from the TTL channel and the behaviour files.

Deterministic port of the authors' import function (Diesburg; `functions/ImportRawData.m` in
sourcedata/zenodo-4784092/functions.zip), applied to the BIDS stop-signal runs:
  * trigger channel `Inpt_RZ2_chn001`; sub-118: the 24 kHz TTL run (acq-fs24000ttl), resampled 2/24 as in the code
    (scipy.signal.resample_poly, the counterpart of MATLAB resample) onto the 2 kHz LFP run (acq-fs2000);
  * bigsamples = samples > 1; triggers = the last sample of each run of consecutive bigsamples, minus 3 samples
    (MATLAB `bigsamples(logical([diff(bigsamples)>1; 1]))-3`, converted to 0-based samples);
  * sub-101: first trigger deleted; sub-104: triggers 257 onwards deleted (as in the code);
  * expected count = n_trials x 4/3 (one trigger per go trial, two per stop trial); a run whose count differs is
    left without task events and reported (the code stops with 'Triggers and trials mismatch');
  * negative stop-signal delays set to 0 (as in the code);
  * events: GoStimulus at each go trigger; StopStimulus at the go trigger + SSD of the trial's side (column 5 for
    side 1, column 6 for side 2) x srate / 1000 (the code's correction: "trigger sent at time not SSD"); Response at
    the go trigger + round(RT) x srate / 1000 for go triggers with RT > 0.
  * srate: 24000 for subjects 101, 104, 105, 106, else 2000 (as in the code); checked against the run's header.
The TDT epoc rows already in events.tsv are kept; task rows are added with extra columns. Output: one events.tsv per
stop-signal run, a report JSON. Usage: fix-20261030_stopsignal_events.py <dataset root (with annexed content)> <report>

Partial recordings (added for sub-116, which the authors excluded before import: StopOR_initialize.m removes
datasets([11 20]) = Subject_116 and Subject_128 by sorted file order). When the trigger count differs from the code's
expectation, the run is aligned only if the alignment is unique and exact, else it is left without task events:
  * completed behaviour trials = the leading rows with a recorded outcome (acc != 0; Audiostop.m saves trialseq at the
    end of every trial, so rows of trials that never ran stay all-zero apart from their design columns);
  * the TTL trigger train is split into trials: a trigger followed by a second one < 1.05 s later is a stop trial
    (go trigger + stop trigger; the task's SSD maximum is 1000 ms and trials last 4 s), otherwise a go trial;
  * every contiguous placement (TTL trial offset o, behaviour row offset b) is scored over its overlap: identical
    go/stop sequence and trial-onset intervals equal to the behaviour `time` column intervals within 25 ms each;
  * accepted only if exactly one placement covers all completed rows; triggers outside it must be at most one
    trailing go trigger (a trial started after the last saved one, e.g. at the end of the recording), reported.
"""
import csv, glob, io, json, os, re, sys
import numpy as np
import scipy.io as sio
from scipy.signal import resample_poly

root, report_path = sys.argv[1], sys.argv[2]
COL = dict(num=0, blo=1, dir=2, stop=3, lssd=4, rssd=5, resp=6, rt=7, acc=8, time=9)  # Basicstop_columns (1-based -1)


def vhdr_info(vhdr):
    txt = open(vhdr, encoding="utf-8", errors="replace").read()
    nch = int(re.search(r"NumberOfChannels=(\d+)", txt).group(1))
    fs = 1e6 / float(re.search(r"SamplingInterval=([0-9.]+)", txt).group(1))
    fmt = re.search(r"BinaryFormat=(\w+)", txt).group(1)
    names = [re.match(r"Ch\d+=([^,]*)", l).group(1) for l in txt.splitlines() if re.match(r"Ch\d+=", l)][:nch]
    df = re.search(r"DataFile=(.*)", txt).group(1).strip()
    return nch, fs, fmt, names, os.path.join(os.path.dirname(vhdr), df)


def channel(vhdr, name):
    nch, fs, fmt, names, eeg = vhdr_info(vhdr)
    dt = {"IEEE_FLOAT_32": "<f4", "INT_16": "<i2"}[fmt]
    a = np.memmap(eeg, dtype=dt, mode="r")
    return np.asarray(a.reshape(-1, nch)[:, names.index(name)], dtype=np.float64), fs


def align_partial(trig, ts, srate, pair_s=1.05, tol_ms=25.0):
    """Unique exact placement of the TTL trial train on the completed behaviour rows (see module docstring)."""
    done = int(np.argmin(ts[:, COL["acc"]] != 0)) if (ts[:, COL["acc"]] == 0).any() else len(ts)
    if done == 0 or (ts[done:, COL["acc"]] != 0).any():
        return dict(status="no_completed_prefix", n_completed=done)
    kinds, first_trig, i = [], [], 0
    while i < len(trig):
        if i + 1 < len(trig) and (trig[i + 1] - trig[i]) / srate < pair_s:
            kinds.append(1); first_trig.append(i); i += 2
        else:
            kinds.append(0); first_trig.append(i); i += 1
    kinds = np.array(kinds); on = trig[first_trig] / srate
    bk = ts[:done, COL["stop"]].astype(int); bt = ts[:done, COL["time"]]
    fits = []
    placements = [(o, 0) for o in range(len(kinds))] + [(0, b) for b in range(1, done)]  # one per relative shift
    for o, b in placements:
        n = min(len(kinds) - o, done - b)
        if n < 10:
            continue
        if not np.array_equal(kinds[o:o + n], bk[b:b + n]):
            continue
        dev = np.abs(np.diff(on[o:o + n]) - np.diff(bt[b:b + n])) * 1000
        if dev.max() <= tol_ms:
            fits.append(dict(ttl_trial=o, row=b, n=int(n), max_interval_dev_ms=float(dev.max()),
                             median_interval_dev_ms=float(np.median(dev))))
    full = [f for f in fits if f["row"] == 0 and f["n"] == done]
    out = dict(n_completed=done, n_ttl_trials=int(len(kinds)), n_ttl_stop=int(kinds.sum()), n_fits=len(fits),
               fits=fits[:20], tol_ms=tol_ms, pair_s=pair_s)
    if len(fits) != 1 or len(full) != 1:
        out["status"] = "ambiguous_or_none"; return out
    f = full[0]; o = f["ttl_trial"]
    t0 = first_trig[o]; t1 = first_trig[o + done - 1] + (1 if kinds[o + done - 1] == 1 else 0)
    left = list(range(0, t0)) + list(range(t1 + 1, len(trig)))
    if not (len(left) == 0 or (left == [len(trig) - 1] and kinds[-1] == 0)):
        out["status"] = "unexplained_triggers"; out["left"] = left; return out
    gaps = [(trig[first_trig[o + k] + 1] - trig[first_trig[o + k]]) / srate * 1000 - (ts[k, COL["lssd"]] if ts[k, COL["dir"]] == 1 else ts[k, COL["rssd"]])
            for k in range(done) if kinds[o + k] == 1]
    out.update(status="aligned", trigger_first=int(t0), trigger_last=int(t1), row_first=0, row_last=done - 1,
               unmatched_triggers=[dict(index=int(j), onset_s=float(trig[j] / srate),
                                        s_after_previous=float((trig[j] - trig[j - 1]) / srate)) for j in left],
               stop_gap_minus_ssd_ms=dict(min=float(np.min(gaps)), median=float(np.median(gaps)), max=float(np.max(gaps))))
    return out


rep = {}
for beh in sorted(glob.glob(f"{root}/sourcedata/dryad-gf1vhhmq0/behav/Subject_*.mat")):
    sn = re.search(r"Subject_(\d+)\.mat", beh).group(1)
    sub = f"sub-{sn}"
    runs = sorted(glob.glob(f"{root}/{sub}/ieeg/{sub}_task-stopsignal*_ieeg.vhdr"))
    lfp = [r for r in runs if "ttl" not in os.path.basename(r)]
    ttl = [r for r in runs if "ttl" in os.path.basename(r)] or lfp
    if len(lfp) != 1:
        rep[sub] = dict(status="skipped", reason=f"{len(lfp)} non-TTL stop-signal runs"); continue
    lfp, ttl = lfp[0], ttl[0]
    try:
        trig, fs_t = channel(ttl, "Inpt_RZ2_chn001")
    except Exception as e:
        rep[sub] = dict(status="skipped", reason=f"no Inpt_RZ2_chn001: {e}"); continue
    _, fs_l, _, _, _ = vhdr_info(lfp)
    srate = 24000 if sn in ("101", "104", "105", "106") else 2000
    if abs(fs_l - srate) > 1e-6:
        rep[sub] = dict(status="skipped", reason=f"header rate {fs_l} != code srate {srate}"); continue
    if fs_t != fs_l:
        if round(fs_t) == 24000 and srate == 2000:
            trig = resample_poly(trig, 2, 24)
        else:
            rep[sub] = dict(status="skipped", reason=f"TTL rate {fs_t} vs LFP {fs_l}"); continue
    big = np.flatnonzero(trig > 1)                       # 0-based
    if big.size == 0:
        rep[sub] = dict(status="skipped", reason="no samples > 1 in Inpt_RZ2_chn001"); continue
    last = big[np.r_[np.diff(big) > 1, True]]
    triggers = list(last - 3)
    if sn == "101":
        triggers = triggers[1:]
    if sn == "104":
        triggers = triggers[:256]
    ts = sio.loadmat(beh)["trialseq"].astype(float)
    expected = len(ts) + len(ts) / 3
    partial = None
    if expected != len(triggers):
        partial = align_partial(np.asarray(triggers), ts, srate)
        if partial["status"] != "aligned":
            rep[sub] = dict(status="mismatch", n_triggers=len(triggers), n_trials=len(ts), expected=expected,
                            alignment=partial); continue
        triggers = triggers[partial["trigger_first"]:partial["trigger_last"] + 1]
        ts = ts[partial["row_first"]:partial["row_last"] + 1]
        assert len(triggers) == len(ts) + int((ts[:, COL["stop"]] == 1).sum())
    ts[ts[:, COL["lssd"]] < 0, COL["lssd"]] = 0
    ts[ts[:, COL["rssd"]] < 0, COL["rssd"]] = 0
    cls, tnum = [], []
    for it in range(len(ts)):
        if ts[it, COL["stop"]] == 0:
            cls.append(0); tnum.append(it)
        elif ts[it, COL["stop"]] == 1:
            cls += [0, 1]; tnum += [it, it]
    ev = []
    for i, lat in enumerate(triggers):
        t = ts[tnum[i]]
        row = dict(trial=int(t[COL["num"]]), block=int(t[COL["blo"]]), side=int(t[COL["dir"]]), stop_trial=int(t[COL["stop"]]),
                   resp_side=int(t[COL["resp"]]), rt=float(t[COL["rt"]]), acc=int(t[COL["acc"]]))
        if cls[i] == 0:
            ev.append(dict(row, trial_type="GoStimulus", sample=int(lat)))
            if t[COL["rt"]] > 0:
                ev.append(dict(row, trial_type="Response", sample=int(lat + round(t[COL["rt"]]) * srate / 1000)))
        else:
            ssd = t[COL["lssd"]] if t[COL["dir"]] == 1 else t[COL["rssd"]]
            go = triggers[i - 1]
            ev.append(dict(row, trial_type="StopStimulus", sample=int(round(go + ssd * srate / 1000)), ssd=float(ssd),
                           stop_trigger_sample=int(lat)))
    ev.sort(key=lambda e: e["sample"])
    evf = lfp.replace("_ieeg.vhdr", "_events.tsv")
    old = list(csv.DictReader(open(evf), delimiter="\t"))
    cols = ["onset", "duration", "trial_type", "value", "sample", "trial", "block", "side", "stop_trial", "ssd",
            "resp_side", "rt", "acc", "stop_trigger_sample"]
    out = []
    for o in old:
        out.append({c: o.get(c, "n/a") for c in cols})
    for e in ev:
        out.append(dict(onset=f"{e['sample'] / srate:.6f}", duration="0", trial_type=e["trial_type"], value="n/a",
                        sample=str(e["sample"]), trial=str(e["trial"]), block=str(e["block"]), side=str(e["side"]),
                        stop_trial=str(e["stop_trial"]), ssd=(f"{e['ssd']:g}" if "ssd" in e else "n/a"),
                        resp_side=str(e["resp_side"]), rt=f"{e['rt']:g}", acc=str(e["acc"]),
                        stop_trigger_sample=str(e.get("stop_trigger_sample", "n/a"))))
    for o in out:
        for c in cols:
            if o.get(c) in (None, ""):
                o[c] = "n/a"
    out.sort(key=lambda r: float(r["onset"]))
    buf = io.StringIO(); w = csv.DictWriter(buf, fieldnames=cols, delimiter="\t", lineterminator="\n"); w.writeheader(); w.writerows(out)
    open(evf, "w", newline="").write(buf.getvalue())
    _, fs_chk, _, _, _ = vhdr_info(lfp)
    nsamp = os.path.getsize(vhdr_info(lfp)[4]) // (vhdr_info(lfp)[0] * (4 if vhdr_info(lfp)[2] == "IEEE_FLOAT_32" else 2))
    rep[sub] = dict(status="ok", run=os.path.basename(lfp), ttl_run=os.path.basename(ttl), n_trials=len(ts),
                    n_triggers=len(triggers), n_go=sum(e["trial_type"] == "GoStimulus" for e in ev),
                    n_stop=sum(e["trial_type"] == "StopStimulus" for e in ev),
                    n_resp=sum(e["trial_type"] == "Response" for e in ev),
                    first_s=ev[0]["sample"] / srate, last_s=ev[-1]["sample"] / srate, n_samples=int(nsamp),
                    all_inside=bool(all(0 <= e["sample"] < nsamp for e in ev)))
    if partial is not None:
        rep[sub]["partial_alignment"] = partial
    print(sub, rep[sub], flush=True)
json.dump(rep, open(report_path, "w"), indent=1)
print("subjects", len(rep), {s: v["status"] for s, v in rep.items()})
