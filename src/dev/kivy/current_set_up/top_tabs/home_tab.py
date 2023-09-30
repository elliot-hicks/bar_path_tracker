from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout


class HomeTab(TabbedPanelItem):
    def __init__(self, **kwargs):
        super(HomeTab, self).__init__(**kwargs)
        self.text = "Home"
        self.background_normal = ""
        self.background_color = (0, 0, 0, 1)
        self.border = (0, 0, 0, 0)

        anchor = AnchorLayout(anchor_x="center", anchor_y="center")
        anchor.add_widget(
            Image(
                source="images/bar_path_black_png.png",
                size_hint=(0.3, 0.3),
                allow_stretch=True,
            )
        )

        self.add_widget(anchor)
