# Лабиринт сокровищ

Текстовая приключенческая игра на Python. Игрок исследует лабиринт, собирает предметы, решает загадки и пытается найти сокровище.

## Требования

- Python 3.11+
- Poetry

## Установка

```bash
make install
# или
poetry install
```

## Запуск

```bash
make project
# или
poetry run project
```

## Команды в игре

| Команда | Описание |
|---------|----------|
| `go <direction>` | Перейти в направлении (north/south/east/west) |
| `north/south/east/west` | Быстрое движение |
| `look` | Осмотреть текущую комнату |
| `take <item>` | Поднять предмет |
| `use <item>` | Использовать предмет |
| `inventory` | Показать инвентарь |
| `solve` | Решить загадку или открыть сундук |
| `help` | Показать справку |
| `quit` | Выход из игры |

## Структура проекта

```
project1_petrov_daniil_m25_555/
├── labyrinth_game/
│   ├── __init__.py
│   ├── main.py
│   ├── constants.py
│   ├── player_actions.py
│   └── utils.py
├── Makefile
├── README.md
├── pyproject.toml
├── poetry.lock
└── .gitignore
```

## Разработка

Линтинг кода:

```bash
make lint
```

## Демонстрация

Запись игровой сессии в файле `demo.cast`. Для просмотра:

```bash
asciinema play demo.cast
```

Или можно посмотреть онлайн

```bash
https://asciinema.org/a/qRDsgTTaHCa42X9y
```

## Автор

Петров Даниил М25-555