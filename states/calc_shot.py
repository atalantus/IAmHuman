from IAmHuman.state import State
from IAmHuman.state_transitions import *
from IAmHuman.game_values import Dimensions

from rlbot.agents.base_agent import SimpleControllerState


class CalcShot(State):
    def __init__(self):
        self.goal = Vector3([0, 0, 0])

    def debug_render(self, agent):
        agent.renderer.draw_line_3d(self.goal.data, agent.ball.location.data,
                                    agent.renderer.create_color(255, 255, 0, 0))
        agent.renderer.draw_line_3d(agent.me.location.data, agent.get_target_pos().data,
                                    agent.renderer.create_color(255, 0, 0, 255))

    def activate(self, agent):
        pass

    def execute(self, agent):
        self.goal = Vector3([0, -sign(agent.team) * Dimensions.FIELD_LENGTH / 2, 100])
        goal_to_ball = (agent.ball.location - self.goal).normalize()

        goal_to_agent = (agent.me.location - self.goal).normalize()
        difference = goal_to_ball - goal_to_agent
        error = cap(abs(difference.data[0]) + abs(difference.data[1]), 1, 10)

        target_distance = (100 + distance2d(agent.ball.location, agent.me.location) * (error ** 2)) / 1.95
        agent.target = agent.ball.location + Vector3(
            [goal_to_ball.data[0] * target_distance, goal_to_ball.data[1] * target_distance, 0])
        agent.get_target_pos().data[0] = cap(agent.get_target_pos().data[0], -4120, 4120)

        target_local = calc_local_vector(agent.get_target_pos() - agent.me.location, agent.me.rotation_matrix)
        angle_to_target = math.atan2(target_local.data[1], target_local.data[0])
        distance_to_target = distance2d(agent.me.location, agent.get_target_pos())
        speed_correction = ((1 + abs(angle_to_target) ** 2) * 300)
        speed = 2300 - speed_correction + cap((distance_to_target / 16) ** 2, 0, speed_correction)

        if can_half_flip(agent, angle_to_target, distance_to_target):
            agent.brain.push_only("HalfFlip")
        elif can_power_slide(agent, angle_to_target):
            agent.brain.push_only("PowerSlide")
        elif ball_project(agent) < 10:
            agent.brain.pop_only()

        return self.controller(agent, agent.get_target_pos(), speed)

    def controller(self, agent, target_location, target_speed):
        location = calc_local_vector(target_location - agent.me.location, agent.me.rotation_matrix)
        controller_state = SimpleControllerState()
        angle_to_ball = math.atan2(location.data[1], location.data[0])

        current_speed = velocity2d(agent.me.velocity)
        controller_state.steer = steer(angle_to_ball)

        # throttle
        if target_speed > current_speed:
            controller_state.throttle = 1.0
            if target_speed > 1400 and current_speed < 2250:
                controller_state.boost = True
        elif target_speed < current_speed:
            controller_state.throttle = -1.0
        return controller_state

    def terminate(self, agent):
        pass
