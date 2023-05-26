import requests
from bs4 import BeautifulSoup


from kivy.properties import StringProperty
from kivy.uix.scatter import Scatter
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.lang import Builder
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivy.factory import Factory
from kivymd.toast import toast
from kivymd.uix.bottomsheet import MDGridBottomSheet
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.toolbar import MDTopAppBar

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        box_layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        self.username_input = TextInput(hint_text='Username')
        self.password_input = TextInput(hint_text='Password', password=True)
        box_layout.add_widget(self.username_input)
        box_layout.add_widget(self.password_input)
        login_button = Button(text="Login")
        login_button.bind(on_press=self.go_to_next_screen)
        box_layout.add_widget(login_button)
        self.add_widget(box_layout)
        self.dict_task_image = {}
        self.name_student = ''
        self.solition_task = ''


    def go_to_next_screen(self, instance):
        self.autification()
        self.second_screen = self.manager.get_screen('second_screen')
        self.second_screen.name_student_lb = self.name_student
        MDApp.get_running_app().root.current = 'second_screen'

    def get_image_task(self):
        return self.dict_task_image
    def autification(self):
        ses = requests.Session()
        ses.post('https://api.100points.ru/login',
                 data={'email': 'sashalobov3@gmail.com',
                       'password': 'sashalobov3@gmail.com', '_xsrf': '_xsrf',
                       'remember': '1'})

        ses.post("https://api.100points.ru/shift/start", data={"checked_25": "25"})  # запрос начать смену
        student = ses.get("https://api.100points.ru/student_homework/view/3279236?from=from_homework")

        soup_student = BeautifulSoup(student.text, "html.parser")



        self.name_student = soup_student.find(attrs={"readonly": not (None)})
        self.name_student = self.name_student.get("value").strip()
        # ses.post("https://api.100points.ru/exchange/block/" + id_student)  # запрос начать проверку
        # student.response = Error.ckeced_500(student.href.get('href'))
        # soup_student = BeautifulSoup(student.response.text, 'lxml')

        point_name = soup_student.find_all("select",
                                           class_="form-control")
        checked_name = soup_student.find_all(
            class_="custom-control-input")
        comment_name = soup_student.find_all("textarea",
                                             class_="form-control comment-form-children")
        size_c_n = len(checked_name)
        l = 0
        while (l < size_c_n):
            checked_name[l] = checked_name[l].get("name")
            if checked_name[l] == None:
                checked_name.pop(l)
                size_c_n -= 1
                l = l - 1
            l += 1
        for l in range(len(point_name)):
            point_name[l] = point_name[l].get("name")
            comment_name[l] = comment_name[l].get("name")
        blocks = soup_student.find_all(string="Прикрепленный документ")

        checked_files = [0] * len(blocks)
        self.solition_task = [0] * len(blocks)

        solition_task_count = 0

        for l in range(len(blocks)):
            block_files = blocks[
                l].parent.parent.parent.next_sibling.next_sibling
            if (block_files.text.find("Файлы ученика") != -1):
                checked_files[l] = 1
                self.solition_task[solition_task_count] = blocks[
                                                             l].parent.parent.parent  # решение конкретной задачи
                solition_task_count += 1
                self.dict_task_image["task_" + str(l + 1)] = ""
                # os.mkdir("dz/task_" + str(l + 1))
                files = blocks[
                    l].parent.parent.parent.next_sibling.next_sibling.find(
                    "ul", class_="mailbox-attachments")

                if files == None:
                    continue
                files = files.find_all("li")
                mas_image_task = []
                for i in range(len(files)):
                    files[i] = files[i].find("a")["href"]
                    rashirenie = str(files[i]).split('.')
                    rashirenie = rashirenie[-1]
                    mas_image_task.append(files[i])
                    # urllib.request.urlretrieve(files[i],
                    # "dz/task_" + str(
                    #  l + 1) + "/" + str(
                    #  i + 1) + "." + rashirenie)

                self.dict_task_image["task_" + str(l + 1)] = mas_image_task

        count_w = 0
        point = [-1] * len(point_name)
        comment = [""] * len(comment_name)

        while len(point_name) > count_w:
            if checked_files[count_w] == 0:  # нет файла в задании
                point[count_w] = 0
                comment[count_w] = ""

            count_w = count_w + 1

        self.image_dict_for_send = self.dict_task_image

        # solition_task
        # student.set_data(id_student, checked_name, point_name, point,
        # comment_name, comment)
        # self.student = student
        # if not (1 in checked_files):
        #print(self.dict_task_image)

