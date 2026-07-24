# Task 6: More on Classes


class TictactoeException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class Board:
    valid_moves = [
        "upper left", "upper center", "upper right",
        "middle left", "center", "middle right",
        "lower left", "lower center", "lower right"
    ]

    def __init__(self):
        self.board_array = [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "]
        ]
        self.turn = "X"
        self.last_move = None

    def __str__(self):
        lines = []
        lines.append(f" {self.board_array[0][0]} | {self.board_array[0][1]} | {self.board_array[0][2]} \n")
        lines.append("-----------\n")
        lines.append(f" {self.board_array[1][0]} | {self.board_array[1][1]} | {self.board_array[1][2]} \n")
        lines.append("-----------\n")
        lines.append(f" {self.board_array[2][0]} | {self.board_array[2][1]} | {self.board_array[2][2]} \n")
        return "".join(lines)

    def move(self, move_string):
        if move_string not in Board.valid_moves:
            raise TictactoeException("That's not a valid move.")

        move_index = Board.valid_moves.index(move_string)
        row = move_index // 3
        column = move_index % 3

        if self.board_array[row][column] != " ":
            raise TictactoeException("That spot is taken.")

        self.board_array[row][column] = self.turn
        self.last_move = move_string

        if self.turn == "X":
            self.turn = "O"
        else:
            self.turn = "X"

    def whats_next(self):
        win = False
        winner = None

        for row in self.board_array:
            if row[0] != " " and row[0] == row[1] == row[2]:
                win = True
                winner = row[0]

        for column in range(3):
            if self.board_array[0][column] != " ":
                if self.board_array[0][column] == self.board_array[1][column] == self.board_array[2][column]:
                    win = True
                    winner = self.board_array[0][column]

        if self.board_array[1][1] != " ":
            if self.board_array[0][0] == self.board_array[1][1] == self.board_array[2][2]:
                win = True
                winner = self.board_array[1][1]

            if self.board_array[0][2] == self.board_array[1][1] == self.board_array[2][0]:
                win = True
                winner = self.board_array[1][1]

        if win:
            return (True, f"{winner} wins!")

        board_is_full = True

        for row in self.board_array:
            for spot in row:
                if spot == " ":
                    board_is_full = False

        if board_is_full:
            return (True, "Cat's Game.")

        return (False, f"{self.turn}'s turn.")


board = Board()
game_over = False

print(board)

while not game_over:
    print("Valid moves:")
    print(", ".join(Board.valid_moves))

    move_string = input(f"{board.turn}'s turn. Enter move: ")

    try:
        board.move(move_string)
        print(board)
        game_over, message = board.whats_next()
        print(message)

    except TictactoeException as error:
        print(error.message)