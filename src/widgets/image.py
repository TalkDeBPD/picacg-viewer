import asyncio
import io

from httpx import HTTPError

from kivy.app import App
from kivy.cache import Cache
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from picaapi.downloader import PictureClient


async def load_texture(path, max_tries: int = 3):
    data = Cache.get('images', path)

    if data is None:
        picture_client = App.get_running_app().picture_client
        assert isinstance(picture_client, PictureClient)
        for i in range(max_tries):
            try:
                data = await picture_client.fetch(path)
                Cache.append('images', path, data)
                return CoreImage(io.BytesIO(data), ext='jpg').texture
            except HTTPError:
                if i + 1 == max_tries:
                    raise
        return None
    else:
        Cache.append('images', path, data)
        return CoreImage(io.BytesIO(data), ext='jpg').texture


class RetryImage(BoxLayout):
    max_tries = NumericProperty(3)
    path = StringProperty()
    fit_mode = StringProperty('contain')

    def load(self):
        asyncio.create_task(self.async_load())

    async def async_load(self):
        self.clear_widgets()
        label = Label(text='Loading...', valign='center', halign='center')
        label.bind(size=label.setter('text_size'))
        self.add_widget(label)
        try:
            texture = await load_texture(self.path, max_tries=self.max_tries)
            image = Image(texture=texture, fit_mode=self.fit_mode)
            self.clear_widgets()
            self.add_widget(image)
        except HTTPError as e:
            label.text = f'{type(e)}: {e}'


class ComicImage(BoxLayout):
    max_tries = NumericProperty(3)
    path = StringProperty()
    _lock = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, None)
        self.bind(minimum_height=self.setter('height'))

    def load(self):
        asyncio.create_task(self.async_load())

    async def async_load(self):
        self._lock = True
        self.clear_widgets()
        label = Label(text='Loading...')
        label.bind(width=self.setter('height'))
        self.add_widget(label)
        try:
            texture = await load_texture(self.path, max_tries=self.max_tries)
            image = Image(texture=texture, size_hint=(1, None), keep_ratio=True, fit_mode='cover')
            image.bind(image_ratio=ComicImage.set_height, width=ComicImage.set_height)
            self.clear_widgets()
            self.add_widget(image)
        except HTTPError as e:
            label.text = f'{type(e)}: {e}'
            self._lock = False

    def on_touch_up(self, touch):
        if not self._lock:
            self.load()

    @staticmethod
    def set_height(instance, _value):
        assert isinstance(instance, Image)
        instance.height = instance.width / instance.image_ratio
