from .command import BunnyCommand

from flask import redirect, request

class SimpleRedirectCommand(BunnyCommand):
    def __init__(self, route, target):
        self.route = route
        self.target = target

    def flask_routes(self):
        return [f"/{self.route}/"]

    def gen_response(self):
        return redirect(self.target)
