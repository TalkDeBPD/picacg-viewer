from kivy.app import App
from kivy.lang.builder import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout

from screens.manager import MyScreenManager


class ComicItem(ButtonBehavior, BoxLayout):
    comic = ObjectProperty()

    def load(self):
        self.ids.image.load()

    def on_release(self):
        manager = App.get_running_app().root
        assert isinstance(manager, MyScreenManager)
        manager.screen_open('info', (self.comic.id, ))


Builder.load_file('widgets/comicitem.kv')
