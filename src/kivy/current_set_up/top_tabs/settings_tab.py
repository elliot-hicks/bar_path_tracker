from kivy.uix.tabbedpanel import TabbedPanelItem


class SettingsTab(TabbedPanelItem):
    def __init__(self, **kwargs):
        super(SettingsTab, self).__init__(**kwargs)
        self.text = "Settings"
        self.background_normal = ""
        self.background_color = (0, 0, 0, 1)
        self.border = (0, 0, 0, 0)
