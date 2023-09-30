from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App


from screens.main_screen import MainScreen
from screens.loading_screen import LoadingScreen
from kivy.uix.screenmanager import ScreenManager
from kivy.clock import Clock


class TestApp(App):
    def build(self):
        Window.clearcolor = (0, 0, 0, 1)

        self.manager = ScreenManager()

        loading_screen = LoadingScreen()
        main_screen = MainScreen()

        self.manager.add_widget(loading_screen)
        self.manager.add_widget(main_screen)

        Clock.schedule_once(self.loading_screen_callback, 3)

        return self.manager

    def loading_screen_callback(self, dt):
        self.manager.current = "main_screen"


TestApp().run()
