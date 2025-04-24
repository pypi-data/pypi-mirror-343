from typing import List, Dict, Callable

from cyanprintsdk.domain.core.deterministic import IDeterminism


class StatelessDeterminism(IDeterminism):
    def __init__(self, states: List[Dict[str, str]], pointer: int):
        self.states = states
        self._pointer = pointer  # Treat _pointer as a private variable

    def get(self, key: str, origin: Callable[[], str]) -> str:
        if self._pointer + 1 >= len(self.states):
            raise RuntimeError("NullReferenceException")

        states = self.states[self._pointer + 1]
        state = states.get(key)

        if state is not None:
            return state

        val = origin()
        states[key] = val
        return val
