from kivy.core.window import Window
from kivy.uix.tabbedpanel import TabbedPanel


class Tabs(TabbedPanel):
    def __init__(self, **kwargs):
        super(Tabs, self).__init__(**kwargs)
        self.tab_pos = "bottom_mid"
        self.tab_width = Window.size[0] / 4
        self.do_default_tab = False
        self.background_color = (1, 1, 1, 1)
        self.border = (0, 0, 0, 0)
        # dummy, required but not used:
        self.background_image = "images/bar_path.png"
