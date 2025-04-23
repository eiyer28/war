# model.py

from enum import Enum
import random
from constants import Action, decision_matrix
from constants import Defense, ShieldDefense, ReflectDefense


# --- Weapon System ---

class Weapon:
    def __init__(self, name="Weapon", ammo_cost=1, lethal=True, priority=0):
        self.name = name
        self.ammo_cost = ammo_cost
        self.lethal = lethal
        self.priority = priority

    def can_use(self, player):
        return player.bullets >= self.ammo_cost

    def use(self, attacker, defender):
        if not self.can_use(attacker):
            return
        attacker.bullets -= self.ammo_cost
        if isinstance(defender.defense, ShieldDefense):
            return
        if isinstance(defender.defense, ReflectDefense):
            defender.defense.defend(attacker, defender)
            return
        if defender.last_action == "reload":
            defender.alive = False


class Gun(Weapon):
    def __init__(self):
        super().__init__("Gun", 1, True, 2)

    def use(self, attacker, defender):
        if not self.can_use(attacker):
            return
        attacker.bullets -= self.ammo_cost
        if isinstance(defender.defense, ReflectDefense):
            defender.defense.defend(attacker, defender)
            return
        if isinstance(defender.defense, ShieldDefense):
            return
        if defender.last_action == "bow":
            defender.alive = False
            return
        if defender.last_action == "reload":
            defender.alive = False


class Bow(Weapon):
    def __init__(self):
        super().__init__("Bow", 1, True, 1)

    def use(self, attacker, defender):
        if not self.can_use(attacker):
            return
        if defender.last_action == "gun":
            return
        attacker.bullets -= self.ammo_cost
        if isinstance(defender.defense, ShieldDefense):
            return
        if isinstance(defender.defense, ReflectDefense):
            defender.alive = False
            return
        if defender.last_action == "reload":
            defender.alive = False


class Cannon(Weapon):
    def __init__(self):
        super().__init__("Cannon", 2, True, 0)

    def use(self, attacker, defender):
        if not self.can_use(attacker):
            return
        attacker.bullets -= self.ammo_cost
        if defender.last_action in ["gun", "bow"]:
            attacker.alive = False
        else:
            defender.alive = False


# --- Player Class ---

class Player:
    def __init__(self, name):
        self.name = name
        self.bullets = 0
        self.alive = True
        self.last_action = None
        self.defense = Defense()
        self.weapons = {
            "gun": Gun(),
            "bow": Bow(),
            "cannon": Cannon()
        }
        self.current_weapon = None

    def choose_action(self, action):
        self.last_action = action
        self.current_weapon = None

        if action == "reload":
            self.bullets += 1
            self.defense = Defense()
        elif action == "shield":
            self.defense = ShieldDefense()
        elif action == "reflect":
            self.defense = ReflectDefense()
        elif action in self.weapons:
            self.current_weapon = self.weapons[action]
            self.defense = Defense()
        else:
            self.defense = Defense()

    def act(self, opponent):
        if self.current_weapon and self.current_weapon.can_use(self):
            self.current_weapon.use(self, opponent)


# --- Game Logic ---

class Game:
    def __init__(self):
        self.player = Player("You")
        self.ai = Player("AI")
        self.game_over = False
        self.winner = None
        self.turn_number = 0

    def ai_decide(self):
        if self.turn_number == 0:
            return "reload"

        available = ["reload", "shield", "reflect"]
        if self.ai.weapons["gun"].can_use(self.ai):
            available.append("gun")
        if self.ai.weapons["bow"].can_use(self.ai):
            available.append("bow")
        if self.ai.weapons["cannon"].can_use(self.ai):
            available.append("cannon")

        if self.player.last_action in ["shield", "reflect"] and "cannon" in available:
            return "cannon"

        return random.choice(available)

    def resolve_turn(self):
        p1_action = Action(self.player.last_action)
        p2_action = Action(self.ai.last_action)

        result = decision_matrix.get((p1_action, p2_action), "continue")

        if result == "p1_wins":
            self.ai.alive = False
        elif result == "p2_wins":
            self.player.alive = False

        self.player.act(self.ai)
        self.ai.act(self.player)

        if not self.player.alive or not self.ai.alive:
            self.game_over = True
            self.winner = (
                "Draw" if not self.player.alive and not self.ai.alive
                else "You Win!" if self.player.alive else "You Lose!"
            )

        self.turn_number += 1

    def handle_player_action(self, action):
        if self.game_over:
            return
        self.player.choose_action(action)
        self.ai.choose_action(self.ai_decide())
        self.resolve_turn()
