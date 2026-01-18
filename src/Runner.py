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
            call_remove(args)
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


def invalid_index_message(idx: int, max_idx: int) -> str:
    return f'Invalid index: {idx} (must be 1-{max_idx})'


def call_add(args: List[str]) -> None:
    loadout_len = len(loadout.lineup)
    try:
        idx = int(args[-1])
        if 1 <= idx <= loadout_len:
            unit = ' '.join(args[:-1])
            loadout.modify(idx, unit, mode='add')
        else:
            print(invalid_index_message(idx, loadout_len))
    except IndexError:
        print("Missing argument: unit")
    except ValueError:
        idx = None
        unit = ' '.join(args)
        loadout.modify(idx, unit, mode='add')


def call_remove(args: List[str]) -> None:
    loadout_len = len(loadout.lineup)
    has_valid_idx = False
    has_unit = False
    if len(args) >= 1:
        try:
            idx = int(args[-1])
            # Command has index
            if 1 <= idx <= loadout_len:
                # Command has valid index
                has_valid_idx = True
                if len(args) > 1:
                    # Command has valid index and unit
                    has_unit = True
            else:
                print(invalid_index_message(idx, loadout_len))
                return
        except ValueError:
            # Command only has unit
            has_unit = True
    idx = None
    unit = None
    if has_valid_idx:
        idx = int(args[-1])
    if has_unit:
        unit = ' '.join(args)
    loadout.modify(idx, unit, mode='remove')


loadout = Loadout()
run()