from IAmHuman.state import State
from IAmHuman.util import *
from IAmHuman.mathf import *

from rlbot.agents.base_agent import SimpleControllerState


class PowerSlide(State):
    def __init__(self):
        self.angle_to_target = 0

    def debug_render(self, agent):
        agent.renderer.draw_line_3d(agent.me.location.data, agent.get_target_pos().data,
                                    agent.renderer.create_color(255, 0, 0, 255))
        agent.renderer.draw_rect_3d(agent.me.location.data, 150,
                                    20, True, agent.renderer.black())
        agent.renderer.draw_string_3d(agent.me.location.data, 1,
                                      1, str(self.angle_to_target), agent.renderer.white())

    def activate(self, agent):
        pass

    def execute(self, agent):
        local_target = calc_local_vector(agent.get_target_pos() - agent.me.location, agent.me.rotation_matrix)
        self.angle_to_target = math.atan2(local_target.data[1], local_target.data[0])

        if agent.me.has_wheel_contact is False or (
                -0.3 <= self.angle_to_target <= 0.3 and -0.7 <= agent.me.angular_velocity.data[2] <= 0.7):
            agent.brain.pop_only()

        return self.controller(agent, self.angle_to_target)

    def controller(self, agent, angle):
        controller_state = SimpleControllerState()

        steer_value = steer(angle)
        controller_state.steer = steer_value
        controller_state.throttle = 1
        controller_state.handbrake = True

        balance_threshold = 0.25 * abs(agent.me.angular_velocity.data[2]) ** 2 + 0.05

        if balance_threshold * -1 <= angle <= balance_threshold:
            controller_state.handbrake = False
            controller_state.boost = True
            if abs(agent.me.angular_velocity.data[2]) >= 0.15:
                controller_state.steer = sign(agent.me.angular_velocity.data[2]) * -1
            else:
                controller_state.steer = 0

        return controller_state

    def terminate(self, agent):
        pass
