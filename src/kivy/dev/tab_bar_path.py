from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.tabbedpanel import TabbedPanel

Builder.load_file("tab_design.kv")


class TabBarPath(TabbedPanel):
    pass


class BarPathApp(App):
    def build(self):
        return TabBarPath()


BarPathApp().run()
