import random
from collections import defaultdict
from constants import Action, decision_matrix
from model import Player

def random_ai_decide(player: Player) -> str:
    actions = ["reload", "shield", "reflect"]
    if player.weapons["gun"].can_use(player):
        actions.append("gun")
    if player.weapons["bow"].can_use(player):
        actions.append("bow")
    if player.weapons["cannon"].can_use(player):
        actions.append("cannon")
    return random.choice(actions)

def strategic_ai_decide(player: Player, opponent: Player, turn: int) -> str:
    if turn == 0:
        return "reload"
    if opponent.bullets == 0 and player.bullets >= 2:
        return "cannon"

    available = ["reload", "shield", "reflect"]
    if player.weapons["gun"].can_use(player):
        available.append("gun")
    if player.weapons["bow"].can_use(player):
        available.append("bow")
    if player.weapons["cannon"].can_use(player):
        available.append("cannon")

    if opponent.last_action in ["shield", "reflect"] and "cannon" in available:
        return "cannon"
    if player.bullets == 0:
        return "reload"

    return random.choice(available)

def simulate_game():
    rand_ai = Player("Random")
    strat_ai = Player("Strategic")
    turn = 0

    while rand_ai.alive and strat_ai.alive:
        rand_action = random_ai_decide(rand_ai)
        strat_action = strategic_ai_decide(strat_ai, rand_ai, turn)

        rand_ai.choose_action(rand_action)
        strat_ai.choose_action(strat_action)

        # Use decision matrix to resolve result
        result = decision_matrix.get((Action(rand_action), Action(strat_action)), "continue")

        if result == "p1_wins":
            strat_ai.alive = False
        elif result == "p2_wins":
            rand_ai.alive = False

        turn += 1

    return "random" if rand_ai.alive else "strategic"

# Run 100 games
results = defaultdict(int)
for _ in range(10000):
    winner = simulate_game()
    results[winner] += 1

print("RESULTS AFTER 10000 GAMES")
print(f"Strategic AI Wins: {results['strategic']}")
print(f"Random AI Wins   : {results['random']}")