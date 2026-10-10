%% Main beta burst analysis
% This script was run section by section to analyze our preprocessed LFP
% data and create results figures. A description of what each section does is included at the top of
% each section.

%% Initialize
% This section sets up the analysis by creating a dataset structure w/
% important filenames and information, as well as setting parameters for
% the beta burst detection script.
StopOR_initialize; % script that makes folder paths, dataset struct

%% Beta event detection 
% This section identifies beta bursts in our LFP data around all event
% markers, then saves indices of bursts for further analysis.
DetectBetaBursts;

%% Pull sample behavioral results
% In this section we extract accuracy and rt from the trials that were
% included in the beta analysis.
PullSampleBehavior; % outputs info to command window

%% Make average ERSPs at subgaleal electrodes
% This script makes and plots broadband ERSPs following go trials in SMC from the
% localizer and main blocks and the difference between stop and go trials in
% the main block from subcortical regions. The figures will open in a separate window.
% This section will take some time to run!
StopOR_ERSP;

%% Sort trial events for trial histograms (stimulus-locked)
% This script goes through our saved files of beta bursts and separates
% bursts into stimulus-locked time bins, depending on trial type. It
% outputs figures of Go- and stop-locked burst rates.
StimulusLockedBursts;

%% Sort trial events for trial histograms (response- or SSRT-locked)
% Based on reviewer suggestion, we repeated the time bins analysis from the above
% cell, timelocking bins to response (for go) or SSRT (for stop) instead of
% stimulus.
RespSSRTLockedBursts;

%% Test difference in beta counts for ss vs fs in SSD-SSRT delay
% This section counts the number of bursts between SSD and SSRT for each
% trial type. It outputs figures of burst counts in the SSD-SSRT delay for
% each trial type, across implant location groups. 
SSDtoSSRTBurstCounts;

%% M1 bursts after BG bursts
% This section evaluates the timing of M1 bursts time-locked to bursts in
% VIM or STN in 500ms after stimulus (whether stopsignal or gosignal).
% This analysis done only for subjects with both depth and M1
% electrodes (STN/VIM included as STN).
BurstLockedBursts;

%% Determine first occurrence of event at each recording site
% This section finds the first beta bursts occuring at each recording site
% and sorts them by trial type.
RegionalBurstTiming;

%% Check laterality of beta burst changes in basal ganglia
% This code plots beta burst rates separated by whether the response was
% ipsi- or contralateral to the subcortical region recorded from.
BG_latcheck;

%% Run lagged coherence analysis
% Lagged coherence provides a measure of how "burst-like" and
% non-oscillatory signatures in certain frequency bands are. This script
% pulls STN, thalamic, and SMC data from beta files and runs lagged
% coherence using the fieldtrip lagged coherence function.
% You'll need to have the FieldTrip package downloaded to do this.
% PLEASE NOTE - this script takes quite a bit of time (on the order of days) to run.
StopOR_laggedcoherence;
BurstDetails;
%% Segment STN recording results by dorsal/ventral sections
% This script recalculates the results for the stimulus-locked and
% burst-locked results, but instead of looking at the STN contacts with the
% greatest number of bursts, we look at ventral (contacts 0, 1) vs. dorsal
% (contacts 2, 3) STN contacts.
% It has two sections (one does the stim-locked and the other the burst-
% locked analysis), so running this specific section here will run them
% both.
DorsalVentralSTN;