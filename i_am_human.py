import time
from stack_fsm import StackFSM
from game_elements import *
from mathf import *
from states.example_atba import ATBAState

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket


class IAmHuman(BaseAgent):

    def initialize_agent(self):
        # This runs once before the bot starts up
        self.brain = StackFSM()
        self.me = Car()
        self.team = []
        self.opponents = []
        self.ball = Ball()
        self.start = time.time()

        # Add ATBAState state
        self.brain.push_only(ATBAState())

    def get_output(self, game: GameTickPacket) -> SimpleControllerState:
        self.preprocess(game)

        return self.brain.update(self)

    def exampleController(self, target_object, target_speed):
        location = target_object.local_location
        controller_state = SimpleControllerState()
        angle_to_ball = math.atan2(location.data[1], location.data[0])

        current_speed = velocity2D(self.me)
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
        time_difference = time.time() - self.start
        if time_difference > 2.2 and distance2D(target_object.location, self.me.location) > 1000 and abs(
                angle_to_ball) < 1.3:
            self.start = time.time()
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

    def preprocess(self, game):
        # set up own bot object
        self.me.location.data = [game.game_cars[self.index].physics.location.x,
                                 game.game_cars[self.index].physics.location.y,
                                 game.game_cars[self.index].physics.location.z]
        self.me.rotation.data = [game.game_cars[self.index].physics.rotation.pitch,
                                 game.game_cars[self.index].physics.rotation.yaw,
                                 game.game_cars[self.index].physics.rotation.roll]
        self.me.velocity.data = [game.game_cars[self.index].physics.velocity.x,
                                 game.game_cars[self.index].physics.velocity.y,
                                 game.game_cars[self.index].physics.velocity.z]
        self.me.angular_velocity.data = [game.game_cars[self.index].physics.angular_velocity.x,
                                         game.game_cars[self.index].physics.angular_velocity.y,
                                         game.game_cars[self.index].physics.angular_velocity.z]
        self.me.rotation_matrix = to_rotation_matrix(self.me.rotation.data)
        self.me.boost = game.game_cars[self.index].boost

        # set up ball object
        self.ball.location.data = [game.game_ball.physics.location.x, game.game_ball.physics.location.y,
                                   game.game_ball.physics.location.z]
        self.ball.rotation.data = [game.game_ball.physics.rotation.pitch, game.game_ball.physics.rotation.yaw,
                                   game.game_ball.physics.rotation.roll]
        self.ball.velocity.data = [game.game_ball.physics.velocity.x, game.game_ball.physics.velocity.y,
                                   game.game_ball.physics.velocity.z]
        self.ball.angular_velocity.data = [game.game_ball.physics.angular_velocity.x,
                                           game.game_ball.physics.angular_velocity.y,
                                           game.game_ball.physics.angular_velocity.z]

        self.ball.local_location = to_local_coordinates(self.ball.location - self.me.location, self.me.rotation_matrix)
