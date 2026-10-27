import asyncio
from httpx import HTTPError
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from picaapi.client import Client as PicaClient
from util import format_http_error
from screens.manager import PageScreen
from widgets.comicitem import ComicItem
from widgets.popup import MessagePopup


class FavoriteScreen(PageScreen):
    sort = StringProperty('dd')
    docs = []
    cache = {}
    _locked = False
    _initial = True

    def on_kv_post(self, base_widget):
        self.ids.sort.bind(value=lambda _w, _v: self.flush())

    def save_content(self) -> tuple:
        return (self.pindex,)

    def load_content(self, args):
        if not args:
            args = (1,)
        if self._initial:
            self.cache.clear()
            self.load_page()
        elif self.pindex != args[0]:
            self.pindex = args[0]
            self.load_page()

    async def async_load_content(self):
        if self._locked:
            return
        try:
            self._locked = True
            if self.pindex in self.cache:
                self.docs = self.cache[self.pindex]
            else:
                api_client = App.get_running_app().api_client
                assert isinstance(api_client, PicaClient)
                for i in range(3):
                    try:
                        page = await api_client.favourite(self.sort, self.pindex)
                        self.pindex = page.page
                        self.ptotal = page.pages
                        self.docs = page.docs
                        self._initial = False
                        if self.pindex not in self.cache:
                            self.cache[self.pindex] = self.docs
                    except HTTPError:
                        if i == 2:
                            raise
            # 更新控件
            self.ids.page_index.text = str(self.pindex)
            self.ids.docs.clear_widgets()
            for comic in self.docs:
                item = ComicItem(comic=comic)
                item.load()
                self.ids.docs.add_widget(item)
        except HTTPError as e:
            MessagePopup(text=format_http_error(e), title='错误').open()
        finally:
            self._locked = False

    def flush(self):
        try:
            self.pindex = int(self.ids.page_index.text)
        except ValueError:
            self.pindex = 1
        self.sort = self.ids.sort.value
        asyncio.create_task(self.async_load_content())

    def fresh_cache(self):
        self.cache.clear()

    def load_page(self):
        asyncio.create_task(self.async_load_content())


Builder.load_file('screens/favoritescreen.kv')
