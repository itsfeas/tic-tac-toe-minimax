from math import inf as infinity
from random import choice
from random import seed as randomseed       # Paul Lu
import platform
import time
from os import system

"""
An implementation of Minimax AI Algorithm in Tic Tac Toe,
using Python.
This software is available under GPL license.
Author: Clederson Cruz
Year: 2017
License: GNU GENERAL PUBLIC LICENSE (GPL)

Muhammad Fiaz
CCID:  mfiaz
"""

class the_board:
    """docstring for board"""
    def __init__(self):
        self.type = str(self.__class__)
        self.board = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        ]
        return

    def __str__(self):
        return(self.type)

    def __repr__(self):
        representation = "[" + str("<" + str(id(self)) + "> ") + str(self.type) + "]"
        return(representation)

    def set_board(self, board):
        self.board = board
        return
    
    def get_board(self):
        return(self.board)

    def empty_cells(self):
        """
        Each empty cell will be added into cells' list
        :param state: the state of the current board
        :return: a list of empty cells
        """
        cells = []
        board = self.get_board()
        for x, row in enumerate(board):
            for y, cell in enumerate(row):
                if cell == 0:
                    cells.append([x, y])

        return cells

    def valid_move(self, x, y):
        """
        A move is valid if the chosen cell is empty
        :param x: X coordinate
        :param y: Y coordinate
        :return: True if the board[x][y] is empty
        """
        if [x, y] in self.empty_cells():
            return True
        else:
            return False


    def set_move(self, x, y, player):
        """
        Set the move on board, if the coordinates are valid
        :param x: X coordinate
        :param y: Y coordinate
        :param player: the current player
        """
        board = self.get_board()
        if self.valid_move(x, y):
            board[x][y] = player
            return True
        else:
            return False

    def clean(self):
        """
        Clears the console
        """
        # Paul Lu.  Do not clear screen to keep output human readable.
        print()
        return

        os_name = platform.system().lower()
        if 'windows' in os_name:
            system('cls')
        else:
            system('clear')
    

