from kivy.animation import Animation
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, ColorProperty
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.uix.behaviors import TouchRippleButtonBehavior
from kivy.uix.label import Label
from kivy.utils import rgba


class RippleButton(TouchRippleButtonBehavior, Label):
    background_color = ColorProperty(rgba('#ED97B7ff'))
    now_background_color = ColorProperty(rgba('#ED97B7ff'))
    press_background_color = ColorProperty(rgba('#E04D83FF'))
    background_color_duration = NumericProperty(0.05)
    radius = NumericProperty(0)

    def __init__(self, **kwargs):
        super(RippleButton, self).__init__(**kwargs)
        self.now_background_color = self.background_color

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            Animation(now_background_color=self.press_background_color, duration=self.background_color_duration).start(self)
        return super(RippleButton, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            Animation(now_background_color=self.background_color, duration=self.background_color_duration).start(self)
        return super(RippleButton, self).on_touch_up(touch)


class SortButton(RippleButton):
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

    def on_kv_post(self, base_widget):
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
            self.ids.ct.add_widget(bb)

    def set_value(self, value):
        self.value = value


Builder.load_file('widgets/button.kv')
