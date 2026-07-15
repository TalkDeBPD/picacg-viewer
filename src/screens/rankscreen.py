import asyncio
from httpx import HTTPError
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty, ListProperty
from picaapi.client import Client as PicaClient
from util import format_http_error
from screens.manager import ReuseScreen
from widgets.comicitem import ComicItem
from widgets.popup import MessagePopup

class RankScreen(ReuseScreen):
    docs = [[], [], []]
    txts = ListProperty([ '日排行', '周排行', '月排行' ])
    rid = NumericProperty(0)

    def __init__(self, **kwargs):
        super(RankScreen, self).__init__(**kwargs)
        self.bind(rid=self.rid_changed)

    def load_content(self, args):
        if not self.docs[0]:
            asyncio.create_task(self.async_load_content())

    async def async_load_content(self):
        try:
            api_client = App.get_running_app().api_client
            assert isinstance(api_client, PicaClient)
            for i in range(3):
                try:
                    if not self.docs[0]: self.docs[0] = await api_client.leaderboard('H24')
                    if not self.docs[1]: self.docs[1] = await api_client.leaderboard('D7')
                    if not self.docs[2]: self.docs[2] = await api_client.leaderboard('D30')
                except HTTPError:
                    if i == 2:
                        raise
            # 更新控件
            self.ids.docs.clear_widgets()
            for comic in self.docs[self.rid]:
                item = ComicItem(comic=comic)
                item.load()
                self.ids.docs.add_widget(item)
        except HTTPError as e:
            MessagePopup(text=format_http_error(e), title='错误').open()

    def rid_changed(self, widget, value):
        self.ids.docs.clear_widgets()
        for comic in self.docs[self.rid]:
            item = ComicItem(comic=comic)
            item.load()
            self.ids.docs.add_widget(item)


Builder.load_file('screens/rankscreen.kv')
