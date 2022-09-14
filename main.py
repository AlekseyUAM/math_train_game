from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.switch import Switch
#from kivy.config import Config
from kivy.properties import ObjectProperty
from random import choice, randint

__version__ = '0.0.4'
#Config.set('graphics', 'resizable', 1)
BACKG_COLOR = (0.894, 0.976, 0.961, 1)
TEXT_COLOR = (0.067, 0.6, 0.62, 1)
BUTTON_COLOR = (0.696, 0.945, 0.961, 1)


def get_button(text):
    return Button(text=text,
                  font_size='64',
                  background_color=BACKG_COLOR,
                  #background_normal='',
                  border=(30, 30, 30, 30),
                  #size=(200, 200),
                  #size_hint=(1, None),
                  color=TEXT_COLOR)


class Game:
    div_options = [(i * j, i, j) for i in range(1, 11) for j in range(1, 11)]

    def __init__(self):
        self.settings = self.get_settings()
        self.score = 0
        self.mark = 0
        self.answer = 0
        self.question = ''

    @staticmethod
    def get_settings():
        return {'plus': True,
                'minus': True,
                'div': True,
                'mult': True,
                'degree': True,
                'sqrt': True,
                'brackets': True,
                'eq_plus': True,
                'eq_minus': True,
                'eq_div': True,
                'eq_mult': True}

    def check_answer(self, answer):
        return answer and answer.replace('-', '').isdigit() and int(answer) == self.answer

    def get_question(self):
        """
        TODO:
        добавить проверку на отсутствие допустимых действий
        """
        action = choice([k for k, v in self.settings.items() if v])
        self.question, self.answer, self.mark = self.__getattribute__('get_' + action + '_question')()

    @staticmethod
    def get_plus_question():
        number0 = randint(-99, 99)
        number1 = randint(0, 99)
        answer = number0 + number1
        mark = 5
        return f'{number0} + {number1} = x', answer, mark

    @staticmethod
    def get_minus_question():
        number0 = randint(-99, 99)
        number1 = randint(0, 99)
        answer = number0 - number1
        mark = 5
        return f'{number0} - {number1} = x', answer, mark

    def get_div_question(self):
        number0, number1, answer = choice(self.div_options)
        mark = 3
        return f'{number0} / {number1} = x', answer, mark

    @staticmethod
    def get_mult_question():
        number0 = randint(0, 99)
        number1 = randint(0, 99 if number0 <= 10 else 10)
        answer = number0 * number1
        if number0 <= 10 and number1 <= 10:
            mark = 2
        elif answer < 100:
            mark = 5
        else:
            mark = 10
        return f'{number0} * {number1} = x', answer, mark

    @staticmethod
    def get_degree_question():
        number0 = randint(0, 10)
        answer = number0**2
        mark = 5
        return f'{number0}\u00B2 = x', answer, mark

    @staticmethod
    def get_sqrt_question():
        answer = randint(0, 10)
        mark = 5
        return f'\u221a{answer**2} = x', answer, mark

    @staticmethod
    def get_brackets_question():
        number0 = randint(0, 9)
        number1 = randint(0, 9)
        number2 = randint(0, 9)
        variant = choice([*range(6)])
        if variant == 0:
            question = f'({number0} + {number1}) * {number2} = x'
            answer = (number0 + number1) * number2
        elif variant == 1:
            question = f'({number0} - {number1}) * {number2} = x'
            answer = (number0 - number1) * number2
        elif variant == 2:
            question = f'{number2} * ({number0} + {number1}) = x'
            answer = number2 * (number0 + number1)
        elif variant == 3:
            question = f'{number2} * ({number0} - {number1}) = x'
            answer = number2 * (number0 - number1)
        elif variant == 4:
            question = f'{number2} + ({number0} * {number1}) = x'
            answer = number2 + (number0 * number1)
        elif variant == 5:
            question = f'{number2} - ({number0} * {number1}) = x'
            answer = number2 - (number0 * number1)
        mark = 10
        return question, answer, mark

    @staticmethod
    def get_eq_plus_question():
        number0 = choice([randint(0, 99), 'x'])
        if number0 == 'x':
            number1 = randint(0, 99)
            answer = randint(0, 99)
            number2 = answer + number1
        else:
            number1 = 'x'
            answer = randint(0, 99)
            number2 = answer + number0
        mark = 6 if number2 < 100 else 10
        return f'{number0} + {number1} = {number2}', answer, mark

    @staticmethod
    def get_eq_minus_question():
        number0 = choice([randint(0, 99), 'x'])
        if number0 == 'x':
            number1 = randint(0, 99)
            answer = randint(number1, 99)
            number2 = answer - number1
        else:
            number1 = 'x'
            answer = randint(0, number0)
            number2 = number0 - answer
        mark = 6 if number2 < 100 else 10
        return f'{number0} - {number1} = {number2}', answer, mark

    @staticmethod
    def get_eq_mult_question():
        number0 = choice([randint(1, 10), 'x'])
        if number0 == 'x':
            number1 = randint(1, 10)
            answer = randint(1, 10)
            number2 = answer * number1
        else:
            number1 = 'x'
            answer = randint(1, 10)
            number2 = answer * number0
        mark = 6
        return f'{number0} * {number1} = {number2}', answer, mark

    def get_eq_div_question(self):
        ch = choice(self.div_options)
        number0 = choice([ch[0], 'x'])
        if number0 == 'x':
            answer, number1, number2 = ch
        else:
            number1 = 'x'
            number2 = ch[2]
            answer = ch[1]
        mark = 10
        return f'{number0} / {number1} = {number2}', answer, mark


