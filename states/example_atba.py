import time

from stack_fsm import State
from mathf import *

from rlbot.agents.base_agent import SimpleControllerState


class ATBAState(State):
    def activate(self, agent):
        pass

    def execute(self, agent):
        target_location = agent.ball
        target_speed = velocity2D(agent.ball) + (distance2D(agent.ball, agent.me) / 1.5)

        return self.exampleController(target_location, target_speed, agent)

    def exampleController(self, target_object, target_speed, agent):
        location = target_object.local_location
        controller_state = SimpleControllerState()
        angle_to_ball = math.atan2(location.data[1], location.data[0])

        current_speed = velocity2D(agent.me)
        # steering
        if angle_to_ball > 0.1:
            controller_state.steer = controller_state.yaw = 1
        elif angle_to_ball < -0.1:
            controller_state.steer = controller_state.yaw = -1
        else:
            controller_state.steer = controller_state.yaw = 0

        # throttle
        if target_speed > current_speed:
            controller_state.throttle = 1.0
            if target_speed > 1400 and agent.start > 2.2 and current_speed < 2250:
                controller_state.boost = True
        elif target_speed < current_speed:
            controller_state.throttle = 0

        # dodging
        time_difference = time.time() - agent.start
        if time_difference > 2.2 and distance2D(target_object.location, agent.me.location) > 1000 and abs(
                angle_to_ball) < 1.3:
            agent.start = time.time()
        elif time_difference <= 0.1:
            controller_state.jump = True
            controller_state.pitch = -1
        elif 0.1 <= time_difference <= 0.15:
            controller_state.jump = False
            controller_state.pitch = -1
        elif 0.15 < time_difference < 1:
            controller_state.jump = True
            controller_state.yaw = controller_state.steer
            controller_state.pitch = -1

        return controller_state

    def terminate(self, agent):
        pass
