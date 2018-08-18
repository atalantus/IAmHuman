import time
import math

from IAmHuman.state import State
from IAmHuman.mathf import *

from rlbot.agents.base_agent import SimpleControllerState


class HalfFlip(State):
    def __init__(self):
        self.time_difference = 0
        self.step1 = 0.1 * 1.65
        self.step2 = 0.15 * 1.65
        self.step3 = 0.35 * 1.65
        self.step4 = 0.4 * 1.65
        self.step401 = 0.45 * 1.65
        self.step5 = 1.75 * 1.65
        self.step501 = 1 * 1.65

    def debug_render(self, agent):
        agent.renderer.draw_rect_3d(agent.me.location.data, 150,
                                    20, True, agent.renderer.black())
        agent.renderer.draw_string_3d(agent.me.location.data, 1,
                                      1, str(self.time_difference), agent.renderer.white())

    def activate(self, agent):
        pass

    def execute(self, agent):
        # return SimpleControllerState()
        return self.controller(agent)

    def controller(self, agent):
        controller_state = SimpleControllerState()

        controller_state.pitch = 1

        # throttle
        controller_state.throttle = -1

        # dodging
        self.time_difference = time.time() - agent.start
        if self.time_difference > 7:
            agent.start = time.time()
        elif self.time_difference <= self.step1:
            controller_state.jump = True
        elif self.step1 <= self.time_difference <= self.step2:
            controller_state.jump = False
        elif self.step2 <= self.time_difference <= self.step3:
            controller_state.jump = True
        elif self.step4 <= self.time_difference <= self.step5:
            controller_state.pitch = -1
        elif self.step5 <= self.time_difference:
            controller_state.throttle = -0.25

        if self.step401 <= self.time_difference <= self.step501:
            controller_state.boost = True
            controller_state.roll = 1
            controller_state.yaw = .75

        return controller_state

    def terminate(self, agent):
        pass
