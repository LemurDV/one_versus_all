import pygame
import random
from player import Player
from enemy import Enemy
from screen_settings import draw_ui, draw_game_over, draw_level_up_screen
from menu import MainMenu
from game_manager import GameManager

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Герой против врагов - Прогрессирующая сложность")

# Цвета
BLACK = (20, 20, 30)

# Состояния игры
MAIN_MENU = 0
GAMEPLAY = 1
LEVEL_UP = 2
GAME_OVER = 3

game_state = MAIN_MENU
player = None
enemies = []
enemy_spawn_timer = 0
main_menu = MainMenu(WIDTH, HEIGHT)
game_manager = GameManager()

# Таймер для отслеживания времени
clock = pygame.time.Clock()
running = True
last_time = pygame.time.get_ticks()

while running:
    current_time = pygame.time.get_ticks()
    dt = (current_time - last_time) / 1000.0  # Дельта времени в секундах
    last_time = current_time

    mouse_pos = pygame.mouse.get_pos()

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == MAIN_MENU:
            result = main_menu.handle_input(event)
            if result == "exit":
                running = False
            elif result in ["axe", "bow"]:
                player = Player(result)
                game_state = GAMEPLAY
                enemies = []
                game_manager.reset()  # Сбрасываем менеджер игры
                enemy_spawn_timer = 0

        elif game_state == GAMEPLAY:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not player.is_attacking:
                    player.attack(enemies, mouse_pos, game_manager.experience_multiplier)
                elif event.key == pygame.K_ESCAPE:
                    game_state = MAIN_MENU

        elif game_state == LEVEL_UP:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    player.apply_upgrade("damage")
                    game_state = GAMEPLAY
                elif event.key == pygame.K_2:
                    player.apply_upgrade("range")
                    game_state = GAMEPLAY
                elif event.key == pygame.K_3:
                    player.apply_upgrade("lifesteal")
                    game_state = GAMEPLAY
                elif event.key == pygame.K_4:
                    player.apply_upgrade("speed")
                    game_state = GAMEPLAY

        elif game_state == GAME_OVER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    player = Player(player.weapon_type)
                    enemies = []
                    game_state = GAMEPLAY
                    game_manager.reset()
                elif event.key == pygame.K_ESCAPE:
                    game_state = MAIN_MENU

    # Обновление игры в зависимости от состояния
    if game_state == MAIN_MENU:
        main_menu.draw(screen)

    elif game_state == GAMEPLAY:
        # Обновляем менеджер игры (время и сложность)
        game_manager.update(dt)

        # Движение игрока
        keys = pygame.key.get_pressed()
        player.move(keys, WIDTH, HEIGHT)

        # Обновление снарядов (для лука)
        if player.weapon_type == "bow":
            player.update_projectiles(enemies)

        # Спавн врагов с учетом текущей сложности
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= game_manager.enemy_spawn_rate:
            enemies.append(Enemy(WIDTH, HEIGHT))
            enemy_spawn_timer = 0

        # Обновление врагов
        for enemy in enemies[:]:
            enemy.move(player.x, player.y)
            enemy.check_collision(player)
            if enemy.health <= 0 or enemy.is_out_of_bounds():
                if enemy in enemies:
                    enemies.remove(enemy)
                    if enemy.health <= 0:
                        player.score += 10

        # Проверка на получение уровня
        if player.gain_experience(0, game_manager.experience_multiplier):
            player.level_up()
            game_state = LEVEL_UP

        # Проверка здоровья игрока
        if not player.update():
            game_state = GAME_OVER

        # Отрисовка геймплея
        screen.fill(BLACK)
        for enemy in enemies:
            enemy.draw(screen)
        player.draw(screen)
        player.draw_health_bar(screen)
        draw_ui(screen, player, enemies, WIDTH, HEIGHT, game_manager)

        # Подсказка для лука
        if player.weapon_type == "bow":
            font = pygame.font.SysFont(None, 20)
            hint_text = font.render("Атакуйте щелчком мыши в направлении врагов", True, (200, 200, 0))
            screen.blit(hint_text, (WIDTH // 2 - hint_text.get_width() // 2, HEIGHT - 60))

    elif game_state == LEVEL_UP:
        # Отрисовка фона геймплея
        screen.fill(BLACK)
        for enemy in enemies:
            enemy.draw(screen)
        player.draw(screen)
        player.draw_health_bar(screen)
        draw_ui(screen, player, enemies, WIDTH, HEIGHT, game_manager)

        # Отрисовка экрана улучшений
        draw_level_up_screen(screen, WIDTH, HEIGHT, player)

    elif game_state == GAME_OVER:
        # Отрисовка фона геймплея
        screen.fill(BLACK)
        for enemy in enemies:
            enemy.draw(screen)
        player.draw(screen)
        player.draw_health_bar(screen)
        draw_ui(screen, player, enemies, WIDTH, HEIGHT, game_manager)

        # Отрисовка экрана завершения игры
        draw_game_over(screen, WIDTH, HEIGHT, player, game_manager)

    # Обновление экрана
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
