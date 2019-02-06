from plugin_framework.plugin import Plugin
from .widgets.hale_list import HaleListWidget

class Main(Plugin):
    #Klasa koja predstavlja konkretni plugin. Nasledjujemo "apstraktnu" klasu Plugin.
    #Ova klasa predstavlja plugin za aplikaciju kontakti (magacin).

    def __init__(self, spec):

        super().__init__(spec)

    def get_widget(self, parent=None): #Ova metoda vraca konkretni widget koji ce biti smesten u centralni deo aplikacije i njenog 
        #glavnog prozora. Može da vrati toolbar, kao i meni, koji će biti smešten u samu aplikaciju.
        
        return HaleListWidget(parent), None, None
