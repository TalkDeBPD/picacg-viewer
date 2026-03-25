from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty, ListProperty
from kivy.app import App
from kivy.uix.behaviors.touchripple import TouchRippleButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label


class ConfigPage(BoxLayout):
    store = None

    def __init__(self, **kwargs):
        super(ConfigPage, self).__init__(**kwargs)

    def load(self):
        self.store = App.get_running_app().config_store
        for child in self.children:
            if isinstance(child, ConfigItem) and self.store.exists(child.config_key):
                child.config_value = self.store.get(child.config_key).get('data', '')

    def get(self, key: str):
        return self.store.get(key).get('data', '') if self.store.exists(key) else ''

    def put(self, key: str, value: str):
        self.store.put(key, data=value)


class ConfigItem(TouchRippleButtonBehavior, BoxLayout):
    config_title = StringProperty()
    config_key = StringProperty()
    config_value = StringProperty()
    background_color = ListProperty([0, 0, 0, 0])
    isPressed = False

    def on_touch_down(self, touch):
        collide_point = self.collide_point(touch.x, touch.y)
        if collide_point:
            touch.grab(self)
            self.background_color = [0, 0, 0, 0.25]
            self.ripple_show(touch)
            self.isPressed = True
            return super().on_touch_down(touch)
        return False

    def on_touch_up(self, touch):
        if touch.grab_current is self and self.isPressed:
            touch.ungrab(self)
            self.background_color = [0, 0, 0, 0]
            self.ripple_fade()
            self.isPressed = False
            return super().on_touch_up(touch)
        return False

    def put(self):
        if isinstance(self.parent, ConfigPage):
            self.parent.put(self.config_key, self.config_value)


class StringConfigItem(ConfigItem):
    def __init__(self, **kwargs):
        super(StringConfigItem, self).__init__(**kwargs)

    def on_release(self):
        popup = StringConfigPopup(title=self.config_title, config_value=self.config_value, item=self)
        popup.open()


class StringConfigPopup(Popup):
    config_value = StringProperty()

    def __init__(self, item: StringConfigItem | None = None, **kwargs):
        super(StringConfigPopup, self).__init__(**kwargs)
        self.item = item

    def confirm(self):
        if self.item is not None:
            self.item.config_value = self.ids.input.text
            self.item.put()
        self.dismiss()


class SelectConfigItem(ConfigItem):
    config_options = ListProperty([])

    def on_release(self):
        SelectConfigPopup(self, title=self.config_title, config_value=self.config_value, config_options=self.config_options).open()


class SelectConfigPopup(Popup):
    config_value = StringProperty()
    config_options = ListProperty([])
    def __init__(self, item: StringConfigItem | None = None, **kwargs):
        super(SelectConfigPopup, self).__init__(**kwargs)
        self.item = item

    def on_kv_post(self, base_widget):
        super(SelectConfigPopup, self).on_kv_post(base_widget)
        for option in self.config_options:
            boxlayout = BoxLayout(height=dp(30), size_hint_y=None)
            checkbox = CheckBox(group='ops', size_hint_x=None)
            checkbox.kv = option
            if self.config_value == option:
                checkbox.active = True
            checkbox.bind(height=checkbox.setter('width'))
            checkbox.bind(active=(lambda instance, value: value and self.set_value(instance.kv)))
            label = Label(text=option, halign='left', valign='center', color=(1, 1, 1, 1))
            label.bind(size=label.setter('text_size'))
            boxlayout.add_widget(checkbox)
            boxlayout.add_widget(label)
            self.ids.ops.add_widget(boxlayout)

    def confirm(self):
        if self.item is not None:
            self.item.config_value = self.config_value
            self.item.put()
        self.dismiss()

    def set_value(self, value):
        self.config_value = value


Builder.load_file('widgets/config.kv')
