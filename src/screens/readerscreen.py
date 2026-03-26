import asyncio
from httpx import HTTPError
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from picaapi.client import Client as PicaClient
from screens.manager import ReuseScreen
from widgets.image import ComicImage


class ReaderScreen(ReuseScreen):
    comic_id = StringProperty()
    order = NumericProperty(1)
    pindex = NumericProperty(1)
    ptotal = NumericProperty(1)
    scale = NumericProperty(1)
    title = StringProperty('')
    docs = []
    cache = {}
    _load_ok = False

    def save_content(self) -> tuple:
        args = self._build_args()
        if args not in self.cache and self._load_ok:
            self.cache[args] = (self.docs, self.ptotal, self.title)
        return args

    def load_content(self, args: tuple) -> None:
        self.comic_id, self.order, self.pindex = args
        asyncio.create_task(self.async_load_content())

    async def async_load_content(self):
        self._load_ok = False
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
                    self.cache[args] = (self.docs, self.ptotal)
                except HTTPError:
                    if i == 2:
                        return
        self._load_ok = True
        # 更新控件
        self.ids.docs.clear_widgets()
        for i in self.docs:
            image = ComicImage(path=i.path)
            image.load()
            self.ids.docs.add_widget(image)

    def last(self):
        if self.pindex > 1:
            self.pindex -= 1
            asyncio.create_task(self.async_load_content())

    def next(self):
        if self.pindex < self.ptotal:
            self.pindex += 1
            asyncio.create_task(self.async_load_content())

    def _build_args(self) -> tuple:
        return self.comic_id, self.order, self.pindex


Builder.load_file('screens/readerscreen.kv')
