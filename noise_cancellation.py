import scipy.io.wavfile as wavfile
import scipy.fftpack as fftpk
import numpy as np
from matplotlib import pyplot as plt
import sounddevice as sd
import scipy.fft
import winsound

fs = 44100  # Sample rate
seconds = 3  # Duration of recording

myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
sd.wait()  # Wait until recording is finished

signal = myrecording

FFT = abs(scipy.fft(signal))
freqs = fftpk.fftfreq(len(FFT), (1.0/fs))

plt.Figure(figsize=(20,20))
plt.subplot((121))
plt.plot(myrecording)
plt.subplot((122))
plt.plot(freqs[range(len(FFT)//2)], FFT[range(len(FFT)//2)])                                                          
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.tight_layout()
plt.show()

sd.play(myrecording, fs)
sd.wait()
