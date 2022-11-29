from tkinter import *

import numpy as np

board_size = 600
symbol_size = board_size / 10
symbol_thickness = 20
symbol_X_color = '#FF1E1E'
symbol_O_color = '#0014FF'
line_color = '#65647C'
background_color = "#EFEFEF"
green_color = '#379237'


def convert_logical_to_grid_position(logical_position):
    logical_position = np.array(logical_position, dtype=int)
    return (board_size / 3) * logical_position + board_size / 6


def convert_grid_to_logical_position(grid_position):
    grid_position = np.array(grid_position)
    return np.array(grid_position // (board_size / 3), dtype=int)


class TicTacToe:
    def __init__(self):
        self.window = Tk()
        self.window.title('Tic Tac Toe: X play first')
        self.window.resizable(0, 0)
        self.canvas = Canvas(self.window, width=board_size, height=board_size, bg=background_color)
        self.canvas.pack()
        # Input from user in form of clicks
        self.window.bind('<Button-1>', self.click)

        self.initialize_board()
        self.is_X_turn = True
        self.board_status = np.zeros(shape=(3, 3))

        self.player_X_starts = True
        self.reset_board = False
        self.game_over = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False

        self.X_score = 0
        self.O_score = 0
        self.tie_score = 0

    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        for i in range(2):
            self.canvas.create_line((i + 1) * board_size / 3, 0, (i + 1) * board_size / 3, board_size, width=5,
                                    fill=line_color)

        for i in range(2):
            self.canvas.create_line(0, (i + 1) * board_size / 3, board_size, (i + 1) * board_size / 3, width=5,
                                    fill=line_color)

    def play_again(self):
        self.initialize_board()
        self.player_X_starts = not self.player_X_starts
        self.is_X_turn = self.player_X_starts
        if self.is_X_turn:
            self.window.title("X Turn")
        else:
            self.window.title("O Turn")
        self.board_status = np.zeros(shape=(3, 3))

    '''
    Drawing Functions:
    The modules required to draw required game based object on canvas
    '''

    def draw_O(self, logical_position):
        logical_position = np.array(logical_position)
        # logical_position = grid value on the board
        # grid_position = actual pixel values of the center of the grid
        grid_position = convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                outline=symbol_O_color)

    def draw_X(self, logical_position):
        grid_position = convert_logical_to_grid_position(logical_position)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)

    def display_game_over(self):
        if self.player_X_starts:
            self.window.title("Next turn: O play first")
        else:
            self.window.title("Next turn: X play first")

        if self.X_wins:
            self.X_score += 1
            text = 'Winner: X'
            color = symbol_X_color
        elif self.O_wins:
            self.O_score += 1
            text = 'Winner: O'
            color = symbol_O_color
        else:
            self.tie_score += 1
            text = 'Its a tie'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(board_size / 2, board_size / 3, font="cmr 60 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(board_size / 2, 5 * board_size / 8, font="cmr 40 bold", fill=green_color,
                                text=score_text)

        score_text = 'Player 1 (X):\t' + str(self.X_score) + '\n'
        score_text += 'Player 2 (O):\t' + str(self.O_score) + '\n'
        score_text += 'Tie:\t\t' + str(self.tie_score)
        self.canvas.create_text(board_size / 2, 3 * board_size / 4, font="cmr 30 bold", fill=green_color,
                                text=score_text)
        self.reset_board = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(board_size / 2, 15 * board_size / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)

    '''
    Logical Functions:
    The modules required to carry out game logic
    '''

    def is_grid_occupied(self, logical_position):
        if self.board_status[logical_position[0]][logical_position[1]] == 0:
            return False
        else:
            return True

    def is_winner(self, player):

        player = -1 if player == 'X' else 1

        # Three in a row
        for i in range(3):
            if self.board_status[i][0] == self.board_status[i][1] == self.board_status[i][2] == player:
                return True
            if self.board_status[0][i] == self.board_status[1][i] == self.board_status[2][i] == player:
                return True

        # Diagonals
        if self.board_status[0][0] == self.board_status[1][1] == self.board_status[2][2] == player:
            return True

        if self.board_status[0][2] == self.board_status[1][1] == self.board_status[2][0] == player:
            return True

        return False

    def is_tie(self):

        r, c = np.where(self.board_status == 0)
        tie = False
        if len(r) == 0:
            tie = True

        return tie

    def is_game_over(self):
        # Either someone wins or all grid occupied
        self.X_wins = self.is_winner('X')
        if not self.X_wins:
            self.O_wins = self.is_winner('O')

        if not self.O_wins:
            self.tie = self.is_tie()

        game_over = self.X_wins or self.O_wins or self.tie

        if self.X_wins:
            print('X wins')
        if self.O_wins:
            print('O wins')
        if self.tie:
            print('Its a tie')

        return game_over

    def click(self, event):
        grid_position = [event.x, event.y]
        logical_position = convert_grid_to_logical_position(grid_position)

        if not self.reset_board:
            if self.is_X_turn:
                if not self.is_grid_occupied(logical_position):
                    self.draw_X(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = -1
                    self.is_X_turn = not self.is_X_turn
                self.window.title("O Turn")
            else:
                if not self.is_grid_occupied(logical_position):
                    self.draw_O(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = 1
                    self.is_X_turn = not self.is_X_turn
                self.window.title("X Turn")

            # Check if game is concluded
            if self.is_game_over():
                self.display_game_over()

        else:  # Play Again
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False


game_instance = TicTacToe()
game_instance.mainloop()
