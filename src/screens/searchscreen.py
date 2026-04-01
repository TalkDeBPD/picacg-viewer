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


class SearchScreen(PageScreen):
    keyword = StringProperty()
    sort = StringProperty('dd')
    docs = []
    _locked = False

    def load(self):
        if not self._locked:
            asyncio.create_task(self.async_load())
            self._locked = True

    async def async_load(self):
        try:
            app = App.get_running_app()
            assert isinstance(app.api_client, PicaClient)
            for i in range(0, 3):
                try:
                    page = await app.api_client.advanced_search(self.keyword, sort=self.sort, page=self.pindex)
                    self.ptotal = page.pages
                    self.docs = page.docs
                    break
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

    def on_search(self):
        try:
            self.pindex = int(self.ids.page_index.text)
        except ValueError:
            self.pindex = 1
        self.keyword = self.ids.keyword.text
        self.sort = self.ids.sort.value
        self.load()

    def load_page(self):
        self.load()


Builder.load_file('screens/searchscreen.kv')
