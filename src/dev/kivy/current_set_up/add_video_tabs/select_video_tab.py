from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.filechooser import FileChooserIconView, FileChooserListView
import os
from kivy.uix.gridlayout import GridLayout
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.image import Image


class SelectVideoTab(TabbedPanelItem):
    def __init__(self, **kwargs):
        super(SelectVideoTab, self).__init__(**kwargs)
        self.text = "Select Video"
        self.video_selected = False

        self.layout = GridLayout(rows=2)

        file_chooser = FileChooserListView(
            path=os.getcwd(), on_submit=self.show_selection
        )

        self.layout.add_widget(file_chooser)
        self.video = VideoPlayer()
        self.layout.add_widget(self.video)
        self.add_widget(self.layout)

    def show_selection(self, chooser, selection, *args):
        self.selection = selection[0]
        print(self.selection)

        self.video.state = "stop"
        self.video.source = self.selection
        self.video.state = "play"
