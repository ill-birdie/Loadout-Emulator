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
        case 'add'|'place'|'touch':
            args = full_cmd[1:]
            call_modify(args, option='add')
        case 'insert'|'ins':
            args = full_cmd[1:]
            call_modify(args, option='insert')
        case 'remove'|'rm':
            args = full_cmd[1:]
            call_modify(args, option='remove')
        case 'fill':
            loadout.fill()
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


def call_modify(args: List[str], *, option='add') -> None:
    idx = None
    unit = None
    if len(args) >= 1:
        try:
            idx = int(args[-1])
            if 1 <= idx <= len(loadout.lineup):
                if len(args) > 1:
                    unit = ' '.join(args[:-1])
            else:
                print(f'Invalid index: {idx} (must be in range 1-{len(loadout.lineup)})')
                return
        except ValueError:
            unit = ' '.join(args)
    exception = ''
    if option == 'add':
        full_loadout = loadout.num_units() == len(loadout.lineup)
        if full_loadout and (idx is None) and (unit is not None):
            exception = 'attempted to append unit to full loadout'
        elif (idx is None) and (unit is None):
            exception = 'missing index, unit'
        elif (idx is not None) and (unit is None):
            exception = 'missing unit'
    elif option == 'remove':
        if (idx is None) and (unit not in loadout.lineup):
            exception = 'unit does not exist in lineup'
    if len(exception) != 0:
        print(f'Command "{option}" failed: {exception}')
        return
    loadout.modify(idx, unit, mode=option)


loadout = Loadout()
run()