from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout


class CommentItem(BoxLayout):
    comment = ObjectProperty()

    def on_kv_post(self, widget):
        self.ids.image.load()


Builder.load_file('widgets/commentitem.kv')
