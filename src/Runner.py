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
            call_add(args)
        case 'remove'|'rm':
            args = full_cmd[1:]
        case 'squish':
            loadout.squish()
        case 'clear':
            loadout.clear()
        case 'print' | 'display' | 'show' | 'ls':
            pass
        case 'quit':
            print("Exiting. Final loadout:")
        case _:
            print(f'Unknown command: "{cmd}"')
    print(loadout)


def call_add(args: List[str]):
    loadout_len = len(loadout.lineup)
    try:
        idx = int(args[-1])
        if 1 <= idx <= loadout_len:
            unit = ' '.join(args[:-1])
            loadout.modify(idx, unit, mode='add')
        else:
            print(f"Invalid index: {idx} (must be 1-{loadout_len})")
    except IndexError:
        print("Missing argument: unit")
    except ValueError:
        idx = None
        unit = ' '.join(args)
        loadout.modify(idx, unit, mode='add')


loadout = Loadout()
run()