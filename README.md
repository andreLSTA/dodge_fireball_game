# Dodge Fireball Game

A simple game made for personal learning. This game was created to learn neural networks applied in games in a evolutionary model.

## Requirements
- [python 3.6](https://www.python.org/downloads/release/python-360/)

## Installation

Use the package [pip](https://pip.pypa.io/en/stable/) to install the libraries. Try to download the libraries in versions used in the project to avoid compatibility problems. Run the following commands or check it out in their official pages:
- [pygame (v1.9.6)](https://www.pygame.org/wiki/GettingStarted):
```bash
$ pip3 install pygame
```
- [numpy (v1.18.5)](https://numpy.org/install/):
```bash
$ pip3 install numpy
```

## Project Structure

```
dodgefireballgame/
│
├── assets/                  # (Sprites used in the project)
├── models/                  # (Classes used in the project)
│   
├── player_vs_player.py      # (Run this to play against a friend)
├── player_vs_bot.py         # (Run this to play against a bot)
├── only_player.py           # (Run this to play alone)
├── only_bot.py              # (Run this to watch the bot playing alone) 
└── bot_training.py          # (Run this to watch the bot training)
```

## How to run

Any of the codes in the root directory can be used to play. Choose one according to what was written in the project structure description. To run them, use the command below:

```bash
$ python3 FILE_YOU_CHOSE.py
```

### Bot training

If you run the command below, a new neural network can be created based on your training:

```bash
$ python3 bot_training.py
```

The details of each generation are shown in the terminal. Whenever the whole population dies, the game generates a file named "neural_network.p", until reaching a desirable number of waves survived. To replace the AI used in the bots, you can rename it to "bot_neural_network.p", so the bots will switch their behavior to this new one generated on your training. 

After cloning/downloading this project, it will have an initial "bot_neural_network.p", so you won't need to train it again if you're just testing the game. But for the ones wanting to watch the process of learning you can execute the previous steps.


