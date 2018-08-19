from IAmHuman.state import State

from rlbot.agents.base_agent import SimpleControllerState


class PowerSlide(State):
    def debug_render(self, agent):
        pass

    def activate(self, agent):
        pass

    def execute(self, agent):
        if agent.me.has_wheel_contact is False:
            agent.brain.pop_only()

        return self.controller(agent)

    def controller(self, agent):
        controller_state = SimpleControllerState()

        controller_state.handbrake = True

        return controller_state

    def terminate(self, agent):
        pass
