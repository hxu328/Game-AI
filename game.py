import random
import copy
import time

class Teeko2Player:
    """ An object representation for an AI game player for the game Teeko2.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a Teeko2Player object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this Teeko2Player object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """


        drop_phase = True
        # count the number of ai's piece and empty spot
        count = 0
        empty_count = 0

        for i in range(5):
            for j in range(5):
                if state[i][j] == self.my_piece:
                    count += 1
                if state[i][j] == ' ':
                    empty_count += 1

        # I use a trick position (2, 2) when AI goes first, the position is computed by a "smarter" AI
        # using a min_max() function with a deeper depth (ex. depth = 3) when it goes first. Computing
        # this position(2, 2) consumes more than 5 seconds so I just simply assume AI will choose it as
        # this first place to go. It makes a "simpler" AI (depth = 2) with a shallower depth more likely
        # to win in the future
        if empty_count == 25:
            return [(2, 2)]

        if count == 4:
            drop_phase = False

        if self.my_piece == self.pieces[0]:
            player = 0
        else:
            player = 1

        if not drop_phase:
            succ_for_drop = self.succ(state, player)
            max_for_drop = float('-inf')
            for s in succ_for_drop:
                temp = self.max_value(s, 0, (player+1)%2)
                if temp >= max_for_drop:
                    max_for_drop = temp
                    this_s = s
            move = self.helper_move(state, this_s)

            return move

        # select an unoccupied space randomly
        # TODO: implement a minimax algorithm to play better

        succ_for_move = self.succ(state, player)
        max_for_move = float('-inf')
        for s in succ_for_move:
            temp = self.max_value(s, 0, (player+1)%2)
            if temp >= max_for_move:
                max_for_move = temp
                this_s = s
        move = self.helper_move(state, this_s)

        return move

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.

        Returns:
            int: 1 if this Teeko2Player wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and 3x3 square corners wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i] == self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col] == self.my_piece else -1

        # check \ diagonal wins
        for i in range(2):
            for j in range(2):
                if state[i][j] != ' ' and state[i][j] == state[i+1][j+1] == state[i+2][j+2] == state[i+3][j+3]:
                    return 1 if state[i][j] == self.my_piece else -1

        # check / diagonal wins
        for i in range(3, 5):
            for j in range(2):
                if state[i][j] != ' ' and state[i][j] == state[i-1][j+1] == state[i-2][j+2] == state[i-3][j+3]:
                    return 1 if state[i][j] == self.my_piece else -1

        # check 3x3 square corners wins
        for i in range(1, 4):
            for j in range(1, 4):
                if (state[i][j] == ' ' and
                        state[i-1][j-1] != ' ' and
                        state[i-1][j-1] == state[i-1][j+1] == state[i+1][j-1] == state[i+1][j+1]):
                    return 1 if state[i-1][j-1] == self.my_piece else -1

        return 0 # no winner yet

    def succ(self, state, player):
        player_piece = self.pieces[player]
        opp_piece = self.pieces[(player+1)%2]
        successors = []
        player_locations = []
        opp_locations = []
        empty_locations = []
        # record all pieces and empty spots of the current state
        for i in range(5):
            for j in range(5):
                if state[i][j] == player_piece:
                    player_locations.append((i, j))
                elif state[i][j] == opp_piece:
                    opp_locations.append((i, j))
                elif state[i][j] == ' ':
                    empty_locations.append((i, j))

        #  if it is during the drop phase, add a new piece of the current player's type to the board
        if len(player_locations) < 4:
            for loc in empty_locations:
                new_state = copy.deepcopy(state)
                new_state[loc[0]][loc[1]] = player_piece
                successors.append(new_state)
            return successors

        # if it is during continued gameplay, this means moving any one of the current player's
        # pieces to an unoccupied location on the board
        for p_loc in player_locations:
            if p_loc[0] - 1 >= 0 and (p_loc[0] - 1, p_loc[1]) in empty_locations:
                new_state = copy.deepcopy(state)
                new_state[p_loc[0]][p_loc[1]] = ' '
                new_state[p_loc[0] - 1][p_loc[1]] = player_piece
                successors.append(new_state)
            if p_loc[0] + 1 <= 4 and (p_loc[0] + 1, p_loc[1]) in empty_locations:
                new_state = copy.deepcopy(state)
                new_state[p_loc[0]][p_loc[1]] = ' '
                new_state[p_loc[0] + 1][p_loc[1]] = player_piece
                successors.append(new_state)
            if p_loc[1] - 1 >= 0 and (p_loc[0], p_loc[1] - 1) in empty_locations:
                new_state = copy.deepcopy(state)
                new_state[p_loc[0]][p_loc[1]] = ' '
                new_state[p_loc[0]][p_loc[1] - 1] = player_piece
                successors.append(new_state)
            if p_loc[1] + 1 <= 4 and (p_loc[0], p_loc[1] + 1) in empty_locations:
                new_state = copy.deepcopy(state)
                new_state[p_loc[0]][p_loc[1]] = ' '
                new_state[p_loc[0]][p_loc[1] + 1] = player_piece
                successors.append(new_state)
            if p_loc[0] - 1 >= 0 and p_loc[1] - 1 >= 0 and (p_loc[0] - 1, p_loc[1] - 1) in empty_locations:
                new_state = copy.deepcopy(state)
                new_state[p_loc[0]][p_loc[1]] = ' '
                new_state[p_loc[0] - 1][p_loc[1] - 1] = player_piece
                successors.append(new_state)
            if p_loc[0] - 1 >= 0 and p_loc[1] + 1 <= 4 and (p_loc[0] - 1, p_loc[1] + 1) in empty_locations:
                new_state = copy.deepcopy(state)
                new_state[p_loc[0]][p_loc[1]] = ' '
                new_state[p_loc[0] - 1][p_loc[1] + 1] = player_piece
                successors.append(new_state)
            if p_loc[0] + 1 <= 4 and p_loc[1] + 1 <= 4 and (p_loc[0] + 1, p_loc[1] + 1) in empty_locations:
                new_state = copy.deepcopy(state)
                new_state[p_loc[0]][p_loc[1]] = ' '
                new_state[p_loc[0] + 1][p_loc[1] + 1] = player_piece
                successors.append(new_state)
            if p_loc[0] + 1 <= 4 and p_loc[1] - 1 >= 0 and (p_loc[0] + 1, p_loc[1] - 1) in empty_locations:
                new_state = copy.deepcopy(state)
                new_state[p_loc[0]][p_loc[1]] = ' '
                new_state[p_loc[0] + 1][p_loc[1] - 1] = player_piece
                successors.append(new_state)
        return successors

    def heuristic_game_value(self, state):
        # determine whether the state is a terminal state before evaluating it heuristically
        if self.game_value(state) != 0:
            return self.game_value(state)

        # if not terminal state, then evaluating heuristically
        player_piece = self.my_piece
        opp_piece = self.opp
        player_locations = []
        opp_locations = []
        empty_locations = []
        sum_player = 0
        sum_opp = 0

        # record all pieces of the current state
        for i in range(5):
            for j in range(5):
                if state[i][j] == player_piece:
                    player_locations.append((i, j))
                elif state[i][j] == opp_piece:
                    opp_locations.append((i, j))
                elif state[i][j] == ' ':
                    empty_locations.append((i, j))

        # check horizontal wins
        for i in range(5):
            for j in range(2):
                win_loc = [(i, j), (i, j + 1), (i, j + 2), (i, j + 3)]
                summary = self.helper_heuristic_game_value(win_loc, player_locations, opp_locations, empty_locations)
                sum_player += summary[0]
                sum_opp += summary[1]

        # check vertical wins
        for j in range(5):
            for i in range(2):
                win_loc = [(i, j), (i + 1, j), (i + 2, j), (i + 3, j)]
                summary = self.helper_heuristic_game_value(win_loc, player_locations, opp_locations, empty_locations)
                sum_player += summary[0]
                sum_opp += summary[1]

        # check \ diagonal wins
        for i in range(2):
            for j in range(2):
                win_loc = [(i, j), (i + 1, j + 1), (i + 2, j + 2), (i + 3, j + 3)]
                summary = self.helper_heuristic_game_value(win_loc, player_locations, opp_locations, empty_locations)
                sum_player += summary[0]
                sum_opp += summary[1]

        # check / diagonal wins
        for i in range(3, 5):
            for j in range(2):
                win_loc = [(i, j), (i - 1, j + 1), (i - 2, j + 2), (i - 3, j + 3)]
                summary = self.helper_heuristic_game_value(win_loc, player_locations, opp_locations, empty_locations)
                sum_player += summary[0]
                sum_opp += summary[1]

        # check 3x3 square corners wins
        for i in range(1, 4):
            for j in range(1, 4):
                win_loc = [(i - 1, j - 1), (i + 1, j - 1), (i - 1, j + 1), (i + 1, j + 1)]
                summary = self.helper_heuristic_game_value(win_loc, player_locations, opp_locations, empty_locations)
                if state[i][j] == ' ':
                    sum_player += summary[0]
                    sum_opp += summary[1]

        if sum_player + sum_opp == 0:
            return 0.0
        else:
            return (2.0 / (sum_player + sum_opp + 1)) * sum_player - 1

    def helper_heuristic_game_value(self, win_loc, player_locations, opp_locations, empty_locations):
        sum_player = 0
        sum_opp = 0
        player_occupy = list(set. intersection(set(player_locations), set(win_loc)))
        opp_occupy = list(set. intersection(set(opp_locations), set(win_loc)))
        if len(player_occupy) == 2:
            remain_for_player = list(set(win_loc) - set(player_occupy))
            if set(remain_for_player).issubset(set(empty_locations)):
                sum_player = 1

        if len(player_occupy) == 3:
            remain_for_player = list(set(win_loc) - set(player_occupy))
            if set(remain_for_player).issubset(set(empty_locations)):
                sum_player = 3

        if len(opp_occupy) == 2:
            remain_for_opp = list(set(win_loc) - set(opp_occupy))
            if set(remain_for_opp).issubset(set(empty_locations)):
                sum_opp = 1

        if len(opp_occupy) == 3:
            remain_for_opp = list(set(win_loc) - set(opp_occupy))
            if set(remain_for_opp).issubset(set(empty_locations)):
                sum_opp = 3

        return (sum_player, sum_opp)

    def max_value(self, state, depth, player):
        # the actual depth is 2, since I compute the successors before I call this function on each successor
        bound = 1
        if self.game_value(state) == 1:
            return 1
        elif self.game_value(state) == -1:
            return -1

        successors = self.succ(state, player)
        if depth == bound:
            return self.heuristic_game_value(state)
        elif self.my_piece == self.pieces[player]:
            max_value = float('-inf')
            for s in successors:
                temp = self.max_value(s, depth+1, (player+1)%2)
                if temp >= max_value:
                    max_value = temp
            return max_value
        else:
            min_value = float('inf')
            for s in successors:
                temp = self.max_value(s, depth+1, (player+1)%2)
                if temp <= min_value:
                    min_value = temp
            return min_value

    def helper_move(self, origin_state, new_state):
        move = []
        for i in range(5):
            for j in range(5):
                if origin_state[i][j] == self.my_piece and new_state[i][j] == ' ':
                    move.append((i, j))
                if origin_state[i][j] == ' ' and new_state[i][j] == self.my_piece:
                    move.insert(0, (i, j))
        return move

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = Teeko2Player()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
