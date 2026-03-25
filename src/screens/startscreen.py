import asyncio
from httpx import HTTPError
from kivy.app import App
from kivy.lang import Builder

from picaapi.client import Client as PicaClient
from picaapi.error import PicaAPIError
from picaapi.downloader import PictureClient, DEFAULT_PICTURE_SERVER
from screens.manager import ReuseScreen
from widgets.popup import MessagePopup


class StartScreen(ReuseScreen):
    _locked = False

    def sign_in(self):
        if not self._locked:
            self._locked = True
            asyncio.create_task(self.async_sign_in())

    async def async_sign_in(self):
        app = App.get_running_app()
        if app.config_store.exists('apiserver') and app.config_store.get('apiserver')['data']:
            app.api_client = PicaClient(app.config_store.get('apiserver')['data'])
        else:
            app.api_client = PicaClient()
        if app.config_store.exists('pictureserver') and app.config_store.get('pictureserver')['data']:
            app.picture_client = PictureClient(app.config_store.get('pictureserver')['data'], max_conn=20)
        else:
            app.picture_client = PictureClient(DEFAULT_PICTURE_SERVER[1])

        try:
            flag: bool = False
            if app.config_store.exists('token') and app.config_store.get('token')['data']:
                try:
                    app.api_client.token = app.config_store.get('token')['data']
                    await app.api_client.categories()
                    flag = True
                except PicaAPIError:
                    pass
            if not flag and app.config_store.exists('email') and app.config_store.exists('password'):
                await app.api_client.login(app.config_store.get('email')['data'], app.config_store.get('password')['data'])
                app.config_store.put('token', data=app.api_client.token)
                flag = True
            if flag:
                self.manager.screen_open_start('categories')
        except HTTPError as e:
            MessagePopup(text=f'网络异常！\n{type(e).__name__}: {str(e)}', title='错误').open()
        except PicaAPIError:
            MessagePopup(text='请检查你的用户名/邮箱及密码是否设置正确！', title='错误').open()
        finally:
            self._locked = False



Builder.load_file('screens/startscreen.kv')
