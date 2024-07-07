from abc import ABC, abstractmethod

class BunnyCommand(ABC):

    @abstractmethod
    def flask_routes(self):
        pass

    @abstractmethod
    def gen_response(self, request):
        pass


