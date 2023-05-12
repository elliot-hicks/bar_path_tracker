from kivy.uix.tabbedpanel import TabbedPanelItem


class SettingsTab(TabbedPanelItem):
    def __init__(self, **kwargs):
        super(SettingsTab, self).__init__(**kwargs)
        self.text = "Settings"
