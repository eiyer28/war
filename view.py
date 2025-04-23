# view.py

import pygame
from constants import BLUE, RED, BLACK, GREEN, GRAY, PURPLE, WHITE, WIDTH, HEIGHT, Action

class Button:
    def __init__(self, label, x, y, color, action):
        self.text = label
        self.color = color
        self.action = action
        self.rect = pygame.Rect(x, y, 180, 50)

    def draw(self, surface, font):
        pygame.draw.rect(surface, self.color, self.rect)
        label = font.render(self.text, True, WHITE)
        surface.blit(label, (self.rect.x + 20, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class GameView:
    def __init__(self, game, screen):
        self.game = game
        self.screen = screen
        self.font = pygame.font.SysFont("arial", 26)
        self.buttons = [
            Button("Reload", 20, 450, BLUE, "reload"),
            Button("Shoot (Gun)", 140, 450, RED, "gun"),
            Button("Shoot (Bow)", 300, 450, BLACK, "bow"),
            Button("Cannon", 460, 450, PURPLE, "cannon"),
            Button("Shield", 20, 510, GREEN, "shield"),
            Button("Reflect", 200, 510, GRAY, "reflect")
        ]

    def draw(self):
        self.screen.fill(GRAY)
        p_text = self.font.render(f"You: {self.game.player.bullets} bullets | Last: {self.game.player.last_action}", True, BLACK)
        a_text = self.font.render(f"AI: {self.game.ai.bullets} bullets | Last: {self.game.ai.last_action}", True, BLACK)
        self.screen.blit(p_text, (40, 40))
        self.screen.blit(a_text, (40, 80))

        if self.game.player.current_weapon:
            self.screen.blit(self.font.render(f"Your Weapon: {self.game.player.current_weapon.name}", True, BLACK), (30, 110))

        if self.game.ai.current_weapon:
            self.screen.blit(self.font.render(f"AI Weapon: {self.game.ai.current_weapon.name}", True, BLACK), (30, 150))

        if self.game.game_over:
            result = self.font.render(self.game.winner, True, RED)
            self.screen.blit(result, (WIDTH // 2 - result.get_width() // 2, HEIGHT // 2))
        else:
            for btn in self.buttons:
                btn.draw(self.screen, self.font)

        pygame.display.flip()

    def check_click(self, pos):
        for btn in self.buttons:
            if btn.is_clicked(pos):
                # Validate ammo before selecting a weapon
                if btn.action in self.game.player.weapons:
                    weapon = self.game.player.weapons[btn.action]
                    if not weapon.can_use(self.game.player):
                        return
                self.game.handle_player_action(btn.action)