class SecondScreen(Screen):
    name_student_lb = 's'
    def load_image(self,i):

        self.buf_i = self.buf_i + i
        if( self.buf_i  == -1):
            self.buf_i = 0
        elif ( self.buf_i  == len(list(self.image_dict_for_load.keys()))):
            self.buf_i = len(list(self.image_dict_for_load.keys())) - 1
        self.current_key = list(self.image_dict_for_load.keys())[self.buf_i]
        self.image.source  = self.image_dict_for_load[self.current_key ][0]

    def get_name(self):
        print(self.login_screen.name_student)
        return self.login_screen.name_student
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        self.image = AsyncImage(size_hint=(1, 1))
        self.s = ScatterLayout(size_hint=(1, 1))
        self.s.z = -1
        self.s.add_widget(self.image)
        self.box_layout = AnchorLayout(anchor_x='center', anchor_y='bottom', size_hint=(1, 0.8))

        self.box_layout.add_widget(self.s)

        self.current_index = 0

        layout = AnchorLayout(anchor_x='center', anchor_y='top')

        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.8),
                                  spacing=500)
        prev_button = Button(size_hint=(.1, 0.8), background_color=(0, 0, 0, 0))
        prev_button.bind(on_press=self.show_previous_image)
        next_button = Button(size_hint=(.1, 0.8), background_color=(0, 0, 0, 0))
        next_button.bind(on_press=self.show_next_image)

        button_layout.add_widget(prev_button)

        button_layout.add_widget(next_button)


        float_layout = FloatLayout(size_hint=(.5, 0.2),
                                   pos_hint={'x': 0., 'y': 0})
        circular_button = Button(size_hint=(.5, 1),
                                 pos_hint={'center_x': .5, 'y': -4},
                                background_color = (0,0,0,1),on_press=self.open_bottomsheet)
        float_layout.add_widget(circular_button)
        layout.add_widget(float_layout)
        layout.add_widget(self.box_layout)
        layout.add_widget(button_layout)
        self.lable_name = Label(size_hint=(1, 0.1), text=self.name_student_lb, color=(0, 0, 0, 1))
        self.anchor_l = AnchorLayout(anchor_x='center', anchor_y='top')
        self.anchor_l.add_widget(self.lable_name)

        layout.add_widget(self.anchor_l)


        self.add_widget(layout)
    def set_name(self):
        self.lable_name.text = self.name_student_lb
    def on_pre_enter(self, *args):

        print(self.name_student_lb)
        self.set_name()
        self.buf_i = 0
        self.login_screen = self.manager.get_screen('login_screen')
        self.image_dict_for_load = self.login_screen.get_image_task()


        self.load_image(0)


    def open_bottomsheet(self, obj):

        self.obj = MDCustomBottomSheet(screen=Factory.CustomBottomSheet(), animation=True, radius=20)
        g =self.obj.do_layout

        self.obj.open()


    def show_previous_image(self, instance):

        if self.image_dict_for_load[self.current_key]:
            self.current_index -= 1
            if self.current_index < 0:
                self.current_index = len(self.image_dict_for_load[ self.current_key]) - 1

            self.image.source = self.image_dict_for_load[self.current_key][self.current_index]

    def show_next_image(self, instance):
        if self.image_dict_for_load[ self.current_key]:
            self.current_index += 1
            if self.current_index >= len(self.image_dict_for_load[ self.current_key]):
                self.current_index = 0
            self.image.source = self.image_dict_for_load[ self.current_key][self.current_index]



class ThirdScreen(Screen):

    def on_pre_enter(self, *args):
        self.login_screen = self.manager.get_screen('login_screen')
        self.text_task = self.login_screen.solition_task[0].text
        self.add_widget(Label(text=str(self.text_task), color=(0, 0, 0, 1)))









class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)
        self.transition = SlideTransition()

    def on_touch_move(self, touch):
        pass
        # if self.current == 'second_screen':
        #     if touch.dx > 50:
        #         self.transition.direction = 'right'
        #         self.current = self.next()

        # elif self.current == 'other_screen':
        #     if touch.dy > 50:
        #         self.transition.direction = 'down'
        #         self.current = 'second_screen'

        # elif self.current == 'third_screen':
        #     if touch.dx < -50:
        #         self.transition.direction = 'left'
        #         self.current = self.previous()

    def show_grid_bottom_sheet(self):
        pass




class MyApp(MDApp):
    def build(self):
        self.screen_manager = MyScreenManager()
        self.screen_manager.add_widget(LoginScreen(name='login_screen1'))
        self.screen_manager.add_widget(ThirdScreen(name='third_screen1'))
        self.screen_manager.swipe_distance = 50
        return self.screen_manager


if __name__ == '__main__':
    MyApp().run()
