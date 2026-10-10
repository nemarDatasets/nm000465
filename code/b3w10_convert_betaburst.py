"""d3-dryad-beta-burst (Dryad doi:10.5061/dryad.gf1vhhmq0; Diesburg, Greenlee & Wessel, eLife 2021, doi:10.7554/eLife.70270) -> BIDS-iEEG.
Source: data.zip (TDT RZ2 exports as MATLAB structs, one file per subject: data/main = stop-signal task, data/localizers =
go-only localizer), behav.zip, DataREADME.txt; channel -> location from getchans.m / getlocchans.m in the authors' code
(Zenodo doi:10.5281/zenodo.4784092, functions.zip, CC-BY-4.0).
Per file every struct with a 'dat' field is one channel (LFPx_RZ2_chnNNN = recording channels, Inpt_RZ2_chnNNN = analog TTL
inputs, written as TRIG channels); structs with 'evnt' + 'time' are TDT epoc stores -> events.tsv. Values unchanged
(float32; units not stated -> n/a). Channel types: STN/VIM LFP = DBS; 'subgaleal' strips (under the scalp, outside the skull;
DataREADME) = EEG.
Privacy: the TDT 'tank' strings hold a recording date (pt<id><yymmdd>...); sourcedata copies are re-saved with day 01.
Usage: python b3w10_convert_betaburst.py <sourcedata_dl> <bids root>"""
import glob, io, json, os, re, shutil, sys, zipfile
import numpy as np, scipy.io as sio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from b3w10_common import write_run, wtsv, wjson, sha256_file, scrub_mat_header, mat_strings, flag_strings

SRC, OUT = sys.argv[1], sys.argv[2]
W = os.path.dirname(SRC.rstrip("/"))
X_ = os.path.join(W, "extract")
ZC = os.path.join(W, "sourcedata", "zenodo-4784092")
fz = zipfile.ZipFile(os.path.join(ZC, "functions.zip"))
def parse_chans(member):
    txt = fz.read([n for n in fz.namelist() if n.endswith(member)][0]).decode("latin-1")
    out = {}
    for blk in re.split(r"(?:else)?if\s+strcmpi\(subnum,\s*'", txt)[1:]:
        sid = blk[:blk.index("'")]
        out[sid] = dict(re.findall(r"'((?:LFPx|Inpt)_RZ2_chn\d+)'\s*,\s*'([^']*)'", blk))
    return out
CH = {"main": parse_chans("getchans.m"), "localizers": parse_chans("getlocchans.m")}
report = {"runs": [], "chanmaps": CH, "privacy": {}, "unmapped": []}
SD = os.path.join(OUT, "sourcedata", "dryad-gf1vhhmq0")
DAYRE = re.compile(r"(pt\d{3})(\d\d)(\d\d)(\d\d)")


def scrub(v):
    if isinstance(v, str):
        return DAYRE.sub(lambda q: q[1] + q[2] + q[3] + "01", v)
    return v


def chtype(label):
    l = label.lower()
    if "subgaleal" in l: return "EEG"
    if "stn" in l or "vim" in l or "thal" in l: return "DBS"
    return "MISC"


