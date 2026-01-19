from typing import List
from src.LoadoutLogic import Loadout


def run() -> None:
    user_input = ''
    while user_input != 'quit':
        user_input = input('> ')
        execute(user_input)


def execute(full_cmd: str) -> None:
    cmd, opts, args = parse_cmd(full_cmd)
    match cmd:
        case 'add'|'append'|'place'|'touch':
            call_modify(args, mode='append')
        case 'insert'|'ins':
            call_modify(args, mode='insert')
        case 'remove'|'rm':
            call_modify(args, mode='remove')
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


def parse_cmd(s: str) -> List:
    s = s.strip().split(' ')

    command = None
    options = None
    arguments = None

    try:
        command = s[0]
        options = any(opt[0] == '-' for opt in s[1:])
        arguments = [arg for arg in s[1:] if arg[0] != '-']
    except IndexError:
        pass

    return [command, options, arguments]


def parse_args_modify(args: List) -> List:
    index = None
    unit_name = None

    if args is not None:
        try:
            index = int(args[-1])
            if len(args) > 1:
                unit_name = ' '.join(args[:-1])

        except ValueError:
            unit_name = ' '.join(args)

        except IndexError:
            pass

    return [index, unit_name]


def display_error(cmd: str, error: str) -> None:
    if len(error) > 0:
        print(f'Command "{cmd}" failed: {error}')


def call_modify(args: List, *, mode='append') -> None:
    idx, unit = parse_args_modify(args)

    e = ''
    if mode == 'append':
        e = loadout.append(idx, unit)

    elif mode == 'insert':
        e = loadout.insert(idx, unit)

    elif mode == 'remove':
        e = loadout.remove(idx, unit)

    display_error(mode, e)


loadout = Loadout()
run()