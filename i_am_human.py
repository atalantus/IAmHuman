import time

from IAmHuman.stack_fsm import StackFSM
from IAmHuman.game_elements import *
from IAmHuman.mathf import *
from IAmHuman.quick_chat import QuickChat

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket


class IAmHuman(BaseAgent):

    def get_target_pos(self):
        if isinstance(self.target, Vector3):
            return self.target
        elif isinstance(self.target, GameObject):
            return self.target.location
        else:
            return None

    def initialize_agent(self):
        # This runs once before the bot starts up
        self.brain = StackFSM()
        self.brain.agent = self
        self.me = Car()
        self.teammates = []
        self.opponents = []
        self.ball = Ball()
        self.game_info = GameInfo()

        self.average_frame_time = 0
        self.fps = 60
        self.show_debug_info = True
        self.use_quick_chat = True
        self.quick_chat = QuickChat()

        self.target = Vector3([0, 0, 0])

    def get_output(self, game: GameTickPacket) -> SimpleControllerState:
        fps_start = time.time()
        self.preprocess(game)

        if self.brain.get_current_state() is None:
            # Prevent bot from doing nothing
            self.brain.push_only('QuickShot')

        if self.show_debug_info:
            self.render_cur_state()

        if self.use_quick_chat:
            self.quick_chat.check(self)

        controller = self.brain.update(self)
        self.calc_bot_fps(fps_start, time.time())

        return controller

    def calc_bot_fps(self, start_time, end_time):
        smoothing = 0.9
        self.average_frame_time = (self.average_frame_time * smoothing) + ((end_time - start_time) * (1 - smoothing))
        self.fps = 1 / self.average_frame_time

    def render_cur_state(self):
        self.renderer.begin_rendering()

        # Colors
        background_color = self.renderer.create_color(150, 0, 0, 0)
        text_color = self.renderer.create_color(255, 255, 255, 255)
        text_color2 = self.renderer.create_color(150, 255, 255, 255)
        green = self.renderer.create_color(255, 0, 255, 0)

        # Bot FPS
        self.renderer.draw_rect_2d(20, 220, 200, 25, True, background_color)
        self.renderer.draw_string_2d(25, 225, 1, 1, self.name + " FPS:",
                                     text_color)
        self.renderer.draw_string_2d(150, 225, 1, 1, str(int(round(self.fps))),
                                     green if (self.fps >= 60) else self.renderer.red())

        # States Stack
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

        # set up game info object
        self.game_info.is_match_ended = game.game_info.is_match_ended
        self.game_info.seconds_elapsed = game.game_info.seconds_elapsed

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

        car_object.is_demolished = car_data.is_demolished
        car_object.has_wheel_contact = car_data.has_wheel_contact
        car_object.boost = car_data.boost
        car_object.team = car_data.team

        car_object.rotation_matrix = calc_rotation_matrix(car_object.rotation.data)

        return car_object
