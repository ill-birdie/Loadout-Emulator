from typing import List, Optional

def same_parity(n1: int, n2: int) -> bool:
    return (n1 % 2 == 0) == (n2 % 2 == 0)

class Loadout:
    def __init__(self):
        self._lineup: List[Optional[str]] = [None] * 10
        self._longest_len = 0

    def tile(self, unit) -> str:
        total_spaces = self._longest_len
        tile: str
        if unit is not None:
            unit_len = len(unit)
            side_spaces = (total_spaces - unit_len) // 2
            spaces = ' ' * side_spaces
            extra_space = ''
            if not same_parity(total_spaces, unit_len):
                extra_space = ' '
            tile = f'[ {spaces}{unit}{spaces}{extra_space} ]'
        else:
            spaces = ' ' * total_spaces
            tile = f'[ {spaces} ]'
        return tile

    def __str__(self) -> str:
        result = ''
        for idx, unit in enumerate(self._lineup, start=1):
            result += self.tile(unit) + ' '
            if idx == 5:
                result += '\n'
        return result

    @property
    def lineup(self) -> List[str]:
        return self._lineup


    def units(self) -> List[str]:
        return [unit for unit in self._lineup if unit is not None]

    def num_units(self) -> int:
        return len(self.units())


    def clear(self) -> None:
        self._lineup = [None] * 10
        self.update_longest()

    def fill(self) -> None:
        for i in range(1, 11):
            self.append(None, str(i))
        self.update_longest()

    def squish(self) -> None:
        units = self.units()
        self.clear()
        for unit in units:
            self.append(None, unit)


    def index(self, unit: str) -> int:
        return self._lineup.index(unit) + 1

    def next_empty_idx(self) -> int:
        try:
            return self._lineup.index(None) + 1
        except ValueError:
            return -1

    def last_unit_idx(self) -> int:
        for idx, unit in enumerate(self._lineup[::-1]):
            if unit is not None:
                return len(self._lineup) - idx
        return -1

    def valid_index(self, idx: int) -> bool:
        return 1 <= idx <= len(self._lineup)


    def update_longest(self) -> None:
        units = self.units()
        new_longest = 0
        if len(units) > 0:
            new_longest = len(max(units, key=len))
        self._longest_len = new_longest


    def append(self, idx, unit) -> str:
        next_open = self.next_empty_idx()
        has_next = (next_open != -1)

        if idx is None:
            idx = next_open

        error_msg = ''
        match (unit, has_next):
            case (None, _):
                error_msg = 'missing unit'

            case (_, _) if not self.valid_index(idx):
                error_msg = f'invalid index ({idx})'

            case (_, False):
                error_msg = 'no space to append unit'

            case _:
                self._lineup.pop(next_open - 1)
                self._lineup.insert(idx - 1, unit)

        self.update_longest()
        return error_msg


    def insert(self, idx, unit) -> str:
        error_msg = ''
        match (idx, unit):
            case (None, None):
                error_msg = 'missing index, unit'

            case (None, _):
                error_msg = 'missing index'

            case (_, None):
                error_msg = 'missing unit'

            case (_, _) if not self.valid_index(idx):
                error_msg = f'invalid index: {idx}'

            case _:
                self._lineup.pop(idx - 1)
                self._lineup.insert(idx - 1, unit)

        self.update_longest()
        return error_msg


    def remove(self, idx, unit) -> str:
        error_msg = ''
        valid_unit = unit in self.units()
        match (idx, unit, valid_unit):
            case (None, None, _):
                idx = self.last_unit_idx()

            case (None, unit, True) if unit is not None:
                idx = self.index(unit)

            case (_, _, False) if unit is not None:
                error_msg = f'{unit} does not exist in loadout'

            case (idx, unit, _) if (idx is not None) and (unit is not None):
                error_msg = f'too many arguments: "{idx}" and "{unit}"'

        if not len(error_msg) > 1 and self.valid_index(idx):
            self._lineup[idx - 1] = None
            self.update_longest()

        return error_msg