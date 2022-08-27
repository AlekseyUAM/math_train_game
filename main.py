from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config
from random import choice, randint


__version__ = '0.0.3'
Config.set('graphics', 'resizable', 1)


class MenuScreen(Screen):
    pass


class ImageTrueScreen(Screen):
    pass


class ImageFalseScreen(Screen):
    pass


class GameScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.score = 0
        self.mark = 0
        self.answer = 0
        self.div_options = [(i * j, i, j) for i in range(1, 11) for j in range(1, 11)]
        self.update_labels()

    def update_labels(self):
        print(self.ids)
        self.ids.answer_label.text = self.get_score_text()
        self.ids.question_label.text = self.get_question()
        self.ids.entry.text = ''

    def get_question(self):
        action = choice(['+', '-', '/', '*'])
        is_eq = choice([True, False])
        if is_eq:
            if action == '+':
                number0 = choice([randint(0, 99), 'x'])
                if number0 == 'x':
                    number1 = randint(0, 99)
                    self.answer = randint(0, 99)
                    number2 = self.answer + number1
                else:
                    number1 = 'x'
                    self.answer = randint(0, 99)
                    number2 = self.answer + number0
                self.mark = 6 if number2 < 100 else 12
            elif action == '-':
                number0 = choice([randint(0, 99), 'x'])
                number0 = 'x'
                if number0 == 'x':
                    number1 = randint(0, 99)
                    self.answer = randint(number1, 99)
                    number2 = self.answer - number1
                else:
                    number1 = 'x'
                    self.answer = randint(0, number0)
                    number2 = number0 - self.answer
                self.mark = 6 if number2 < 100 else 12
            elif action == '*':
                number0 = choice([randint(1, 10), 'x'])
                if number0 == 'x':
                    number1 = randint(1, 10)
                    self.answer = randint(1, 10)
                    number2 = self.answer * number1
                else:
                    number1 = 'x'
                    self.answer = randint(1, 10)
                    number2 = self.answer * number0
                self.mark = 10
            elif action == '/':
                ch = choice(self.div_options)
                number0 = choice([ch[0], 'x'])
                if number0 == 'x':
                    number1 = ch[1]
                    number2 = ch[2]
                    self.answer = ch[0]
                else:
                    number1 = 'x'
                    number2 = ch[2]
                    self.answer = ch[1]
                self.mark = 10
            return f'{number0} {action} {number1} = {number2}'
        else:
            if action == '+':
                number0 = randint(0, 99)
                number1 = randint(0, 99)
                self.answer = number0 + number1
                self.mark = 1 if number0 < 10 else 2 + 1 if number1 < 10 else 2
            elif action == '-':
                number0 = randint(0, 99)
                number1 = randint(0, number0)
                self.answer = number0 - number1
                self.mark = 1 if number0 < 10 else 2 + 1 if number1 < 10 else 2
            elif action == '*':
                number0 = randint(0, 99)
                number1 = randint(0, 99 if number0 <= 10 else 10)
                self.answer = number0 * number1
                if number0 <= 10 and number1 <= 10:
                    self.mark = 2
                elif self.answer < 100:
                    self.mark = 5
                else:
                    self.mark = 10
            elif action == '/':
                ch = choice(self.div_options)
                number0 = ch[0]
                number1 = ch[1]
                self.answer = ch[2]
                self.mark = 3
            return f'{number0} {action} {number1} = x'

    def get_score_text(self):
        return 'Баллов: ' + str(self.score)

    def check_answer(self, answer):
        if answer and answer.isdigit() and int(answer) == self.answer:
            self.score += self.mark
            self.update_labels()
            self.manager.current = 'image_true'
        else:
            self.manager.current = 'image_false'


class CalcGridLayout(GridLayout):
    pass


class TrainApp(App):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(ImageTrueScreen(name='image_true'))
        sm.add_widget(ImageFalseScreen(name='image_false'))

        return sm


if __name__ == '__main__':
    TrainApp().run()
