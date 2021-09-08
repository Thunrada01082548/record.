import numpy as np #importing libraries
import matplotlib.pyplot as plt #importing libraries
import scipy.io.wavfile as wavfile #importing libraries
import sounddevice as sd
import scipy.fft as fft
import scipy.fftpack as fftpk
import soundfile as sf

def FFT():
    plt.rcParams['figure.figsize'] = [10,16]
    plt.rcParams.update({'font.size': 18})
    plt.style.use('seaborn')

    filename = 'output.wav'
    data, fs = sf.read(filename)

    n = len(data)
    t=np.linspace(0,len(data)/fs,n)#sanmple to time


    fhat = fft.fft(data) #computes the fft
    psd = fhat * np.conj(fhat)/n
    freq = fftpk.fftfreq(len(data), (1.0/fs)) #frequency array
    idxs_half = np.arange(0, n//2) #first half index

    th1=int(len(fhat)/fs*500) #index place for 500Hz
    th2=int(len(fhat)/fs*8000) #index place for 8000Hz

    k1=int(len(fhat)/fs*1000) #index place for 1000Hz
    k2=int(len(fhat)/fs*10000) #index place for 10000Hz
    n1=int(len(fhat)/fs*0.1) #index place for 0.1Hz
    n2=int(len(fhat)/fs*90) #index place for 90Hz
    n3=int(len(fhat)/fs*10001) #index place for 1001Hz
    n4=int(len(fhat)/fs*25000) #index place for 25000Hz

    threshold = 0.25
    psd_idxs = np.ones(n)
    psd_idxs[:th1] = psd[:th1] > threshold #array of 0 and 1
    psd_idxs[th2:] = psd[th2:] > threshold #array of 0 and 1
    psd_clean = psd * psd_idxs #zero out all the unnecessary powers
    fhat_clean = psd_idxs * fhat #used to retrieve the signal
    fhat = fhat_clean

    fd=abs(fhat) #Taking absolute values
    x=fd[0:int((len(fd)/2)-1)] #Half Range
    faxis=np.linspace(0,fs/2,len(x)) #Range frequency axis


    fhat[n3:n4]=fhat[n3:n4]/60 # Noise reduction
    fhat[int(len(fhat)-n4):int(len(fhat)-n3)]=fhat[int(len(fhat)-n4):int(len(fhat)-n3)]/60
    fhat[n1:n2]=fhat[n1:n2]/60
    fhat[int(len(fhat)-n2):int(len(fhat)-n1)]=fhat[int(len(fhat)-n2):int(len(fhat)-n1)]/60

    fhat[k1:k2]=fhat[k1:k2]*10# hamonics amplification
    fhat[int(len(fhat)-k2):int(len(fhat)-k1)]=fhat[int(len(fhat)-k2):int(len(fhat)-k1)]*10


    enhanced=np.fft.ifft(fhat) #IFFT function transform to time domain
    clr=np.real(enhanced) # Real part extraction
    audio = clr.astype(np.float32) #Convert to 32 bit data

    sd.play(audio, fs)
    sd.wait()



    wavfile.write('improved.wav',fs,audio) #writing enhanced audio file