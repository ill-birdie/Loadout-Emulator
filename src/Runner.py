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


def parse_args(args: List[str]) -> list:
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
        except ValueError:
            unit = ' '.join(args)
    return [idx, unit]


def call_modify(args: List[str], *, option='add') -> None:
    idx, unit = parse_args(args)

    exception = None


    if option == 'add':
        full_loadout = loadout.num_units() == len(loadout.lineup)
        match (full_loadout, idx, unit):
            case (True, _, _):
                exception = 'attempted to append unit to full loadout'

            case (_, None, None):
                exception = 'missing index, unit'

            case (_, idx, None) if idx is not None:
                exception = 'missing unit'

            case _:
                exception = None


    elif option == 'insert':
        missing = []
        if idx is None:
            missing.append('index')

        if unit is None:
            missing.append('unit')

        if len(missing) > 0:
            exception = f'missing {', '.join(missing)}'


    elif option == 'remove':
        if (idx is None) and (unit not in loadout.lineup):
            exception = 'unit does not exist in lineup'


    if exception is not None:
        print(f'Command "{option}" failed: {exception}')
        return
    loadout.modify(idx, unit, mode=option)


loadout = Loadout()
run()