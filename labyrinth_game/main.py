#!/usr/bin/env python3

from labyrinth_game.player_actions import (
    get_input,
    use_item,
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    show_help,
    solve_puzzle,
)


def process_command(game_state, command):
    """Обработать команду пользователя."""
    from labyrinth_game.player_actions import (
        move_player,
        show_inventory,
        take_item,
    )
    from labyrinth_game.utils import describe_current_room

    parts = command.strip().split(maxsplit=1)
    if not parts:
        return True

    cmd = parts[0].lower()
    arg = parts[1].lower() if len(parts) > 1 else None

    match cmd:
        case 'look':
            describe_current_room(game_state)
        case 'inventory':
            show_inventory(game_state)
        case 'go':
            if not arg:
                print("Укажите направление (north/south/east/west).")
            else:
                move_player(game_state, arg)
        case "take":
            if not arg:
                print("Укажите предмет для поднятия.")
            else:
                take_item(game_state, arg)
        case "use":
            if not arg:
                print("Укажите предмет для использования.")
            else:
                use_item(game_state, arg)
        case "solve":
            if game_state["current_room"] == "treasure_room":
                if attempt_open_treasure(game_state):
                    return False
            else:
                solve_puzzle(game_state)
        case "help":
            show_help()
        case "quit" | "exit":
            return False
        case _:
            print(
                f"Неизвестная команда: {cmd}. "
                "Введите 'help' для справки."
            )

    return True


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
        command_line = get_input("\n> ")
        result = process_command(game_state, command_line)
        if result is False:
            game_state['game_over'] = True


if __name__ == "__main__":
    main()
