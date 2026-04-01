import asyncio
from httpx import HTTPError
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from picaapi.client import Client as PicaClient
from util import format_http_error
from screens.manager import PageScreen
from widgets.image import ComicImage
from widgets.popup import MessagePopup


class ReaderScreen(PageScreen):
    comic_id = StringProperty()
    order = NumericProperty(1)
    scale = NumericProperty(1)
    title = StringProperty('')
    docs = []
    cache = {}
    _locked = False

    def save_content(self) -> tuple:
        return self._build_args()

    def load_content(self, args: tuple) -> None:
        self.comic_id, self.order, self.pindex = args
        asyncio.create_task(self.async_load_content())

    async def async_load_content(self):
        if self._locked:
            return
        try:
            self._locked = True
            args = self._build_args()
            if args in self.cache:
                self.docs = self.cache[args][0]
                self.ptotal = self.cache[args][1]
                self.title = self.cache[args][2]
            else:
                api_client = App.get_running_app().api_client
                assert isinstance(api_client, PicaClient)
                for i in range(3):
                    try:
                        page, self.title = await api_client.pages(self.comic_id, self.order, self.pindex)
                        self.docs = page.docs
                        self.ptotal = page.pages
                        self.cache[args] = (self.docs, self.ptotal, self.title)
                    except HTTPError:
                        if i == 2:
                            raise
            # 更新控件
            self.ids.docs.clear_widgets()
            for i in self.docs:
                image = ComicImage(path=i.path)
                image.load()
                self.ids.docs.add_widget(image)
        except HTTPError as e:
            MessagePopup(text=format_http_error(e), title='错误').open()
        finally:
            self._locked = False

    def _build_args(self) -> tuple:
        return self.comic_id, self.order, self.pindex

    def load_page(self):
        asyncio.create_task(self.async_load_content())


Builder.load_file('screens/readerscreen.kv')
