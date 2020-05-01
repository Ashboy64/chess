# chess

A simple chess playing program. The backend with the actual rules and the opponent agent is a flask server that can be found in the folder 'server'. The front end that interacts with it and allows you to play against it is in 'front-end'.

## Details

The agent itself does a simple minimax search of depth only 3 to plan its moves. It evaluates the board based on the sum of the values of each of its pieces minus that of the opponent, with the value of each piece determined by 'key.yml' in server/data. For now, it always plays as white and the player plays as black.

## Usage

For now, download Flask and run main.py to start the server on your localhost port 5000. Open main.html in your browser to play against the agent.
