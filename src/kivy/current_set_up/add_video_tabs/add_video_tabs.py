from kivy.uix.tabbedpanel import TabbedPanel

from .select_weight_tab import SelectWeightTab
from .select_video_tab import SelectVideoTab


class AddVideoTabs(TabbedPanel):
    def __init__(self, **kwargs):
        super(AddVideoTabs, self).__init__(**kwargs)
        self.size_hint = (1, 1)
        self.tab_pos = "left_mid"
        self.tab_width = self.size[0]
        self.do_default_tab = False
        self.add_widget(SelectWeightTab())
        self.add_widget(SelectVideoTab())