scans = {}
seen_stems = set()
for kind, task in (("main", "stopsignal"), ("localizers", "localizer")):
    for p in sorted(glob.glob(os.path.join(X_, "data", kind, "Subject_*.mat"))):
        base = os.path.basename(p)[:-4]
        m_ = re.fullmatch(r"Subject_(\d+)(?:_(\d+))?", base)
        sid, part = m_.group(1), m_.group(2)
        sub = f"sub-{sid}"
        m = sio.loadmat(p, squeeze_me=True, struct_as_record=False)
        chans, epocs = {}, {}
        for k, v in m.items():
            if k.startswith("__") or not hasattr(v, "_fieldnames"):
                continue
            if "dat" in v._fieldnames:
                fs = np.unique(np.atleast_1d(v.fs))
                chans[k] = (np.asarray(v.dat, dtype=np.float32).ravel(), float(fs[0]) if len(fs) == 1 else None)
            elif "evnt" in v._fieldnames and "time" in v._fieldnames:
                epocs[k] = (np.atleast_1d(v.evnt), np.atleast_1d(v.time))
        cmap = CH[kind].get(sid) or CH[kind].get(sid.lstrip("0")) or {}
        groups = {}
        for k, (d, fs) in chans.items():
            assert fs is not None, (p, k)
            groups.setdefault((len(d), fs), []).append(k)
        for gi, ((n, fs), names) in enumerate(sorted(groups.items(), key=lambda x: -len(x[1])), 1):
            names = sorted(names, key=lambda k: (not k.startswith("LFPx"), k))
            X = np.stack([chans[k][0] for k in names], axis=1)
            labels = [cmap.get(k, "n/a") for k in names]
            report["unmapped"] += [f"{base}/{kind}:{k}" for k, l in zip(names, labels) if l == "n/a" and k.startswith("LFPx")]
            types = ["TRIG" if k.startswith("Inpt") else chtype(l) for k, l in zip(names, labels)]
            # 2026-10-10: a TTL-only group (Inpt_*) can share the LFP sampling rate with a different length (sub-117, sub-118
            # localizer); the old acq-fs<rate> label then collided and the TTL file overwrote the LFP file. TTL-only groups
            # now get acq-fs<rate>ttl whenever a file has more than one group.
            ttl = all(k.startswith("Inpt") for k in names)
            stem = f"{sub}_task-{task}" + ((f"_acq-fs{int(fs)}" + ("ttl" if ttl else "")) if len(groups) > 1 else "") + (f"_run-{int(part)}" if part else "")
            assert stem not in seen_stems, ("duplicate BIDS stem", stem, p)
            seen_stems.add(stem)
            D = os.path.join(OUT, sub, "ieeg")
            r = write_run(D, stem, X, fs, names, ["n/a"] * len(names), types, {
                "TaskName": task,
                "TaskDescription": ("Auditory stop-signal task (go tone; on stop trials a second tone signals to cancel the response)" if task == "stopsignal"
                                    else "Go-only two-choice localizer used to confirm the placement of the subgaleal strips over hand motor regions") + " (DataREADME / article)",
                "PowerLineFrequency": 60, "SoftwareFilters": "n/a",
                "HardwareFilters": {"LowPass": {"Description": "7.5 kHz hardware low-pass (Dryad methods)"}},
                "iEEGReference": "n/a (not stated in the release)",
                "iEEGPlacementScheme": "Intraoperative: DBS leads (Medtronic 3387) in the subthalamic nucleus or thalamus (VIM) plus 4/6/8-contact strips in the subgaleal space over sensorimotor cortex (Dryad methods); per-channel location from the authors' getchans.m/getlocchans.m",
                "Manufacturer": "Tucker-Davis Technologies", "ManufacturersModelName": "RZ2 with RA16PA Medusa preamplifier and RA16LI headstage (Dryad methods)",
                "ElectricalStimulation": False,
            }, ch_extra=[{"description": (f"{l} (authors' getchans/getlocchans); TDT store {k}" if not k.startswith("Inpt") else f"analog TTL input {k}"),
                          "group": (re.sub(r"\s*\d+$", "", l) if l != "n/a" else "n/a"), "reference": "n/a"} for k, l in zip(names, labels)],
                comment=f"b3w10_convert_betaburst.py: Dryad gf1vhhmq0 data/{kind}/{base}.mat")
            ev = []
            for ek, (codes, times) in sorted(epocs.items()):
                for c, t in zip(codes, times):
                    ev.append([round(float(t), 6), 0, ek, float(c), int(round(float(t) * fs))])
            ev.sort(key=lambda e: (e[0], e[2]))
            wtsv(os.path.join(D, stem + "_events.tsv"), ["onset", "duration", "trial_type", "value", "sample"], ev)
            r.update(stem=stem, file=f"{kind}/{base}.mat", channels=names, labels=labels, n_events=len(ev), epoc_stores=sorted(epocs))
            report["runs"].append(r); scans.setdefault(sub, []).append([f"ieeg/{stem}_ieeg.vhdr", "n/a"])
            print(stem, json.dumps({k: r[k] for k in ("n_samples", "sfreq", "duration_s", "roundtrip_ok", "n_events", "epoc_stores")}), flush=True)
            del X
        # sourcedata copy with scrubbed tank strings
        raw = sio.loadmat(p, squeeze_me=False, struct_as_record=True)
        tanks = set()
        for k, v in list(raw.items()):
            if k.startswith("__") or not (isinstance(v, np.ndarray) and v.dtype.names):
                continue
            for f in ("tank", "block"):
                if f in v.dtype.names:
                    for idx in np.ndindex(v.shape):
                        s = str(np.asarray(v[f][idx]).ravel()[0]) if np.asarray(v[f][idx]).size else ""
                        tanks.add(s)
                        v[f][idx] = np.array([scrub(s)])
        dst = os.path.join(SD, "data", kind, base + ".mat"); os.makedirs(os.path.dirname(dst), exist_ok=True)
        sio.savemat(dst, {k: v for k, v in raw.items() if not k.startswith("__")}, long_field_names=True, do_compression=True)
        b0 = open(dst, "rb").read(); b1, _ = scrub_mat_header(b0); open(dst, "wb").write(b1)
        report["privacy"][f"{kind}/{base}"] = {"n_tank_block_strings_scrubbed": len(tanks), "after": sorted({scrub(t) for t in tanks})}
        del m, raw, chans
for sub, rows in scans.items():
    wtsv(os.path.join(OUT, sub, f"{sub}_scans.tsv"), ["filename", "acq_time"], sorted(rows))
# behaviour + README + authors' code
for p in sorted(glob.glob(os.path.join(X_, "behav", "**", "*"), recursive=True)):
    if os.path.isfile(p) and not os.path.basename(p).startswith("."):
        dst = os.path.join(SD, os.path.relpath(p, X_)); os.makedirs(os.path.dirname(dst), exist_ok=True)
        if p.endswith(".mat"):
            b0 = open(p, "rb").read(); b1, _ = scrub_mat_header(b0); open(dst, "wb").write(b1)
        else:
            shutil.copy(p, dst)
shutil.copy(os.path.join(SRC, "DataREADME.txt"), os.path.join(SD, "DataREADME.txt"))
shutil.copytree(ZC, os.path.join(OUT, "sourcedata", "zenodo-4784092"), dirs_exist_ok=True)
report["behav_flags"] = flag_strings(set().union(*[mat_strings(p) for p in glob.glob(os.path.join(SD, "behav", "**", "*.mat"), recursive=True)] or [set()]))
os.makedirs(os.path.join(OUT, "code"), exist_ok=True)
for fn in (__file__, "b3w10_common.py", "b3w3_common.py"):
    shutil.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.basename(fn)), os.path.join(OUT, "code", os.path.basename(fn)))
json.dump(report, open(os.path.join(OUT, "code", "conversion_report.json"), "w"), indent=1, default=str)
R = report["runs"]
print(json.dumps({"runs": len(R), "subjects": len({r['stem'].split('_')[0] for r in R}), "hours": sum(r["duration_s"] for r in R) / 3600,
                  "rt_all": all(r["roundtrip_ok"] for r in R), "unmapped": report["unmapped"][:30], "behav_flags": report["behav_flags"][:20],
                  "tank_example": list(report["privacy"].items())[:2]}, indent=1, default=str))
print("CONVERT_DONE")
