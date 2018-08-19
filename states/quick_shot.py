from IAmHuman.state import State
from IAmHuman.util import *
from IAmHuman.game_values import Dimensions

from rlbot.agents.base_agent import SimpleControllerState


class QuickShot(State):
    def __init__(self):
        self.start = 0

    def debug_render(self, agent):
        agent.renderer.draw_line_3d(agent.me.location.data, agent.target_position.data,
                                    agent.renderer.create_color(255, 0, 0, 255))

    def activate(self, agent):
        pass

    def execute(self, agent):
        offset = (agent.ball.location.data[0] / Dimensions.FIELD_WIDTH) * 3.14
        x = agent.ball.location.data[0] + 100 * abs(math.cos(offset)) * sign(offset)
        y = agent.ball.location.data[1] + 100 * abs(math.sin(offset)) * sign(agent.team)
        agent.target_position = Vector3([x, y, agent.ball.location.data[2]])

        location = calc_local_vector(agent.target_position - agent.me.location, agent.me.rotation_matrix)
        angle_to_target = math.atan2(location.data[1], location.data[0])
        distance_to_target = distance2d(agent.me.location, agent.target_position)

        speed_correction = ((1 + abs(angle_to_target) ** 2) * 300)
        speed = 2000 - speed_correction + cap((distance_to_target / 16) ** 2, 0, speed_correction)

        if ball_ready(agent) and ball_project(agent) > 500 and abs(agent.ball.location.data[0]) < 3900:
            agent.brain.push_only('CalcShot')
        elif can_half_flip(agent, angle_to_target, distance_to_target):
            agent.brain.push_only("HalfFlip")
        elif can_power_slide(agent, angle_to_target):
            agent.brain.push_only("PowerSlide")
        elif distance2d(agent.me.location, agent.ball.location) < 400 and abs(angle_to_target) > 2:
            agent.brain.pop_only()

        return self.controller(agent, agent.target_position, speed)

    def controller(self, agent, target_location, target_speed):
        goal_local = calc_local_vector(
            Vector3([0, -sign(agent.team) * Dimensions.FIELD_LENGTH / 2, 100]) - agent.me.location,
            agent.me.rotation_matrix)
        goal_angle = math.atan2(goal_local.data[1], goal_local.data[0])

        location = calc_local_vector(target_location - agent.me.location, agent.me.rotation_matrix)
        controller_state = SimpleControllerState()
        angle_to_target = math.atan2(location.data[1], location.data[0])

        current_speed = velocity2d(agent.me.velocity)

        # steering
        controller_state.steer = steer(angle_to_target)

        # throttle
        if target_speed > 1400 and target_speed > current_speed and self.start > 2.5 and current_speed < 2250:
            controller_state.boost = True
        if target_speed > current_speed:
            controller_state.throttle = 1.0
        elif target_speed < current_speed:
            controller_state.throttle = 0

        # dodging
        time_difference = agent.game_info.seconds_elapsed - self.start
        if ball_ready(agent) and time_difference > 2.2 and distance2d(target_location, agent.me.location) <= 270:
            self.start = agent.game_info.seconds_elapsed
        elif time_difference <= 0.1:
            controller_state.jump = True
            controller_state.pitch = -1
        elif 0.1 <= time_difference <= 0.15:
            controller_state.jump = False
            controller_state.pitch = -1
        elif 0.15 < time_difference < 1:
            controller_state.jump = True
            controller_state.yaw = math.sin(goal_angle)
            controller_state.pitch = -abs(math.cos(goal_angle))

        return controller_state

    def terminate(self, agent):
        pass
