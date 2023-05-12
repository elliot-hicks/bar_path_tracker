from kivy.uix.tabbedpanel import TabbedPanelItem


class HomeTab(TabbedPanelItem):
    def __init__(self, **kwargs):
        super(HomeTab, self).__init__(**kwargs)
        self.text = "Home"
