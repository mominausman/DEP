import sys

class RedBlueNim:
    def __init__(self, red, blue, game_type='standard', player_type='computer', search_depth=4):
        self.red = red
        self.blue = blue
        self.game_type = game_type
        self.player_type = player_type
        self.search_depth = search_depth
        self.turn = 'human' if player_type == 'human' else 'computer'

    def is_game_over(self):
        return self.red == 0 or self.blue == 0

    def evaluate(self):
        if self.is_game_over():
            if self.game_type == 'standard':
                return -1 if self.turn == 'computer' else 1
            else:
                return 1 if self.turn == 'computer' else -1
        return 0

    def get_possible_moves(self):
        moves = []
        if self.red > 0:
            moves.append(('red', 1))
        if self.blue > 0:
            moves.append(('blue', 1))
        if self.red > 1:
            moves.append(('red', 2))
        if self.blue > 1:
            moves.append(('blue', 2))
        return moves

    def make_move(self, move):
        color, amount = move
        if color == 'red':
            self.red -= amount
        else:
            self.blue -= amount

    def undo_move(self, move):
        color, amount = move
        if color == 'red':
            self.red += amount
        else:
            self.blue += amount

    def minimax(self, depth, alpha, beta, maximizing):
        if depth == 0 or self.is_game_over():
            return self.evaluate(), None

        best_move = None

        if maximizing:
            max_eval = float('-inf')
            for move in self.get_possible_moves():
                self.make_move(move)
                eval, _ = self.minimax(depth - 1, alpha, beta, False)
                self.undo_move(move)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in self.get_possible_moves():
                self.make_move(move)
                eval, _ = self.minimax(depth - 1, alpha, beta, True)
                self.undo_move(move)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def get_computer_move(self):
        _, best_move = self.minimax(self.search_depth, float('-inf'), float('inf'), True)
        return best_move

    def play(self):
        while not self.is_game_over():
            if self.turn == 'human':
                print(f"Red marbles: {self.red}, Blue marbles: {self.blue}")
                move = input("Enter your move (color amount): ").split()
                color, amount = move[0], int(move[1])
                if (color == 'red' and 0 < amount <= self.red) or (color == 'blue' and 0 < amount <= self.blue):
                    self.make_move((color, amount))
                    self.turn = 'computer'
                else:
                    print("Invalid move. Try again.")
            else:
                move = self.get_computer_move()
                print(f"Computer move: {move}")
                self.make_move(move)
                self.turn = 'human'

        if self.game_type == 'standard':
            print("Computer wins!" if self.turn == 'computer' else "Human wins!")
        else:
            print("Human wins!" if self.turn == 'computer' else "Computer wins!")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python red_blue_nim.py <number_of_red_marbles> <number_of_blue_marbles> <game_type> <player_type> [<search_depth>]")
        sys.exit(1)

    red = int(sys.argv[1])
    blue = int(sys.argv[2])
    game_type = sys.argv[3]
    player_type = sys.argv[4]
    search_depth = int(sys.argv[5]) if len(sys.argv) > 5 else 4

    game = RedBlueNim(red, blue, game_type, player_type, search_depth)
    game.play()
