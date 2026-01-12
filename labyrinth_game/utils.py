# labyrinth_game/utils.py
from labyrinth_game.constants import ROOMS


def describe_current_room(game_state):
    """Вывести описание текущей комнаты."""
    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]

    print(f"\n== {current_room_name.upper()} ==")
    print(room['description'])

    if room['items']:
        items_list = ', '.join(room['items'])
        print(f"\nЗаметные предметы: {items_list}")

    exits_list = ', '.join(room['exits'].keys())
    print(f"Выходы: {exits_list}")

    if room['puzzle']:
        print("Кажется, здесь есть загадка (используйте команду solve).")
