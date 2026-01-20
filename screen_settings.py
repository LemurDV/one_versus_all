import pygame


def draw_ui(screen, player, enemies, width, height, game_manager):
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)

    font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 24)
    tiny_font = pygame.font.SysFont(None, 20)

    # Получаем информацию о сложности
    difficulty_info = game_manager.get_difficulty_info()

    # Отрисовка счета и времени
    score_text = font.render(f"Счет: {player.score}", True, WHITE)
    screen.blit(score_text, (width - 150, 20))

    # Время игры и сложность
    minutes = int(game_manager.game_time // 60)
    seconds = int(game_manager.game_time % 60)
    time_text = small_font.render(f"Время: {minutes:02d}:{seconds:02d}", True, WHITE)
    screen.blit(time_text, (width - 150, 50))

    # Уровень сложности
    difficulty_text = small_font.render(f"Сложность: {difficulty_info['level']}", True, YELLOW)
    screen.blit(difficulty_text, (width - 150, 80))

    # Множитель опыта
    exp_mult_text = small_font.render(f"Опыт: x{difficulty_info['exp_multiplier']:.1f}", True, CYAN)
    screen.blit(exp_mult_text, (width - 150, 110))

    # Отрисовка характеристик
    stats_text = tiny_font.render(
        f"Урон: {player.damage} | Радиус: {player.attack_range} | "
        f"Вампиризм: {player.lifesteal}% | Скорость: {player.speed} | "
        f"Убийств: {player.total_kills}",
        True, WHITE
    )
    screen.blit(stats_text, (20, 70))

    # Отрисовка количества врагов
    enemies_text = font.render(f"Врагов: {len(enemies)}", True, WHITE)
    screen.blit(enemies_text, (20, 100))

    # Отрисовка управления
    controls_text = small_font.render("WASD: движение, SPACE: атака, ESC: меню", True, WHITE)
    screen.blit(controls_text, (20, height - 30))

    # Прогресс до следующего уровня сложности
    next_level_progress = (game_manager.game_time % 60) / 60
    pygame.draw.rect(screen, (100, 100, 100), (20, height - 60, 200, 10))
    pygame.draw.rect(screen, YELLOW, (20, height - 60, 200 * next_level_progress, 10))
    next_level_text = tiny_font.render("След. уровень сложности", True, YELLOW)
    screen.blit(next_level_text, (20, height - 75))


def draw_game_over(screen, width, height, player, game_manager):
    RED = (255, 50, 50)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)

    font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 28)
    tiny_font = pygame.font.SysFont(None, 24)

    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    # Статистика игры
    minutes = int(game_manager.game_time // 60)
    seconds = int(game_manager.game_time % 60)

    game_over_text = font.render("ИГРА ОКОНЧЕНА!", True, RED)
    stats_text = small_font.render(
        f"Время: {minutes:02d}:{seconds:02d} | Уровень: {player.level} | "
        f"Убийств: {player.total_kills} | Счет: {player.score}",
        True, WHITE
    )
    restart_text = small_font.render("R: рестарт, ESC: меню", True, WHITE)

    screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - 80))
    screen.blit(stats_text, (width // 2 - stats_text.get_width() // 2, height // 2 - 30))
    screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 20))

    # Рекорд сложности
    difficulty_text = tiny_font.render(
        f"Достигнутая сложность: Уровень {game_manager.difficulty_level} "
        f"(x{game_manager.experience_multiplier:.1f} опыт)",
        True, YELLOW
    )
    screen.blit(difficulty_text, (width // 2 - difficulty_text.get_width() // 2, height // 2 + 60))


def draw_level_up_screen(screen, width, height, player):
    BLUE = (50, 120, 255)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    GREEN = (50, 200, 50)

    font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 28)

    # Затемнение фона
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))

    # Заголовок
    title_text = font.render(f"ПОЗДРАВЛЯЕМ! Уровень {player.level}", True, YELLOW)
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 100))

    # Опции улучшений
    options = [
        {"type": "damage", "text": f"+10 урона (сейчас: {player.damage})", "key": "1"},
        {"type": "range", "text": f"+20 радиуса атаки (сейчас: {player.attack_range})", "key": "2"},
        {"type": "lifesteal", "text": f"+15% вампиризма (сейчас: {player.lifesteal}%)", "key": "3"}
    ]

    for i, option in enumerate(options):
        y_pos = 200 + i * 80
        # Фон опции
        pygame.draw.rect(screen, (50, 50, 70), (width // 2 - 200, y_pos, 400, 60), border_radius=10)
        pygame.draw.rect(screen, BLUE, (width // 2 - 200, y_pos, 400, 60), 3, border_radius=10)

        # Текст опции
        option_text = small_font.render(option["text"], True, WHITE)
        screen.blit(option_text, (width // 2 - option_text.get_width() // 2, y_pos + 15))

        # Клавиша выбора
        key_text = small_font.render(f"Нажмите {option['key']}", True, GREEN)
        screen.blit(key_text, (width // 2 - key_text.get_width() // 2, y_pos + 40))
