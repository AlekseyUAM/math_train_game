from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config
import random


__version__ = '0.0.1'
Config.set('graphics', 'resizable', 1)


class MenuScreen(Screen):
    pass


class GameScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.answers = 0
        self.answer = 0
        self.div_options = [(i * j, i, j) for i in range(1, 11)
                            for j in range(1, 11)]
        self.update_labels()

    def update_labels(self):
        print(self.ids)
        self.ids.answer_label.text = self.get_answers_text()
        self.ids.question_label.text = self.get_question()
        self.ids.entry.text = ''

    def get_question(self):
        action = random.choice(['+', '-', '/', '*'])
        if action == '+':
            number0 = random.randint(0, 99)
            number1 = random.randint(0, 99)
            self.answer = number0 + number1
        elif action == '-':
            number0 = random.randint(0, 99)
            number1 = random.randint(0, number0)
            self.answer = number0 - number1
        elif action == '*':
            number0 = random.randint(0, 10)
            number1 = random.randint(0, 10)
            self.answer = number0 * number1
        elif action == '/':
            choice = random.choice(self.div_options)
            number0 = choice[0]
            number1 = choice[1]
            self.answer = choice[2]
        return f'{number0} {action} {number1} = '

    def get_answers_text(self):
        return 'Ответов: ' + str(self.answers)

    def check_answer(self, answer):
        if answer and int(answer) == self.answer:
            self.answers += 1
            self.update_labels()
            self.ids.entry.background_color = 'white'
        else:
            self.ids.entry.background_color = 'red'


class CalcGridLayout(GridLayout):
    pass


class TrainApp(App):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GameScreen(name='game'))

        return sm


if __name__ == '__main__':
    TrainApp().run()
