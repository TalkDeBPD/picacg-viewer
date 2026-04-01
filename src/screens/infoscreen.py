import asyncio
from httpx import HTTPError
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from picaapi.client import Client as PicaClient
from util import format_http_error
from screens.manager import ReuseScreen
from widgets.popup import MessagePopup


class InfoScreen(ReuseScreen):
    cache = {}
    comic = ObjectProperty()
    args = ('',)
    _locked = False

    def __init__(self, **kwargs):
        super(InfoScreen, self).__init__(**kwargs)
        self.bind(comic=self.update_comic)

    def save_content(self):
        return self.args

    def load_content(self, args: tuple):
        if args[0] != self.args[0]:
            self.args = args
            asyncio.create_task(self.async_load_content())

    async def async_load_content(self):
        if self._locked:
            return
        try:
            self._locked = True
            if self.args[0] in self.cache:
                self.comic = self.cache[self.args[0]]
            else:
                app = App.get_running_app()
                assert isinstance(app.api_client, PicaClient)
                for i in range(0, 3):
                    try:
                        self.comic = await app.api_client.comic(self.args[0])
                        self.cache[self.args[0]] = self.comic
                        break
                    except HTTPError:
                        if i == 2:
                            raise
            self.ids.image.load()
        except HTTPError as e:
            MessagePopup(text=format_http_error(e), title='错误').open()
        finally:
            self._locked = False

    def update_comic(self, _i, _v):
        if self.comic is None:
            return
        self.ids.tags.clear_widgets()
        for i in self.comic.categories:
            self.ids.tags.add_widget(CategoryLabel(text=i))
        for i in self.comic.tags:
            self.ids.tags.add_widget(TagLabel(text=i))


class CategoryLabel(ButtonBehavior, Label):
    def on_release(self):
        App.get_running_app().root.screen_open('comics', ('c', self.text, 'dd', 1))


class TagLabel(ButtonBehavior, Label):
    def on_release(self):
        App.get_running_app().root.screen_open('comics', ('t', self.text, 'dd', 1))


Builder.load_file('screens/infoscreen.kv')
