from IAmHuman.util import *


def can_half_flip(agent, angle_to_target, distance):
    if abs(angle_to_target) >= 2.75 and agent.me.has_wheel_contact and is_inside_arena(
            agent.me.location) and distance >= 400:
        return True
    return False


def can_power_slide(agent, angle_to_target):
    if agent.me.has_wheel_contact and is_inside_arena(agent.me.location) and abs(angle_to_target) > 1.5:
        return True
    return False
