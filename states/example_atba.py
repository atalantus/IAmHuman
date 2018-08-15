from stack_fsm import State
from mathf import *


class ATBAState(State):
    def activate(self, agent):
        pass

    def execute(self, agent):
        target_location = agent.ball
        target_speed = velocity2D(agent.ball) + (distance2D(agent.ball, agent.me) / 1.5)

        return agent.exampleController(target_location, target_speed)

    def terminate(self, agent):
        pass
