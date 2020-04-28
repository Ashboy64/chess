from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from agent import Agent
from chess import Chess, Action

app = Flask(__name__)
CORS(app)
chess = Chess()
agent = Agent(chess, 0, 1)


@app.route("/")
@cross_origin()
def home():
    return jsonify(chess.to_array())


@app.route("/take_action")
@cross_origin()
def take_action():
    a_type = int(request.args.get('type'))
    new = request.args.get('new')
    new = [[int(new[0]), int(new[2])], [int(new[4]), int(new[6])]]

    a = Action(a_type, new)
    chess.real_step(a)

    agent.act()

    return jsonify(chess.to_array())


if __name__ == "__main__":
    app.run(debug=True)
