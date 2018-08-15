from stack_fsm import StackFSM
from game_elements import *
from mathf import *

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket


class IAmHuman(BaseAgent):

    def initialize_agent(self):
        # This runs once before the bot starts up
        self.controller_state = SimpleControllerState()
        self.brain = StackFSM()
        self.me = Car()
        self.team = []
        self.opponents = []
        self.ball = Ball()

    def get_output(self, game: GameTickPacket) -> SimpleControllerState:
        self.preprocess(game)

        self.controller_state.throttle = 1.0
        self.controller_state.steer = 0
        self.controller_state.boost = True

        return self.controller_state

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
