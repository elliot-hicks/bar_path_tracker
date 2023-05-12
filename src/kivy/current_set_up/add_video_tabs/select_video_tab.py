from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.filechooser import FileChooserIconView


class SelectVideoTab(TabbedPanelItem):
    def __init__(self, **kwargs):
        super(SelectVideoTab, self).__init__(**kwargs)
        self.text = "Select Video"

        file_chooser = FileChooserIconView()
        self.add_widget(file_chooser)
