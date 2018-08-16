import time

from stack_fsm import StackFSM
from game_elements import *
from mathf import *
from states.example_atba import ATBAState
from states.quick_chat import QuickChat

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
        self.game_info = GameInfo()

        self.start = time.time()
        self.show_debug_info = True
        self.use_quick_chat = True
        self.quick_chat = QuickChat()

        # Add ATBAState state
        self.brain.push_only(ATBAState())

    def get_output(self, game: GameTickPacket) -> SimpleControllerState:
        self.team.clear()
        self.opponents.clear()

        self.preprocess(game)

        if self.show_debug_info:
            self.render_cur_state()

        if self.use_quick_chat:
            self.quick_chat.execute(self)

        return self.brain.update(self)

    def render_cur_state(self):
        self.renderer.begin_rendering()
        background_color = self.renderer.create_color(150, 0, 0, 0)
        text_color = self.renderer.create_color(255, 255, 255, 255)
        self.renderer.draw_rect_2d(20, 250, 200, 100, True, background_color)
        self.renderer.draw_string_2d(25, 255, 1, 1, 'State: ' + self.brain.get_current_state().__class__.__name__,
                                     text_color)

        self.renderer.draw_rect_3d([self.me.location.data[0], self.me.location.data[1], self.me.location.data[2]], 100,
                                   20, True, background_color)
        self.renderer.draw_string_3d(
            [self.me.location.data[0], self.me.location.data[1], self.me.location.data[2]], 1, 1,
            self.brain.get_current_state().__class__.__name__, text_color)
        self.renderer.end_rendering()

    def preprocess(self, game):
        # set up own car object
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

        self.me.stats.score = game.game_cars[self.index].score_info.score
        self.me.stats.goals = game.game_cars[self.index].score_info.goals
        self.me.stats.own_goals = game.game_cars[self.index].score_info.own_goals
        self.me.stats.assists = game.game_cars[self.index].score_info.assists
        self.me.stats.saves = game.game_cars[self.index].score_info.saves
        self.me.stats.shots = game.game_cars[self.index].score_info.shots
        self.me.stats.demolitions = game.game_cars[self.index].score_info.demolitions

        self.me.rotation_matrix = to_rotation_matrix(self.me.rotation.data)
        self.me.boost = game.game_cars[self.index].boost
        self.me.team = game.game_cars[self.index].team

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

        # set up game info objects
        self.game_info.is_match_ended = game.game_info.is_match_ended

        # set up other car objects
        for i, car in enumerate(game.game_cars):
            if i != self.index:
                new_car = Car()
                new_car.location.data = [game.game_cars[i].physics.location.x,
                                         game.game_cars[i].physics.location.y,
                                         game.game_cars[i].physics.location.z]
                new_car.rotation.data = [game.game_cars[i].physics.rotation.pitch,
                                         game.game_cars[i].physics.rotation.yaw,
                                         game.game_cars[i].physics.rotation.roll]
                new_car.velocity.data = [game.game_cars[i].physics.velocity.x,
                                         game.game_cars[i].physics.velocity.y,
                                         game.game_cars[i].physics.velocity.z]
                new_car.angular_velocity.data = [game.game_cars[i].physics.angular_velocity.x,
                                                 game.game_cars[i].physics.angular_velocity.y,
                                                 game.game_cars[i].physics.angular_velocity.z]

                new_car.stats.score = game.game_cars[i].score_info.score
                new_car.stats.goals = game.game_cars[i].score_info.goals
                new_car.stats.own_goals = game.game_cars[i].score_info.own_goals
                new_car.stats.assists = game.game_cars[i].score_info.assists
                new_car.stats.saves = game.game_cars[i].score_info.saves
                new_car.stats.shots = game.game_cars[i].score_info.shots
                new_car.stats.demolitions = game.game_cars[i].score_info.demolitions

                new_car.rotation_matrix = to_rotation_matrix(self.me.rotation.data)
                new_car.boost = game.game_cars[i].boost
                new_car.team = game.game_cars[i].team

                if car.team == self.me.team:
                    self.team.append(new_car)
                else:
                    self.opponents.append(new_car)
