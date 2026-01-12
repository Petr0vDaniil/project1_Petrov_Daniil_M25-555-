# labyrinth_game/utils.py
import math

EVENT_PROBABILITY = 10
EVENT_TYPES_COUNT = 3
TRAP_DAMAGE_THRESHOLD = 3
TRAP_DAMAGE_RANGE = 10

def describe_current_room(game_state):
    """Вывести описание текущей комнаты."""
    from labyrinth_game.constants import ROOMS

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
    from labyrinth_game.constants import ROOMS
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

    answer_variants = {
        "10": ["10", "десять"],
        "шаг шаг шаг": ["шаг шаг шаг"],
        "резонанс": ["резонанс"],
        "луна": ["луна"],
        "молчание": ["молчание"],
    }

    is_correct = False
    for variants_list in answer_variants.values():
        if user_answer in [v.lower() for v in variants_list]:
            if correct_answer_lower in [v.lower() for v in variants_list]:
                is_correct = True
                break

    if is_correct:
        print("✓ Верно! Загадка решена!")
        room["puzzle"] = None

        if current_room_name == "trap_room":
            game_state["player_inventory"].append("treasure_key")
            print("Вы получили: treasure_key")
        elif current_room_name == "hall":
            game_state["player_inventory"].append("treasure_key")
            print("Вы получили: treasure_key")
        elif current_room_name == "library":
            game_state["player_inventory"].append("treasure_key")
            print("Вы получили: treasure_key")
        elif current_room_name == "crystal_chamber":
            game_state["player_inventory"].append("crystal_key")
            print("Вы получили: crystal_key")
        elif current_room_name == "underground_river":
            game_state["player_inventory"].append("artifact_key")
            print("Вы получили: artifact_key")
    else:
        print("✗ Неверно. Попробуйте снова.")
        if current_room_name == "trap_room":
            trigger_trap(game_state)


def attempt_open_treasure(game_state):
    """Попытаться открыть сундук с сокровищами.

    Возвращает True если сундук открыт (победа).
    """
    from labyrinth_game.constants import ROOMS
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
    from labyrinth_game.constants import COMMANDS

    print("\nДоступные команды:")
    for command, description in COMMANDS.items():
        print(f"  {command:<16} - {description}")


def pseudo_random(seed, modulo):
    """Генерировать псевдослучайное число на основе синуса.

    Args:
        seed: целое число (например, количество шагов)
        modulo: диапазон результата [0, modulo)

    Returns:
        целое число в диапазоне [0, modulo)
    """
    sin_value = math.sin(seed * 12.9898)
    stretched = sin_value * 43758.5453
    fractional_part = stretched - math.floor(stretched)
    result = fractional_part * modulo
    return int(result)


def trigger_trap(game_state):
    """Имитировать срабатывание ловушки."""
    print("Ловушка активирована! Пол стал дрожать...")

    inventory = game_state['player_inventory']

    if inventory:
        random_index = pseudo_random(
            game_state['steps_taken'],
            len(inventory)
        )
        lost_item = inventory.pop(random_index)
        print(f"Вы потеряли: {lost_item}")
    else:
        random_damage = pseudo_random(
            game_state['steps_taken'],
            TRAP_DAMAGE_RANGE
        )
        if random_damage < TRAP_DAMAGE_THRESHOLD:
            print("Ловушка нанесла смертельный урон! Вы погибли!")
            game_state['game_over'] = True
        else:
            print("Вам удалось избежать опасности!")



def random_event(game_state):
    """Генерировать случайное событие при перемещении."""
    from labyrinth_game.constants import ROOMS
    event_chance = pseudo_random(game_state['steps_taken'], EVENT_PROBABILITY)

    if event_chance != 0:
        return

    event_type = pseudo_random(game_state['steps_taken'] + 1, EVENT_TYPES_COUNT)

    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]

    if event_type == 0:
        print("\n✨ Вы нашли монетку на полу!")
        room['items'].append('coin')
    elif event_type == 1:
        print("\n🎵 Вы слышите странный шорох...")
        if 'sword' in game_state['player_inventory']:
            print("Вы отпугиваете существо своим мечом!")
    elif event_type == 2:
        if (current_room_name == 'trap_room' and
                'torch' not in game_state['player_inventory']):
            print("\n⚠️  Опасность! Вы активировали ловушку!")
            trigger_trap(game_state)
