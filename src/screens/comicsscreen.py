import asyncio
from httpx import HTTPError
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from picaapi.client import Client as PicaClient
from screens.manager import ReuseScreen
from widgets.comicitem import ComicItem


class ComicsScreen(ReuseScreen):
    KEYS: dict[str, str] = {
        'c': '分类',
        't': '标签',
        'a': '作者',
        'ca': '骑士',
        'ct': '汉化',
    }
    key = StringProperty()
    value = StringProperty()
    pindex = NumericProperty(1)
    sort = StringProperty('dd')
    ptotal = NumericProperty(1)
    docs = []
    cache = {}

    def save_content(self) -> tuple:
        args = self._build_args()
        if args not in self.cache and self.docs:
            self.cache[args] = (self.ptotal, self.docs)
        return args

    def load_content(self, args):
        if self._build_args() != args:
            self.key, self.value, self.sort, self.pindex = args
            asyncio.create_task(self.async_load_content())

    async def async_load_content(self):
        args = self._build_args()
        if args in self.cache:
            self.ptotal, docs = self.cache[args]
        else:
            api_client = App.get_running_app().api_client
            assert isinstance(api_client, PicaClient)
            for i in range(3):
                try:
                    page = await api_client.comics(self.key, self.value, self.sort, self.pindex)
                    self.pindex = page.page
                    self.ptotal = page.pages
                    self.docs = page.docs
                except HTTPError:
                    if i == 2:
                        return
        # 更新控件
        self.ids.page_index.text = str(self.pindex)
        self.ids.docs.clear_widgets()
        for comic in self.docs:
            item = ComicItem(comic=comic)
            item.load()
            self.ids.docs.add_widget(item)

    def flush(self):
        try:
            self.pindex = int(self.ids.page_index.text)
        except ValueError:
            self.pindex = 1
        self.sort = self.ids.sort.value
        asyncio.create_task(self.async_load_content())

    def _build_args(self) -> tuple:
        return self.key, self.value, self.sort, self.pindex


Builder.load_file('screens/comicsscreen.kv')
