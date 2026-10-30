[![DOI](https://img.shields.io/badge/DOI-10.82901%2Fnemar.nm000465-blue)](https://doi.org/10.82901/nemar.nm000465)

# Intraoperative STN/thalamic LFP + subgaleal sensorimotor strips during a stop-signal task (Diesburg, Greenlee & Wessel, 2021)

Local field potentials recorded during deep brain stimulation surgery (University of Iowa Hospitals and Clinics, April 2018 -
March 2020; DataREADME) from DBS leads (Medtronic 3387) in the subthalamic nucleus (STN) or the ventral intermediate thalamus
(VIM), together with 4-, 6- or 8-contact strips in the subgaleal space over sensorimotor cortex, while patients performed an
auditory stop-signal task ("main") and a go-only localizer. Article: beta bursts in STN/thalamus on successful stop trials are
followed within 50 ms by beta bursts over sensorimotor cortex.

## Source
- Dryad: Darcy A. Diesburg, Jeremy D. W. Greenlee, Jan R. Wessel. Cortico-subcortical beta burst dynamics underlying movement cancellation in humans.
  doi:10.5061/dryad.gf1vhhmq0. License CC0 1.0. Article: eLife 10:e70270 (2021), doi:10.7554/eLife.70270.
- Authors' code (channel tables getchans.m/getlocchans.m): Zenodo doi:10.5281/zenodo.4784092 (CC-BY-4.0), copied unchanged
  to sourcedata/zenodo-4784092.
- data.zip, behav.zip and DataREADME.txt were downloaded through the Dryad API on Voyager (SHA-256 verified). Not mirrored:
  pp.zip (EEGLAB preprocessed data) and beta.zip (beta-burst indices), both derived.

## Contents
- `sub-<id>/ieeg/sub-<id>_task-stopsignal_*` and `task-localizer`: 47 recordings, 23 subjects, 7.33 h.
  Sampling rates 2000, 24000 Hz (TDT export, per file). Values unchanged from the release
  (float32); units are not stated (n/a). Dryad methods: TDT system with RA16PA Medusa preamplifier and RA16LI headstage,
  hardware low-pass 7.5 kHz.
- Channels: `LFPx_RZ2_chnNNN` = recording channels, labelled from the authors' tables (DBS = STN/VIM lead contacts 0-3; EEG =
  subgaleal strip contacts, which lie under the scalp outside the skull); `Inpt_RZ2_chnNNN` = analog TTL inputs (TRIG) that
  carry the task triggers (DataREADME: "Triggers are represented as up-flanks (from TTL pulses) in an input channel").
  Channels without a label in the tables: Subject_116_1/main:LFPx_RZ2_chn004, Subject_116_1/main:LFPx_RZ2_chn013, Subject_116_1/main:LFPx_RZ2_chn014, Subject_116_1/main:LFPx_RZ2_chn015, Subject_116_1/main:LFPx_RZ2_chn016, Subject_117/main:LFPx_RZ2_chn020, Subject_118/main:LFPx_RZ2_chn020, Subject_119/main:LFPx_RZ2_chn017, Subject_119/main:LFPx_RZ2_chn018, Subject_119/main:LFPx_RZ2_chn019, Subject_119/main:LFPx_RZ2_chn020, Subject_122/main:LFPx_RZ2_chn017, Subject_122/main:LFPx_RZ2_chn018, Subject_122/main:LFPx_RZ2_chn019, Subject_122/main:LFPx_RZ2_chn020, Subject_126/main:LFPx_RZ2_chn017, Subject_126/main:LFPx_RZ2_chn018, Subject_126/main:LFPx_RZ2_chn019, Subject_126/main:LFPx_RZ2_chn020, Subject_128/main:LFPx_RZ2_chn001, Subject_128/main:LFPx_RZ2_chn002, Subject_128/main:LFPx_RZ2_chn003, Subject_128/main:LFPx_RZ2_chn004, Subject_128/main:LFPx_RZ2_chn005, Subject_128/main:LFPx_RZ2_chn006, Subject_128/main:LFPx_RZ2_chn007, Subject_128/main:LFPx_RZ2_chn008, Subject_128/main:LFPx_RZ2_chn009, Subject_128/main:LFPx_RZ2_chn010, Subject_128/main:LFPx_RZ2_chn011, Subject_128/main:LFPx_RZ2_chn012, Subject_128/main:LFPx_RZ2_chn013, Subject_128/main:LFPx_RZ2_chn014, Subject_128/main:LFPx_RZ2_chn015, Subject_128/main:LFPx_RZ2_chn016, Subject_128/main:LFPx_RZ2_chn017, Subject_128/main:LFPx_RZ2_chn018, Subject_128/main:LFPx_RZ2_chn019, Subject_128/main:LFPx_RZ2_chn020, Subject_129/main:LFPx_RZ2_chn017, Subject_129/main:LFPx_RZ2_chn018, Subject_129/main:LFPx_RZ2_chn019, Subject_129/main:LFPx_RZ2_chn020, Subject_101/localizers:LFPx_RZ2_chn009, Subject_101/localizers:LFPx_RZ2_chn010, Subject_101/localizers:LFPx_RZ2_chn011, Subject_101/localizers:LFPx_RZ2_chn012, Subject_101/localizers:LFPx_RZ2_chn013, Subject_101/localizers:LFPx_RZ2_chn014, Subject_101/localizers:LFPx_RZ2_chn015, Subject_101/localizers:LFPx_RZ2_chn016, Subject_104/localizers:LFPx_RZ2_chn005, Subject_104/localizers:LFPx_RZ2_chn006, Subject_104/localizers:LFPx_RZ2_chn007, Subject_104/localizers:LFPx_RZ2_chn008, Subject_104/localizers:LFPx_RZ2_chn009, Subject_104/localizers:LFPx_RZ2_chn010, Subject_104/localizers:LFPx_RZ2_chn011, Subject_104/localizers:LFPx_RZ2_chn012, Subject_104/localizers:LFPx_RZ2_chn013, Subject_104/localizers:LFPx_RZ2_chn014, Subject_104/localizers:LFPx_RZ2_chn015, Subject_104/localizers:LFPx_RZ2_chn016, Subject_105/localizers:LFPx_RZ2_chn009, Subject_105/localizers:LFPx_RZ2_chn010, Subject_105/localizers:LFPx_RZ2_chn011, Subject_105/localizers:LFPx_RZ2_chn012, Subject_105/localizers:LFPx_RZ2_chn013, Subject_105/localizers:LFPx_RZ2_chn014, Subject_105/localizers:LFPx_RZ2_chn015, Subject_105/localizers:LFPx_RZ2_chn016, Subject_106/localizers:LFPx_RZ2_chn009, Subject_106/localizers:LFPx_RZ2_chn010, Subject_106/localizers:LFPx_RZ2_chn011, Subject_106/localizers:LFPx_RZ2_chn012, Subject_106/localizers:LFPx_RZ2_chn013, Subject_106/localizers:LFPx_RZ2_chn014, Subject_106/localizers:LFPx_RZ2_chn015, Subject_106/localizers:LFPx_RZ2_chn016, Subject_109/localizers:LFPx_RZ2_chn009, Subject_109/localizers:LFPx_RZ2_chn010, Subject_109/localizers:LFPx_RZ2_chn011, Subject_109/localizers:LFPx_RZ2_chn012, Subject_109/localizers:LFPx_RZ2_chn013, Subject_109/localizers:LFPx_RZ2_chn014, Subject_109/localizers:LFPx_RZ2_chn015, Subject_109/localizers:LFPx_RZ2_chn016, Subject_110/localizers:LFPx_RZ2_chn009, Subject_110/localizers:LFPx_RZ2_chn010, Subject_110/localizers:LFPx_RZ2_chn011, Subject_110/localizers:LFPx_RZ2_chn012, Subject_110/localizers:LFPx_RZ2_chn013, Subject_110/localizers:LFPx_RZ2_chn014, Subject_110/localizers:LFPx_RZ2_chn015, Subject_110/localizers:LFPx_RZ2_chn016, Subject_113/localizers:LFPx_RZ2_chn013, Subject_113/localizers:LFPx_RZ2_chn014, Subject_113/localizers:LFPx_RZ2_chn015, Subject_113/localizers:LFPx_RZ2_chn016, Subject_114/localizers:LFPx_RZ2_chn013, Subject_114/localizers:LFPx_RZ2_chn014, Subject_114/localizers:LFPx_RZ2_chn015, Subject_114/localizers:LFPx_RZ2_chn016, Subject_114/localizers:LFPx_RZ2_chn017, Subject_114/localizers:LFPx_RZ2_chn018, Subject_114/localizers:LFPx_RZ2_chn019, Subject_114/localizers:LFPx_RZ2_chn020, Subject_115/localizers:LFPx_RZ2_chn017, Subject_115/localizers:LFPx_RZ2_chn018, Subject_115/localizers:LFPx_RZ2_chn019, Subject_115/localizers:LFPx_RZ2_chn020, Subject_115/localizers:LFPx_RZ2_chn021, Subject_115/localizers:LFPx_RZ2_chn022, Subject_115/localizers:LFPx_RZ2_chn023, Subject_115/localizers:LFPx_RZ2_chn024, Subject_117/localizers:LFPx_RZ2_chn009, Subject_117/localizers:LFPx_RZ2_chn010, Subject_117/localizers:LFPx_RZ2_chn011, Subject_117/localizers:LFPx_RZ2_chn012, Subject_117/localizers:LFPx_RZ2_chn013, Subject_117/localizers:LFPx_RZ2_chn014, Subject_117/localizers:LFPx_RZ2_chn015, Subject_117/localizers:LFPx_RZ2_chn016, Subject_117/localizers:LFPx_RZ2_chn017, Subject_117/localizers:LFPx_RZ2_chn018, Subject_117/localizers:LFPx_RZ2_chn019, Subject_117/localizers:LFPx_RZ2_chn020, Subject_118/localizers:LFPx_RZ2_chn009, Subject_118/localizers:LFPx_RZ2_chn010, Subject_118/localizers:LFPx_RZ2_chn011, Subject_118/localizers:LFPx_RZ2_chn012, Subject_118/localizers:LFPx_RZ2_chn013, Subject_118/localizers:LFPx_RZ2_chn014, Subject_118/localizers:LFPx_RZ2_chn015, Subject_118/localizers:LFPx_RZ2_chn016, Subject_118/localizers:LFPx_RZ2_chn017, Subject_118/localizers:LFPx_RZ2_chn018, Subject_118/localizers:LFPx_RZ2_chn019, Subject_118/localizers:LFPx_RZ2_chn020, Subject_119/localizers:LFPx_RZ2_chn009, Subject_119/localizers:LFPx_RZ2_chn010, Subject_119/localizers:LFPx_RZ2_chn011, Subject_119/localizers:LFPx_RZ2_chn012, Subject_119/localizers:LFPx_RZ2_chn013, Subject_119/localizers:LFPx_RZ2_chn014, Subject_119/localizers:LFPx_RZ2_chn015, Subject_119/localizers:LFPx_RZ2_chn016, Subject_119/localizers:LFPx_RZ2_chn017, Subject_119/localizers:LFPx_RZ2_chn018, Subject_119/localizers:LFPx_RZ2_chn019, Subject_119/localizers:LFPx_RZ2_chn020, Subject_120/localizers:LFPx_RZ2_chn009, Subject_120/localizers:LFPx_RZ2_chn010, Subject_120/localizers:LFPx_RZ2_chn011, Subject_120/localizers:LFPx_RZ2_chn012, Subject_120/localizers:LFPx_RZ2_chn013, Subject_120/localizers:LFPx_RZ2_chn014, Subject_120/localizers:LFPx_RZ2_chn015, Subject_120/localizers:LFPx_RZ2_chn016, Subject_121/localizers:LFPx_RZ2_chn009, Subject_121/localizers:LFPx_RZ2_chn010, Subject_121/localizers:LFPx_RZ2_chn011, Subject_121/localizers:LFPx_RZ2_chn012, Subject_121/localizers:LFPx_RZ2_chn013, Subject_121/localizers:LFPx_RZ2_chn014, Subject_121/localizers:LFPx_RZ2_chn015, Subject_121/localizers:LFPx_RZ2_chn016, Subject_122/localizers:LFPx_RZ2_chn009, Subject_122/localizers:LFPx_RZ2_chn010, Subject_122/localizers:LFPx_RZ2_chn011, Subject_122/localizers:LFPx_RZ2_chn012, Subject_122/localizers:LFPx_RZ2_chn013, Subject_122/localizers:LFPx_RZ2_chn014, Subject_122/localizers:LFPx_RZ2_chn015, Subject_122/localizers:LFPx_RZ2_chn016, Subject_122/localizers:LFPx_RZ2_chn017, Subject_122/localizers:LFPx_RZ2_chn018, Subject_122/localizers:LFPx_RZ2_chn019, Subject_122/localizers:LFPx_RZ2_chn020, Subject_125/localizers:LFPx_RZ2_chn009, Subject_125/localizers:LFPx_RZ2_chn010, Subject_125/localizers:LFPx_RZ2_chn011, Subject_125/localizers:LFPx_RZ2_chn012, Subject_125/localizers:LFPx_RZ2_chn013, Subject_125/localizers:LFPx_RZ2_chn014, Subject_125/localizers:LFPx_RZ2_chn015, Subject_125/localizers:LFPx_RZ2_chn016, Subject_126/localizers:LFPx_RZ2_chn009, Subject_126/localizers:LFPx_RZ2_chn010, Subject_126/localizers:LFPx_RZ2_chn011, Subject_126/localizers:LFPx_RZ2_chn012, Subject_126/localizers:LFPx_RZ2_chn013, Subject_126/localizers:LFPx_RZ2_chn014, Subject_126/localizers:LFPx_RZ2_chn015, Subject_126/localizers:LFPx_RZ2_chn016, Subject_126/localizers:LFPx_RZ2_chn017, Subject_126/localizers:LFPx_RZ2_chn018, Subject_126/localizers:LFPx_RZ2_chn019, Subject_126/localizers:LFPx_RZ2_chn020, Subject_128/localizers:LFPx_RZ2_chn009, Subject_128/localizers:LFPx_RZ2_chn010, Subject_128/localizers:LFPx_RZ2_chn011, Subject_128/localizers:LFPx_RZ2_chn012, Subject_128/localizers:LFPx_RZ2_chn013, Subject_128/localizers:LFPx_RZ2_chn014, Subject_128/localizers:LFPx_RZ2_chn015, Subject_128/localizers:LFPx_RZ2_chn016, Subject_128/localizers:LFPx_RZ2_chn017, Subject_128/localizers:LFPx_RZ2_chn018, Subject_128/localizers:LFPx_RZ2_chn019, Subject_128/localizers:LFPx_RZ2_chn020, Subject_129/localizers:LFPx_RZ2_chn009, Subject_129/localizers:LFPx_RZ2_chn010, Subject_129/localizers:LFPx_RZ2_chn011, Subject_129/localizers:LFPx_RZ2_chn012, Subject_129/localizers:LFPx_RZ2_chn013, Subject_129/localizers:LFPx_RZ2_chn014, Subject_129/localizers:LFPx_RZ2_chn015, Subject_129/localizers:LFPx_RZ2_chn016, Subject_129/localizers:LFPx_RZ2_chn017, Subject_129/localizers:LFPx_RZ2_chn018, Subject_129/localizers:LFPx_RZ2_chn019, Subject_129/localizers:LFPx_RZ2_chn020, Subject_130/localizers:LFPx_RZ2_chn009, Subject_130/localizers:LFPx_RZ2_chn010, Subject_130/localizers:LFPx_RZ2_chn011, Subject_130/localizers:LFPx_RZ2_chn012, Subject_130/localizers:LFPx_RZ2_chn013, Subject_130/localizers:LFPx_RZ2_chn014, Subject_130/localizers:LFPx_RZ2_chn015, Subject_130/localizers:LFPx_RZ2_chn016.
- `events.tsv`: TDT epoc stores (tick markers etc.). Trial-level behaviour (stop-signal delays, responses) is in
  sourcedata/dryad-gf1vhhmq0/behav/.

## Localisation
Per-contact structure and side from the authors' channel tables; no coordinates are released.

## Privacy
The TDT tank names in the original files contain a recording date; the copies in sourcedata/dryad-gf1vhhmq0/data were re-saved
with the day set to 01 (MAT headers too). The behaviour files contain no age/sex/name (empty fields); output folder paths only.

## Ethics
Quoted verbatim from the article (Diesburg DA, Greenlee JDW, Wessel JR (2021), eLife 10:e70270, doi:10.7554/eLife.70270;
section "Additional information" > "Ethics", full text Europe PMC PMC8691838):

> Human subjects: Research participants signed a written informed consent document during a clinic visit prior to surgery. Experimental protocols were approved by the University of Iowa's Institutional Review Board (#201402720).

The Materials and methods ("Participants") state the same approval: "These experimental protocols were approved by the
University of Iowa’s Institutional Review Board (#201402720)." The Dryad deposit doi:10.5061/dryad.gf1vhhmq0 is the data
release of this article.

## Units when reading with MNE (added 2026-10-17, version 1.0.3)

The release does not state the physical unit of the signal values, so the BrainVision headers and channels.tsv give
the unit `n/a` (resolution 1) and the values are the release's numbers, unchanged. MNE and MNE-BIDS read a channel
with unit `n/a` as volts with scale 1: `raw.get_data()` returns the stored numbers as they are, labelled V. If the
numbers are microvolt-sized, anything that assumes volts (plot scalings, rejection thresholds, µV conversions) sees
them 1e6 times too large. In the 2026-10-17 check the channels had a robust SD of about 14-290 in the runs read. No unit is assigned here because the source does not state one; treat the values as the
release's numbers in an unknown unit.

## Task events and sub-128 channel types (fix-20261030, Oct 2026)

**Task events are not in `events.tsv` yet.** The `events.tsv` files list the TDT epoc stores only (`Epoc`, `LATT`, `RATT`,
`Tic2`, ... at the start of the file); they are not the task events. The go and stop stimuli and the responses can be
rebuilt from the release with the authors' own import code (`functions/ImportRawData.m` in
`sourcedata/zenodo-4784092/functions.zip`): TTL up-flanks in `Inpt_RZ2_chn001` (samples where the channel exceeds 1,
first sample of each run, minus 3 samples), one trigger per go trial and two per stop trial, matched in order to the
trial table `trialseq` of `sourcedata/dryad-gf1vhhmq0/behav/Subject_<n>.mat` (columns of `Basicstop_columns.m`); the
stop-signal latency is then the go trigger plus the left/right stop-signal delay, and the response the go trigger plus
the RT. The code also removes one extra trigger at the start of sub-101 and a go-only block at the end of sub-104
(triggers 257 onwards), and down-samples the 24 kHz trigger channel of sub-118. This procedure was ported to
`code/fix-20261030_stopsignal_events.py` and applied: the stop-signal `events.tsv` of all 23 participants (sub-116 for
the recorded half of its session, see below) now also
hold `GoStimulus`, `StopStimulus` and `Response` rows with the trial's behaviour columns (`task-stopsignal_events.json`);
the TDT epoc rows are unchanged. In the 22 other runs the trigger count equals the expected 256 (192 trials, 64 with a stop
signal) and every event lies inside the recording (`code/fix-20261030_stopsignal_events_report.json`). Event times
inherit the authors' rules (trigger = last high sample minus 3; stop signal = go trigger + SSD).

**sub-116: partial recording.** The authors excluded subject 116 before import (`StopOR_initialize.m` removes
`datasets([11 20])`, which are Subject_116 and Subject_128 in sorted file order, as "subs who have data but didn't perform to
behavioral criteria"), so their code never aligned this run. Its TTL channel has 129 triggers. The behaviour file
`behav/Subject_116.mat` holds 192 planned trials, but only the first 96 have a recorded outcome: the task saves each
trial when it ends, so trials 97-192 never ran. Splitting the triggers into trials (a second trigger < 1.05 s after a go
trigger is the stop trigger) gives 97 trials. Trials 1-96 match behaviour rows 1-96 trial for trial: the go/stop
sequence is identical (32 stop trials, 96 + 32 = 128 triggers), and the trial-onset intervals equal the behaviour
`time` column (median difference 0.3 ms, maximum 15.8 ms, including the 55.6 s block break). This is the only
placement of the trigger train on the behaviour rows within 25 ms. The trial table of the separate file
`behav/116 extra/Subject_116.mat` (90 trials, one block) fits nowhere in this recording.
The one remaining trigger comes 7.7 s after trial 96, after the block-2 break, about 3.5 s before the recording ends.
It is the start of a trial whose behaviour was never saved, and it gets no event. sub-116 therefore has events for
trials 1-96 (96 GoStimulus, 32 StopStimulus, 77 Response), built with the same rules. The
alignment check is in `code/fix-20261030_stopsignal_events.py` (`align_partial`). The stop TTL comes 35-153 ms
(median 42.5 ms) after go + SSD; as for the other participants, the StopStimulus onset is go + SSD and the trigger is
kept in `stop_trigger_sample`.

**sub-128 stop-signal run: channel types not given.** The authors' stop-signal channel table (`getchans.m`) has no
entry for subject 128 (the release does not say why), so its 20 `LFPx_RZ2_chn*`
channels stay MISC with an empty label. The localizer table (`getlocchans.m`) does label sub-128 channels 1-8 as
subgaleal contacts, but the wiring is not always the same in the two tasks (in subject 115 the left and right strips
are swapped between the tables), so the localizer labels are not copied to the stop-signal run.
