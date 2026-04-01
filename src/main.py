import asyncio
import os.path
from kivy.app import App
from kivy.cache import Cache
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.utils import platform


class PicacgViewerApp(App):
    config_store = None
    api_client = None
    picture_client = None

    def build(self):
        self.config_store = JsonStore(os.path.join(self.user_data_dir, 'config.json'))
        return super().build()


if __name__ == '__main__':
    # 重置字体
    LabelBase.register(
        name='Roboto',
        fn_regular='./fonts/SourceHanSansCN-Regular.otf',
        fn_bold='./fonts/SourceHanSansCN-Bold.otf'
    )
    # 测试以适配手机
    if platform != 'android' and platform != 'ios':
        Window.size = (360, 640)
    Cache.register('images', 64, 300)
    Cache.register('comic_images', 32, 300)
    Builder.load_file('styles.kv')
    asyncio.run(PicacgViewerApp().async_run('asyncio'))
