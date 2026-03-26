import asyncio
from httpx import HTTPError
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from picaapi.client import Client as PicaClient
from screens.manager import ReuseScreen, MyScreenManager
from widgets.popup import MessagePopup


class EpsScreen(ReuseScreen):
    comic_id = StringProperty()
    eps = ListProperty([])
    cache = {}

    def load_content(self, args: tuple):
        self.comic_id = args[0]
        asyncio.create_task(self.async_load())

    async def async_load(self):
        if self.comic_id in self.cache:
            self.eps = self.cache[self.comic_id]
        else:
            api_client = App.get_running_app().api_client
            assert isinstance(api_client, PicaClient)
            async def retry_get_page(page):
                for i in range(3):
                    try:
                        return await api_client.eps(self.comic_id, page)
                    except HTTPError:
                        if i == 2:
                            raise
                return None
            try:
                p1 = await retry_get_page(1)
                assert p1 is not None
                tasks = [retry_get_page(i) for i in range(2, p1.pages + 1)]
                rslt = await asyncio.gather(*tasks)
                self.eps = p1.docs
                for r in rslt:
                    self.eps += r.docs
            except HTTPError as e:
                MessagePopup(title='网络错误', text=f'{type(e).__name__}:{e}').open()
                return

        self.ids.grid.clear_widgets()
        for i in self.eps:
            eb = EpsButton(comic_id=self.comic_id, order=i.order, text=i.title)
            self.ids.grid.add_widget(eb)
        if len(self.eps) < 4:
            for i in range(4 - len(self.eps)):
                self.ids.grid.add_widget(Widget(size_hint_y=None))

    def save_content(self) -> tuple:
        if self.comic_id and self.comic_id not in self.cache:
            self.cache[self.comic_id] = self.eps
        return (self.comic_id,)


class EpsButton(ButtonBehavior, Label):
    comic_id = StringProperty()
    order = NumericProperty(1)

    def on_release(self):
        manager = App.get_running_app().root
        assert isinstance(manager, MyScreenManager)
        manager.screen_open('reader', (self.comic_id, self.order, 1))


Builder.load_file('screens/epsscreen.kv')
