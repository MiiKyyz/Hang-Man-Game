import datetime
import math
import random
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.list import TwoLineIconListItem, IconLeftWidget, ThreeLineIconListItem
from nltk.corpus import words
from PyDictionary import PyDictionary
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
import Database
from kivymd.icon_definitions import md_icons

word_list = words.words()
print(len(word_list))


class NewSnackBar(Snackbar):
    icon = StringProperty(None)


class Panel(MDBoxLayout):
    pass


class MainLayout(Widget):
    letter_object = []


    ImgList = []
    ImgCounter = 0

    x = 500
    y = -1000

    xx = -300
    yy = -1000

    x3 = -400
    y3 = -1000

    x4 = 100
    y4 = -1000

    LayerActivator = False
    ListOdWords = []

    WinnerCounter = 0
    LosingCounter = 0

    setGravity = False

    Icon_List = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)



        Database.MainDataBase().ConectionToDataBase()
        for i in md_icons:
            self.Icon_List.append(i)
        self.ids.guess_letter.icon_right = f'{self.Icon_List[random.randint(0, len(self.Icon_List))]}'
        self.ids.TextWord.icon_right = f'{self.Icon_List[random.randint(0, len(self.Icon_List))]}'
        Database.MainDataBase().ShowData()

        self.dialog = MDDialog(text="Login out",
                               title="Menu Log Out",
                               buttons=[
                                   MDFlatButton(text="Log Out",
                                                theme_text_color="Custom",
                                                text_color=(0 / 255, 0 / 255, 0 / 255, 1),
                                                on_press=self.LogOut),
                                   MDFlatButton(text="Cancel",
                                                theme_text_color="Custom",
                                                text_color=(0 / 255, 0 / 255, 0 / 255, 1),
                                                on_press=self.Cancel)
                               ],
                               radius=[15])

        self.dialogData = MDDialog(text=f"",
                                   title=f"",
                                   type='custom',
                                   content_cls=self.ids.ortiz,
                                   buttons=[
                                       MDFlatButton(text="Close",
                                                    theme_text_color="Custom",
                                                    text_color=(0 / 255, 0 / 255, 0 / 255, 1),
                                                    on_press=self.CloseData),

                                   ],
                                   radius=[15])

        self.data_base_list = []


        for name in Database.MainDataBase().ShowColumnName():
            self.data_base_list.append(name[0])

        self.ImgList = [self.ids.body, self.ids.Head, self.ids.left_arm, self.ids.right_arm
            , self.ids.right_leg, self.ids.left_leg]
        self.ids.winner.pos = (self.x, self.y)
        self.ids.winner_two.pos = (self.xx, self.yy)
        self.ids.winner_three.pos = (self.x3, self.y3)
        self.ids.winner_four.pos = (self.x4, self.y4)

        self.dictionary = PyDictionary()

        self.file = open("words.txt")

        for i in self.file:
            self.ListOdWords.append(i.strip())

        self.file.close()
        Clock.schedule_interval(self.RealTimeApp, 0.000001)
        Clock.schedule_interval(self.Menu, math.cos(2))

        self.TextDisplayed = MDDropdownMenu()

        Clock.schedule_interval(self.Intro, 0.1)

    CloseText = False

    IntroCount = 0

    def Intro(self, ins):
        if self.ids.manager.current_screen == self.ids.manager.get_screen('intro'):
            self.ids.Intro.value_opacity += 0.04
            if self.IntroCount < 40:

                self.IntroCount += 1
            elif self.IntroCount >= 40:
                self.ids.manager.current = 'login'

    def ShowRecord(self):
        if self.ids.manager.current_screen == self.ids.manager.get_screen('record'):
            pass
        else:
            self.ids.manager.current = 'record'
            self.ids.ListOfPlayers.clear_widgets()
            for Player in Database.MainDataBase().ShowData():
                new_players_list = TwoLineIconListItem(text=f'{Player[0]}', secondary_text=f"Created on: {Player[1]}",
                                                       on_press=self.DisplayData,
                                                       text_color=[74 / 255, 36 / 255, 0 / 255, 1],
                                                       theme_text_color="Custom",
                                                       secondary_text_color=[74 / 255, 36 / 255, 0 / 255, 1],
                                                       secondary_theme_text_color='Custom'
                                                       )

                new_players_list.add_widget(
                    IconLeftWidget(icon=f"{self.Icon_List[random.randint(0, len(self.Icon_List))]}",
                                   theme_text_color='Custom', text_color=[74 / 255, 36 / 255, 0 / 255, 1])
                    )

                self.ids.ListOfPlayers.add_widget(new_players_list)

    def DisplayData(self, data):
        DataPlayer = []
        for player in Database.MainDataBase().ShowData():
            if player[0] == data.text:
                DataPlayer = player

        self.dialogData.text = f'Data Of User'
        self.dialogData.title = f'Player: {DataPlayer[0]}'
        self.ids.DATE.text = f"Account Created on: {DataPlayer[1]}"
        self.ids.W.text = f'Wins: {DataPlayer[2]}'
        self.ids.L.text = f'Loses: {DataPlayer[3]}'
        self.dialogData.open()

    def CloseData(self, ins):
        self.dialogData.dismiss()

    def CloseMenu(self, word):

        self.ids.TextSeekWord.text = f'{word}'
        self.TextDisplayed.dismiss()
        self.CloseText = True

    def DisplayWord(self, word):
        menu_item = [{"text": f'{timezone}',
                      "viewclass": "OneLineListItem",
                      "on_release": lambda x=f"{timezone}": self.CloseMenu(x)}
                     for timezone in word]
        self.TextDisplayed.caller = self.ids.TextSeekWord
        self.TextDisplayed.items = menu_item
        self.TextDisplayed.width_mult = 4
        self.TextDisplayed.open()

    OldText = ''

    def Menu(self, ins):
        if self.ids.TextSeekWord.text != self.OldText:
            self.OldText = self.ids.TextSeekWord.text
            self.new_word = []
            self.TextDisplayed.dismiss()
            if self.ids.TextSeekWord.text:
                if self.ids.TextSeekWord.text in self.ListOdWords or self.ids.TextSeekWord.text not in self.ListOdWords:
                    for wd in self.ListOdWords:
                        if self.ids.TextSeekWord.text in wd or self.ids.TextSeekWord.text in wd.lower():
                            self.new_word.append(wd)
                    if self.CloseText is False:
                        self.DisplayWord(self.new_word)
                        self.CloseText = False

    def RealTimeApp(self, ins):

        if self.setGravity is True:
            self.ids.winner.pos = (self.x, self.y)
            self.ids.winner_two.pos = (self.xx, self.yy)
            self.ids.winner_three.pos = (self.x3, self.y3)
            self.ids.winner_four.pos = (self.x4, self.y4)

            self.x4 -= 1
            self.y4 = -((self.x4 ** 2) / 25) + 50

            self.x3 += 1
            self.y3 = -((self.x3 ** 2) / 50) + 200

            self.xx += 1
            self.yy = -((self.xx ** 2) / 100) + 100

            self.x -= 2
            self.y = -((self.x ** 2) / 300) + 150

    def GoBack(self):
        self.ids.manager.current = "dict"
        self.ids.tool.right_action_items = [[""]]
        self.CloseText = False
        self.ids.TextSeekWord.text = ''

    def SeekWord(self):

        if len(self.ids.TextSeekWord.text) == 0:
            NewSnackBar(text="Type a word", snackbar_x='10dp',
                        snackbar_y='10dp',
                        size_hint_x=0.9, bg_color=(255/255,123/255,0/255, 0.5), icon="delete-empty-outline").open()
        else:

            try:
                self.ids.manager.current = 'word'
                self.ids.tool.right_action_items = [["arrow-left", lambda x: self.GoBack()]]
                self.ids.type.text = ''
                self.ids.Defi.text = ''
                word = self.dictionary.meaning(self.ids.TextSeekWord.text)
                self.ids.w.text = f'word: {self.ids.TextSeekWord.text}'

                for type, definition in word.items():
                    self.ids.type.text = f'type: {type}'

                    for difi in definition[0:3]:
                        self.ids.Defi.text += f'{difi}. ' \
                                              f'\n '

            except:
                self.ids.type.text = 'type: None'
                self.ids.Defi.text = 'None Definition'
                self.ids.tool.right_action_items = [["arrow-left", lambda x: self.GoBack()]]

                """for defi in range(len(definition)):

                    self.ids.Defi.text += f' {definition[defi]}, '"""

    def panel(self):

        if self.ids.manager.current_screen == self.ids.manager.get_screen(
                'intro') or self.ids.manager.current_screen == self.ids.manager.get_screen('login'):
            pass
        elif self.ids.manager.current_screen == self.ids.manager.get_screen(
                'menu') or self.ids.manager.current_screen == self.ids.manager.get_screen('dict') \
                or self.ids.manager.current_screen == self.ids.manager.get_screen('record'):
            self.ids.nav_drawer.set_state('open')

    def GuessWord(self):

        R = random.randint(0, 255)
        G = random.randint(0, 255)
        B = random.randint(0, 255)

        self.ids.ButtonWord.icon = f'{self.Icon_List[random.randint(0, len(self.Icon_List))]}'
        self.ids.ButtonWord.icon_color=(R / 255, G / 255, B / 255, 1)

        M = Animation(line_color=(R / 255, G / 255, B / 255, 1), icon_color=(R / 255, G / 255, B / 255, 1),
                      text_color=(R / 255, G / 255, B / 255, 1), duration=0.4)

        M += Animation(line_color=(240 / 255, 112 / 255, 0 / 255, 1), icon_color=(240 / 255, 112 / 255, 0 / 255, 1),
                       text_color=(240 / 255, 112 / 255, 0 / 255, 1), duration=0.4)

        M.start(self.ids.ButtonWord)

        if len(self.ids.TextWord.text) == 0:
            print("Type a word")

            NewSnackBar(text="Type a word", snackbar_x='10dp',
                        snackbar_y='10dp',
                        size_hint_x=0.9, bg_color=(255/255,123/255,0/255, 0.5), icon="delete-empty-outline").open()

        elif self.RandomWord == self.ids.TextWord.text:
            self.ids.TextWord.text = ''
            self.ids.word_container.clear_widgets()
            self.letter_object.clear()
            self.ids.button_letter.disabled = True
            self.ids.ButtonWord.disabled = True

            self.setGravity = True
            anim_winner = Animation(opacity=1, duration=2.5, size_hint=(0.7, 0.7))
            # winning
            anim_winner.start(self.ids.win)
            self.ids.tool.right_action_items = [[""]]
            anim = Animation(opacity=1, duration=1)

            self.ids.TextWord.line_color_normal = (200 / 255, 200 / 255, 200 / 255)
            self.ids.TextWord.text_color = (200 / 255, 200 / 255, 200 / 255)
            self.ids.TextWord.icon_right_color = (200 / 255, 200 / 255, 200 / 255)

            self.ids.guess_letter.line_color_normal = (200 / 255, 200 / 255, 200 / 255)
            self.ids.guess_letter.text_color = (200 / 255, 200 / 255, 200 / 255)
            self.ids.guess_letter.icon_right_color = (200 / 255, 200 / 255, 200 / 255)

            self.ids.guess_letter.disabled = True
            self.ids.TextWord.disabled = True

            for i in range(len(self.RandomWord)):
                self.ids.win.image = f'LogoWinner.png'
                self.winning_label = MDLabel(text=f'[font=STENCIL]{self.RandomWord[i]}[/font]', halign='center',
                                             opacity=0, text_color=(255 / 255, 255 / 255, 255 / 255, 1),
                                             theme_text_color='Custom', markup=True, bold=True, italic=True)
                self.ids.word_container.add_widget(self.winning_label)
                self.letter_object.append(self.winning_label)

            for i in self.letter_object:
                anim.start(i)

            new_record = 0
            record = Database.MainDataBase().ShowData()
            New_List = []
            for r in record:
                if r[0] == self.ids.UserName.text:
                    New_List = r
            new_record = New_List[2]
            new_record += 1
            print("new: ", new_record)

            Database.MainDataBase().UpdateWins(self.ids.UserName.text, new_record)
            print("new record of wins: ", new_record)




        elif self.RandomWord != self.ids.TextWord.text:

            NewSnackBar(text="wrong word", snackbar_x='10dp',
                        snackbar_y='10dp',
                        size_hint_x=0.9, bg_color=(255/255,123/255,0/255, 0.5), icon="police-badge").open()
    approove = []

    NumberLetter = 0
    def GuessLetter(self):

        R = random.randint(0,255)
        G = random.randint(0,255)
        B = random.randint(0,255)

        self.ids.button_letter.icon = f'{self.Icon_List[random.randint(0, len(self.Icon_List))]}'

        M = Animation(line_color= (R/255,G/255,B/255,1), icon_color= (R/255,G/255,B/255,1), text_color= (R/255,G/255,B/255,1),duration=0.4)

        M += Animation(line_color= (240/255,112/255,0/255,1), icon_color= (240/255,112/255,0/255,1), text_color= (240/255,112/255,0/255,1),duration=0.4)

        M.start(self.ids.button_letter)


        if len(self.ids.guess_letter.text) == 0:
            #print("empty box")


            NewSnackBar(text="Type a letter", snackbar_x='10dp',
                        snackbar_y='10dp',
                        size_hint_x=0.9, bg_color=(255/255,123/255,0/255, 0.5), icon="delete-empty-outline").open()


        elif self.ids.guess_letter.text in self.RandomWord:

            # print("founded")

            self.LetterBool = True
            for apro,L,R in zip(self.approove,self.letter_object, self.RandomWord):
                if self.LetterBool is True:
                    if apro is False and self.ids.guess_letter.text == R:
                        self.LetterBool = False
                        self.approove[self.NumberLetter] = True
                        self.WinnerCounter += 1
                        self.letter_object[self.NumberLetter].text = f'[font=STENCIL]{self.ids.guess_letter.text}[/font]'
                        self.letter_object[self.NumberLetter].opacity = 0
                        animBody = Animation(opacity=1, duration=1)

                        animBody.start(self.letter_object[self.NumberLetter])

                self.NumberLetter += 1
                #print(apro,L.text,R)
            self.NumberLetter = 0
            """for apro, L, R in zip(self.approove, self.letter_object, self.RandomWord):
                print(apro, L.text, R)
            print("")"""



            # print(self.WinnerCounter)
            # print("len of words", len(self.RandomWord))

            if self.WinnerCounter == len(self.RandomWord):
                self.ids.tool.right_action_items = [[""]]
                self.setGravity = True
                self.index_two = 0
                self.LocalIndex = 0
                self.index_list = []
                self.ids.win.image = "LogoWinner.png"
                self.ids.button_letter.disabled = True
                self.ids.ButtonWord.disabled = True
                anim_winner = Animation(opacity=1, duration=2.5, size_hint=(0.7, 0.7))

                anim_winner.start(self.ids.win)

                self.ids.TextWord.line_color_normal = (200 / 255, 200 / 255, 200 / 255)
                self.ids.TextWord.text_color = (200 / 255, 200 / 255, 200 / 255)
                self.ids.TextWord.icon_right_color = (200 / 255, 200 / 255, 200 / 255)

                self.ids.guess_letter.line_color_normal = (200 / 255, 200 / 255, 200 / 255)
                self.ids.guess_letter.text_color = (200 / 255, 200 / 255, 200 / 255)
                self.ids.guess_letter.icon_right_color = (200 / 255, 200 / 255, 200 / 255)

                self.ids.guess_letter.disabled = True
                self.ids.TextWord.disabled = True

                new_record = 0
                record = Database.MainDataBase().ShowData()
                New_List = []
                for r in record:
                    if r[0] == self.ids.UserName.text:
                        New_List = r
                new_record = New_List[2]
                new_record += 1
                #print("new: ", new_record)

                Database.MainDataBase().UpdateWins(self.ids.UserName.text, new_record)
                #print("new record of wins: ", new_record)

        if len(self.ids.guess_letter.text) > 1:

            NewSnackBar(text="type just one letter", snackbar_x='10dp',
                        snackbar_y='10dp',
                        size_hint_x=0.9, bg_color=(255/255,123/255,0/255, 0.5), icon="alert").open()

        elif self.ids.guess_letter.text not in self.RandomWord:

            NewSnackBar(text="Wrong letter", snackbar_x='10dp',
                        snackbar_y='10dp',
                        size_hint_x=0.9, bg_color=(255/255,123/255,0/255, 0.5), icon="police-badge").open()

            animBody = Animation(opacity=1, duration=1)

            animBody.start(self.ImgList[self.ImgCounter])

            self.ImgCounter += 1

            self.LosingCounter += 1

            if len(self.ImgList) == self.LosingCounter:
                # lost
                self.ids.button_letter.disabled = True
                self.ids.ButtonWord.disabled = True

                self.ids.guess_letter.disabled = True
                self.ids.TextWord.disabled = True

                self.ids.TextWord.line_color_normal = (200 / 255, 200 / 255, 200 / 255)
                self.ids.TextWord.text_color = (200 / 255, 200 / 255, 200 / 255)
                self.ids.TextWord.icon_right_color = (200 / 255, 200 / 255, 200 / 255)

                self.ids.guess_letter.line_color_normal = (200 / 255, 200 / 255, 200 / 255)
                self.ids.guess_letter.text_color = (200 / 255, 200 / 255, 200 / 255)
                self.ids.guess_letter.icon_right_color = (200 / 255, 200 / 255, 200 / 255)

                self.ids.win.image = "lost.png"

                anim_lost = Animation(opacity=1, duration=2.5, size_hint=(0.7, 0.7))

                anim_lost.start(self.ids.win)

                new_record = 0
                record = Database.MainDataBase().ShowData()
                New_List = []
                for r in record:
                    if r[0] == self.ids.UserName.text:
                        New_List = r
                new_record = New_List[3]
                new_record += 1
                # print("new: ", new_record)

                Database.MainDataBase().UpdateLoses(self.ids.UserName.text, new_record)
                # print("new record of wins: ", new_record)

        self.ids.guess_letter.text = ''

    def LogOut(self, ins):
        self.ids.manager.current = 'menu'
        self.ids.tool.right_action_items = [[""]]
        self.dialog.dismiss()
        self.ids.word_container.clear_widgets()

    def Dialog(self):
        self.dialog.open()

    def Cancel(self, ins):
        self.dialog.dismiss()

    def StartGame(self, ins):
        self.ids.word_container.clear_widgets()
        self.ids.TextWord.line_color_normal = (255 / 255, 191 / 255, 0 / 255)
        self.ids.TextWord.text_color = (255 / 255, 191 / 255, 0 / 255)
        self.ids.TextWord.icon_right_color = (255 / 255, 191 / 255, 0 / 255)

        self.ids.guess_letter.line_color_normal = (255 / 255, 191 / 255, 0 / 255)
        self.ids.guess_letter.text_color = (255 / 255, 191 / 255, 0 / 255)
        self.ids.guess_letter.icon_right_color = (255 / 255, 191 / 255, 0 / 255)

        self.ids.guess_letter.disabled = False
        self.ids.TextWord.disabled = False

        self.ids.button_letter.disabled = False
        self.ids.ButtonWord.disabled = False
        self.setGravity = False
        self.x = 500
        self.y = -1000

        self.xx = -300
        self.yy = -1000

        self.x3 = -400
        self.y3 = -1000

        self.x4 = 100
        self.y4 = -1000

        self.ids.winner.pos = (self.x, self.y)
        self.ids.winner_two.pos = (self.xx, self.yy)
        self.ids.winner_three.pos = (self.x3, self.y3)
        self.ids.winner_four.pos = (self.x4, self.y4)

        self.WinnerCounter = 0
        self.ids.win.opacity = 0
        self.ids.win.size_hint = (0, 0)
        self.ImgCounter = 0
        self.LosingCounter = 0
        self.label_container = []
        self.letter_container = []
        self.letter_object = []
        self.ids.tool.right_action_items = [["logout", lambda x: self.Dialog()]]
        self.approove = []

        for img in self.ImgList:
            img.opacity = 0
        number = random.randint(0, len(self.ListOdWords))
        self.RandomWord = self.ListOdWords[number]
        print(self.RandomWord)
        for i in range(len(self.RandomWord)):
            self.Label = MDLabel(text=f'[font=STENCIL]__[/font]', halign='center', text_color=(255 / 255, 255 / 255, 255 / 255, 1),
                                 theme_text_color='Custom', markup=True)
            self.letter_object.append(self.Label)
            self.ids.word_container.add_widget(self.Label)
            self.approove.append(False)


    def Start_Game(self):
        self.StartGame(None)

        self.index_list = []
        self.list_letter_non_repeated = []

    def LogIn(self):

        if len(self.ids.LoginName.text) == 0:
            NewSnackBar(text="Missing a name", snackbar_x='10dp',
                        snackbar_y='10dp',
                        size_hint_x=0.9, bg_color=(255/255,123/255,0/255, 0.5), icon="car-shift-pattern").open()
        elif self.ids.LoginName.text in self.data_base_list:
            NewSnackBar(text=f"Welcome Back, {self.ids.LoginName.text}!", snackbar_x='10dp',
                        snackbar_y='10dp',
                        size_hint_x=0.9, bg_color=(255/255,123/255,0/255, 0.5), icon="eiffel-tower").open()

            self.ids.manager.current = 'menu'

            self.ids.UserName.text = f'{self.ids.LoginName.text}'

        elif self.ids.LoginName.text not in self.data_base_list:
            NewSnackBar(text=f"Account Created, Welcome! {self.ids.LoginName.text}", snackbar_x='10dp',
                        snackbar_y='10dp',
                        size_hint_x=0.9, bg_color=(255/255,123/255,0/255, 0.5), icon="human-greeting").open()
            date = "{:%A, %B %d, %Y}.".format(datetime.datetime.today())
            dt_today = datetime.datetime.today()
            Database.MainDataBase().CreateAccount(self.ids.LoginName.text,date + f" at {dt_today.hour}:{dt_today.minute}:{dt_today.second}")

            self.ids.UserName.text = f'{self.ids.LoginName.text}'

            self.ids.manager.current = 'menu'
        self.ids.LoginName.text = ''


class HangMan(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Orange"
        return MainLayout()


HangMan().run()
