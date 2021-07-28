import numpy as np #importing libraries
import matplotlib.pyplot as plt #importing libraries
import scipy.io.wavfile as wavfile #importing libraries
import sounddevice as sd
import scipy.fft as fft
import scipy.fftpack as fftpk

fs = 44100  # Sample rate
seconds = 5  # Duration of recording
data = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype = 'float32')
data = data.reshape(len(data))
sd.wait()

t=np.linspace(0,len(data)/fs,len(data))#sample to time 
plt.figure(1) #separate figure
plt.plot(t,data) #plotting in time domain
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.title('Time domain')
dataf=np.fft.fft(data) #FFT function
fd=abs(dataf) #Taking absolute values
x=fd[0:int((len(fd)/2)-1)] #Half Range
faxis=np.linspace(0,fs/2,len(x)) #Range frequency axis

plt.figure(2) #separate figure
plt.xlabel('frequency')
plt.ylabel('Amplitude in dB')
plt.title('Frequency Domain')
plt.xscale('log') #plotting x-axis in logarithmic axis
plt.plot(faxis,20*np.log10(x/len(data)))# plotting frequency axis vs amplitude(dB)

k1=int(len(dataf)/fs*1000) #index place for 1000Hz
k2=int(len(dataf)/fs*10000) #index place for 10000Hz
n1=int(len(dataf)/fs*0.1) #index place for 0.1Hz
n2=int(len(dataf)/fs*90) #index place for 90Hz
n3=int(len(dataf)/fs*10001) #index place for 1001Hz
n4=int(len(dataf)/fs*25000) #index place for 25000Hz


dataf[n3:n4]=dataf[n3:n4]/90 # Noise reduction 
dataf[int(len(dataf)-n4):int(len(dataf)-n3)]=dataf[int(len(dataf)-n4):int(len(dataf)-n3)]/90
dataf[n1:n2]=dataf[n1:n2]/90
dataf[int(len(dataf)-n2):int(len(dataf)-n1)]=dataf[int(len(dataf)-n2):int(len(dataf)-n1)]/90

dataf[k1:k2]=dataf[k1:k2]*10 # hamonics amplification 
dataf[int(len(dataf)-k2):int(len(dataf)-k1)]=dataf[int(len(dataf)-k2):int(len(dataf)-k1)]*10


plt.figure(3) # separate figure
plt.plot(faxis,20*np.log10(dataf[0:int(len(dataf)/2)-1]/len(dataf)))# frequency vs amplitude(db)
plt.xlabel('frequency')
plt.ylabel('Amplitude in dB')
plt.title('Improved frequency domain')
plt.xscale('log') #plotting x-axis in logarithmic axis


enhanced=np.fft.ifft(dataf) #IFFT function transform to time domain
clr=np.real(enhanced) # Real part extraction
audio = clr.astype(np.float32) #Convert to 32 bit data

plt.figure(4) #separate figure
plt.plot(t,clr) #plotting in time domain
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.title('Improved time domain')
plt.show()

sd.play(audio, fs)
sd.wait()



wavfile.write('improved.wav',fs,audio) #writing enhanced audio file