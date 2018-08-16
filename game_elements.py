from abc import ABC
from mathf import *


class GameObject(ABC):
    def __init__(self):
        self.location = Vector3([0, 0, 0])
        self.rotation = Vector3([0, 0, 0])
        self.velocity = Vector3([0, 0, 0])
        self.angular_velocity = Vector3([0, 0, 0])


class Car(GameObject):
    def __init__(self):
        super().__init__()
        self.stats = ScoreboardStats()
        self.is_demolished = False
        self.has_wheel_contact = True
        self.is_super_sonic = False
        self.is_bot = True
        self.jumped = False
        self.double_jumped = False
        self.name = 'IAmHuman'
        self.team = 0
        self.boost = 0
        self.local_location = Vector3([0, 0, 0])


class ScoreboardStats:
    def __init__(self):
        self.score = 0
        self.goals = 0
        self.own_goals = 0
        self.assists = 0
        self.saves = 0
        self.shots = 0
        self.demolitions = 0

    def clone(self):
        ss = ScoreboardStats()
        ss.score = self.score
        ss.goals = self.goals
        ss.own_goals = self.own_goals
        ss.assists = self.assists
        ss.saves = self.saves
        ss.shots = self.shots
        ss.demolitions = self.demolitions
        return ss



class Ball(GameObject):
    def __init__(self):
        super().__init__()
        self.latest_touch = LatestTouch()
        self.local_location = Vector3([0, 0, 0])


class LatestTouch:
    def __init__(self):
        self.player_name = ''
        self.time_seconds = 0
        self.hit_location = Vector3([0, 0, 0])
        self.hit_normal = Vector3([0, 0, 0])


class GameInfo:
    def __init__(self):
        self.num_cars = 0
        self.boost_info = BoostInfo()
        self.seconds_elapsed = 0
        self.game_time_remaining = 0
        self.is_overtime = False
        self.is_unlimited_time = False
        self.is_round_active = True
        self.is_kickoff_pause = False
        self.is_match_ended = False


class BoostInfo:
    def __init__(self):
        self.num_boost = 36
