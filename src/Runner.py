from src.LoadoutLogic import Loadout
from typing import List

def run() -> None:
    user_input = ''
    while user_input != 'quit':
        user_input = input('> ')
        execute(user_input)

def execute(full_cmd: str) -> None:
    full_cmd = full_cmd.strip().split(' ')
    cmd = full_cmd[0]
    match cmd:
        case 'add'|'insert'|'place'|'touch':
            args = full_cmd[1:]
            add(args)
            print(loadout)
        case 'print'|'display'|'show'|'ls':
            print(loadout)
        case 'quit':
            print('Exiting')
        case _:
            print(f'Unknown command: "{cmd}"')

def add(args: List) -> None:
    try:
        idx = int(args[-1])
        if not 1 <= idx <= 10:
            raise ValueError
        unit = ' '.join(args[:-1])
        loadout.add(idx, unit)
    except ValueError:
        unit = ' '.join(args)
        loadout.add(None, unit)

loadout = Loadout()
run()