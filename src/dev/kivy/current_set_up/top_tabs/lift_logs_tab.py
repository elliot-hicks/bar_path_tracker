from kivy.uix.tabbedpanel import TabbedPanelItem


class LiftLogsTab(TabbedPanelItem):
    def __init__(self, **kwargs):
        super(LiftLogsTab, self).__init__(**kwargs)
        self.text = "Log"
        self.background_normal = ""
        self.background_color = (0, 0, 0, 1)
        self.border = (0, 0, 0, 0)
