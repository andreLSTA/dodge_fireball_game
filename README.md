# Dodge Fireball Game

A simple game made for personal learning. The goal is to survive in a forest with random fireballs coming in your direction. This game was created in the purpose of learning neural networks applied in games.

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

If you run:

```bash
$ python3 bot_training.py
```

Whenever all the population dies, the game stops and generates a file named "neural_network.p". To replace the AI used in the bots, you can rename it to "bot_neural_network.p", so the file used by the bots can be changed to the new one generated on your training and you can test it. 

After cloning/downloading this project, it will have an initial "bot_neural_network.p", so you won't need to train it again if you're just testing the game. But for the one wanting to watch the process of learning you can execute the previous steps.


