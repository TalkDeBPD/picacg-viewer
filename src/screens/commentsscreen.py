import asyncio
from httpx import HTTPError
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.properties import StringProperty, ListProperty
from picaapi.client import Client as PicaClient
from screens.manager import PageScreen
from widgets.popup import MessagePopup
from widgets.commentitem import CommentItem


class CommentsScreen(PageScreen):
    comic_id = StringProperty()
    docs = ListProperty([])
    top = ListProperty([])
    cache = {}
    _locked = False

    def load_content(self, args: tuple):
        self.comic_id, self.pindex = args
        asyncio.create_task(self.async_load_content())

    async def async_load_content(self):
        if self._locked:
            return
        try:
            self._locked = True
            args = self._build_args()
            if args in self.cache:
                self.docs, self.top, self.ptotal = self.cache[args]
            else:
                api_client = App.get_running_app().api_client
                assert isinstance(api_client, PicaClient)
                for i in range(3):
                    try:
                        page, self.top = await api_client.comments(self.comic_id, self.pindex)
                        self.docs = page.docs
                        self.ptotal = page.pages
                    except HTTPError:
                        if i == 2:
                            raise
            self.ids.docs.clear_widgets()
            for i in self.top:
                item = CommentItem(comment=i)
                self.ids.docs.add_widget(item)
            for i in self.docs:
                item = CommentItem(comment=i)
                self.ids.docs.add_widget(item)
        except HTTPError as e:
            MessagePopup(text=f'{type(e).__name__}: {e}', title='错误！').open()
        finally:
            self._locked = False

    def save_content(self):
        args = self._build_args()
        if not self._locked:
            self.cache[args] = (self.docs, self.top, self.ptotal)
        return args

    def _build_args(self):
        return self.comic_id, self.pindex

    def load_page(self):
        asyncio.create_task(self.async_load_content())


Builder.load_file('screens/commentsscreen.kv')
