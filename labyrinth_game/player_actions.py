# labyrinth_game/player_actions.py

def show_inventory(game_state):
    """Показать инвентарь игрока."""
    inventory = game_state['player_inventory']
    if inventory:
        items_list = ', '.join(inventory)
        print(f"\nИнвентарь: {items_list}")
    else:
        print("\nИнвентарь пуст.")


def get_input(prompt="> "):
    """Получить ввод от пользователя."""
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def move_player(game_state, direction):
    """Переместить игрока в указанном направлении."""
    from labyrinth_game.constants import ROOMS
    from labyrinth_game.utils import describe_current_room

    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]

    if direction not in room['exits']:
        print("Нельзя пойти в этом направлении.")
        return

    new_room_name = room['exits'][direction]
    game_state['current_room'] = new_room_name
    game_state['steps_taken'] += 1

    describe_current_room(game_state)


def take_item(game_state, item_name):
    """Взять предмет из комнаты."""
    from labyrinth_game.constants import ROOMS

    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]

    if item_name not in room['items']:
        print("Такого предмета здесь нет.")
        return

    game_state['player_inventory'].append(item_name)
    room['items'].remove(item_name)
    print(f"Вы подняли: {item_name}")


def use_item(game_state, item_name):
    """Использовать предмет из инвентаря."""
    if item_name not in game_state['player_inventory']:
        print("У вас нет такого предмета.")
        return

    if item_name == 'torch':
        print("Факел озаряет всё вокруг. Становится светлее!")
    elif item_name == 'sword':
        print(
            "Вы берёте меч в руку. "
            "Чувствуете уверенность и силу!"
        )
    elif item_name == 'bronze_box':
        print("Вы открываете бронзовую шкатулку...")
        if 'rusty_key' not in game_state['player_inventory']:
            game_state['player_inventory'].append('rusty_key')
            print("Внутри вы находите ржавый ключ!")
        else:
            print("Шкатулка пуста.")
    else:
        print(f"Вы не знаете, как использовать {item_name}.")
