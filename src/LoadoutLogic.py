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
    def lineup(self):
        return self._lineup

    def clear(self):
        self._lineup = [None] * 10
        self.update_longest()

    def squish(self):
        units = [u for u in self._lineup if u is not None]
        self.clear()
        for u in units:
            self.modify(None, u, mode='add')

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
        units = [u for u in self._lineup if u is not None]
        new_longest = 0
        if len(units) > 0:
            new_longest = len(max(units, key=len))
        self._longest_len = new_longest

    def modify(self, idx, unit, *, mode='add') -> None:
        assert mode in {'add', 'remove'}, 'Invalid mode for method "modify()"'
        if mode == 'add':
            if idx is None:
                idx = self.next_empty_idx()
            if 1 <= idx <= 10:
                new_value = unit
                self._lineup[idx - 1] = new_value
        elif mode == 'remove':
            if idx is None:
                idx = self.last_unit_idx()
            if 1 <= idx <= 10:
                self._lineup[idx - 1] = None
        self.update_longest()