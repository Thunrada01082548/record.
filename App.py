from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.logger import Logger
import sounddevice as sd
from scipy.io.wavfile import write
import soundfile as sf
import FFT as FFT

class myapp(BoxLayout):
    def __init__(self,**kwargs):
        super(myapp,self).__init__(**kwargs)
        self.padding = 250

        btn1 = Button(text='Close Window')
        btn2 = Button(text='record')
        btn3 = Button(text='play')
        btn4 = Button(text='FFT')
        btn1.bind(on_press=self.clkfunc)
        btn2.bind(on_press=self.record)
        btn3.bind(on_press=self.record)
        btn4.bind(on_press=FFT)
        self.add_widget(btn1)
        self.add_widget(btn2)
        self.add_widget(btn3)
        self.add_widget(btn4)

    def clkfunc(self , obj):
        App.get_running_app().stop()
        Window.close()

    def record(self , obj):

        fs = 44100  # Sample rate
        seconds = 5  # Duration of recording

        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
        sd.wait()  # Wait until recording is finished
        write('output.wav', fs, myrecording)  # Save as WAV file


    def play(self , obj):


        filename = 'output.wav'
        data, fs = sf.read(filename)
        sd.play(data, fs)
        sd.wait()


class SimpleKivy(App):
    def on_stop(self):
        Logger.critical('App: Aaaargh I\'m dying!')

    def build(self):
        return myapp()


if __name__ == '__main__':
    SimpleKivy().run()