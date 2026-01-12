# labyrinth_game/player_actions.py
"""Функции для управления действиями и состоянием игрока.

Содержит функции для взаимодействия с инвентарём, перемещения,
использования предметов и получения пользовательского ввода.
"""


def get_input(prompt="> "):
    """Получить ввод от пользователя с обработкой ошибок.

    Безопасно читает пользовательский ввод и обрабатывает прерывание
    (Ctrl+C) и конец потока ввода (Ctrl+D).

    Args:
        prompt (str): Строка приглашения для вывода. По умолчанию "> ".

    Returns:
        str: Введённая строка или "quit" в случае прерывания.

    Side Effects:
        - Выводит приглашение в консоль
        - При прерывании выводит "Выход из игры."
    """
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def show_inventory(game_state):
    """Показать инвентарь игрока.

    Выводит список предметов в инвентаре или сообщение о пустом инвентаре.

    Args:
        game_state (dict): Словарь состояния игры с ключом 'player_inventory'.

    Side Effects:
        - Выводит инвентарь в консоль
    """
    inventory = game_state["player_inventory"]
    if inventory:
        items_list = ", ".join(inventory)
        print(f"\nИнвентарь: {items_list}")
    else:
        print("\nИнвентарь пуст.")


def move_player(game_state, direction):
    """Переместить игрока в указанном направлении.

    Проверяет наличие выхода в данном направлении и переводит игрока
    в соседнюю комнату. Перед treasure_room проверяет наличие rusty_key.
    После перемещения генерирует случайное событие.

    Args:
        game_state (dict): Словарь состояния игры.
        direction (str): Направление (north, south, east, west).

    Side Effects:
        - Выводит сообщения об ошибке или успехе
        - Обновляет текущую комнату и счётчик шагов
        - Вызывает describe_current_room()
        - Вызывает random_event()
    """
    from labyrinth_game.constants import ROOMS
    from labyrinth_game.utils import (
        describe_current_room,
        random_event,
    )

    current_room_name = game_state["current_room"]
    room = ROOMS[current_room_name]

    if direction not in room["exits"]:
        print("Нельзя пойти в этом направлении.")
        return

    new_room_name = room["exits"][direction]

    if new_room_name == "treasure_room":
        if "rusty_key" not in game_state["player_inventory"]:
            print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
            return
        else:
            print(
                "Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ."
            )

    game_state["current_room"] = new_room_name
    game_state["steps_taken"] += 1

    describe_current_room(game_state)
    random_event(game_state)


def take_item(game_state, item_name):
    """Взять предмет из текущей комнаты.

    Добавляет предмет в инвентарь игрока и удаляет его из комнаты.
    Не позволяет поднять слишком тяжелые предметы (treasure_chest).

    Args:
        game_state (dict): Словарь состояния игры.
        item_name (str): Название предмета.

    Side Effects:
        - Выводит сообщение об успехе или ошибке
        - Может добавить предмет в инвентарь
        - Может удалить предмет из комнаты
    """
    from labyrinth_game.constants import ROOMS

    current_room_name = game_state["current_room"]
    room = ROOMS[current_room_name]

    if item_name == "treasure_chest":
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return

    if item_name not in room["items"]:
        print("Такого предмета здесь нет.")
        return

    game_state["player_inventory"].append(item_name)
    room["items"].remove(item_name)
    print(f"Вы подняли: {item_name}")


def use_item(game_state, item_name):
    """Использовать предмет из инвентаря.

    Выполняет уникальное действие для каждого предмета:
        - torch: озаряет комнату
        - sword: вселяет уверенность
        - bronze_box: открывает шкатулку и выдаёт ключ
        - other: выводит сообщение о неизвестном использовании

    Args:
        game_state (dict): Словарь состояния игры.
        item_name (str): Название предмета.

    Side Effects:
        - Выводит сообщение о результате
        - Может добавить предмет в инвентарь (bronze_box)
    """
    if item_name not in game_state["player_inventory"]:
        print("У вас нет такого предмета.")
        return

    if item_name == "torch":
        print("Факел озаряет всё вокруг. Становится светлее!")
    elif item_name == "sword":
        print("Вы берёте меч в руку. Чувствуете уверенность и силу!")
    elif item_name == "bronze_box":
        print("Вы открываете бронзовую шкатулку...")
        if "rusty_key" not in game_state["player_inventory"]:
            game_state["player_inventory"].append("rusty_key")
            print("Внутри вы находите ржавый ключ!")
        else:
            print("Шкатулка пуста.")
    else:
        print(f"Вы не знаете, как использовать {item_name}.")
