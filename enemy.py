import pygame
import random
import math


class Enemy:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        side = random.choice(["top", "right", "bottom", "left"])
        if side == "top":
            self.x = random.randint(0, width)
            self.y = -30
        elif side == "right":
            self.x = width + 30
            self.y = random.randint(0, height)
        elif side == "bottom":
            self.x = random.randint(0, width)
            self.y = height + 30
        else:
            self.x = -30
            self.y = random.randint(0, height)

        self.radius = 20
        self.speed = 2
        self.health = 50
        self.color = (255, 50, 50)
        self.hit_animation = 0

    def draw(self, screen):
        RED = (255, 50, 50)
        WHITE = (255, 255, 255)
        BLACK = (20, 20, 30)
        GREEN = (50, 200, 50)

        # Эффект получения урона
        if self.hit_animation > 0:
            flash_color = WHITE
            self.hit_animation -= 1
        else:
            flash_color = self.color

        pygame.draw.circle(screen, flash_color, (self.x, self.y), self.radius)
        # Глаза врага
        pygame.draw.circle(screen, BLACK, (self.x - 5, self.y - 3), 5)
        pygame.draw.circle(screen, BLACK, (self.x + 5, self.y - 3), 5)

        # Индикатор здоровья
        pygame.draw.rect(screen, RED, (self.x - 20, self.y - 30, 40, 5))
        pygame.draw.rect(screen, GREEN, (self.x - 20, self.y - 30, 40 * (self.health / 50), 5))

    def move(self, player_x, player_y):
        # Движение к игроку
        angle = math.atan2(player_y - self.y, player_x - self.x)
        self.x += self.speed * math.cos(angle)
        self.y += self.speed * math.sin(angle)

    def check_collision(self, player):
        distance = math.sqrt((self.x - player.x) ** 2 + (self.y - player.y) ** 2)
        if distance < self.radius + player.radius:
            player.health -= 0.5
            return True
        return False

    def is_out_of_bounds(self):
        return (self.x < -50 or self.x > self.width + 50 or
                self.y < -50 or self.y > self.height + 50)
