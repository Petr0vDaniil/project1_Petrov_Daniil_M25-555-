#!/usr/bin/env python3

from labyrinth_game.player_actions import get_input
from labyrinth_game.utils import describe_current_room


def main():
    game_state = {
        'player_inventory': [],
        'current_room': 'entrance',
        'game_over': False,
        'steps_taken': 0
    }

    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)

    while not game_state['game_over']:
        command = get_input("\n> ")
        if command.lower() == 'quit':
            game_state['game_over'] = True


if __name__ == "__main__":
    main()
