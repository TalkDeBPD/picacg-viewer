import asyncio
import json
import aiofiles
import webbrowser
from kivy.lang import Builder
from kivy.app import App
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from picaapi.objects import Category
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
        async with aiofiles.open('cached/categories.json', mode='r') as f:
            content = await f.read()
        data = json.loads(content)
        categories = [Category(i) for i in data['categories']]

        for i in self.ids.gl.children:
            if isinstance(i, CategoryItem): i.load()
        for i in categories:
            image = CategoryItem(text=i.title, image_path=f'img/categories/{i.thumb.originalName}', is_web=i.isWeb, link=('' if i.link is None else i.link), img_saved=True)
            image.load()
            self.ids.gl.add_widget(image)


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
            webbrowser.open(self.link)
        else:
            App.get_running_app().root.screen_open('comics', ('c', self.text, 'dd', 1))


Builder.load_file('screens/categoriesscreen.kv')
