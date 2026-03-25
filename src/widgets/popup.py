from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.popup import Popup


class MessagePopup(Popup):
    text = StringProperty()


Builder.load_file('widgets/popup.kv')
