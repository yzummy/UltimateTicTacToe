#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.properties import (ListProperty, NumericProperty)

from kivy.uix.gridlayout import GridLayout

from kivy.uix.button import Button
from kivy.properties import ListProperty
from kivy.core.window import Window

Window.size = (600, 640)


class GridEntry(Button):
    coords = ListProperty([0, 0])


class humanVshuman(Button):
    text = "Human vs. Human"
    size_hint = (1, 0.2)
    # background_color = (1,2,1,2)


class compVshuman(Button):
    text = "Computer vs. Human"
    size_hint = (1, 0.2)


class compVscomp(Button):
    text = "Computer vs. Computer"
    size_hint = (1, 0.2)


class TicTacToeGrid(GridLayout):
    status = ListProperty([0, 0, 0, 0, 0, 0, 0, 0, 0])
    current_player = NumericProperty(1)
    position_in_board = -1

    def __init__(self, *args, **kwargs):
        super(TicTacToeGrid, self).__init__(*args, **kwargs)

        for row in range(3):
            for column in range(3):
                grid_entry = GridEntry(coords=(row, column))
                grid_entry.bind(on_release=self.button_pressed)
                self.add_widget(grid_entry)

    # def button_pressed(self, button):
    #     # Print output just to see what's going on
    #     print('{} button clicked!'.format(button.coords))

    def button_pressed(self, button):

        if TicTacToeApp.game_over:
            print("Game is over!!!")
            return
        if TicTacToeApp.is_full[
            TicTacToeApp.next_grids_pos] != 1 and TicTacToeApp.game_steps > 0 and TicTacToeApp.next_grids_pos != self.position_in_board:
            print("Follow the rules")
            return

        # Create player symbol and colour lookups
        player = {1: 'O', -1: 'X'}
        colours = {1: (1, 0, 0, 1), -1: (0, 1, 0, 1)}  # (r, g, b, a)

        row, column = button.coords  # The pressed button is automatically
        print(row, column)

        # passed as an argument

        # Convert 2D grid coordinates to 1D status index
        status_index = 3 * row + column
        already_played = self.status[status_index]

        # If nobody has played here yet, make a new move
        if not already_played:
            TicTacToeApp.next_grids_pos = row * 3 + column
            self.status[status_index] = pow(-1, TicTacToeApp.game_steps % 2)
            button.text = {1: 'O', -1: 'X'}[pow(-1, TicTacToeApp.game_steps % 2)]
            button.background_color = colours[pow(-1, TicTacToeApp.game_steps % 2)]
            TicTacToeApp.game_steps += 1

    def on_status(self, instance, new_value):
        print(self.position_in_board)
        status = new_value
        status_overall = TicTacToeApp.status
        print(status, status_overall)

        # Sum each row, column and diagonal.
        # Could be shorter, but let’s be extra
        # clear what’s going on

        sums = [sum(status[0:3]),  # rows
                sum(status[3:6]), sum(status[6:9]), sum(status[0::3]),  # columns
                sum(status[1::3]), sum(status[2::3]), sum(status[::4]),  # diagonals
                sum(status[2:-2:2])]
        # Sums can only be +-3 if one player
        # filled the whole line
        if 3 in sums:
            TicTacToeApp.status[self.position_in_board] = 1
            print('O wins miniboard', self.position_in_board)
        elif -3 in sums:
            TicTacToeApp.status[self.position_in_board] = -1
            print('X wins miniboard', self.position_in_board)
        if 0 not in self.status:
            # 2 indicate it is full
            print('Draws in miniboard', self.position_in_board)
            TicTacToeApp.is_full[self.position_in_board] = 1

        sum_overall = [sum(status_overall[0:3]),  # rows
                       sum(status_overall[3:6]), sum(status_overall[6:9]), sum(status_overall[0::3]),  # columns
                       sum(status_overall[1::3]), sum(status_overall[2::3]), sum(status_overall[::4]),  # diagonals
                       sum(status_overall[2:-2:2])]
        if 3 in sum_overall:
            TicTacToeApp.status[self.position_in_board] = 1
            game_over = True
            print('O wins the game!')
        elif -3 in sum_overall:
            game_over = True
            TicTacToeApp.status[self.position_in_board] = -1
            print('X wins the game!')
        elif 0 not in sum_overall:
            print("DRAW")

            # Note the *args parameter! It's important later when we make a binding

    # to reset, which automatically passes an argument that we don't care about
    def reset(self, *args):
        self.status = [0 for _ in range(9)]
        TicTacToeApp.game_steps = 0
        # self.children is a list containing all child widgets
        for child in self.children:
            child.text = ''
            child.background_color = (1, 1, 1, 1)

        self.current_player = 1


class ultimateGrid(TicTacToeGrid):
    coords = ListProperty([0, 0])


class UltimateTicTacToeGrid(GridLayout):
    def __init__(self, *args, **kwargs):
        super(UltimateTicTacToeGrid, self).__init__(*args, **kwargs)

        for row in range(3):
            for column in range(3):
                grid_entry = ultimateGrid(coords=(row, column))
                grid_entry.position_in_board = row * 3 + column
                grid_entry.bind()
                self.add_widget(grid_entry)
        hvh_button = humanVshuman()
        hvh_button.bind()
        self.add_widget(hvh_button)
        cvh_button = compVshuman()
        cvh_button.bind()
        self.add_widget(cvh_button)
        cvc_button = compVscomp()
        cvc_button.bind()
        self.add_widget(cvc_button)



class TicTacToeApp(App):
    game_over = False
    game_steps = 0
    next_grids_pos = -1
    status = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    is_full = [0, 0, 0, 0, 0, 0, 0, 0, 0]


    def build(self):
        return UltimateTicTacToeGrid()

    pass


if __name__ == "__main__":
    TicTacToeApp().run()
