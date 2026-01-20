import pygame
import math


class Player:
    def __init__(self, weapon_type="axe"):
        self.x = 400
        self.y = 300
        self.radius = 30
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.weapon_type = weapon_type
        self.set_weapon_stats(weapon_type)
        self.attack_cooldown = 0
        self.score = 0
        self.experience = 0
        self.experience_to_level = 100
        self.level = 1
        self.is_attacking = False
        self.attack_animation = 0
        self.lifesteal = 0
        self.projectiles = [] if weapon_type == "bow" else None
        self.total_kills = 0

    def set_weapon_stats(self, weapon_type):
        self.weapon_type = weapon_type
        if weapon_type == "axe":
            self.damage = 35
            self.attack_range = 80
            self.attack_speed = 20
            self.color = (50, 120, 255)
        elif weapon_type == "bow":
            self.damage = 25
            self.attack_range = 200
            self.attack_speed = 15
            self.color = (0, 150, 0)
            self.projectiles = []

    def draw(self, screen):
        WHITE = (255, 255, 255)
        BLACK = (20, 20, 30)
        LIGHT_YELLOW = (255, 255, 150)

        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, WHITE, (self.x - 10, self.y - 5), 8)
        pygame.draw.circle(screen, WHITE, (self.x + 10, self.y - 5), 8)
        pygame.draw.circle(screen, BLACK, (self.x - 10, self.y - 5), 4)
        pygame.draw.circle(screen, BLACK, (self.x + 10, self.y - 5), 4)
        pygame.draw.arc(screen, BLACK, (self.x - 15, self.y, 30, 20), 0, 3.14, 2)

        if self.weapon_type == "axe":
            self.draw_axe(screen)
        elif self.weapon_type == "bow":
            self.draw_bow(screen)
            self.draw_projectiles(screen)

        if self.is_attacking:
            self.draw_attack_effect(screen)

    def draw_axe(self, screen):
        BROWN = (139, 69, 19)
        GRAY = (100, 100, 100)
        pygame.draw.rect(screen, BROWN, (self.x + 15, self.y - 25, 25, 5))
        pygame.draw.polygon(screen, GRAY, [
            (self.x + 40, self.y - 25),
            (self.x + 55, self.y - 30),
            (self.x + 55, self.y - 20),
            (self.x + 40, self.y - 20)
        ])

    def draw_bow(self, screen):
        BROWN = (139, 69, 19)
        WHITE = (255, 255, 255)
        pygame.draw.arc(screen, BROWN, (self.x + 10, self.y - 20, 30, 40), 0.5, 2.6, 4)
        pygame.draw.line(screen, WHITE, (self.x + 10, self.y), (self.x + 40, self.y), 2)

    def draw_projectiles(self, screen):
        for projectile in self.projectiles:
            pygame.draw.circle(screen, (255, 200, 0), (int(projectile['x']), int(projectile['y'])), 5)

    def draw_attack_effect(self, screen):
        LIGHT_YELLOW = (255, 255, 150)

        if self.weapon_type == "axe":
            pulse = math.sin(pygame.time.get_ticks() * 0.01) * 5 + 5
            pygame.draw.circle(screen, LIGHT_YELLOW, (self.x, self.y), self.attack_range + pulse, 4)

            if self.attack_animation < 20:
                wave_radius = self.attack_range + self.attack_animation * 5
                alpha = 255 - (self.attack_animation * 12)
                wave_surface = pygame.Surface((wave_radius * 2, wave_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(wave_surface, (255, 255, 0, alpha), (wave_radius, wave_radius), wave_radius, 3)
                screen.blit(wave_surface, (self.x - wave_radius, self.y - wave_radius))
                self.attack_animation += 1

        elif self.weapon_type == "bow":
            if self.attack_animation < 10:
                arrow_length = self.attack_animation * 8
                pygame.draw.line(
                    screen, LIGHT_YELLOW, (self.x, self.y),
                    (self.x + arrow_length, self.y), 3),
                self.attack_animation += 2

    def move(self, keys, width, height):
        if keys[pygame.K_a] and self.x - self.radius > 0:
            self.x -= self.speed
        if keys[pygame.K_d] and self.x + self.radius < width:
            self.x += self.speed
        if keys[pygame.K_w] and self.y - self.radius > 0:
            self.y -= self.speed
        if keys[pygame.K_s] and self.y + self.radius < height:
            self.y += self.speed

    def attack(self, enemies, mouse_pos=None, exp_multiplier=1.0):
        self.is_attacking = True
        self.attack_animation = 0

        if self.weapon_type == "axe":
            self.axe_attack(enemies, exp_multiplier)
        elif self.weapon_type == "bow" and mouse_pos:
            self.bow_attack(enemies, mouse_pos, exp_multiplier)

    def axe_attack(self, enemies, exp_multiplier=1.0):
        total_lifesteal = 0
        for enemy in enemies:
            distance = math.sqrt((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2)
            if distance < self.attack_range + enemy.radius:
                enemy.health -= self.damage
                enemy.hit_animation = 10

                lifesteal_amount = self.damage * (self.lifesteal / 100)
                total_lifesteal += lifesteal_amount

                if enemy.health <= 0:
                    self.gain_experience(20, exp_multiplier)
                    enemies.remove(enemy)
                    self.score += 10
                    self.total_kills += 1

        if total_lifesteal > 0:
            self.health = min(self.max_health, self.health + total_lifesteal)

    def bow_attack(self, enemies, mouse_pos, exp_multiplier=1.0):
        angle = math.atan2(mouse_pos[1] - self.y, mouse_pos[0] - self.x)
        self.projectiles.append({
            'x': self.x,
            'y': self.y,
            'angle': angle,
            'distance': 0,
            'max_distance': self.attack_range,
            'exp_multiplier': exp_multiplier
        })

    def update_projectiles(self, enemies):
        if self.weapon_type != "bow":
            return

        i = 0
        while i < len(self.projectiles):
            projectile = self.projectiles[i]
            projectile['x'] += math.cos(projectile['angle']) * 10
            projectile['y'] += math.sin(projectile['angle']) * 10
            projectile['distance'] += 10

            collision_occurred = False
            for enemy in enemies:
                distance = math.sqrt((projectile['x'] - enemy.x) ** 2 + (projectile['y'] - enemy.y) ** 2)
                if distance < enemy.radius + 5:
                    enemy.health -= self.damage
                    enemy.hit_animation = 10

                    # Вампиризм
                    lifesteal_amount = self.damage * (self.lifesteal / 100)
                    self.health = min(self.max_health, self.health + lifesteal_amount)

                    if enemy.health <= 0:
                        # Используем множитель из снаряда
                        exp_multiplier = projectile.get('exp_multiplier', 1.0)
                        self.gain_experience(20, exp_multiplier)
                        if enemy in enemies:
                            enemies.remove(enemy)
                        self.score += 10
                        self.total_kills += 1

                    collision_occurred = True
                    break  # Выходим из цикла по врагам после столкновения

            # Удаляем снаряд если было столкновение или он улетел далеко
            if collision_occurred or projectile['distance'] >= projectile['max_distance']:
                self.projectiles.pop(i)
            else:
                i += 1  # Переходим к следующему снаряду только если не удалили текущий

    def gain_experience(self, amount, exp_multiplier=1.0):
        actual_exp = int(amount * exp_multiplier)
        self.experience += actual_exp
        if self.experience >= self.experience_to_level:
            return True
        return False

    def level_up(self):
        self.level += 1
        self.experience = 0
        self.experience_to_level = 100 + (self.level - 1) * 50
        self.max_health += 20
        self.health = self.max_health

    def apply_upgrade(self, upgrade_type):
        if upgrade_type == "damage":
            self.damage += 10
        elif upgrade_type == "range":
            self.attack_range += 20
        elif upgrade_type == "lifesteal":
            self.lifesteal += 15
        elif upgrade_type == "speed":
            self.speed += 1

    def update(self):
        if self.is_attacking:
            if self.weapon_type == "axe" and self.attack_animation >= 20:
                self.is_attacking = False
            elif self.weapon_type == "bow" and self.attack_animation >= 10:
                self.is_attacking = False

        return self.health > 0

    def draw_health_bar(self, screen):
        RED = (255, 50, 50)
        GREEN = (50, 200, 50)
        PURPLE = (128, 0, 128)
        WHITE = (255, 255, 255)

        pygame.draw.rect(screen, RED, (20, 20, 200, 20))
        pygame.draw.rect(screen, GREEN, (20, 20, 200 * (self.health / self.max_health), 20))
        pygame.draw.rect(screen, (100, 100, 100), (20, 45, 200, 10))
        pygame.draw.rect(screen, PURPLE, (20, 45, 200 * (self.experience / self.experience_to_level), 10))

        font = pygame.font.SysFont(None, 24)
        level_text = font.render(f"Ур. {self.level} | {self.get_weapon_name()}", True, WHITE)
        screen.blit(level_text, (230, 20))

    def get_weapon_name(self):
        if self.weapon_type == "axe":
            return "Топор"
        elif self.weapon_type == "bow":
            return "Лук"
        return "Оружие"
