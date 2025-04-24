import pygame

class Enemy:
    def __init__(self, x, y):
        self.width = 40
        self.height = 30
        self.x = x
        self.y = y
        self.color = (255, 0, 0)
        self.direction = 1  # 1 for right, -1 for left
        self.move_counter = 0

    def update(self):
        # Move left/right and descend every 60 frames
        self.x += self.direction * 2
        self.move_counter += 1
        if self.x <= 0 or self.x + self.width >= 800:
            self.direction *= -1
            self.y += 20
            self.move_counter = 0

    def draw(self, screen):
        # Draw a red ellipse for the enemy spaceship
        pygame.draw.ellipse(screen, self.color, (self.x, self.y, self.width, self.height))