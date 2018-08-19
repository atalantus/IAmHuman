from IAmHuman.state import State
from IAmHuman.mathf import *

from rlbot.agents.base_agent import SimpleControllerState


class ATBA(State):
    def __init__(self):
        self.start = 0

    def debug_render(self, agent):
        pass

    def activate(self, agent):
        pass

    def execute(self, agent):
        target_object = agent.ball
        agent.target_position = target_object.location
        target_speed = velocity2d(agent.ball.velocity) + (distance2d(agent.ball.location, agent.me.location) / 1.5)

        return self.controller(target_object, target_speed, agent)

    def controller(self, target_object, target_speed, agent):
        location = target_object.local_location
        controller_state = SimpleControllerState()
        angle_to_ball = math.atan2(location.data[1], location.data[0])

        current_speed = velocity2d(agent.me.velocity)
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
            if target_speed > 1400 and self.start > 2.2 and current_speed < 2250:
                controller_state.boost = True
        elif target_speed < current_speed:
            controller_state.throttle = 0

        # dodging
        time_difference = agent.game_info.seconds_elapsed - self.start
        if time_difference > 2.2 and distance2d(target_object.location, agent.me.location) > 1000 and abs(
                angle_to_ball) < 1.3:
            self.start = agent.game_info.seconds_elapsed
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
