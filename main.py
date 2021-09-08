from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.logger import Logger
import sounddevice as sd
from scipy.io.wavfile import write
import soundfile as sf
from FFT import FFT
from kivy.graphics import *
from kivy.core.window import Window
from kivy.lang import Builder

KV = '''
MDScreen:
    Widget:
        canvas:
            Color:
                rgba: 0.952,0.945,0.956,1
            Rectangle:
                size: self.size
                pos: self.pos

    MDLabel:
        text: "Let's try my model App !"
        pos_hint: {"center_x": .9, "center_y": .7}
        theme_text_color: "Custom"
        text_color: 0, 0, 0, 1
        
    
    MDRoundFlatIconButton:
        icon: "close"
        text: "Close window"
        text_color: 1, 1, 1, 1
        pos_hint: {"center_x": .5, "center_y": .6}
        md_bg_color: 0.4,0.525,0.776,1
        on_press: app.closewindow()
        
    MDRoundFlatIconButton:
        icon: "record"
        text: "record"
        text_color: 1, 1, 1, 1
        pos_hint: {"center_x": .5, "center_y": .5}
        md_bg_color: 0.384,0.56,0.65,1
        on_press: app.clickrecord()
        
    MDRoundFlatIconButton:
        icon: "square"
        text: "play"
        text_color: 0.384,0.56,0.65,1
        pos_hint: {"center_x": .5, "center_y": .4}
        md_bg_color: 1,0.882,0.678,1
        on_press: app.clickplay()
        
    MDRoundFlatIconButton:
        icon: "play"
        text: "FFT"
        text_color: 1, 1, 1, 1
        pos_hint: {"center_x": .5, "center_y": .3}
        md_bg_color: 0.941,0.549,0.505,1
        on_press: app.clickFFT()
        
'''


class Noiseless(MDApp):

    def build(self):
        self.icon = 'myicon.png'
        return Builder.load_string(KV)

    def closewindow(self_):
        MDApp.get_running_app().stop()
        Window.close()

    def clickrecord(self_):

        fs = 44100  # Sample rate
        seconds = 10  # Duration of recording

        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
        sd.wait()  # Wait until recording is finished
        write('output.wav', fs, myrecording)  # Save as WAV file


    def clickplay(self_):

        filename = 'output.wav'
        data, fs = sf.read(filename)
        sd.play(data, fs)
        sd.wait()

    def clickFFT(self_):
        FFT()

Noiseless().run()