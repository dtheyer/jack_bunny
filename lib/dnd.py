from .command import BunnyCommand

import random

class DndCommand(BunnyCommand):

    def flask_routes(self):
        return [
                "/d<int:num_sides>/",
                "/<int:num_dice>d<int:num_sides>"
        ]

    def gen_response(self, num_sides, num_dice=1):
        resp = ""
        for d in range(num_dice):
            roll = random.randint(1, num_sides)
            resp += f"Rolled a d{num_sides} and got {roll}<br>"
        return resp
