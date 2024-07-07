from .command import BunnyCommand

from flask import redirect, request

class QueryPassCommand(BunnyCommand):
    def __init__(self, route, target):
        self.route = route
        self.target = target

    def flask_routes(self):
        return [f"/{self.route}/"]

    def gen_response(self):
        query = str(request.args.get('q', ''))
        query = query.removeprefix(self.route).strip()
        if query == '':
            return redirect(self.target)

        url = f"{self.target}?q={query}"
        return redirect(url)
