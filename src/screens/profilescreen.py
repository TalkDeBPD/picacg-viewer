import asyncio
from httpx import HTTPError
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from picaapi.client import Client as PicaClient
from util import format_http_error
from screens.manager import ReuseScreen
from widgets.popup import MessagePopup


class ProfileScreen(ReuseScreen):
    profile = ObjectProperty(None)
    _locked = False

    def on_pre_enter(self):
        asyncio.create_task(self.async_load())

    async def async_load(self):
        if not self.profile and not self._locked:
            try:
                self._locked = True
                api_client = App.get_running_app().api_client
                assert isinstance(api_client, PicaClient)
                for i in range(3):
                    try:
                        self.profile = await api_client.profile()
                    except HTTPError:
                        if i == 2:
                            raise
                self.ids.avatar.load()
            except HTTPError as e:
                MessagePopup(text=format_http_error(e), title='错误').open()
            finally:
                self._locked = False


Builder.load_file('screens/profilescreen.kv')
