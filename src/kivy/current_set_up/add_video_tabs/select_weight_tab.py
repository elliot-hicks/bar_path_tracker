from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.floatlayout import FloatLayout


from .highlight_weight import HighlightWeight
from .video_frame_screen import VideoFrameScreen


class SelectWeightTab(TabbedPanelItem):
    def __init__(self, **kwargs):
        super(SelectWeightTab, self).__init__(**kwargs)
        self.text = "Add Video"

        weight_highlighter = HighlightWeight()

        weight_selector_canvas = FloatLayout()
        weight_selector_canvas.add_widget(weight_highlighter)

        starting_frame = VideoFrameScreen("images/bar_path_black_png.png")
        starting_frame.add_widget(weight_selector_canvas)

        self.add_widget(starting_frame)
