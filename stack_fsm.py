from abc import ABC, abstractmethod


class StackFSM:
    def __init__(self):
        self.stack = []

    def update(self):
        cur_state = self.get_current_state()
        if cur_state is not None:
            cur_state.perform()

    def pop_and_push(self, new_state):
        self.get_current_state().terminate()
        self.stack.pop()

        if self.stack == []:
            self.stack.append(new_state)
        else:
            if self.get_current_state() != new_state:
                self.stack.append(new_state)

        new_state.activate()

    def pop_only(self):
        self.get_current_state().terminate()
        self.stack.pop()
        self.get_current_state().activate()

    def push_only(self, new_state):
        cur_state = self.get_current_state()

        if cur_state != new_state:
            if cur_state != None:
                cur_state.terminate()

            new_state.activate()
            self.stack.append(new_state)

    def get_current_state(self):
        if self.stack == []:
            return None
        else:
            return self.stack[-1]


class State(ABC):

    @abstractmethod
    def activate(self):
        pass

    @abstractmethod
    def perform(self):
        pass

    @abstractmethod
    def terminate(self):
        pass
