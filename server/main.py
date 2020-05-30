from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from agent import Agent
from chess import Chess, Action

app = Flask(__name__)
CORS(app)
chess = Chess()
agent = Agent(chess, 0, 4)


@app.route("/")
@cross_origin()
def home():
    return jsonify(chess.to_array())


@app.route("/take_action")
@cross_origin()
def take_action(chess=chess):
    a_type = int(request.args.get('type'))
    new = request.args.get('new')
    new = [[int(new[0]), int(new[2])], [int(new[4]), int(new[6])]]

    a2 = None
    if chess.board[new[0][0]][new[0][1]].index == 6 and chess.board[new[0][0]][new[0][1]].color == 1:
        if new[1][1] > new[0][1]:
            a2 = Action(2, [1, "king"])
        else:
            a2 = Action(2, [1, "queen"])

    a = Action(a_type, new)
    if chess.real_step(a) or ((a2 is not None) and (chess.real_step(a2))):
        if chess.checkmate(0):
            # chess.reset()
            return jsonify({"worked": True, "opp_checkmated": True})
        else:
            return jsonify({"worked": True, "opp_checkmated": False})

    return jsonify({"worked": False})


@app.route("/opponent_step")
@cross_origin()
def opponent_step(chess=chess):
    move = agent.act()
    if chess.checkmate(1):
        return jsonify({"user_checkmated": True, "user_check": chess.check(1)})
    return jsonify({"user_checkmated": False, "user_check": chess.check(1)})


@app.route("/reset")
@cross_origin()
def reset(chess=chess):
    chess.reset()
    return jsonify({"reset": True})


if __name__ == "__main__":
    app.run(debug=True)
