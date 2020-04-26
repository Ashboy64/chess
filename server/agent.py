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
        self.game.real_step(self.get_action(self.depth))

    def get_action(self, depth):
        """ONLY WORKS FOR ACTION TYPE 0"""
        action_values = {}
        possible_moves = self.game.possible_moves(self.color)
        for action in possible_moves:
            frontier = LIFO()
            frontier.push(self.game.step(action))
            visited = []
            action_values[(tuple(action.new[0]), tuple(action.new[1]))] = self.recursive_minimax(frontier, visited, -1, depth)
        print(action_values)
        max_move = list(max(action_values, key=action_values.get))
        return Action(0, [list(max_move[0]), list(max_move[1])])

    def recursive_minimax(self, frontier, visited, status, depth):
        # status 1 is max, type -1 is min
        n = frontier.pop()
        visited.append(n)

        if (status == 0 and self.color == 0) or (status == 1 and self.color == 1):
            c = 0  # playing white
        else:
            c = 1  # playing black

        if depth == 0:
            return status * self.game.evaluate(c, n)  # return the value of the node

        # Expand all the nodes
        actions = self.game.possible_moves(c, n)

        for action in actions:
            new_state = self.game.step(action, board=n)

            if not ((True in [are_equal(el, new_state) for el in visited]) or frontier.contains(new_state, are_equal)):
                frontier.push(new_state)

        return self.recursive_minimax(frontier, visited, -1 * status, depth - 1)
