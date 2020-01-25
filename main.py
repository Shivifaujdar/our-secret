import kivy

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget

#from kivymd.app import MDApp
#from kivymd.toast import toast
#from kivymd.uix.filemanager import MDFileManager

import os
from stegano import lsb, tools


class MainScreen(Screen):
    pass

class EmbedScreen(Screen):

    def open_embed(self, path, filename):
        try:
            with open(os.path.join(path, filename[0])) as f:

                # display the image
                self.ids.eimage.source = filename[0]

                offs = self.ids.offsetinte.text
                # use Stegano's tools to open the image for analysis
                theimg = tools.open_image(os.path.join(path, filename[0]))
                secret = lsb.hide(theimg, self.ids.secmsg.text, "UTF-8", int(offs))
                head, tail = os.path.split(filename[0])
                secret.save(os.path.join(path, "STEG-" + tail))
                print("FILE SAVED AS: STEG-" + tail)
                self.ids.savedmsg.text = "FILE SAVED AS:  STEG-" + tail
        except:
            print("Error in EMBED")

    def selected(self, filename):
        try:
            self.ids.eimage.source = filename[0]
            head, tail = os.path.split(filename[0])
            self.ids.revmsg.text = tail
            print("file selected:  " + tail)
        except:
            print("Error of some kind... probably no FILE selected b/c transversing up a Dir")

    pass

class RevealScreen(Screen):

    def open_reveal(self, path, filename):
        try:
            with open(os.path.join(path, filename[0])) as f:
                # display the image
                self.ids.rimage.source = filename[0]
                offs = self.ids.offsetintr.text
                theimg = tools.open_image(os.path.join(path, filename[0]))
                revealed = lsb.reveal(theimg, "UTF-8", int(offs))
                # PRINT THE RESPONSE
                if revealed:
                    self.ids.revmsg.text = revealed
                else:
                    self.ids.revmsg.text = "Nothing found."
        except:
            self.ids.revmsg.text = "Nothing Found."
            print("Error in REVEAL")

    def selected(self, filename):
        try:
            self.ids.rimage.source = filename[0]
            head, tail = os.path.split(filename[0])
            self.ids.revmsg.text = tail
            print("file selected:  " + tail)
        except:
            print("Error of some kind... probably no FILE selected b/c transversing up a Dir")

    pass


class SCRManager(ScreenManager):
    pass




class MyApp(App):


    def __init__(self, **kwargs):
        self.title = "Steg0saurus"
        super().__init__(**kwargs)

        #self.theme_cls.theme_style = "Dark"
        #self.theme_cls.primary_palette = "Teal"


    def build(self):
        kv = Builder.load_file("steg.kv")
        return kv


if __name__ == '__main__':
    MyApp().run()


