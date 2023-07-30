class Connect4:
    def __init__(self):
        self.board = self.create_board()
        self.game_over = False
        self.winner = None
        # 1 represents player 1 and -1 represents player 2
        self.current_player = 1

    def create_board(self):
        # The board has 6 rows and 7 columns
        return [[0 for _ in range(7)] for _ in range(6)]

    def print_board(self):
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board]))

    def is_valid_move(self, col):
        # A move is valid if the top row of a column is not occupied
        return self.board[0][col] == 0

    def get_valid_moves(self):
        return [c for c in range(7) if self.is_valid_move(c)]

    def make_move(self, col):
        if self.is_valid_move(col):
            for r in range(5, -1, -1):
                if self.board[r][col] == 0:
                    self.board[r][col] = self.current_player
                    break
            if self.is_winner(self.current_player):
                self.game_over = True
                self.winner = self.current_player
            else:
                # Switch to the other player
                self.current_player *= -1
            return True
        else:
            return False

    def is_winner(self, piece):
        # Check horizontal, vertical and diagonal directions
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for r in range(6):
            for c in range(7):
                if self.board[r][c] == piece:
                    for dr, dc in directions:
                        if self.check_direction(r, c, dr, dc, piece):
                            return True
        return False

    def check_direction(self, r, c, dr, dc, piece):
        # Check four positions in the given direction
        for i in range(1, 4):
            nr, nc = r + dr * i, c + dc * i
            if not (0 <= nr < 6 and 0 <= nc < 7) or self.board[nr][nc] != piece:
                return False
        return True

    def get_state(self):
        # Flatten the board into a 1D list and return it
        return [cell for row in self.board for cell in row]
