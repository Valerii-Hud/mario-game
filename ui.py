import pygame
from utils import get_background
from settings import PIXEL_FONT, PIXEL_FONT_MEDIUM, PIXEL_FONT_LARGE, COLOR_BLACK, COLOR_WHITE, COLOR_YELLOW, WIDTH, HEIGHT


def draw(window, background, bg_image, player, objects, offset_x, score, hearts):
    for tile in background:
        window.blit(bg_image, tile)
    for obj in objects:
        obj.draw(window, offset_x)
    player.draw(window, offset_x)
    shadow = PIXEL_FONT.render("COINS: " + str(score), False, (COLOR_BLACK))
    window.blit(shadow, (12, 12))
    score_text = PIXEL_FONT.render(
        "COINS: " + str(score), False, (COLOR_WHITE))
    window.blit(score_text, (10, 10))
    hearts.draw(window)
    if player.fade_alpha > 0:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(player.fade_alpha)
        window.blit(overlay, (0, 0))
    pygame.display.update()


def draw_end_screen(window, background, bg_image, score, message="GAME OVER"):
    go_bg_tiles, go_bg_img = get_background("Gray.png")
    for tile in go_bg_tiles:
        window.blit(go_bg_img, tile)
    message_shadow = PIXEL_FONT_LARGE.render(message, False, COLOR_BLACK)
    message_text = PIXEL_FONT_LARGE.render(message, False, (255, 50, 50))
    message_rect = message_text.get_rect(
        center=(WIDTH // 2, HEIGHT // 2 - 100))
    window.blit(message_shadow, (message_rect.x + 3, message_rect.y + 3))
    window.blit(message_text, message_rect)
    score_shadow = PIXEL_FONT_MEDIUM.render(
        f"COINS: {score}", False, COLOR_BLACK)
    score_text = PIXEL_FONT_MEDIUM.render(
        f"COINS: {score}", False, COLOR_YELLOW)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    window.blit(score_shadow, (score_rect.x + 2, score_rect.y + 2))
    window.blit(score_text, score_rect)
    instruction_shadow = PIXEL_FONT.render(
        "Naciśnij ESC aby wrócić do menu", False, COLOR_BLACK)
    instruction_text = PIXEL_FONT.render(
        "Naciśnij ESC aby wrócić do menu", False, COLOR_WHITE)
    instruction_rect = instruction_text.get_rect(
        center=(WIDTH // 2, HEIGHT // 2 + 100))
    window.blit(instruction_shadow,
                (instruction_rect.x + 1, instruction_rect.y + 1))
    window.blit(instruction_text, instruction_rect)
    pygame.display.update()
