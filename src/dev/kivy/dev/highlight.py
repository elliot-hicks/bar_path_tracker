from kivy.core.window import Window

Window.clearcolor = (1, 1, 1, 1)
Window.size = (500, 500)

from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.uix.scatterlayout import ScatterLayout
from kivy.graphics.transformation import Matrix
from kivy.graphics import Color, Line, Rectangle, Ellipse
from kivy.uix.screenmanager import Screen
from kivy.graphics.svg import Svg

from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem


class AddImageTabs(TabbedPanelItem):
    def __init__(self, **kwargs):
        super(AddImageTabs, self).__init__(**kwargs)
        self.text = "Add Video"


class NewDataTabs(TabbedPanel):
    def __init__(self, **kwargs):
        super(NewDataTabs, self).__init__(**kwargs)


class SnapshotImageScreen(Screen):
    def __init__(self, **kwargs):
        super(SnapshotImageScreen, self).__init__(**kwargs)

    def on_kv_post(self, base_widget):
        i = Image(
            source="images/bar_path_black_png.png",
            allow_stretch=True,
            size_hint=(1, 1),  # =Window.size,
        )

        self.add_widget(i)


class HighlightCanvas(ScatterLayout):
    def __init__(self, **kwargs):
        super(HighlightCanvas, self).__init__(**kwargs)
        self.corner = None
        self.start_pos = [0, 0]

    def on_kv_post(self, base_widget):
        self.width = 0
        self.height = 0
        with self.canvas.before:
            Color(0, 0, 1, 0.1)
            self.r = Rectangle(pos=(0, 0), size_hint=(1, 1))

    def on_touch_down(self, touch):
        x, y = self.to_local(*touch.pos)
        self.r.size = [
            0,
            0,
        ]
        self.r.pos = [x, y - self.height]
        self.start_pos = [x, y]

    def on_touch_move(self, touch):
        x, y = self.to_local(*touch.pos)

        self.height = self.start_pos[1] - y
        if self.height < 0:
            self.height = 0
        self.width = x - self.start_pos[0]
        if self.width < 0:
            self.width = 0

        self.r.size = [
            abs(self.width),
            abs(self.height),
        ]
        self.r.pos = [self.start_pos[0], y]


class TestApp(App):
    def build(self):
        base = HighlightCanvas()

        float = FloatLayout()
        float.add_widget(base)

        root = SnapshotImageScreen()
        root.add_widget(float)

        layout = NewDataTabs()

        tab = AddImageTabs()
        tab.add_widget(root)

        layout.add_widget(tab)

        return layout


TestApp().run()
