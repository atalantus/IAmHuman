from abc import ABC, abstractmethod


class State(ABC):

    @abstractmethod
    def activate(self, agent):
        pass

    @abstractmethod
    def execute(self, agent):
        pass

    @abstractmethod
    def terminate(self, agent):
        pass

    @abstractmethod
    def debug_render(self, agent):
        pass