class MenuScreen(Screen):
    container = ObjectProperty(None)

    def __init__(self, game, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.game = game
        layout = BoxLayout(orientation='vertical')
        btn_begin = get_button('Начать')
        btn_begin.bind(on_press=self.btn_begin_press)
        layout.add_widget(btn_begin)
        btn_settings = get_button('Настройки')
        btn_settings.bind(on_press=self.btn_settings_press)
        layout.add_widget(btn_settings)
        btn_exit = get_button('Выход')
        btn_exit.bind(on_press=self.btn_exit_press)
        layout.add_widget(btn_exit)
        self.add_widget(layout)

    def btn_begin_press(self, event):
        self.manager.current = 'game'

    def btn_settings_press(self, event):
        self.manager.current = 'settings'

    def btn_exit_press(self, event):
        quit()


class SettingsScreen(Screen):
    def __init__(self, game, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.game = game
        self.layout = GridLayout(cols=2)
        self.add_switch('Сложение', 'plus')
        self.add_switch('Вычитание', 'minus')
        self.add_switch('Деление', 'div')
        self.add_switch('Умножение', 'mult')
        self.add_switch('Степень', 'degree')
        self.add_switch('Корень', 'sqrt')
        self.add_switch('Скобки', 'brackets')
        self.add_switch('Уравнение сложение', 'eq_plus')
        self.add_switch('Уравнение вычитание', 'eq_minus')
        self.add_switch('Уравнение деление', 'eq_div')
        self.add_switch('Уравнение вычитание', 'eq_mult')

        btn_back = get_button('Назад')
        btn_back.bind(on_press=self.btn_back_press)
        self.layout.add_widget(btn_back)
        self.add_widget(self.layout)

    def btn_back_press(self, event):
        self.manager.current = 'menu'

    def add_switch(self, label_name, setting_name):
        self.layout.add_widget(Label(text=label_name, font_size=44))
        s = Switch(active=True, ids={'setting': setting_name})
        s.bind(active=self.switch_callback)
        self.layout.add_widget(s)

    def switch_callback(self, switch_object, switch_value):
        self.game.settings[switch_object.ids.setting] = switch_value


class ImageTrueScreen(Screen):
    pass


class ImageFalseScreen(Screen):
    pass


class CalcGridLayout(GridLayout):
    pass


class SetGridLayout(GridLayout):
    pass


class GameScreen(Screen):
    def __init__(self, game, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.game = game
        self.update_labels()

    def update_labels(self):
        self.game.get_question()
        self.ids.answer_label.text = self.get_score_text()
        self.ids.question_label.text = self.game.question
        self.ids.entry.text = ''

    def get_score_text(self):
        return 'Баллов: ' + str(self.game.score)

    def check_answer(self, answer):
        if self.game.check_answer(answer):
            self.game.score += self.game.mark
            self.update_labels()
            self.manager.current = 'image_true'
        else:
            self.manager.current = 'image_false'


class TrainApp(App):

    def build(self):
        game = Game()
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu', game=game))
        sm.add_widget(GameScreen(name='game', game=game))
        sm.add_widget(ImageTrueScreen(name='image_true'))
        sm.add_widget(ImageFalseScreen(name='image_false'))
        sm.add_widget(SettingsScreen(name='settings', game=game))

        return sm


if __name__ == '__main__':
    TrainApp().run()
