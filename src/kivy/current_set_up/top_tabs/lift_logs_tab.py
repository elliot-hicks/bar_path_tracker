from kivy.uix.tabbedpanel import TabbedPanelItem


class LiftLogsTab(TabbedPanelItem):
    def __init__(self, **kwargs):
        super(LiftLogsTab, self).__init__(**kwargs)
        self.text = "Log"
