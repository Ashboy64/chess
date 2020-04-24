from flask import Flask, jsonify
from flask_cors import CORS

from chess import Chess

app = Flask(__name__)
CORS(app)
chess = Chess()


@app.route("/")
def home():
    return jsonify(chess.to_array())


if __name__ == "__main__":
    app.run(debug=True)
