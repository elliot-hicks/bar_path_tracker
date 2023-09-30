from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_file("barpath_design.kv")


class StartScreenGridLayout(Widget):
    name1 = ObjectProperty(None)
    name2 = ObjectProperty(None)
    name3 = ObjectProperty(None)

    def press(self):
        name1 = self.name1.text
        name2 = self.name2.text
        name3 = self.name3.text

        print(name1, name2, name3)

        self.name1.text = ""
        self.name2.text = ""
        self.name3.text = ""


class BarPathApp(App):
    def build(self):
        return StartScreenGridLayout()


BarPathApp().run()
