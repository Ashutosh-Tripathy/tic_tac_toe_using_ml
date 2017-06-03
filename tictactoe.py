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
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def get_x(self):
        """ Get x cordinate."""
        return self._x

    def get_y(self):
        """ Get y cordinate."""
        return self._y

class Board:
    """docstring for Board"""
    def __init__(self, l, w):
        self.l = l
        self.w = w
        self.marked_cells = {}
        self.total_cell = l * w

    def mark_cell(self, user, cordinate):
        """ Mark cell for each turn."""
        self.marked_cells[(cordinate.get_x(), cordinate.get_y())] = Cell(user)

    def is_cell_marked_by_user(self, user, cordinate):
        """Check weather give user marked the cell or not."""
        if self.is_cell_marked(cordinate) and \
        self.get_marked_user(cordinate) == user.get_id():
            return 1
        else:
            return 0
    def is_cell_marked(self, cordinate):
        """ Return weather a cell is marked or not."""
        return (cordinate.get_x(), cordinate.get_y()) in self.marked_cells

    def get_marked_user(self, cordinate):
        """ Return user who marked the cell."""
        return self.marked_cells[(cordinate.get_x(), cordinate.get_y())].get_marked_user()


class Game():
    """ Game class."""
    def __init__(self):
        self._board = Board(3, 3)
        self._counter = 0

    def _get_cordinate(self):
        """ Get cordinate from user."""
        x, y = map(int, input("Enter space separated cordinate: ").strip().split())
        return Cordinate(x, y)

    def _is_valid_cordinate(self, cordinate):
        """ Check for validity of input cordinate."""
        return -1 < cordinate.get_x() < self._board.l and -1 < cordinate.get_y() < self._board.w \
        and (cordinate.get_x(), cordinate.get_y()) not in self._board.marked_cells

    def _is_horizenatally_completed(self, user, cordinate):
        """ Check weather user marked all horizenatal cell of current cordinate."""
        return sum([self._board.is_cell_marked_by_user(user, Cordinate(cordinate.get_x(), y)) \
        for y in range(self._board.w)]) == self._board.w

    def _is_verically_completed(self, user, cordinate):
        """ Check weather user marked all verical cell of current cordinate."""
        return sum([self._board.is_cell_marked_by_user(user, Cordinate(x, cordinate.get_y())) \
        for x in range(self._board.l)]) == self._board.l

    def _is_diagonally_completed(self, user, cordinate):
        """ Check weather user marked all diagonal cell of current cordinate."""
        # Check only when x is equeal to y.
        # Check top down diagonal.
        # Check bootom up diagonal.
        board_length = self._board.l
        return cordinate.get_x() == cordinate.get_y() and \
        (sum([self._board.is_cell_marked_by_user(user, Cordinate(x, board_length - 1 - x)) \
        for x in range(board_length)]) == board_length or \
        sum([self._board.is_cell_marked_by_user(user, Cordinate(x, x)) \
        for x in range(board_length)]) == board_length
        )

    def _is_game_completed(self, user, cordinate):
        """ Check weather game is finished or not"""
        return self._is_horizenatally_completed(user, cordinate) \
        or self._is_verically_completed(user, cordinate) \
        or self._is_diagonally_completed(user, cordinate)

    def _print_board(self):
        # "\n".join(["".join([self._board.get_marked_user() if self._board.is_cell_marked(Cordinate(x, y)) else " " for y in range(self._board.w)])) for x in range(self._board.l) ])
        print("\n".join(["| ".join([str(self._board.get_marked_user(Cordinate(x, y))) if \
        self._board.is_cell_marked(Cordinate(x, y)) else " " for y in range(self._board.w)]) \
         for x in range(self._board.l)]))


        # "\n".join([userid if cellmaked else "" ] for y in range(self._board.w))
        # for x in range(self._board.l):
        #     for y in range(self._board.w):
        #         is_cell_marked_by_user

    def start_game(self):
        """ Starting game."""
        while True:
            self._print_board()
            while True:
                try:
                    cordinate = self._get_cordinate()
                    if self._is_valid_cordinate(cordinate):
                        break
                    else:
                        print("Invalid/Already used cordinate. Try again.")
                except Exception:
                    print("Cordinate not in expected format. Try again.")

            user = User(self._counter % 2)
            self._board.mark_cell(user, cordinate)
            _is_user_won = self._is_game_completed(user, cordinate)
            if self._counter >= self._board.total_cell or _is_user_won:
                break
            self._counter += 1

        if _is_user_won:
            print("%s won the game!!! :)"%(user.get_id()))
        else:
            print("It's a tie.")




game = Game()
game.start_game()