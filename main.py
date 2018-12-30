# The plan:
# Execute MCTS in rust
# game logic in rust
# network evaluation in python

# Start python
# Load network
# Start first game
# retrieve game moves from rust
# select using neuralnetwork
# retrieve mcts in rust
# Do best move (and store state and move selected)
# once end go back and learn
import numpy as np
import os.path
import alphazero
from keras.models import load_model
from tictactoe import Player, TicTacToeState, TicTacToeAction, create_model
import mcts
print("Hello world")

# XO_
# _X_
# __Ox



# One plane for player 1
# One plane for player 1 previous
# One plane for player 2
# One plane for player 2 previous
# One plane for colour to play
#
# state = np.array([[
#     [[1, 0, 0], [0, 1, 0], [0, 0, 0]],
#     [[1, 0, 0], [0, 1, 0], [0, 0, 0]],
#     [[0, 1, 0], [0, 0, 0], [0, 0, 1]],
#     [[0, 1, 0], [0, 0, 0], [0, 0, 0]],
#     [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
# ]])
#
# print(state.shape)

# result = model.predict(state)
#
# print("Policy")
# print(np.reshape(result[0], (3, 3)))
#
#
# print("Value")
# print(result[1][0,0])

def playable(model):
    current = TicTacToeState(Player.Cross, Player.Cross, model, 0)
    searcher = mcts.mcts(iterationLimit=100)

    history = []

    while not current.isTerminal():
        current.pretty_print()
        # First computer

        #Evaluate position
        current.evaluate(history)
        best_action = searcher.search(current)
        history.append(current)
        current = current.takeAction(best_action)

        current.pretty_print()

        if current.isTerminal():
            break

        entered = input("enter: x,y: ").split(',')
        x = int(entered[0])
        y = int(entered[1])

        current.evaluate(history)
        player_action = TicTacToeAction(x, y, 1)
        history.append(current)
        current = current.takeAction(player_action)

    current.evaluate(history)
    current.pretty_print()
    print("Played match, winner: {}".format(current.get_winner()))


def test1(model):

    catzero = alphazero.CatZero(iterationLimit=100, model=model)
    terminal = catzero.play(TicTacToeState(Player.Cross, Player.Cross, model, 0))

    for (a, b) in catzero.get_states():
        a.pretty_print()

    print(terminal.get_winner())
def test2(model):
    catzero = alphazero.CatZero(iterationLimit=800, model=model)

    for i in range(10):
        # Play a simulation
        terminal = catzero.play(TicTacToeState(Player.Cross, Player.Cross, model, 0))
        terminal.pretty_print()

        print("Played match, winner: {}".format(terminal.get_winner()))

        # Get
        states = catzero.get_states()
        history = []
        positions = []

        for j in range(len(states)):
            positions.append(states[j][0].get_neural_input(history))
            history.append(states[j][0])

        probabilities = np.array([np.array(a.get_action_probs()) for (a, b) in states])

        if terminal.get_winner() is Player.Cross:
            reward = 1
        elif terminal.get_winner() is Player.Circle:
            reward = -1
        else:
            reward = 0

        catzero.learn(positions=positions, value=reward, probabilities=probabilities)

    model.save("trained_model.h5")
    test1(model)

#sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))

if os.path.isfile("trained_model.h5"):
    model = load_model("trained_model.h5")
    print("Loaded existing model")
else:
    model = create_model()

#test1(model)
playable(model)
for i in range(300):
     test2(model)
