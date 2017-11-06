from tkinter import *
from tkinter import messagebox


class User:
    """Save user id"""

    def __init__(self, id):
        self._id = id

    def get_id(self):
        """ Get id of user."""
        return self._id


class Cell:
    """Cell for board"""

    def __init__(self, user):
        self._marked_user = user.get_id()

    def get_marked_user(self):
        """ Return the user who marked the current cell."""
        return self._marked_user


class Cordinate:
    """ Hold cordinate info"""

    def __init__(self, row_index, col_index):
        self._row_index = row_index
        self._col_index = col_index

    def get_row_index(self):
        """ Get x cordinate."""
        return self._row_index

    def get_column_index(self):
        """ Get y cordinate."""
        return self._col_index


class Board:
    """docstring for Board"""

    def __init__(self, row_length, col_length, handle_button_click):
        self.row_length = row_length
        self.col_length = col_length
        self.marked_cells = {}
        self.total_cell = row_length * col_length
        self.handle_button_click = handle_button_click
        # root = Tk()
        # app_view = Baord(root, l, w)
        # app_view.pack(side='top', fill='both', expand=True)
        self._widget = {}
        # self._view = self._create_view(root, l, w)
        # root.mainloop()

    def create_view(self, root, row_length, col_length):
        """ Create board view."""
        Grid.rowconfigure(root, 0, weight=1)
        Grid.columnconfigure(root, 0, weight=1)

        # Create & Configure frame
        frame = Frame(root)
        frame.grid(row=0, column=0, sticky=N + S + E + W)

        root.geometry('400x400+300+100')
        root.title('My app')

        # Create a 5x10 (rows x columns) grid of buttons inside the frame
        for row_index in range(row_length):
            Grid.rowconfigure(frame, row_index, weight=1)
            for col_index in range(col_length):
                Grid.columnconfigure(frame, col_index, weight=1)
                btn = Button(frame,
                             borderwidth=1,
                             command=lambda cordinate=Cordinate(row_index, col_index):
                             self.handle_button_click(cordinate), bg='White', fg='Black')
                btn.grid(row=row_index, column=col_index, sticky=N + S + E + W)
                self._widget[(row_index, col_index)] = btn

    def show_marked_user(self, user, cordinate):
        """  On button click, display user id on borad."""
        self._widget[(cordinate.get_row_index(), cordinate.get_column_index())].\
            configure(text='%s' % (user.get_id()), state="disabled")

    def add_into_marked_cell(self, user, cordinate):
        """ Mark cell for each turn."""
        self.marked_cells[(cordinate.get_row_index(),
                           cordinate.get_column_index())] = Cell(user)

    def is_cell_marked_by_user(self, user, cordinate):
        """Check weather give user marked the cell or not."""
        return 1 if self.is_cell_marked(cordinate) and \
            self.get_marked_user(cordinate) == user.get_id() else 0

    def is_cell_marked(self, cordinate):
        """ Return weather a cell is marked or not."""
        return (cordinate.get_row_index(), cordinate.get_column_index()) in self.marked_cells

    def get_marked_user(self, cordinate):
        """ Return user who marked the cell."""
        return self.marked_cells[(cordinate.get_row_index(),
                                  cordinate.get_column_index())].get_marked_user()


class Game():
    """ Game class."""

    def __init__(self, row_count, column_count, root):
        self._root = root
        self._board = Board(row_count, column_count, self.handle_button_click)
        self._user = User(0)
        self._view = self._board.create_view(
            self._root, row_count, column_count)
        self._root.mainloop()

    def _get_current_user(self):
        return self._user

    def _is_valid_cordinate(self, cordinate):
        """ Check for validity of input cordinate."""
        return -1 < cordinate.get_row_index() < self._board.row_length and -1 < \
            cordinate.get_column_index() < self._board.col_length and \
            (cordinate.get_row_index(), cordinate.get_column_index()
             ) not in self._board.marked_cells

    def _update_current_user(self):
        self._user = User((self._user.get_id() + 1) % 2)

    def _is_horizenatally_completed(self, cordinate):
        """ Check weather user marked all horizenatal cell of current cordinate."""
        user = self._get_current_user()
        return sum([self._board.is_cell_marked_by_user(
            user, Cordinate(cordinate.get_row_index(), index))
            for index in range(self._board.col_length)]) == self._board.col_length

    def _is_verically_completed(self, cordinate):
        """ Check weather user marked all verical cell of current cordinate."""
        user = self._get_current_user()
        return sum([self._board.is_cell_marked_by_user(
            user, Cordinate(index, cordinate.get_column_index()))
            for index in range(self._board.row_length)]) == self._board.row_length

    def _is_diagonally_completed(self, cordinate):
        """ Check weather user marked all diagonal cell of current cordinate."""
        # Check only when x is equeal to y.
        # Check top down diagonal.
        # Check bootom up diagonal.
        user = self._get_current_user()
        board_length = self._board.row_length
        row_index, column_index = cordinate.get_row_index(), cordinate.get_column_index()
        return (row_index == column_index or row_index == board_length - 1 - column_index) and \
            (sum([self._board.is_cell_marked_by_user(user, Cordinate(index, board_length - 1 - index))
                  for index in range(board_length)]) == board_length or
             sum([self._board.is_cell_marked_by_user(user, Cordinate(index, index))
                  for index in range(board_length)]) == board_length
             )

    def _is_user_won(self, cordinate):
        """ Check weather game is finished or not"""
        return self._is_horizenatally_completed(cordinate) \
            or self._is_verically_completed(cordinate) \
            or self._is_diagonally_completed(cordinate)

    def handle_button_click(self, cordinate):
        """ Handle borad button click."""
        if self._is_valid_cordinate(cordinate):
            user = self._get_current_user()
            self._board.show_marked_user(user, cordinate)
            self._board.add_into_marked_cell(user, cordinate)
            if self._is_user_won(cordinate):
                messagebox.showinfo(
                    "Game completed", 'User won: %s !!!' % (user.get_id()))
                self._root.quit()
            elif len(self._board.marked_cells) == self._board.total_cell:
                messagebox.showinfo("Game tied", 'Tied.')
                self._root.quit()
            else:
                self._update_current_user()


def confirm_quit():
    global is_quitting, already_asked
    is_quitting = messagebox.askquestion(
        'tic tac toe', 'Do you want to quit?') == 'yes'
    already_asked = True
    master.quit()
    # is_quitting = True
    # master.destroy()
    # sys.exit()


is_quitting = False
if __name__ == '__main__':
    n = int(input("Please enter matrics size: "))
    while True:
        already_asked = False
        master = Tk()
        master.protocol("WM_DELETE_WINDOW", confirm_quit)
        Game(n, n, master)
        if not already_asked:
            confirm_quit()
        master.destroy()
        if is_quitting:
            break

        # if messagebox.askquestion('tic tac toe', 'Do you want to play again?') == 'no':
        #     master.destroy()
        #     break
        # master.destroy()
