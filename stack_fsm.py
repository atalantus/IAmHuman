from abc import ABC, abstractmethod


class StackFSM:
    def __init__(self):
        self.stack = []
        self.agent = None

    def update(self, agent):
        self.agent = agent

        cur_state = self.get_current_state()
        if cur_state is not None:
            return cur_state.execute(self.agent)
        else:
            return None

    def pop_and_push(self, new_state):
        self.get_current_state().terminate(self.agent)
        self.stack.pop()

        if self.stack == []:
            self.stack.append(new_state)
        else:
            if self.get_current_state() != new_state:
                self.stack.append(new_state)

        new_state.activate(self.agent)

    def pop_only(self):
        self.get_current_state().terminate(self.agent)
        self.stack.pop()
        self.get_current_state().activate(self.agent)

    def push_only(self, new_state):
        cur_state = self.get_current_state()

        if cur_state != new_state:
            if cur_state != None:
                cur_state.terminate(self.agent)

            new_state.activate(self.agent)
            self.stack.append(new_state)

    def get_current_state(self):
        if self.stack == []:
            return None
        else:
            return self.stack[-1]


class State(ABC):

    @abstractmethod
    def activate(self, agent):
        pass

    @abstractmethod
    def execute(self, agent):
        pass

    @abstractmethod
    def terminate(self, agent):
        pass

    @abstractmethod
    def debug_render(self, agent):
        pass
