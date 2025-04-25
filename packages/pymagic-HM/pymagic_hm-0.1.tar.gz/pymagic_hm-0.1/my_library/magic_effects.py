# magic_effects.py
import pygame


class MagicEffects:
    def __init__(self, screen):
        self.screen = screen

    def fireball(self, start_x, start_y, end_x, end_y):
        pygame.draw.line(self.screen, (255, 0, 0), (start_x, start_y), (end_x, end_y), 5)

class FireballEffect:
    def __init__(self, screen):
        self.screen = screen
        self.color = (255, 0, 0)
        self.size = 10

    def create_fireball(self, start_x, start_y, end_x, end_y):
        x, y = start_x, start_y
        dx = end_x - start_x
        dy = end_y - start_y
        steps = max(abs(dx), abs(dy))
        dx /= steps
        dy /= steps
        for _ in range(steps):
            x += dx
            y += dy
            pygame.draw.circle(self.screen, self.color, (int(x), int(y)), self.size)

class ExplosionEffect:
    def __init__(self, screen):
        self.screen = screen
        self.color = (255, 165, 0)

    def create_explosion(self, x, y):
        pygame.draw.circle(self.screen, self.color, (x, y), 50)
