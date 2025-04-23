
WAR (2017 Edition)
===========================

Based on a game I played in my childhood. This is a strategic, turn-based 1v1 game built in Python with Pygame, structured using the MVC (Model-View-Controller) design pattern. Players choose from offensive and defensive actions to defeat the opponent. Features AI logic and an extensible weapon system.

PROJECT STRUCTURE
-----------------
shootout_game_mvc/
├── main.py           -> Entry point (Controller)
├── model.py          -> Core game logic (Model)
├── view.py           -> GUI rendering and input handling (View)
├── constants.py      -> Enums, decision matrix, color and screen settings
├── README.txt        -> Project documentation

GAMEPLAY OVERVIEW
-----------------
Each turn, both the player and the AI choose one of the following actions:

  - RELOAD     : Gain 1 bullet
  - GUN        : Costs 1 bullet. Kills reloading players. Loses to Reflect.
  - BOW        : Costs 1 bullet. Pierces Reflect. Dies to Gun.
  - CANNON     : Costs 2 bullets. Kills shielded and reflected players. Dies to Gun/Bow.
  - SHIELD     : Blocks Gun and Bow.
  - REFLECT    : Reflects Gun back at attacker.

Special Logic:
- Gun beats Bow.
- Bow beats Reflect.
- Cannon beats Shield/Reflect.
- Using the same weapon (e.g., Gun vs Gun) results in no kills.
- The AI always reloads on turn 1.

FEATURES
--------
- Clear MVC architecture for maintainability
- AI opponent with logical behavior
- Button-based UI with Pygame
- Decision matrix for scalable and testable interaction logic
- Easily add new actions, weapons, or players

INSTALLATION
------------
1. Requires Python 3.8+ and Pygame
2. To install Pygame:
   pip install pygame

3. To run the game:
   python main.py

EXTENDING THE GAME
------------------
To add a new action:
1. Add it to the Action enum in constants.py
2. Create a new Weapon subclass in model.py
3. Add a button for it in view.py
4. Define its outcomes in the decision_matrix in constants.py

AUTHOR
------
Created by Eashan Iyer
MIT License
"""
