import time

from IAmHuman.stack_fsm import State
from IAmHuman.mathf import *
from IAmHuman.game_values import Dimensions

from rlbot.agents.base_agent import SimpleControllerState


class ATBAShooting(State):
    def __init__(self):
        self.left_post = Vector3([0, 0, 0])
        self.right_post = Vector3([0, 0, 0])
        self.target_location = Vector3([0, 0, 0])

    def debug_render(self, agent):
        agent.renderer.draw_line_3d(agent.me.location.data, self.left_post.data,
                                    agent.renderer.create_color(255, 255, 0, 0))
        agent.renderer.draw_line_3d(agent.me.location.data, self.right_post.data,
                                    agent.renderer.create_color(255, 255, 0, 0))
        agent.renderer.draw_line_3d(agent.me.location.data, self.target_location.data,
                                    agent.renderer.create_color(255, 0, 0, 255))

    def activate(self, agent):
        pass

    def execute(self, agent):
        self.left_post = Vector3(
            [sign(agent.team) * Dimensions.GOAL_WIDTH / 2, -sign(agent.team) * Dimensions.FIELD_LENGTH / 2, 100])
        self.right_post = Vector3(
            [-sign(agent.team) * Dimensions.GOAL_WIDTH / 2, -sign(agent.team) * Dimensions.FIELD_LENGTH / 2, 100])

        ball_left = angle2d(agent.ball.location, self.left_post)
        ball_right = angle2d(agent.ball.location, self.right_post)

        our_left = angle2d(agent.me.location, self.left_post)
        our_right = angle2d(agent.me.location, self.right_post)

        target_speed = 1399

        if our_left <= ball_left and our_right >= ball_right:
            self.target_location = agent.ball.location
        elif our_left > ball_left and our_right >= ball_right:  # ball is too far right
            self.target_location = Vector3(
                [agent.ball.location.data[0], agent.ball.location.data[1] + sign(agent.team) * 160,
                 agent.ball.location.data[2]])
        elif our_right < ball_right and our_left <= ball_left:  # ball is too far left
            self.target_location = Vector3(
                [agent.ball.location.data[0], agent.ball.location.data[1] + sign(agent.team) * 160,
                 agent.ball.location.data[2]])
        else:
            self.target_location = Vector3([0, sign(agent.team) * Dimensions.FIELD_LENGTH / 2, 100])

        return self.controller(agent, self.target_location, target_speed)

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
        if angle_to_target > 0.1:
            controller_state.steer = controller_state.yaw = 1
        elif angle_to_target < -0.1:
            controller_state.steer = controller_state.yaw = -1
        else:
            controller_state.steer = controller_state.yaw = 0

        # throttle
        if angle_to_target >= 1.4:
            target_speed -= 1400
        else:
            if target_speed > 1400 and target_speed > current_speed and agent.start > 2.2 and current_speed < 2250:
                controller_state.boost = True
        if target_speed > current_speed:
            controller_state.throttle = 1.0
        elif target_speed < current_speed:
            controller_state.throttle = 0

        # dodging
        time_difference = time.time() - agent.start
        if time_difference > 2.2 and distance2d(target_location, agent.me.location) <= 270:
            agent.start = time.time()
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
