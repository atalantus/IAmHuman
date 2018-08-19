from IAmHuman.state import State

from rlbot.agents.base_agent import SimpleControllerState


class HalfFlip(State):
    def __init__(self):
        self.time_difference = 0
        self.start = 0

    def debug_render(self, agent):
        agent.renderer.draw_rect_3d(agent.me.location.data, 150,
                                    20, True, agent.renderer.black())
        agent.renderer.draw_string_3d(agent.me.location.data, 1,
                                      1, str(self.time_difference), agent.renderer.white())

    def activate(self, agent):
        self.time_difference = 0
        self.start = agent.game_info.seconds_elapsed

    def execute(self, agent):
        if self.time_difference > 1.75:
            agent.brain.pop_only()

        return self.controller(agent)

    def controller(self, agent):
        controller_state = SimpleControllerState()

        controller_state.pitch = 1
        controller_state.throttle = -1

        self.time_difference = agent.game_info.seconds_elapsed - self.start

        if self.time_difference <= 0.1:
            controller_state.jump = True
        elif 0.1 <= self.time_difference <= 0.15:
            controller_state.jump = False
        elif 0.15 <= self.time_difference <= 0.35:
            controller_state.jump = True
        elif 0.4 <= self.time_difference <= 1.75:
            controller_state.pitch = -1

        if 1.2 <= self.time_difference:
            controller_state.throttle = 1

        if 0.575 <= self.time_difference <= 1.2:
            controller_state.boost = True
            controller_state.roll = 1

        if 0.7 <= self.time_difference <= 1.5:
            controller_state.yaw = .5

        return controller_state

    def terminate(self, agent):
        pass
