import os
import os.path as op
import mne
import numpy as np
import pandas as pd

examples_dir = '/Users/sc/Downloads/SO CRYSTAL'                                 # Path to the raw EEG Data folder
vhdr_file = op.join(examples_dir, '/Users/sc/Downloads/SO CRYSTAL/JOSIE ALPHA.dat')                # Path to the raw EEG header file
raw = mne.io.read_raw_persyst(vhdr_file, misc='auto')        # Returns a Raw object containing BrainVision data
raw.load_data()

raw.resample(256, npad="auto")    # set sampling frequency to 256 points per second

raw.filter(1, 30, fir_design='firwin', picks=['eeg'])  # band-pass filter from 1 to 30 frequency over just
                                                       # EEG channel and not EEG channel
raw.set_eeg_reference('average', projection=True).apply_proj()  # re-referencing with the virtual average reference

%matplotlib qt
raw.plot()       # plot the EEG data. Use the '%matplotlib qt' to see
                 # the data in a bright way and move conveniently

raw.info['bads'] = ['Fp1','Fp2','Fpz']         # Select bad channels visually to interpolate them with channels
                                               # Sleceted channels are not real
raw = raw.interpolate_bads(reset_bads=False)

visual_inspection = pd.read_csv(examples_dir + "\\sub-005_visual_inspection.csv")  # Path to annotation folder
                                                                                  # remove each segment with start and end time
for i in range(visual_inspection.shape[0]):
    result = np.where((mne.events_from_annotations(raw)[0][:,0] > visual_inspection['Start'][i]*256) &
                      (mne.events_from_annotations(raw)[0][:,0] < visual_inspection['End'][i]*256));
    raw.annotations.delete(result)

raw.plot()    # Let's see the data again to be sure that the noisy segemnts have been deleted

events_from_annot, event_dict = mne.events_from_annotations(raw)# Get events and event_id from an Annotations object.
event_dict = {'74':74, '75':75, '76':76}                        # Event dictionaries to extract epochs from continuous data,
reject_criteria = dict(eeg=100e-6)                              # Absolute Amplitude of each epoch sould be smaller than 100 μV
                                                                # tmin is start time before event, tmax is end time after event
                                                                # - 100 ms (baseline) of cue's onset to 600 ms
epochs = mne.Epochs(raw, events_from_annot, event_id=event_dict, tmin=-0.1, tmax=1.6,
                    reject=reject_criteria, baseline = (None,0), preload=True, picks=['eeg'])

                                                                  # Ocular artifacts (EOG)
# eog_evoked = mne.preprocessing.create_eog_epochs(raw).average()   # Conveniently generate epochs around EOG artifact events
# eog_evoked.apply_baseline(baseline=(None, -0.2))
# eog_evoked.plot_joint()
#
#                                                                   # Heartbeat artifacts (ECG)
# ecg_evoked = mne.preprocessing.create_ecg_epochs(raw).average()   # Conveniently generate epochs around ECG artifact events
# ecg_evoked.apply_baseline(baseline=(None, -0.2))
# ecg_evoked.plot_joint()

ica = mne.preprocessing.ICA(n_components=50, random_state=97, method='fastica')
ica.fit(epochs)                                      # Data decomposition with 50 components and fastica method.

%matplotlib inline
# %matplotlib qt
ica.plot_components()  # Plot all decomposed components

ica.exclude = [11, 26, 29, 30, 33, 34, 35, 36, 38, 44, 48, 49, 0, 6, 17]
                                        # Put all comonent which you want to remove containg inspected (manual)
                                        # [11, 26, 29, 30, 33, 34, 35, 36, 38, 44, 48, 49], EOG [0] and ECG [6,17] components
                                        # Selected components are not real
ica.apply(epochs)                       # Channels can be reconstructed using the ICA object’s apply()


epochs.save(examples_dir + "\\sub-006_prerprocessed.fif")