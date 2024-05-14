from st_audiorec import st_audiorec
from scipy.io import wavfile as wav
from scipy.fftpack import fft
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import resample
from scipy.signal import ellip, filtfilt
import streamlit as st
from streamlit_extras import add_vertical_space as avs
import os 

#CONSTANTS 
CHANNELS = 1  # number of channels it means number of sample in every sampling
RATE = 44100  # number of sample in 1 second sampling
BYTES = 1024  # bytes per second

class Computation():
    def __init__(self):
        pass
        
    def plot_fft(self, title, freq, mag, data, max_freq=1000, step=100, min_freq=0):
        # Plot magnitude
        fig, ax = plt.subplots(figsize=(12, 6))
        plt.plot(freq[:len(data)//2], mag[:len(data)//2])
        plt.title(f'Magnitude Vs Frequency: {title}')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')

        plt.xticks(np.arange(0, max_freq + 1, step))  
        plt.xlim(min_freq, max_freq)  # Set the x-axis limit to ensure all data is visible

        # Display the plot in Streamlit
        st.pyplot(fig)

    def bandpass_filter(self,data, lowcut, highcut, fs, order, passband_ripple=0.5, stopband_attenuation=60):
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = ellip(order, passband_ripple, stopband_attenuation, [low, high], btype='band')
        y = filtfilt(b, a, data)
        return y

    def highpass_filter(self,data, cutoff_freq, fs, order, passband_ripple=0.5, stopband_attenuation=60):
        nyquist = 0.5 * fs
        high = cutoff_freq / nyquist
        b, a = ellip(order, passband_ripple, stopband_attenuation, high, btype='highpass')
        y = filtfilt(b, a, data)
        return y

    def adjust_wav_file(self,file):
        WAVE_INPUT_FILENAME = file  # existing recorded file name

        # Read the audio data from the WAV file
        rate, data = wav.read(WAVE_INPUT_FILENAME)

        # Convert to mono 
        if len(data.shape) > 1:
            data = np.mean(data, axis=1)

        # Resample
        if rate != RATE:
            data = resample(data, int(len(data) * RATE / rate))

        # Adjust byte rate if necessary
        bytes_per_sample = data.dtype.itemsize
        if bytes_per_sample != 2:
            # Convert data to 16-bit int (if not already)
            data = (data / np.max(np.abs(data)) * (2 ** 15 - 1)).astype(np.int16)

        # Adjust number of channels if necessary
        if data.ndim > CHANNELS:
            data = data[:, 0]  # Keep only one channel
        
        return rate, data

    def calculate_FFT(self,data):
        fft = np.fft.fft(data)
        mag = np.absolute(fft)
        mag = mag[0:int(len(mag)/2)]
        # Frequencies corresponding to FFT result
        frequencies = np.fft.fftfreq(len(data), 1/RATE)
        return mag, frequencies


    def calculate_energy(self,filtered_mag):
        return np.sum(filtered_mag**2)/len(filtered_mag)

    def test(self,rate, data, plot=None):
        # apply filters
        above6500 = self.highpass_filter(data, 6500,rate, 8)
        filtered_yes_data = self.bandpass_filter(data, 450, 550, rate, 4)
        filtered_no_data = self.bandpass_filter(data, 200, 300, rate, 4)

        # do FFT
        above6500_mag, above6500_freq = self.calculate_FFT(above6500)
        mag, freq = self.calculate_FFT(data)
        mag_yes, freq_yes = self.calculate_FFT(filtered_yes_data)
        mag_no, freq_no = self.calculate_FFT(filtered_no_data)

        #plotting
        if plot is None:
            self.st.subheader("**Plotting after FFT**")
            self.plot_fft('Without Filter',freq=freq , mag=mag, data=data ,max_freq=8000, step=500)
            self.plot_fft('"Yes" detector BPF (1)',freq=freq_yes , mag=mag_yes, data=filtered_yes_data)
            self.plot_fft('"s" detector HPF (2)',freq=above6500_freq , mag=above6500_mag, data=above6500, max_freq=8000, step=500, min_freq=0)
            self.plot_fft('"No" detector BPF',freq=freq_no , mag=mag_no, data=filtered_no_data)

        if plot == 'YES':
            self.plot_fft('Without Filter',freq=freq , mag=mag, data=data ,max_freq=8000, step=500)
            st.caption("Full signal without filteting")
            avs.add_vertical_space(1)
            self.plot_fft('Applying BPF',freq=freq_yes , mag=mag_yes, data=filtered_yes_data)
            self.plot_fft('Applying HPF',freq=above6500_freq , mag=above6500_mag, data=above6500, max_freq=8000, step=500, min_freq=0)
            st.caption("Adding a BPF and HPF to get the 'Yes' detecated frequencies only")

        if plot == 'NO':
            self.plot_fft('Without Filter',freq=freq , mag=mag, data=data ,max_freq=8000, step=500)
            st.caption("Full signal without filteting")
            avs.add_vertical_space(1)
            self.plot_fft('Applying BPF',freq=freq_no , mag=mag_no, data=filtered_no_data)
            st.caption("Adding a BPF to get the 'No' detecated frequencies only")

        # Compute energy distribution rates
        energy_yes = self.calculate_energy(mag_yes)
        energy_no = self.calculate_energy(mag_no)
        energy_6500 = self.calculate_energy(above6500_mag)
        total_energy = self.calculate_energy(mag)
        energy_yes += energy_6500

        min_threshold = 13116058260.837112 #threshold for 's'
        mute_threshold = 125010299572.6434 #if the no energy is less than this it means its silent
        if energy_no < mute_threshold:
            return 'MUTE'
        if energy_no > energy_yes:
            if energy_6500 > min_threshold:
                return 'YES'
            else:
                return 'NO'
        elif energy_no < energy_yes:
            if energy_6500 < min_threshold:
                return 'NO'
            else:
                return 'YES'


    def mean_freq_range(self):
        mean = []
        directory='yes'

        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            # Read the audio data from the WAV file
            sample_rate, data = self.adjust_wav_file(file_path)

            energies = []
            for f in range(200, 1000, 100):
                filtered_data = self.bandpass_filter(data, f-99, f, sample_rate, order=4)
                mag, freq = self.compute_FFT(filtered_data)
                e = self.calculate_energy(mag)
                energies.append(e)

            mean.append((energies.index(max(energies))+2)*100)

        w_c = sum(mean)/len(os.listdir(directory)) #center frequency (mean)
        w_c1 = w_c - 50 # low cutoff frequency
        w_c2 = w_c + 50 # high cutoff frequency