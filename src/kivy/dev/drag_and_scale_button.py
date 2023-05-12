from kivy.core.window import Window

Window.clearcolor = (1, 1, 1, 1)
Window.size = (500, 500)

from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.uix.scatterlayout import ScatterLayout
from kivy.graphics.transformation import Matrix
from kivy.graphics import Color, Line, Rectangle, Ellipse


class BaseScatter(ScatterLayout):
    def __init__(self, **kwargs):
        super(BaseScatter, self).__init__(**kwargs)
        self.corner = None
        self.start_pos = [0, 0]

    def on_kv_post(self, base_widget):
        # makes rect visible
        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.radius = self.width / 15
            self.c1 = Ellipse(
                pos=(1 - self.radius, self.height - self.radius),
                size=(self.radius * 2, self.radius * 2),
            )
            self.c2 = Ellipse(
                pos=(self.width - self.radius, 1 - self.radius),
                size=(self.radius * 2, self.radius * 2),
            )
            Color(0, 1, 0, 0.2)
            self.r = Rectangle(pos=(0, 0), size=(self.width, self.height))

            Color(0, 1, 0, 0.7)
            self.l = Line(rectangle=(0, 0, self.width, self.height))

    def on_touch_down(self, touch):
        x, y = self.to_local(*touch.pos)
        self.start_pos = x, y

        # check which corner is dragged
        # 20 is basically the width/height if the draggable area
        if 0 <= x <= 20 and 0 <= y <= 20:
            self.corner = "bottomleft"

        elif 0 <= x <= 20 and self.height - 20 <= y <= self.height:
            self.corner = "topleft"

        elif (
            self.width - 20 <= x <= self.width and self.height - 20 <= y <= self.height
        ):
            self.corner = "topright"

        elif self.width - 20 <= x <= self.width and 0 <= y <= 20:
            self.corner = "bottomright"

        else:
            self.corner = "drag"

    def get_corner(self, x, y):
        if 0 <= x <= 20 and 0 <= y <= 20:
            self.corner = "bottomleft"

        elif 0 <= x <= 20 and self.height - 20 <= y <= self.height:
            self.corner = "topleft"

        elif (
            self.width - 20 <= x <= self.width and self.height - 20 <= y <= self.height
        ):
            self.corner = "topright"

        elif self.width - 20 <= x <= self.width and 0 <= y <= 20:
            self.corner = "bottomright"

        else:
            self.corner = "drag"

    def on_touch_up(self, touch):
        # transform touch to local space
        x, y = self.to_local(*touch.pos)

        self.get_corner(x, y)

        # calc mouse rel
        relx = self.start_pos[0] - x
        rely = self.start_pos[1] - y

        # resize depending on the corner pressed
        # this does not work with rotation yet since the rel value does not take that into account
        # ill update that maybe soon
        if self.corner == "bottomleft":
            # apply size changes
            self.size[0] += relx
            self.size[1] += rely

            # repos widget (since size changes increase in x and y direction)
            self.x -= relx
            self.y -= rely

        elif self.corner == "topleft":
            # apply size changes
            self.size[0] += relx
            self.size[1] -= rely  # reverse y value

            # repos widget (since size changes increase in x and y direction)
            self.x -= relx
            # y is not needed since we're not moving downwards

        elif self.corner == "topright":
            # apply size changes
            # we need to reverse both
            self.size[0] -= relx
            self.size[1] -= rely

            # repos widget (since size changes increase in x and y direction)
            # we don't need that since we expand our rect in the xy direction

        elif self.corner == "bottomright":
            # apply size changes
            self.size[0] -= relx  # reverse x
            self.size[1] += rely

            # repos widget (since size changes increase in x and y direction)
            # we don't need x
            self.y -= rely

        # else:
        # here goes the drag and drop
        # self.x -= relx
        # self.y -= rely

        # update rectangle
        self.l.rectangle = (0, 0, self.width, self.height)
        self.r.size = [self.width, self.height]
        self.radius = self.width / 15
        self.c1.pos = (1 - self.radius, self.height - self.radius)
        self.c1.size = (self.radius * 2, self.radius * 2)
        self.c2.pos = (self.width - self.radius, 1 - self.radius)
        self.c2.size = (self.radius * 2, self.radius * 2)

        # reset self.corner
        self.corner = None

    def on_touch_move(self, touch):
        # transform touch to local space
        x, y = self.to_local(*touch.pos)

        self.get_corner(x, y)
        # calc mouse rel
        relx = self.start_pos[0] - x
        rely = self.start_pos[1] - y

        if self.corner == "drag":
            # here goes the drag and drop
            self.x -= relx
            self.y -= rely

        # update rectangle
        self.l.rectangle = (0, 0, self.width, self.height)
        self.r.size = [self.width, self.height]
        self.radius = self.width / 15
        self.c1.pos = (1 - self.radius, self.height - self.radius)
        self.c1.size = (self.radius * 2, self.radius * 2)
        self.c2.pos = (self.width - self.radius, 1 - self.radius)
        self.c2.size = (self.radius * 2, self.radius * 2)

        # reset self.corner
        self.corner = None


class TestApp(App):
    def build(self):
        root = FloatLayout()

        # i suppose this should be done separately
        base = BaseScatter(size=(200, 200), size_hint=(None, None), pos=(50, 50))
        lbl = Label(text="Drag to cover weights", color=(0, 0, 0, 1))

        # base.add_widget(lbl)

        root.add_widget(base)

        return root


TestApp().run()
