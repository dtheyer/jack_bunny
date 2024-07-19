from .command import BunnyCommand

import re
import random
from flask import request

class DndCommand(BunnyCommand):

    def flask_routes(self):
        return [
            "/d<int:num_sides>/",
            "/<int:num_dice>d<int:num_sides>"
        ]

    def gen_response(self, num_sides, num_dice=1):
        resp = ""
        total = 0
        for die_info in self.gen_die_info(request.args.get("q", "")):
            outcome, value = self.process_dice(*die_info)
            resp += outcome + "<br>"
            total += value

        resp += f"Total: {total}"
        return resp

    @staticmethod
    def gen_die_info(possible_dice: str):
        dice = possible_dice.split()
        for d in dice:
            pattern = r'(\d*)d(\d+)'
            match = re.search(pattern, d)
            if match:
                num_dice = match.group(1) if match.group(1) else 1
                num_sides = match.group(2)
                yield (int(num_sides), int(num_dice)) 
                

    @staticmethod
    def process_dice(num_sides: int, num_dice: int):
        resp = ""
        total = 0
        for d in range(num_dice):
            roll = random.randint(1, num_sides)
            total += roll
            resp += f"Rolled a d{num_sides} and got {roll}<br>"
        return resp, total

