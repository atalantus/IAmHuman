from IAmHuman.states.testing import *
from IAmHuman.states.atba import *
from IAmHuman.states.calc_shot import *
from IAmHuman.states.quick_shot import *
from IAmHuman.states.half_flip import *
from IAmHuman.states.power_slide import PowerSlide


class StackFSM:
    def __init__(self):
        self.stack = []
        self.agent = None
        self.states = {
            "Testing": Testing(),
            "ATBA": ATBA(),
            "CalcShot": CalcShot(),
            "QuickShot": QuickShot(),
            "HalfFlip": HalfFlip(),
            "PowerSlide": PowerSlide()
        }

    def update(self, agent):
        self.agent = agent

        cur_state = self.get_current_state()
        if cur_state is not None:
            return cur_state.execute(self.agent)
        else:
            return None

    def pop_and_push(self, new_state_id):
        new_state = self.states[new_state_id]

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
        cur_state = self.get_current_state()
        if cur_state is not None:
            self.get_current_state().activate(self.agent)

    def push_only(self, new_state_id):
        new_state = self.states[new_state_id]

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
