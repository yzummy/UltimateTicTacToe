#!/usr/bin/env python3
'''
CS3100 Software Engineering
Fall 2018
Group 11: Paige Huffman, Luke Malloy, Yunchao Zhang,
		  Benjamin Krueger, and Drake Rastorfer

Ultimate Tic Tac Toe

'''
from kivy.config import Config
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'top', '0')
Config.set('graphics', 'left', '0')

from kivy.app import App

from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import *
from kivy.uix.boxlayout import *
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.popup import *

from kivy.properties import ListProperty, NumericProperty, StringProperty

from kivy.core.window import Window

from kivy.clock import *

import random
import numpy as np


# change to desired resolution
# ESC key to exit game
Window.size = (1920, 1080)
Window.fullscreen= True

class GridEntry(Button):
    coords = ListProperty([0, 0])


# class for the 3x3 subgrids
class TicTacToeGrid(GridLayout):
    status = ListProperty([0, 0, 0, 0, 0, 0, 0, 0, 0])
    current_player = NumericProperty(1)
    position_in_board = -1

    def __init__(self, *args, **kwargs):
        super(TicTacToeGrid, self).__init__(*args, **kwargs)

        # populate grid with button widgets
        for row in range(3):
            for column in range(3):
                grid_entry = GridEntry(coords=(row, column))
                grid_entry.bind(on_release=self.button_pressed)
                TicTacToeApp.button_ids.append(grid_entry)
                # print(grid_entry.coords, grid_entry)
                self.add_widget(grid_entry)


    # Print output
    #print('{} button clicked'.format(button.coords))

    # Function for each button press
    def button_pressed(self, button):
        # print(button)
        if TicTacToeApp.game_over:
            print("Game is over!!!")
            return

        if TicTacToeApp.is_full[TicTacToeApp.next_grids_pos] != 1 and TicTacToeApp.game_steps > 0 and TicTacToeApp.next_grids_pos != self.position_in_board:
            print("Follow the rules")
            return
        if TicTacToeApp.AI_player:
            self.status = TicTacToeApp.overall_status[self.position_in_board]

        # Create player symbol and color lookups
        player = {1: 'X', -1: 'O'}
        # divide 0-255 by 255 to get desired color
        colors = {-1: (0, 0.6, 0, .9), 1: (0, 1, 0, 1)}  # (r, g, b, a)

        # Pass button coords as argument 
        row, column = button.coords  
        # print(row, column)

        # Convert 2D grid coordinates to 1D status index
        status_index = 3 * row + column
        already_played = self.status[status_index]

        # If cell has not been played
        if not already_played:
            TicTacToeApp.next_grids_pos = row * 3 + column
            # print("Next position on board has to be: ", TicTacToeApp.next_grids_pos)
            print(pow(-1, TicTacToeApp.game_steps % 2))
            self.status[status_index] = pow(-1, TicTacToeApp.game_steps % 2)
            print("Current status before update: ", TicTacToeApp.overall_status[self.position_in_board])
            TicTacToeApp.overall_status[self.position_in_board][status_index] = pow(-1, TicTacToeApp.game_steps % 2)
            print("Current status after update: ", TicTacToeApp.overall_status[self.position_in_board])

            button.text = player[pow(-1, TicTacToeApp.game_steps % 2)]
            # button.text = str(pow(-1, TicTacToeApp.game_steps % 2))
            button.background_color = colors[pow(-1, TicTacToeApp.game_steps % 2)]
            TicTacToeApp.game_steps += 1

            if TicTacToeApp.AI_player:
                self.SmartMove(TicTacToeApp.next_grids_pos)
            return

    def callback(self,dt):
        pass


    def AI_button_pressed(self, button, mini_board_pos):
        # print("chosen button: ", button.coords)
        if TicTacToeApp.game_over:
            print("Game is over!!!")
            return False


        # Create player symbol and color lookups
        player = {1: 'X', -1: 'O'}
        colors = {-1: (0, 0.6, 0, .9), 1: (0, 1, 0, 1)}  # (r, g, b, a)

        # Pass button coords as argument
        row, column = button.coords
        # print(row, column)

        # Convert 2D grid coordinates to 1D status index
        status_index = 3 * row + column
        already_played = TicTacToeApp.overall_status[mini_board_pos][status_index]

        # If cell has not been played
        # print("Already played: ", already_played)
        if not already_played:
            TicTacToeApp.next_grids_pos = row * 3 + column
            # print("Next position on board has to be: ", TicTacToeApp.next_grids_pos)
            # self.status[status_index] = pow(-1, TicTacToeApp.game_steps % 2)
            print(pow(-1, TicTacToeApp.game_steps % 2))
            print("Current status before update: ", TicTacToeApp.overall_status[mini_board_pos])
            TicTacToeApp.overall_status[mini_board_pos][status_index] = pow(-1, TicTacToeApp.game_steps % 2)
            print("Current status after update: ", TicTacToeApp.overall_status[mini_board_pos])
            button.text = player[pow(-1, TicTacToeApp.game_steps % 2)]
            # button.text = str(pow(-1, TicTacToeApp.game_steps % 2))
            button.background_color = colors[pow(-1, TicTacToeApp.game_steps % 2)]
            
            TicTacToeApp.game_steps += 1
            self.on_ai_status(new_value=TicTacToeApp.overall_status[mini_board_pos], pos=mini_board_pos)
            return True
        return False

    def RandomMove(self, mini_board_pos):

        # schedule time for AI to "think"               # random delay functionality not working?
        randtime = random.uniform(2, 7)                 # random float between 2 and 7 seconds
        Clock.schedule_once(self.callback, randtime)

        if not TicTacToeApp.game_over:

            # if TicTacToeApp.is_full[mini_board_pos] == 0:
            #     chosen_btn = np.random.randint(mini_board_pos * 9, (mini_board_pos + 1) * 9)
            # else:
            #     chosen_btn = np.random.randint(81)
            # # print("Chosen: ", chosen_btn)
            # btn = TicTacToeApp.button_ids[chosen_btn]
            # valid_move = self.AI_button_pressed(btn, chosen_btn//9)
            valid_move = False
            while not valid_move:
                # print("trying another move")
                if TicTacToeApp.is_full[mini_board_pos] == 0:
                    chosen_btn = np.random.randint(mini_board_pos * 9, (mini_board_pos + 1) * 9)
                else:
                    chosen_btn = np.random.randint(81)
                btn = TicTacToeApp.button_ids[chosen_btn]
                valid_move = self.AI_button_pressed(btn, chosen_btn//9)

    def SmartMove(self, mini_board_pos):

        # schedule time for AI to "think"               # random delay functionality not working?
        # randtime = random.uniform(2, 7)                 # random float between 2 and 7 seconds
        # Clock.schedule_once(self.callback, randtime)

        if not TicTacToeApp.game_over:
            valid_move = False
            while not valid_move:
                # print("trying another move")
                if TicTacToeApp.is_full[mini_board_pos] == 0:
                    options, good_ones, bad_ones = self.find_best_options(TicTacToeApp.overall_status[mini_board_pos], mini_board_pos)
                    if len(good_ones) > 0:
                        chosen_btn = np.random.choice(good_ones, 1)[0]+9*mini_board_pos
                    elif len(options) > 0:
                        chosen_btn = np.random.choice(options, 1)[0]+9*mini_board_pos
                    else:
                        chosen_btn = np.random.randint(9)+9*mini_board_pos
                        times = 10
                        while chosen_btn in bad_ones and times > 0 :
                            chosen_btn = np.random.randint(9) + 9 * mini_board_pos
                            times -= 1
                else:
                    random_mini = np.random.randint(9)
                    good_ones = []
                    try_times = 50
                    while len(good_ones) == 0 and try_times > 0:
                        options, good_ones, bad_ones = self.find_best_options(TicTacToeApp.overall_status[random_mini], mini_board_pos)
                        try_times -= 1
                    if len(good_ones) > 0:
                        chosen_btn = np.random.choice(good_ones, 1)[0]+9*mini_board_pos
                    elif len(options) > 0:
                        chosen_btn = np.random.choice(options, 1)[0]+9*mini_board_pos
                    else:

                        chosen_btn = np.random.randint(81)

                btn = TicTacToeApp.button_ids[chosen_btn]
                valid_move = self.AI_button_pressed(btn, chosen_btn//9)

    def find_best_options(self, status, mini_pos):
        print("Checking this miniboard right now: ", mini_pos)
        options = []
        good_ones = []
        bad_ones = []
        if sum(status[0:3]) == -2:
            options.append(status[0:3].index(0))
        if sum(status[3:6]) == -2:
            options.append(status[3:6].index(0)+3)
        if sum(status[6:9]) == -2:
            options.append(status[6:9].index(0)+6)
        if sum(status[0::3]) == -2:
            options.append(status[0::3].index(0)*3)
        if sum(status[1::3]) == -2:
            options.append(status[1::3].index(0)*3+1)
        if sum(status[2::3]) == -2:
            options.append(status[2::3].index(0)*3+2)
        if sum(status[::4]) == -2:
            options.append(status[::4].index(0)*4)
        if sum(status[2:-2:2]) == -2:
            options.append((status[2:-2:2].index(0)+1)*2)
        if sum(status[0:3]) == 2:
            good_ones.append(status[0:3].index(0))
        if sum(status[3:6]) == 2:
            good_ones.append(status[3:6].index(0)+3)
        if sum(status[6:9]) == 2:
            good_ones.append(status[6:9].index(0)+6)
        if sum(status[0::3]) == 2:
            good_ones.append(status[0::3].index(0)*3)
        if sum(status[1::3]) == 2:
            good_ones.append(status[1::3].index(0)*3+1)
        if sum(status[2::3]) == 2:
            good_ones.append(status[2::3].index(0)*3+2)
        if sum(status[::4]) == 2:
            good_ones.append(status[::4].index(0)*4)
        if sum(status[2:-2:2]) == 2:
            good_ones.append((status[2:-2:2].index(0)+1)*2)
        for pos in range(9):
            if TicTacToeApp.overall_status[mini_pos][pos] == 0:
                status = TicTacToeApp.overall_status[pos]
                sums = [sum(status[0:3]), sum(status[3:6]), sum(status[6:9]),  # rows
                        sum(status[0::3]), sum(status[1::3]), sum(status[2::3]),  # columns
                        sum(status[::4]), sum(status[2:-2:2])]

                if 3 in sums or -3 in sums:
                    good_ones.append(pos)
                if (2 in sums or -2 in sums) and pos != mini_pos or TicTacToeApp.is_full[mini_pos]:
                    if pos not in good_ones:
                        bad_ones.append(pos)
                        if pos in options:
                            options.remove(pos)
                    if pos in good_ones:
                        bad_ones.append(pos)
                        good_ones.remove(pos)
        print("Here are some good ones: ", good_ones)
        print("Here are some bad ones: ", bad_ones)
        return options, good_ones, bad_ones

    def on_ai_status(self, new_value, pos):
        status = new_value
        status_overall = TicTacToeApp.status

        # Sum each row, column and diagonal
        sums = [sum(status[0:3]), sum(status[3:6]), sum(status[6:9]), # rows
                sum(status[0::3]), sum(status[1::3]), sum(status[2::3]), # columns
                sum(status[::4]), sum(status[2:-2:2])] # diagonals

        if 3 in sums and TicTacToeApp.status[pos] != 1:
            TicTacToeApp.status[pos] = 1
            x_win = Button(text=f'X\'s win miniboard {pos} !', font_size = 40)
            TicTacToeApp.x_miniboard_count += 1
            #GameWindow.xscore.
            x_popup = Popup(title='Miniboard Won!', content=x_win, auto_dismiss=True, size_hint=(0.3, 0.3))
            x_win.bind(on_press=x_popup.dismiss)
            x_popup.open()
            print('X wins miniboard', pos)

            # Implement graphic for winning of miniboard

        elif -3 in sums and TicTacToeApp.status[pos] != -1:
            TicTacToeApp.status[pos] = -1
            o_win = Button(text=f'O\'s win miniboard {pos} !', font_size = 40)
            TicTacToeApp.o_miniboard_count += 1
            o_popup = Popup(title='Miniboard Won!', content=o_win, auto_dismiss=True, size_hint=(0.3, 0.3))
            o_win.bind(on_press=o_popup.dismiss)
            o_popup.open()

            print('O wins miniboard', pos)

            # Implement graphic for winning of miniboard

        if 0 not in TicTacToeApp.overall_status[pos]:
            # when full, check if it is draw
            if -3 not in sums and 3 not in sums:
                print('Draws in miniboard', pos)
            # 2 indicate it is full
            TicTacToeApp.is_full[pos] = 1
            print(pos, " is full now!")

        sum_overall = [sum(status_overall[0:3]), sum(status_overall[3:6]), sum(status_overall[6:9]),  # rows
                       sum(status_overall[0::3]), sum(status_overall[1::3]), sum(status_overall[2::3]),  # columns
                       sum(status_overall[::4]), sum(status_overall[2:-2:2])]  # diagonals

        # Determine final game score
        if 3 in sum_overall:
            TicTacToeApp.status[pos] = 1
            TicTacToeApp.game_over = True
            x_win = Button(text=f'X is the winner!!!', font_size = 40)
            #GameWindow.xscore.
            x_popup = Popup(title='Game over', content=x_win, auto_dismiss=True, size_hint=(0.3, 0.3))
            x_win.bind(on_press=x_popup.dismiss)
            x_popup.open()
            print('X wins the game!')

        elif -3 in sum_overall:
            TicTacToeApp.game_over = True
            TicTacToeApp.status[pos] = -1
            o_win = Button(text=f'O is the winner!!!', font_size = 40)
            #GameWindow.xscore.
            o_popup = Popup(title='Game over', content=o_win, auto_dismiss=True, size_hint=(0.3, 0.3))
            o_win.bind(on_press=o_popup.dismiss)
            o_popup.open()
            print('O wins the game!')

        elif 0 not in sum_overall:
            TicTacToeApp.game_over = True
            draw = Button(text=f'You draw :(', font_size = 40)
            #GameWindow.xscore.
            draw_popup = Popup(title='Game over', content=draw, auto_dismiss=True, size_hint=(0.3, 0.3))
            draw.bind(on_press=draw_popup.dismiss)
            draw_popup.open()
            print("DRAW")


    def on_status(self, instance, new_value):
        # print(self.position_in_board)
        status = new_value
        status_overall = TicTacToeApp.status
        # print(status, status_overall)

        # Sum each row, column and diagonal
        sums = [sum(status[0:3]), sum(status[3:6]), sum(status[6:9]), # rows
                sum(status[0::3]), sum(status[1::3]), sum(status[2::3]), # columns
                sum(status[::4]), sum(status[2:-2:2])] # diagonals
        x_popup = None
        o_popup = None
        # Determine whether someone has won a miniboard
        if 3 in sums and TicTacToeApp.status[self.position_in_board] != 1:
            TicTacToeApp.status[self.position_in_board] = 1
            x_win = Button(text=f'X\'s win miniboard {self.position_in_board} !', font_size = 40)
            TicTacToeApp.x_miniboard_count += 1
            #GameWindow.xscore.
            x_popup = Popup(title='Miniboard Won!', content=x_win, auto_dismiss=True, size_hint=(0.3, 0.3))
            x_win.bind(on_press=x_popup.dismiss)
            x_popup.open()
            print('X wins miniboard', self.position_in_board)

            # Implement graphic for winning of miniboard

        elif -3 in sums and TicTacToeApp.status[self.position_in_board] != -1:
            TicTacToeApp.status[self.position_in_board] = -1
            o_win = Button(text=f'O\'s win miniboard {self.position_in_board} !', font_size = 40)
            TicTacToeApp.o_miniboard_count += 1
            o_popup = Popup(title='Miniboard Won!', content=o_win, auto_dismiss=True, size_hint=(0.3, 0.3))
            o_win.bind(on_press=o_popup.dismiss)
            o_popup.open()

            print('O wins miniboard', self.position_in_board)

            # Implement graphic for winning of miniboard

        if 0 not in self.status:
            # 2 indicate it is full
            print('Draws in miniboard', self.position_in_board)
            print(self.position_in_board, " is full now!")
            TicTacToeApp.is_full[self.position_in_board] = 1

        sum_overall = [sum(status_overall[0:3]), sum(status_overall[3:6]), sum(status_overall[6:9]), # rows
                       sum(status_overall[0::3]), sum(status_overall[1::3]), sum(status_overall[2::3]), # columns
                       sum(status_overall[::4]), sum(status_overall[2:-2:2])] # diagonals

        # Determine final game score
        if 3 in sum_overall:
            TicTacToeApp.status[self.position_in_board] = 1
            TicTacToeApp.game_over = True
            if x_popup:
                x_popup.dismiss()
            x_win = Button(text=f'X is the winner!!!', font_size = 40)
            #GameWindow.xscore.
            x_popup = Popup(title='Game over', content=x_win, auto_dismiss=True, size_hint=(0.3, 0.3))
            x_win.bind(on_press=x_popup.dismiss)
            x_popup.open()
            print('X wins the game!')

        elif -3 in sum_overall:
            TicTacToeApp.game_over = True
            TicTacToeApp.status[self.position_in_board] = -1
            if o_popup:
                o_popup.dismiss()
            o_win = Button(text=f'O is the winner!!!', font_size = 40)
            #GameWindow.xscore.
            o_popup = Popup(title='Game over', content=o_win, auto_dismiss=True, size_hint=(0.3, 0.3))
            o_win.bind(on_press=o_popup.dismiss)
            o_popup.open()
            print('O wins the game!')

        elif 0 not in sum_overall:
            TicTacToeApp.game_over = True
            draw = Button(text=f'You draw :(', font_size = 40)
            #GameWindow.xscore.
            draw_popup = Popup(title='Game over', content=draw, auto_dismiss=True, size_hint=(0.3, 0.3))
            draw.bind(on_press=draw_popup.dismiss)
            draw_popup.open()
            print("DRAW")


    # Reset cell method for 3x3                     
    def reset(self, *args):
        self.status = [0 for _ in range(9)]

        # for all children in list
        for child in self.children:
            child.text = ''
            child.background_color = (1, 1, 1, 1)

        self.current_player = 1
        TicTacToeApp.AI_player = True
        TicTacToeApp.game_over = False
        TicTacToeApp.game_steps = 0
        TicTacToeApp.next_grids_pos = -1
        TicTacToeApp.status = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        TicTacToeApp.overall_status = [[0 for i in range(9)] for j in range(9)]
        TicTacToeApp.is_full = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        TicTacToeApp.button_ids = []

        x_miniboard_count = 0
        o_miniboard_count = 0
        reset = 0


class ultimateGrid(TicTacToeGrid):
    coords = ListProperty([0, 0])

import time
# Class for the 9x9 grid
class UltimateTicTacToeGrid(GridLayout):
    def __init__(self, *args, **kwargs):
        super(UltimateTicTacToeGrid, self).__init__(*args, **kwargs)

        # populate grid layout with miniboards
        for row in range(3):
            for column in range(3):
                grid_entry = ultimateGrid(coords=(row, column))
                grid_entry.position_in_board = row * 3 + column
                # print("Position in board",grid_entry.position_in_board)
                grid_entry.bind()
                self.add_widget(grid_entry)

        

# Current working window class for game
class GameWindow(FloatLayout):
    xscore = None
    oscore = None 

    def __init__(self, *args, **kwargs):
        super(GameWindow, self).__init__(*args, **kwargs)

        ultGrid = UltimateTicTacToeGrid()
        self.add_widget(ultGrid)

        #TicTacToeApp.x_miniboard_count = StringProperty('0')
        #TicTacToeApp.o_miniboard_count = StringProperty('0')

        xscore = Label(text=str(TicTacToeApp.x_miniboard_count), pos_hint={'center_x': .125, 'center_y': .65}, font_size=80)
        oscore = Label(text=str(TicTacToeApp.x_miniboard_count), pos_hint={'center_x': .875, 'center_y': .65}, font_size=80)

        self.add_widget(xscore)
        self.add_widget(oscore)


    def set_ai(self):
        TicTacToeApp.AI_player = True

    def set_human(self):
        TicTacToeApp.AI_player = False




# App class
class TicTacToeApp(App):
    # Activates AI player or not
    AI_player = True

    game_over = False
    game_steps = 0
    next_grids_pos = -1
    status = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    overall_status = [[0 for i in range(9)] for j in range(9)]
    is_full = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    button_ids = []

    x_miniboard_count = 0
    o_miniboard_count = 0
    reset = 0


    def build(self):
        self.title = "Ultimate Tic Tac Toe"
        #Clock.schedule_once(update(), 1)
        self.root = GameWindow()
    pass


if __name__ == "__main__":
	TicTacToeApp().run()
