from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.popup import Popup


class SortButton(Button):
    value = StringProperty('dd')
    SORT_DICT = {
        'dd': '新到旧',
        'da': '旧到新',
        'ld': '最多爱心',
        'vd': '最多观看',
    }
    def on_release(self):
        popup = SortPopup(value=self.value)
        popup.bind(value=self.setter('value'))
        popup.open()


class SortPopup(Popup):
    value = StringProperty('dd')

    def __init__(self, **kwargs):
        super(SortPopup, self).__init__(**kwargs)
        wid = BoxLayout(orientation='vertical')
        for i, v in SortButton.SORT_DICT.items():
            bb = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(30))
            cb = CheckBox(group='sort', size_hint_x=None, active=(i == self.value))
            cb.kv = i
            cb.bind(active=lambda ins, x: x and self.set_value(ins.kv))
            cb.bind(height=cb.setter('width'))
            bb.add_widget(cb)
            label = Label(text=v, halign='left', valign='center', color=(1, 1, 1, 1))
            label.bind(size=label.setter('text_size'))
            bb.add_widget(label)
            wid.add_widget(bb)
        self.add_widget(wid)

    def set_value(self, value):
        self.value = value


Builder.load_file('widgets/sort.kv')
