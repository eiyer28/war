# constants.py

from enum import Enum

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE  = (0, 0, 200)
GRAY  = (180, 180, 180)
PURPLE = (139, 0, 139)

# Game Actions
class Action(Enum):
    RELOAD = "reload"
    GUN = "gun"
    BOW = "bow"
    CANNON = "cannon"
    SHIELD = "shield"
    REFLECT = "reflect"

# --- Defense Base Classes ---
class Defense:
    def __init__(self, name="None"):
        self.name = name

    def defend(self, attacker, defender):
        return False  # Default: does not protect


class ShieldDefense(Defense):
    def __init__(self):
        super().__init__("Shield")

    def defend(self, attacker, defender):
        return True  # Blocks attack


class ReflectDefense(Defense):
    def __init__(self):
        super().__init__("Reflect")

    def defend(self, attacker, defender):
        attacker.alive = False  # Reflects back and kills attacker
        return True


# Decision matrix (P1 action, P2 action) => outcome
# Outcomes: "p1_wins", "p2_wins", "continue"
decision_matrix = {
    # Reload interactions
    (Action.GUN, Action.RELOAD): "p1_wins",
    (Action.RELOAD, Action.GUN): "p2_wins",
    (Action.BOW, Action.RELOAD): "p1_wins",
    (Action.RELOAD, Action.BOW): "p2_wins",
    (Action.CANNON, Action.RELOAD): "p1_wins",
    (Action.RELOAD, Action.CANNON): "p2_wins",
    (Action.RELOAD, Action.RELOAD): "continue",

    # Gun vs others
    (Action.GUN, Action.BOW): "p1_wins",
    (Action.BOW, Action.GUN): "p2_wins",
    (Action.GUN, Action.SHIELD): "continue",
    (Action.GUN, Action.REFLECT): "p2_wins",
    (Action.GUN, Action.GUN): "continue",

    # Bow vs others
    (Action.BOW, Action.SHIELD): "continue",
    (Action.BOW, Action.REFLECT): "p1_wins",
    (Action.BOW, Action.BOW): "continue",

    # Cannon interactions
    (Action.CANNON, Action.SHIELD): "p1_wins",
    (Action.CANNON, Action.REFLECT): "p1_wins",
    (Action.CANNON, Action.GUN): "p2_wins",
    (Action.CANNON, Action.BOW): "p2_wins",
    (Action.CANNON, Action.CANNON): "continue",

    # Defensive matchups
    (Action.SHIELD, Action.SHIELD): "continue",
    (Action.REFLECT, Action.REFLECT): "continue",
    (Action.SHIELD, Action.REFLECT): "continue",
    (Action.REFLECT, Action.SHIELD): "continue"
}
