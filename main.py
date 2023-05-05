import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
import os


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        box_layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        self.username_input = TextInput(hint_text='Username')
        self.password_input = TextInput(hint_text='Password', password=True)
        box_layout.add_widget(self.username_input)
        box_layout.add_widget(self.password_input)
        login_button = Button(text='Login')
        login_button.bind(on_press=self.go_to_next_screen)
        box_layout.add_widget(login_button)
        self.add_widget(box_layout)

    def go_to_next_screen(self, instance):
        App.get_running_app().root.current = 'second_screen'


class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        pic_path = os.path.join(os.path.dirname(__file__), 'pic')
        file_list = os.listdir(pic_path)

        box_layout = BoxLayout(orientation='horizontal', padding=50, spacing=15,size_hint=(1, 1.4))

        for filename in file_list:
            filepath = os.path.join(pic_path, filename)
            box_layout.add_widget(Image(source=filepath))
        self.add_widget(box_layout)

    def on_swipe_left(self):
        App.get_running_app().root.current = 'third_screen'

    def go_back(self, instance):
        App.get_running_app().root.current = 'login_screen'



class ThirdScreen(Screen):
    def __init__(self, **kwargs):
        super(ThirdScreen, self).__init__(**kwargs)
        self.add_widget(Label(text='Это второй экран'))

class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)
        self.transition = SlideTransition()

    def on_touch_move(self, touch):
        if self.current == 'second_screen':
            if touch.dx > 50:
                self.transition.direction = 'right'
                self.current = self.next()
        elif self.current == 'third_screen':
            if touch.dx < -50:
                self.transition.direction = 'left'
                self.current = self.previous()


class MyApp(App):
    def build(self):
        screen_manager = MyScreenManager()
        screen_manager.add_widget(LoginScreen(name='login_screen1'))
        screen_manager.add_widget(SecondScreen(name='second_screen1'))
        screen_manager.add_widget(ThirdScreen(name='third_screen1'))
        screen_manager.swipe_distance = 50
        return screen_manager


if __name__ == '__main__':
    MyApp().run()

"test"