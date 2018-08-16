from IAmHuman.mathf import *
from IAmHuman.game_values import Dimensions


def ball_ready(agent):
    ball = agent.ball
    if abs(ball.velocity.data[2]) < 100 and ball.location.data[2] < 250:
        if abs(ball.location.data[1]) < 5000:
            return True
    return False


def ball_project(agent):
    goal = Vector3([0, -sign(agent.team) * Dimensions.FIELD_LENGTH / 2, 100])
    goal_to_ball = (agent.ball.location - goal).normalize()
    difference = agent.me.location - agent.ball.location
    return difference * goal_to_ball


def steer(angle):
    final = ((10 * angle + sign(angle)) ** 3) / 20
    return cap(final, -1, 1)