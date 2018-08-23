from IAmHuman.state import State
from IAmHuman.mathf import *
from IAmHuman.util import *
from IAmHuman.state_transitions import *

from rlbot.agents.base_agent import SimpleControllerState


class Testing(State):
    def __init__(self):
        self.start = 0
        self.time_difference = 0

    def debug_render(self, agent):
        pass

    def activate(self, agent):
        self.start = agent.game_info.seconds_elapsed
        self.time_difference = 0

    def execute(self, agent):
        controller_state = SimpleControllerState()

        self.time_difference = agent.game_info.seconds_elapsed - self.start

        if self.time_difference >= 3 and can_power_slide(agent, 3):
            agent.brain.push_only("PowerSlide")

        controller_state.throttle = 1
        cur_speed = velocity2d(agent.me.velocity)

        if cur_speed < 3400:
            controller_state.boost = True

        return controller_state

    def terminate(self, agent):
        pass
