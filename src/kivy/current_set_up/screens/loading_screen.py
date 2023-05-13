from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.app import App


class LoadingScreen(Screen):
    def __init__(self, **kwargs):
        super(LoadingScreen, self).__init__(**kwargs)

        self.name = "loading_screen"

        anchor = AnchorLayout(anchor_x="center", anchor_y="center")
        anchor.add_widget(
            Image(
                source="images/bar_path_black_png.png",
                size_hint=(0.3, 0.3),
                allow_stretch=True,
            )
        )

        self.add_widget(anchor)