class board_state(the_board):
    """docstring for state"""
    def __init__(self):
        super(board_state, self).__init__()
        self.HUMAN = -1
        self.COMP = +1
    
    def get_human(self):
        return(self.HUMAN)
    
    def get_comp(self):
        return(self.COMP)

    def main_function(self):
        """
        Main method that calls all other methods. Adapted from main().
        I converted this to a method, as it would help with encapsulation.
        """
        # Paul Lu.  Set the seed to get deterministic behaviour for each run.
        #       Makes it easier for testing and tracing for understanding.
        randomseed(274 + 2020)
        HUMAN = self.get_human()
        COMP = self.get_comp()
        self.clean()
        h_choice = ''  # X or O
        c_choice = ''  # X or O
        first = ''  # if human is the first
    
        # Human chooses X or O to play
        while h_choice != 'O' and h_choice != 'X':
            try:
                print('')
                h_choice = input('Choose X or O\nChosen: ').upper()
            except (EOFError, KeyboardInterrupt):
                print('Bye')
                exit()
            except (KeyError, ValueError):
                print('Bad choice')
    
        # Setting computer's choice
        if h_choice == 'X':
            c_choice = 'O'
        else:
            c_choice = 'X'
    
        # Human may starts first
        self.clean()
        while first != 'Y' and first != 'N':
            try:
                first = input('First to start?[y/n]: ').upper()
            except (EOFError, KeyboardInterrupt):
                print('Bye')
                exit()
            except (KeyError, ValueError):
                print('Bad choice')
    
        # Main loop of this game
        while len(self.empty_cells()) > 0 and not self.game_over():
            if first == 'N':
                self.ai_turn(c_choice, h_choice)
                first = ''
    
            self.human_turn(c_choice, h_choice)
            self.ai_turn(c_choice, h_choice)
    
        # Game over message
        if self.wins(HUMAN):
            self.clean()
            print(f'Human turn [{h_choice}]')
            self.render(c_choice, h_choice)
            print('YOU WIN!')
        elif self.wins(COMP):
            self.clean()
            print(f'Computer turn [{c_choice}]')
            self.render(c_choice, h_choice)
            print('YOU LOSE!')
        else:
            self.clean()
            self.render(c_choice, h_choice)
            print('DRAW!')

    def evaluate(self):
        """
        Function to heuristic evaluation of state.
        :param state: the state of the current board
        :return: +1 if the computer wins; -1 if the human wins; 0 draw
        """
        HUMAN = self.get_human()
        COMP = self.get_comp()       
        
        if self.wins(COMP):
            score = +1
        elif self.wins(HUMAN):
            score = -1
        else:
            score = 0

        return score


    def wins(self, player):
        """
        This function tests if a specific player wins. Possibilities:
        * Three rows    [X X X] or [O O O]
        * Three cols    [X X X] or [O O O]
        * Two diagonals [X X X] or [O O O]
        :param state: the state of the current board
        :param player: a human or a computer
        :return: True if the player wins
        """
        board = self.get_board()
        win_state = [
            [board[0][0], board[0][1], board[0][2]],
            [board[1][0], board[1][1], board[1][2]],
            [board[2][0], board[2][1], board[2][2]],
            [board[0][0], board[1][0], board[2][0]],
            [board[0][1], board[1][1], board[2][1]],
            [board[0][2], board[1][2], board[2][2]],
            [board[0][0], board[1][1], board[2][2]],
            [board[2][0], board[1][1], board[0][2]],
        ]
        if [player, player, player] in win_state:
            return True
        else:
            return False


    def game_over(self):
        """
        This function test if the human or computer wins
        :param state: the state of the current board
        :return: True if the human or computer wins
        """
        HUMAN = self.get_human()
        COMP = self.get_comp()        
        return self.wins(HUMAN) or self.wins(COMP)

    def minimax(self, depth, player):
        """
        AI function that choice the best move
        :param state: current state of the board
        :param depth: node index in the tree (0 <= depth <= 9),
        but never nine in this case (see iaturn() function)
        :param player: an human or a computer
        :return: a list with [the best row, best col, best score]
        """
        board = self.get_board()
        HUMAN = self.get_human()
        COMP = self.get_comp()
        
        if player == COMP:
            best = [-1, -1, -infinity]
        else:
            best = [-1, -1, +infinity]

        if depth == 0 or self.game_over():
            score = self.evaluate()
            return [-1, -1, score]

        for cell in self.empty_cells():
            x, y = cell[0], cell[1]
            board[x][y] = player
            score = self.minimax(depth - 1, -player)
            board[x][y] = 0
            score[0], score[1] = x, y

            if player == COMP:
                if score[2] > best[2]:
                    best = score  # max value
            else:
                if score[2] < best[2]:
                    best = score  # min value
            self.set_board(board)
        return best
        
    def render(self, c_choice, h_choice):
        """
        Print the board on console
        :param state: current state of the board
        """
        board = self.get_board()
        chars = {
            -1: h_choice,
            +1: c_choice,
            0: ' '
        }
        str_line = '---------------'

        print('\n' + str_line)
        for row in board:
            for cell in row:
                symbol = chars[cell]
                print(f'| {symbol} |', end='')
            print('\n' + str_line)



    def ai_turn(self, c_choice, h_choice):
        """
        It calls the minimax function if the depth < 9,
        else it choices a random coordinate.
        :param c_choice: computer's choice X or O
        :param h_choice: human's choice X or O
        :return:
        """
        COMP = self.get_comp()        
        depth = len(self.empty_cells())
        if depth == 0 or self.game_over():
            return

        self.clean()
        print(f'Computer turn [{c_choice}]')
        self.render(c_choice, h_choice)

        if depth == 9:
            x = choice([0, 1, 2])
            y = choice([0, 1, 2])
        else:
            move = self.minimax(depth, COMP)
            x, y = move[0], move[1]

        self.set_move(x, y, COMP)
        # Paul Lu.  Go full speed.
        # time.sleep(1)


    def human_turn(self, c_choice, h_choice):
        """
        The Human plays choosing a valid move.
        :param c_choice: computer's choice X or O
        :param h_choice: human's choice X or O
        :return:
        """
        HUMAN = self.get_human()        
        depth = len(self.empty_cells())
        if depth == 0 or self.game_over():
            return

        # Dictionary of valid moves
        move = -1
        moves = {
            1: [0, 0], 2: [0, 1], 3: [0, 2],
            4: [1, 0], 5: [1, 1], 6: [1, 2],
            7: [2, 0], 8: [2, 1], 9: [2, 2],
        }

        self.clean()
        print(f'Human turn [{h_choice}]')
        self.render(c_choice, h_choice)

        while move < 1 or move > 9:
            try:
                move = int(input('Use numpad (1..9): '))
                coord = moves[move]
                can_move = self.set_move(coord[0], coord[1], HUMAN)

                if not can_move:
                    print('Bad move')
                    move = -1
            except (EOFError, KeyboardInterrupt):
                print('Bye')
                exit()
            except (KeyError, ValueError):
                print('Bad choice')



def main():
    playing_board = board_state()
    playing_board.main_function()
    exit()

if __name__ == '__main__':
    main()