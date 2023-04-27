from threading import Thread, Lock

from kivy.lang import Builder
from kivy.app import App
from kivy.network.urlrequest import UrlRequest
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

# Для запросов, сторонний request
import urllib.parse

from requests import Session
from bs4 import BeautifulSoup
import json

# def bug_posted(req, result):
#     print('Our bug is posted!')
#     print(result)

class Container(GridLayout):
    # Создаем сессию
    session_authorization = None
    # Для блокировки потоков
    lock_obj = Lock()

    def set_session(self, login_field, password_field):
        with self.lock_obj:
            print(login_field, password_field)
            # Для каждой авторизации инициализируем новую сессию
            self.session_authorization = Session()

            self.session_authorization.post('https://api.100points.ru/login',
                                       data={'email': login_field,
                                             'password': password_field,
                                             '_xsrf': '_xsrf',
                                             'remember': '1'})
            req = self.session_authorization.get("https://api.100points.ru/student_homework/index")
            if (req.url == "https://api.100points.ru/student_homework/index"):
                self.label_wid.text = "Вход выполнен успешно"
            else:
                self.label_wid.text = "Неверные данные для входа"

    def get_text(self):
        # Поле логина
        login_field = self.get_login_input.text
        # Поле пароля
        password_field = self.get_password_input.text
        # Поле для проверки правильного ввода
        self.label_wid = self.label_widget

        # Создаем поток для авторизации
        thread = Thread(target=self.set_session, args=(login_field, password_field))
        thread.start()


        # header = {"Content-Type: application/x-www-form-urlencoded"}
        # req_t_body = f'{{"email": "{login_field}", "password": "{password_field}", "_xsrf": "_xsrf", "remember": "1"}}'
        # print(req_t_body)
        # request = UrlRequest(
        #     'https://api.100points.ru/login', req_body=req_t_body,
        #     on_success=bug_posted)
        #
        # print(request.url)

#
class MyApp(App):
    def build(self):
        return Container()


MyApp().run()
