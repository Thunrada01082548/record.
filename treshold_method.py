import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack as fftpk

plt.rcParams['figure.figsize'] = [10,16]
plt.rcParams.update({'font.size': 18})
plt.style.use('seaborn')

fs = 44100  # Sample rate
seconds = 2  # Duration of recording

#record the input
signal = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype = 'float32')
signal = signal.reshape(len(signal))
sd.wait()  # Wait until recording is finished

sd.play(signal, fs)
sd.wait()

signal_clean = signal


minsignal, maxsignal = signal.min(), signal.max()

n = len(signal)
t = np.linspace(0,seconds,n)
fhat = np.fft.fft(signal) #computes the fft
psd = fhat * np.conj(fhat)/n
freq = fftpk.fftfreq(len(signal), (1.0/fs)) #frequency array
idxs_half = np.arange(0, n//2) #first half index

psd_idxs = np.ones(n)
## Filter out noise
threshold = 0.25
psd_idxs[0:10000] = psd[0:10000] > threshold #array of 0 and 1
psd_clean = psd * psd_idxs #zero out all the unnecessary powers
fhat_clean = psd_idxs * fhat #used to retrieve the signal

signal_filtered = np.fft.ifft(fhat_clean) #inverse fourier transform

## Visualization
fig, ax = plt.subplots(4,1)
ax[0].plot(t, signal, color='b', lw=0.5, label='Noisy Signal')
ax[0].set_ylim([minsignal, maxsignal])
ax[0].set_xlabel('t axis')
ax[0].set_ylabel('Vals')
ax[0].legend()

ax[1].plot(freq[idxs_half], np.abs(psd[idxs_half]), color='b', lw=0.5, label='PSD noisy')
ax[1].set_xlim([-10, 400])
ax[1].set_xlabel('Frequencies in Hz')
ax[1].set_ylabel('Amplitude')
ax[1].legend()

ax[2].plot(freq[idxs_half], np.abs(psd_clean[idxs_half]), color='r', lw=0.5, label='PSD clean')
ax[2].set_xlim([-10, 400])
ax[2].set_xlabel('Frequencies in Hz')
ax[2].set_ylabel('Amplitude')
ax[2].legend()

ax[3].plot(t, signal_filtered, color='r', lw=0.5, label='Clean Signal Retrieved')
ax[3].set_ylim([minsignal, maxsignal])
ax[3].set_xlabel('t axis')
ax[3].set_ylabel('Vals')
ax[3].legend()

plt.tight_layout()
audio = np.real(signal_filtered).astype(np.float32)

sd.play(audio, fs)
sd.wait()