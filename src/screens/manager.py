from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, CardTransition, Screen


class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.history: list[tuple[str, tuple]] = []
        self.transition = CardTransition(duration=0.3)
        Window.bind(on_keyboard=self.on_keyboard)

    def screen_back(self):
        if self.history:
            self.current_screen.save_content()
            last = self.history.pop()
            self.transition.direction = 'right'
            self.transition.mode = 'pop'
            self.current = last[0]
            screen = self.get_screen(last[0])
            assert isinstance(screen, ReuseScreen)
            screen.load_content(last[1])
        else:
            App.get_running_app().stop()

    def screen_open(self, screen_name: str, args: tuple = ()):
        assert isinstance(self.current_screen, ReuseScreen)
        olds = self.current_screen.save_content()
        self.history.append((self.current, olds))
        self.transition.direction = 'left'
        self.transition.mode = 'push'
        self.current = screen_name
        screen = self.get_screen(screen_name)
        assert isinstance(screen, ReuseScreen)
        screen.load_content(args)

    def screen_open_start(self, screen_name: str):
        self.history = []
        self.transition.direction = 'left'
        self.transition.mode = 'push'
        self.current = screen_name

    def on_keyboard(self, _window, key, _scancode, _action, _mods):
        if key == 27:
            self.screen_back()
            return True
        return False


class ReuseScreen(Screen):
    def save_content(self) -> tuple:
        return ()
    def load_content(self, args: tuple):
        pass

