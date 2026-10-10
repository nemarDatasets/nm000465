%% Initialize dataset structure and folder paths
% This script sets up the folders we need for our preprocessing and
% analysis, as well as the datasets structure with important filenames and
% subject info. You will need to have EEGLab installed and on your MATLAB path
% to run the analysis.

% Clear workspace
clear; clc;

% filepaths for eeglab
folders.eeglab = fileparts(which('eeglab.m'));

% shortening folder paths
folders.base = fullfile(cd); % sets the current directory as base folder, 
% from here, subfolders will be set up

% these are files you should already have downloaded from the file exchange
% if errors are thrown at this point - check to make sure they're all
% downloaded and named the same as listed here and in the Dryad folders
folders.raw = '/data/backed_up/raw_or/StopOR/'; %'fullfile(folders.base,'data','main');
folders.localizer = '/data/backed_up/raw_or/Localizers/'; %'fullfile(folders.base,'data','localizer');
folders.behav = fullfile(folders.base,'behav'); 
folders.behavloc = fullfile(folders.behav,'localizers'); % (inside behav folder)
folders.functions = fullfile(folders.base,'functions');
addpath(folders.functions);

% we'll make these files to put analysis outputs in
folders.ersp = fullfile(folders.base,'ersp'); mkdir(folders.ersp);
folders.beta = fullfile(folders.base,'beta'); mkdir(folders.beta);
folders.figs = fullfile(folders.base,'figs'); mkdir(folders.figs);
folders.pp = fullfile(folders.base,'pp'); mkdir(folders.pp);
folders.behavout = fullfile(folders.behav,'out'); mkdir(folders.behavout);

% this function makes a structure with subject numbers and filepaths
datasets = create_datasets_structure(folders);
datasets([11 20]) = []; % remove subs who have data but didn't perform to behavioral criteria
% label site of LFP recordings
datasets(1).loc = 'STN'; datasets(3).loc = 'STN'; datasets(5).loc = 'STN';
datasets(4).loc = 'VIM'; datasets(6).loc = 'VIM'; datasets(7).loc = 'VIM';
datasets(8).loc = 'STN'; datasets(9).loc = 'VIM'; datasets(10).loc = 'VIM';
datasets(11).loc = 'STN'; datasets(12).loc = 'STN';
datasets(13).loc = 'VIM'; datasets(14).loc = 'VIM'; datasets(15).loc = 'VIM';
datasets(16).loc = 'STN'; datasets(17).loc = 'VIM'; datasets(18).loc = 'STN';
datasets(19).loc = 'STN'; datasets(20).loc = 'VIM'; datasets(21).loc = 'VIM';
datasets(2).loc = 'both';
tha = [2 4 6 7 9 10 13 14 15 17 20 21];
stn = [1 2 3 5 8 11 12 16 18 19];

rng('default'); % set global random stream
eeglab; % initialize eeglab (can close when GUI opens)
 disp('Folder trees and subject information structures are ready to go!');