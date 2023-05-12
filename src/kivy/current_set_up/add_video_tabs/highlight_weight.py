from kivy.core.window import Window
from kivy.uix.scatterlayout import ScatterLayout
from kivy.graphics import Color, Rectangle


class HighlightWeight(ScatterLayout):
    def __init__(self, **kwargs):
        super(HighlightWeight, self).__init__(**kwargs)
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
