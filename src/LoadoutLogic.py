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
            self.modify(None, str(i), mode='add')
        self.update_longest()

    def squish(self) -> None:
        units = self.units()
        self.clear()
        for unit in units:
            self.modify(None, unit, mode='add')

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

    def update_longest(self) -> None:
        units = self.units()
        new_longest = 0
        if len(units) > 0:
            new_longest = len(max(units, key=len))
        self._longest_len = new_longest

    def modify(self, idx, unit, *, mode='add') -> None:
        assert mode in {'add', 'insert', 'remove'}, f'Invalid mode for method "modify()": {mode}'
        assert idx is None or 1 <= idx <= len(self._lineup), f'Invalid index: {idx} (must be in range 1-{len(self._lineup)})'
        if mode == 'add':
            next_open = self.next_empty_idx()
            if idx is None:
                idx = next_open

            if (unit is not None) and (next_open != -1):
                self._lineup.pop(next_open - 1)
                self._lineup.insert(idx - 1, unit)


        elif mode == 'insert':
            if idx is not None:
                self._lineup.pop(idx - 1)
                self._lineup.insert(idx - 1, unit)


        elif mode == 'remove':
            match (idx, unit):
                case (None, None):
                    idx = self.last_unit_idx()

                case (None, unit) if unit is not None:
                    if unit in self._lineup:
                        idx = self.index(unit)
                    else:
                        return
            self._lineup[idx - 1] = None
        self.update_longest()