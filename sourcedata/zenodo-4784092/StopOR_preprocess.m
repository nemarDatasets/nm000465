%% Preprocessing code
% This script was executed section-by-section to load in and preprocess LFP
% data. Descriptions of what each section does can be found below.
%% Initialize settings for preprocessing and analysis
StopOR_initialize; % sets up folder paths and datasets structure

%% Import data and filter
% In this section, we take files recorded with Neuralynx equipment and
% merge channel data to the standard EEGLab structure. Information is added
% to event triggers and the data is filtered for line noise and resampled.
for is = 1:length(datasets) % for each dataset
    
    % use the import function to convert raw data for this subject into
    % EEGLab structure with behavioral info saved in event structure at
    % trigger times
    LFP = ImportRawData(is,datasets,folders);
    
    % downsample to 1000Hz and clean line noise from OR machinery
    LFP = pop_resample(LFP,1000); % downsample
    % clean
    LFP = pop_cleanline(LFP, 'bandwidth',3,'chanlist',[1:LFP.nbchan] ,'computepower',1,'linefreqs',[60:60:240] ,'normSpectrum',0,'p',0.01,'pad',2,'plotfigures',0,'scanforlines',1,'sigtype','Channels','tau',100,'verb',2,'winsize',3,'winstep',1.5);
        
    % SAVE
    LFP = eeg_checkset(LFP);
    save(fullfile(folders.pp,['Subject' num2str(datasets(is).subnum) '-LFP.mat']),'LFP');

end
%% Manually inspect and mark rejections
% This code (and following section) executed once for each participant to
% check for sporadic artifacts in the data. Opens a data viewer you can use
% to scroll through data, use mouse to click sections we want to mark for
% removal.
is = 1; % choose which participant to manually inspect data

% load
load(fullfile(folders.pp,['Subject' num2str(datasets(is).subnum) '-LFP.mat']));
eeglab;

% remove boundaries and cut into even spaced epochs
boundary = find(strcmpi({LFP.event.type},'boundary'));
LFP.event(boundary) = []; LFP.xmax = LFP.pnts/LFP.srate;
LFP = eeg_regepochs(LFP, 1, [0 1], NaN);

% plot
LFP.data = double(LFP.data);
pop_eegplot(LFP);
% MAKE SURE TO SAVE REJECTIONS BY SAVING NEXT SECTION, otherwise will not
% save
%% SAVE indices of rejections for removal later 
% run this section immediately after visually inspecting a dataset using
% the previous section
rejections = find(LFP.reject.rejmanual); if isempty(rejections); rejections = 1; end
rejpoints = [[(rejections-1)*1*LFP.srate+1]' [rejections*1*LFP.srate]'];
save(fullfile(folders.pp,['ManualRej' num2str(datasets(is).subnum) '.mat']),'rejpoints','rejections');
%% Preprocess localizer blocks (NOTE: 112, 132 have no localizer)
% This section is the same as the other preprocessing (loading in and
% filtering) section above, but here we do it for the localizer blocks

for is = [1:6 8:20] 
    
    % use the import function to convert raw data for this subject into
    % EEGLab structure with behavioral info saved in event structure at
    % trigger times
    LFP = ImportLocalizerRawData(is,datasets,folders);
    
    % resample to 1000Hz and clean line noise from OR
    LFP = pop_resample(LFP,1000);
    LFP = pop_cleanline(LFP, 'bandwidth',3,'chanlist',[1:LFP.nbchan] ,'computepower',1,'linefreqs',[60:60:240] ,'normSpectrum',0,'p',0.01,'pad',2,'plotfigures',0,'scanforlines',1,'sigtype','Channels','tau',100,'verb',2,'winsize',3,'winstep',1.5);
    
    % SAVE
    LFP = eeg_checkset(LFP);
    %save(fullfile(folders.pp,['Subject' num2str(datasets(is).subnum) '-localizer.mat']),'LFP');
    clear LFPx* Inpt*

end
%% Manually inspect and mark rejections
% This code (and following section) executed once for each participant to
% check for sporadic artifacts in the data. Opens a data viewer you can use
% to scroll through data, use mouse to click sections we want to mark for
% removal.
is = 1; % pick which participant to manually inspect data

% load
load(fullfile(folders.pp,['Subject' num2str(datasets(is).subnum) '-localizer.mat']));
eeglab; 

% remove boundaries and cut into even spaced epochs
boundary = find(strcmpi({LFP.event.type},'boundary'));
LFP.event(boundary) = []; LFP.xmax = LFP.pnts/LFP.srate;
LFP = eeg_regepochs(LFP, 1, [0 1], NaN);

% plot
LFP.data = double(LFP.data);
pop_eegplot(LFP);
% SAVE REJECTIONS BY RUNNING NEXT SECTION, otherwise will not save!
%% SAVE indices of rejections for removal later
% must be run immediately after preceding section to save rejection indices
rejections = find(LFP.reject.rejmanual); if isempty(rejections); rejections = 1; end
rejpoints = [[(rejections-1)*1*LFP.srate+1]' [rejections*1*LFP.srate]'];
save(fullfile(folders.pp,['ManualRej' num2str(datasets(is).subnum) '_localizer.mat']),'rejpoints','rejections');