from settings import FPS, PLAYER_VEL, window, WIDTH
from world import generate_world, handle_move, collect_coins
from ui import draw, draw_end_screen
from objects import Hearts
import pygame


def main_game(window):
    clock = pygame.time.Clock()
    from utils import get_background
    background, bg_image = get_background("Blue.png")
    block_size = 96
    player, objects, portal1, portal2 = generate_world(WIDTH, 800, block_size)
    offset_x = 0
    scroll_area_width = 400
    score = 0
    game_over = False
    level_completed = False
    hearts = Hearts(10, 30, 3)
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_RETURN:
                    return True
                elif not game_over:
                    if (event.key in [pygame.K_SPACE, pygame.K_UP, pygame.K_w]) and player.jump_count < 2:
                        player.jump()
                    elif event.key == pygame.K_ESCAPE:
                        return True
        if not game_over and not level_completed:
            player.loop(FPS)
            if player.appearing:
                offset_x = player.rect.x - WIDTH // 2
            for obj in objects:
                if hasattr(obj, "loop"):
                    obj.loop()
            handle_move(player, objects, portal1, portal2, hearts, PLAYER_VEL)
            score += collect_coins(player, objects)
            game_over = hearts.dead
            level_completed = any(
                obj.name == "checkpoint" and obj.animation_name == "CheckpointYes" for obj in objects)
            draw(window, background, bg_image, player,
                 objects, offset_x, score, hearts)
            if ((player.rect.right - offset_x >= WIDTH - scroll_area_width and player.x_vel > 0) or
                    (player.rect.left - offset_x <= scroll_area_width and player.x_vel < 0)):
                offset_x += player.x_vel
        else:
            if level_completed:
                draw_end_screen(window, background, bg_image,
                                score, message="YOU WIN")
            elif game_over:
                draw_end_screen(window, background, bg_image,
                                score, message="GAME OVER")
    return False
