from kivy.core.window import Window

Window.clearcolor = (1, 1, 1, 1)
Window.size = (500, 500)


from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App


from top_tabs.app_tabs import Tabs
from add_video_tabs.select_weight_tab import SelectWeightTab
from top_tabs.home_tab import HomeTab
from top_tabs.settings_tab import SettingsTab
from top_tabs.lift_logs_tab import LiftLogsTab

from add_video_tabs.add_video_tabs import AddVideoTabs


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.name = "main_screen"
        add_video_tabs = Tabs()

        weight_select_tab = SelectWeightTab()

        new_video_tabs = AddVideoTabs()

        weight_select_tab.add_widget(new_video_tabs)

        add_video_tabs.add_widget(HomeTab())
        add_video_tabs.add_widget(weight_select_tab)
        add_video_tabs.add_widget(LiftLogsTab())
        add_video_tabs.add_widget(SettingsTab())

        self.add_widget(add_video_tabs)
