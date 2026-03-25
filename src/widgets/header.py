from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout


class Header(BoxLayout):
    title = StringProperty('默认标题')


Builder.load_file('widgets/header.kv')
