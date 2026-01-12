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
