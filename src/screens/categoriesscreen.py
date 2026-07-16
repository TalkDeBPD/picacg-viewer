import asyncio
from httpx import HTTPError
from kivy.lang import Builder
from kivy.app import App
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from picaapi.client import Client as PicaClient
from util import format_http_error
from screens.manager import ReuseScreen
from widgets.popup import MessagePopup


class CategoriesScreen(ReuseScreen):
    def __init__(self, **kwargs):
        super(CategoriesScreen, self).__init__(**kwargs)
        self._loaded = False

    def on_pre_enter(self):
        if not self._loaded:
            asyncio.create_task(self.async_load())
            self._loaded = True
        return super(CategoriesScreen, self).on_pre_enter()

    async def async_load(self):
        app = App.get_running_app()
        assert isinstance(app.api_client, PicaClient)

        categories = None
        for i in range(0, 3):
            try:
                categories = await app.api_client.categories()
                break
            except HTTPError as e:
                if i == 2:
                    MessagePopup(text=format_http_error(e), title='错误').open()
                    return
        if categories is None:
            return

        for i in self.ids.gl.children:
            if isinstance(i, CategoryItem): i.load()
        for i in categories:
            image = CategoryItem(text=i.title, image_path=i.thumb.path, is_web=i.isWeb, link=('' if i.link is None else i.link))
            image.load()
            self.ids.gl.add_widget(image)

    def open_search(self):
        self.manager.screen_open('search')


class CategoryItem(ButtonBehavior, BoxLayout):
    text = StringProperty()
    image_path = StringProperty()
    img_saved = BooleanProperty(False)
    image = ObjectProperty(None)
    is_web = BooleanProperty(False)
    link = StringProperty()

    def load(self):
        self.ids.image.load()

    def on_release(self):
        if self.is_web:
            pass
        else:
            App.get_running_app().root.screen_open('comics', ('c', self.text, 'dd', 1))


Builder.load_file('screens/categoriesscreen.kv')
