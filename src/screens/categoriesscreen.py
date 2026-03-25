import asyncio
import traceback
from httpx import HTTPError
from kivy.lang import Builder
from kivy.app import App
from kivy.metrics import dp
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from picaapi.client import Client as PicaClient
from screens.manager import ReuseScreen


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
            except HTTPError:
                if i == 2:
                    self.ids.def_label.text = traceback.format_exc()
                    return
        if categories is None:
            return

        gird = GridLayout(cols=3, size_hint_y=None, spacing=[dp(8), dp(8)], padding=[dp(8), dp(8)])
        gird.bind(minimum_height=gird.setter('height'))
        self.ids.scroll.clear_widgets()
        self.ids.scroll.add_widget(gird)
        for i in categories:
            image = CategoryItem(text=i.title, image_path=i.thumb.path, isWeb=i.isWeb, link=('' if i.link is None else i.link))
            image.load()
            gird.add_widget(image)

    def open_search(self):
        self.manager.screen_open('search')


class CategoryItem(ButtonBehavior, BoxLayout):
    text = StringProperty()
    image_path = StringProperty()
    isWeb = BooleanProperty(False)
    link = StringProperty()

    def load(self):
        self.ids.image.load()

    def on_release(self):
        if self.isWeb:
            pass
        else:
            App.get_running_app().root.screen_open('comics', ('c', self.text, 'dd', 1))


Builder.load_file('screens/categoriesscreen.kv')
