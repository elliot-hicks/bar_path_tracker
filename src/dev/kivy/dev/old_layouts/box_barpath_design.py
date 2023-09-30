from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_file("box_barpath_design.kv")


class BoxBarPathLayout(Widget):
    pass


class BarPathApp(App):
    def build(self):
        return BoxBarPathLayout()


BarPathApp().run()
