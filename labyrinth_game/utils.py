# labyrinth_game/utils.py
from labyrinth_game.constants import ROOMS


def describe_current_room(game_state):
    """Вывести описание текущей комнаты."""
    current_room_name = game_state["current_room"]
    room = ROOMS[current_room_name]

    print(f"\n== {current_room_name.upper()} ==")
    print(room["description"])

    if room["items"]:
        items_list = ", ".join(room["items"])
        print(f"\nЗаметные предметы: {items_list}")

    exits_list = ", ".join(room["exits"].keys())
    print(f"Выходы: {exits_list}")

    if room["puzzle"]:
        print("Кажется, здесь есть загадка (используйте команду solve).")


def solve_puzzle(game_state):
    """Попытаться решить загадку в текущей комнате."""
    from labyrinth_game.player_actions import get_input

    current_room_name = game_state["current_room"]
    room = ROOMS[current_room_name]

    if not room["puzzle"]:
        print("Загадок здесь нет.")
        return

    question, correct_answer = room["puzzle"]
    print(f"\n{question}")

    user_answer = get_input("Ваш ответ: ").strip().lower()
    correct_answer_lower = correct_answer.lower()

    if user_answer == correct_answer_lower:
        print("Верно! Загадка решена!")
        room["puzzle"] = None
        game_state["player_inventory"].append("treasure_key")
        print("Вы получили: treasure_key")
    else:
        print("Неверно. Попробуйте снова.")


def attempt_open_treasure(game_state):
    """Попытаться открыть сундук с сокровищами.

    Возвращает True если сундук открыт (победа).
    """
    from labyrinth_game.player_actions import get_input

    if "treasure_key" in game_state["player_inventory"]:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        ROOMS["treasure_room"]["items"].remove("treasure_chest")
        print("\n В сундуке сокровище! Вы победили!")
        return True

    response = get_input("Сундук заперт. Ввести код? (да/нет): ").strip().lower()

    if response == "да":
        code = get_input("Введите код: ").strip()
        room = ROOMS["treasure_room"]
        if room["puzzle"] and code == room["puzzle"][1]:
            print("Правильный код! Сундук открыт!")
            ROOMS["treasure_room"]["items"].remove("treasure_chest")
            print("\nВ сундуке сокровище! Вы победили!")
            return True
        else:
            print("Неверный код.")
            return False
    else:
        print("Вы отступаете от сундука.")
        return False


def show_help():
    """Показать доступные команды."""
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении "
          "(north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")

