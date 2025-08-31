import pygame
import math


class GameManager:
    def __init__(self):
        self.game_time = 0  # Время игры в секундах
        self.difficulty_level = 1
        self.experience_multiplier = 1.0
        self.enemy_spawn_rate = 30  # Кадров между спавном врагов
        self.minute_counter = 0
        self.last_minute_check = 0

    def update(self, dt):
        # Обновляем время игры
        self.game_time += dt

        # Проверяем, прошла ли минута
        current_minute = math.floor(self.game_time / 60)
        if current_minute > self.minute_counter:
            self.minute_counter = current_minute
            self.increase_difficulty()

    def increase_difficulty(self):
        """Увеличиваем сложность каждую минуту"""
        self.difficulty_level += 1

        # Увеличиваем множитель опыта (на 20% каждую минуту)
        self.experience_multiplier = 1.0 + (self.difficulty_level - 1) * 0.2

        # Ускоряем спавн врагов (максимум до 10 кадров между спавном)
        self.enemy_spawn_rate = max(10, 30 - (self.difficulty_level - 1) * 2)

        print(f"Минута {self.minute_counter}: Уровень сложности {self.difficulty_level}, "
              f"Множитель опыта: {self.experience_multiplier:.1f}x, "
              f"Спавн врагов: каждые {self.enemy_spawn_rate} кадров")

    def get_experience(self, base_exp):
        """Возвращает опыт с учетом множителя"""
        return int(base_exp * self.experience_multiplier)

    def get_difficulty_info(self):
        """Возвращает информацию о сложности"""
        return {
            "minute": self.minute_counter,
            "level": self.difficulty_level,
            "exp_multiplier": self.experience_multiplier,
            "spawn_rate": self.enemy_spawn_rate
        }

    def reset(self):
        """Сброс менеджера игры"""
        self.game_time = 0
        self.difficulty_level = 1
        self.experience_multiplier = 1.0
        self.enemy_spawn_rate = 30
        self.minute_counter = 0