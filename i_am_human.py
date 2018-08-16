import time

from IAmHuman.stack_fsm import StackFSM
from IAmHuman.game_elements import *
from IAmHuman.mathf import *
from IAmHuman.states.atba import ATBA
from IAmHuman.states.quick_chat import QuickChat
from IAmHuman.states.quick_shot import QuickShot
from IAmHuman.states.atba_shooting import ATBAShooting

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket


class IAmHuman(BaseAgent):

    def initialize_agent(self):
        # This runs once before the bot starts up
        self.brain = StackFSM()
        self.me = Car()
        self.teammates = []
        self.opponents = []
        self.ball = Ball()
        self.game_info = GameInfo()

        self.start = time.time()
        self.show_debug_info = True
        self.use_quick_chat = True
        self.quick_chat = QuickChat()

    def get_output(self, game: GameTickPacket) -> SimpleControllerState:
        self.preprocess(game)

        if self.brain.get_current_state() is None:
            # Prevent bot from doing nothing
            self.brain.push_only(ATBAShooting())

        if self.show_debug_info:
            self.render_cur_state()

        if self.use_quick_chat:
            self.quick_chat.execute(self)

        return self.brain.update(self)

    def render_cur_state(self):
        self.renderer.begin_rendering()

        # Colors
        background_color = self.renderer.create_color(150, 0, 0, 0)
        text_color = self.renderer.create_color(255, 255, 255, 255)
        text_color2 = self.renderer.create_color(150, 255, 255, 255)

        # 2D GUI
        self.renderer.draw_rect_2d(20, 250, 200, 100, True, background_color)
        self.renderer.draw_string_2d(25, 255, 1, 1, 'States Stack:',
                                     text_color)
        self.renderer.draw_string_2d(125, 255, 1, 1, self.brain.get_current_state().__class__.__name__, text_color)

        y_offset = 255
        for i, s in reversed(list(enumerate(self.brain.stack))):
            if i != len(self.brain.stack) - 1:
                y_offset += 20
                self.renderer.draw_string_2d(125, y_offset, 1, 1, self.brain.stack[i].__class__.__name__,
                                             text_color2)

        # 3D GUI
        # self.renderer.draw_rect_3d([self.me.location.data[0], self.me.location.data[1], self.me.location.data[2]],
        #                            100, 20, True, background_color)
        # self.renderer.draw_string_3d(
        #    [self.me.location.data[0], self.me.location.data[1], self.me.location.data[2]], 1, 1,
        #    self.brain.get_current_state().__class__.__name__, text_color)

        # State GUI
        self.brain.get_current_state().debug_render(self)

        self.renderer.end_rendering()

    def preprocess(self, game):
        # set up own car object
        self.me.rotation_matrix = calc_rotation_matrix([game.game_cars[self.index].physics.rotation.pitch,
                                                        game.game_cars[self.index].physics.rotation.yaw,
                                                        game.game_cars[self.index].physics.rotation.roll])
        self.preprocess_car(game.game_cars[self.index], self.me)

        # set up ball object
        self.preprocess_game_object(game.game_ball, self.ball)

        # set up game info objects
        self.game_info.is_match_ended = game.game_info.is_match_ended

        # set up other car objects
        self.teammates.clear()
        self.opponents.clear()

        for i, car in enumerate(game.game_cars):
            if i != self.index:
                new_car = Car()
                self.preprocess_car(game.game_cars[i], new_car)

                if car.team == self.me.team:
                    self.teammates.append(new_car)
                else:
                    self.opponents.append(new_car)

    def preprocess_game_object(self, object_data, game_object):
        game_object.location.data = [object_data.physics.location.x, object_data.physics.location.y,
                                     object_data.physics.location.z]
        game_object.rotation.data = [object_data.physics.rotation.pitch, object_data.physics.rotation.yaw,
                                     object_data.physics.rotation.roll]
        game_object.velocity.data = [object_data.physics.velocity.x, object_data.physics.velocity.y,
                                     object_data.physics.velocity.z]
        game_object.angular_velocity.data = [object_data.physics.angular_velocity.x,
                                             object_data.physics.angular_velocity.y,
                                             object_data.physics.angular_velocity.z]

        game_object.local_location = calc_local_vector(game_object.location - self.me.location, self.me.rotation_matrix)

    def preprocess_car(self, car_data, car_object):
        self.preprocess_game_object(car_data, car_object)

        car_object.stats.score = car_data.score_info.score
        car_object.stats.goals = car_data.score_info.goals
        car_object.stats.own_goals = car_data.score_info.own_goals
        car_object.stats.assists = car_data.score_info.assists
        car_object.stats.saves = car_data.score_info.saves
        car_object.stats.shots = car_data.score_info.shots
        car_object.stats.demolitions = car_data.score_info.demolitions

        car_object.rotation_matrix = calc_rotation_matrix(car_object.rotation.data)
        car_object.boost = car_data.boost
        car_object.team = car_data.team

        return car_object
