from src.LoadoutLogic import Loadout
from typing import List, Dict


def run() -> None:
    user_input = ''
    while user_input != 'quit':
        user_input = input('> ')
        execute(user_input)


def execute(full_cmd: str) -> None:
    cmd, opts, args = parse_cmd(full_cmd)
    match cmd:
        case 'add'|'place'|'touch':
            call_append(args)
        case 'insert'|'ins':
            call_modify(args, option='insert')
        case 'remove'|'rm':
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


def parse_cmd(s: str) -> List:
    s = s.strip().split(' ')

    command = None
    options = None
    arguments = None

    try:
        command = s[0]
        second_word = s[1]
        if second_word[0] == '-':
            options = list(second_word[1:])
            arguments = s[2:]
        else:
            arguments = s[1:]
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
    return [index, unit_name]


def call_append(args: List) -> None:
    idx, unit = parse_args_modify(args)
    result = loadout.append(idx, unit)
    if len(result) > 0:
        print(result)


def call_modify(args: List[str], *, option='add') -> None:
    idx, unit = args[-1], args[:-1]

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