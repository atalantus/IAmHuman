import time

from IAmHuman.state import State
from IAmHuman.mathf import *

from rlbot.agents.base_agent import SimpleControllerState


class Testing(State):
    def debug_render(self, agent):
        pass

    def activate(self, agent):
        pass

    def execute(self, agent):
        controller_state = SimpleControllerState()

        return controller_state

    def terminate(self, agent):
        pass
