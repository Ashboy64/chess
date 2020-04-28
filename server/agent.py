from chess import Action
from utils import LIFO, are_equal


class Agent(object):
    """Agent."""

    def __init__(self, game, color, depth):
        super(Agent, self).__init__()
        self.game = game
        self.color = color
        self.depth = depth

    def act(self):
        self.game.real_step(self.minimax_decision(self.depth))

    def minimax_decision(self, depth):
        """ONLY WORKS FOR ACTION TYPE 0"""
        possible_actions = self.game.possible_moves(self.color)
        best_action_value = None
        best_action = None

        for a in possible_actions:
            val = self.min_value(self.game.step(a), (self.color + 1) % 2, depth - 1)
            if (best_action_value is None) or (val > best_action_value):
                best_action_value = val
                best_action = a
        return best_action

    def min_value(self, state, color, depth):
        if depth == 0:
            return self.game.evaluate(self.color, board=state)

        possible_actions = self.game.possible_moves(color, board=state)
        best_action_value = None
        best_action = None

        for a in possible_actions:
            val = self.max_value(self.game.step(a, board=state), (color + 1) % 2, depth - 1)
            if (best_action_value is None) or (val < best_action_value):
                best_action_value = val
                best_action = a

        return best_action_value

    def max_value(self, state, color, depth):
        if depth == 0:
            return self.game.evaluate(self.color, board=state)

        possible_actions = self.game.possible_moves(color, board=state)
        best_action_value = None
        best_action = None

        for a in possible_actions:
            val = self.min_value(self.game.step(a, board=state), (color + 1) % 2, depth - 1)
            if (best_action_value is None) or (val > best_action_value):
                best_action_value = val
                best_action = a

        return best_action_value
