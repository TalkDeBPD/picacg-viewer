from kivy.lang import Builder

from screens.manager import ReuseScreen

class ConfigScreen(ReuseScreen):
    def __init__(self, **kwargs):
        super(ConfigScreen, self).__init__(**kwargs)
        self._loaded = False

    def on_enter(self, *args):
        if not self._loaded:
            self.ids.bl.load()
            self._loaded = True


Builder.load_file('screens/configscreen.kv')
