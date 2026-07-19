import asyncio
from datetime import date
from httpx import HTTPError
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.utils import rgba
from picaapi.base import Gender
from picaapi.client import Client as PicaClient
from picaapi.error import PicaAPIError
from util import format_http_error
from screens.manager import ReuseScreen
from widgets.popup import MessagePopup


GENDERS = {
    '绅士': Gender.MALE,
    '淑女': Gender.FEMALE,
    '机械人': Gender.BOT
}


class RegisterScreen(ReuseScreen):
    _locked = False
    gender = Gender.BOT
    dropdown = DropDown()

    def on_kv_post(self, base_widget):
        today = date.today()
        self.ids.year.text = str(today.year - 18)
        self.ids.month.text = str(today.month)
        self.ids.date.text = str(today.day)
        for k, v in GENDERS.items():
            btn = Button(text=k, size_hint_y=None, height=30, background_color=rgba('#FFFFFFFF'), color=rgba('#E04D83FF'))
            btn.bind(on_release=self.set_gender)
            self.dropdown.add_widget(btn)
        self.ids.gender.bind(on_release=self.dropdown.open)

    def register(self):
        if not self._locked:
            self._locked = True
            asyncio.create_task(self.async_register())

    async def async_register(self):
        app = App.get_running_app()
        if app.config_store.exists('apiserver') and app.config_store.get('apiserver')['data']:
            client = PicaClient(app.config_store.get('apiserver')['data'])
        else:
            client = PicaClient()
        try:
            # 输入合法性判断
            if not (self.ids.name.text and self.ids.email.text and self.ids.question1.text and self.ids.answer1.text and self.ids.question2.text and self.ids.answer2.text and self.ids.question3.text and self.ids.answer3.text):
                raise ValueError('请检查是否有空行！')
            if len(self.ids.pwd.text) < 8:
                raise ValueError('密码应至少为8位！')
            if self.ids.pwd.text != self.ids.pwd2.text:
                raise ValueError('重复密码不相同！')
            # 成年判断逻辑
            birthday = date(int(self.ids.year.text), int(self.ids.month.text), int(self.ids.date.text))
            today = date.today()
            try:
                target = date(today.year - 18, today.month, today.day)
            except ValueError:
                target = date(today.year - 18, 2, 28)
            if target < birthday:
                raise ValueError('未成年！')
            # 注册
            await client.register(self.ids.email.text, self.ids.pwd.text, self.ids.name.text, self.gender, birthday, self.ids.question1.text, self.ids.answer1.text, self.ids.question2.text, self.ids.answer2.text, self.ids.question3.text, self.ids.answer3.text)
            MessagePopup(text='注册成功！').open()
            self.manager.screen_back()
        except PicaAPIError as e:
            MessagePopup(text=e.message, title='注册错误').open()
        except ValueError as e:
            MessagePopup(text=str(e), title='输入错误').open()
        except HTTPError as e:
            MessagePopup(text=format_http_error(e), title='网络错误').open()
        finally:
            await client.close()
            self._locked = False

    def set_gender(self, widget):
        self.gender = GENDERS[widget.text]
        self.ids.gender.text = widget.text
        widget.parent.parent.dismiss()


Builder.load_file('screens/registerscreen.kv')
