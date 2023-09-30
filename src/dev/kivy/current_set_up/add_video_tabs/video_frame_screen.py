from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen


class VideoFrameScreen(Screen):
    def __init__(self, frame_path, **kwargs):
        super(VideoFrameScreen, self).__init__(**kwargs)
        self.frame_path = frame_path

        print(self.frame_path)
        self.i = Image(
            source=self.frame_path,
            allow_stretch=True,
            # size_hint=(1, 1),
        )

        self.add_widget(self.i)
