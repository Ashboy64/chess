import random


class Agent(object):
    """Agent."""

    def __init__(self, game, color, depth):
        super(Agent, self).__init__()
        self.game = game
        self.color = color
        self.depth = depth

    def act(self):
        move = self.minimax_decision(self.depth)
        self.game.real_step(move)
        return move

    def minimax_decision(self, depth):
        """ONLY WORKS FOR ACTION TYPE 0"""
        possible_actions = self.game.possible_moves(self.color)
        random.shuffle(possible_actions)
        best_action_value = None
        best_action = None

        for a in possible_actions:
            if a.type != 2:
                val = self.min_value(self.game.step(a), best_action_value, (self.color + 1) % 2, depth - 1)
                if (best_action_value is None) or (val > best_action_value):
                    best_action_value = val
                    best_action = a
        return best_action

    def min_value(self, state, alpha, color, depth):
        if depth == 0:
            return self.game.evaluate(self.color, board=state)

        possible_actions = self.game.possible_moves(color, board=state)
        random.shuffle(possible_actions)
        best_action_value = None

        for a in possible_actions:
            if a.type != 2:
                val = self.max_value(self.game.step(a, board=state), best_action_value, (color + 1) % 2, depth - 1)
                if (best_action_value is None) or (val < best_action_value):
                    best_action_value = val

                if alpha is not None and best_action_value <= alpha:
                    return best_action_value

        return best_action_value

    def max_value(self, state, beta, color, depth):
        if depth == 0:
            return self.game.evaluate(self.color, board=state)

        possible_actions = self.game.possible_moves(color, board=state)
        random.shuffle(possible_actions)
        best_action_value = None

        for a in possible_actions:
            if a.type != 2:
                val = self.min_value(self.game.step(a, board=state), best_action_value, (color + 1) % 2, depth - 1)
                if (best_action_value is None) or (val > best_action_value):
                    best_action_value = val

                if beta is not None and best_action_value >= beta:
                    return best_action_value

        return best_action_value
