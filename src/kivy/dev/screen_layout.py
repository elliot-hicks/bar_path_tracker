import kivy
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen


class WelcomeScreen(Screen):  # Defines WelcomeScreen instance as a screen widget.
    pass


class DateScreen(Screen):  # Defines DateScreen instance as a screen widget.
    pass


class ResultScreen(Screen):  # Defines ResultScreen instance as a screen widget.
    pass


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.root_widget = Builder.load_file("screen_layout.kv")
        Clock.schedule_once(
            self.screen_switch_one, 36
        )  # clock callback for the first screen
        Clock.schedule_once(
            self.screen_switch_two, 4
        )  # clock callback for the second screen
        return self.root_widget

    def screen_switch_one(self, dt):
        self.root_widget.current = "my_welcome_screen"

    def screen_switch_two(self, dt):
        self.root_widget.current = "my_date_screen"

    def on_press(self):
        self.root_widget.current = "my_welcome_screen"


MainApp().run()
