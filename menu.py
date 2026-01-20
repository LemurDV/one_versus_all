import pygame


class MainMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.selected_option = 0
        self.options = [
            {"name": "Топор", "description": "Ближний бой, высокий урон", "type": "axe"},
            {"name": "Лук", "description": "Дальний бой, быстрое attack", "type": "bow"},
            {"name": "Выход", "description": "Завершить игру", "type": "exit"}
        ]

    def draw(self, screen):
        # Фон
        screen.fill((20, 20, 40))

        # Заголовок
        title_font = pygame.font.SysFont(None, 72)
        title_text = title_font.render("ГЕРОЙ ПРОТИВ ВРАГОВ", True, (255, 255, 0))
        screen.blit(title_text, (self.width // 2 - title_text.get_width() // 2, 80))

        # Подзаголовок
        subtitle_font = pygame.font.SysFont(None, 36)
        subtitle_text = subtitle_font.render("Выберите оружие:", True, (200, 200, 200))
        screen.blit(subtitle_text, (self.width // 2 - subtitle_text.get_width() // 2, 160))

        # Опции выбора
        option_font = pygame.font.SysFont(None, 32)
        desc_font = pygame.font.SysFont(None, 24)

        for i, option in enumerate(self.options):
            y_pos = 250 + i * 100

            # Цвет выделения
            color = (50, 150, 255) if i == self.selected_option else (100, 100, 150)
            border_color = (0, 200, 255) if i == self.selected_option else (70, 70, 100)

            # Фон опции
            pygame.draw.rect(screen, (30, 30, 50), (self.width // 2 - 200, y_pos, 400, 80), border_radius=15)
            pygame.draw.rect(screen, border_color, (self.width // 2 - 200, y_pos, 400, 80), 3, border_radius=15)

            # Текст опции
            option_text = option_font.render(option["name"], True, color)
            screen.blit(option_text, (self.width // 2 - option_text.get_width() // 2, y_pos + 15))

            # Описание
            desc_text = desc_font.render(option["description"], True, (180, 180, 180))
            screen.blit(desc_text, (self.width // 2 - desc_text.get_width() // 2, y_pos + 50))

        # Подсказка управления
        hint_font = pygame.font.SysFont(None, 24)
        hint_text = hint_font.render("↑↓: выбор, ENTER: подтвердить, ESC: выход", True, (150, 150, 150))
        screen.blit(hint_text, (self.width // 2 - hint_text.get_width() // 2, self.height - 50))

        # Рисуем иконки оружия
        self.draw_weapon_icons(screen)

    def draw_weapon_icons(self, screen):
        # Иконка топора
        pygame.draw.rect(screen, (139, 69, 19), (self.width // 2 - 250, 260, 30, 60))
        pygame.draw.polygon(screen, (100, 100, 100), [
            (self.width // 2 - 220, 260),
            (self.width // 2 - 200, 280),
            (self.width // 2 - 200, 300),
            (self.width // 2 - 220, 300)
        ])

        # Иконка лука
        pygame.draw.arc(screen, (139, 69, 19), (self.width // 2 + 170, 260, 40, 60), 0.5, 2.6, 5)
        pygame.draw.line(screen, (200, 200, 200), (self.width // 2 + 170, 290), (self.width // 2 + 210, 290), 2)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_option]["type"]
            elif event.key == pygame.K_ESCAPE:
                return "exit"
        return None
