import pygame
from utils import get_background
from settings import PIXEL_FONT, PIXEL_FONT_MEDIUM, PIXEL_FONT_LARGE, COLOR_BLACK, COLOR_WHITE, COLOR_YELLOW, COLOR_LIGHT_GRAY, WIDTH, HEIGHT


def main_menu(window):
    running = True
    clock = pygame.time.Clock()
    selected_option = 0
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w]:
                    selected_option = 0
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    selected_option = 1
                elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    return selected_option == 0
                elif event.key == pygame.K_ESCAPE:
                    return False
        mm_bg_tiles, mm_bg_img = get_background("Gray.png")
        for tile in mm_bg_tiles:
            window.blit(mm_bg_img, tile)
        title_shadow = PIXEL_FONT_LARGE.render(
            "Pixel Climber", True, COLOR_BLACK)
        title_text = PIXEL_FONT_LARGE.render(
            "Pixel Climber", True, COLOR_WHITE)
        title_rect = title_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 - 150))
        window.blit(title_shadow, (title_rect.x + 4, title_rect.y + 4))
        window.blit(title_text, title_rect)
        play_color = COLOR_YELLOW if selected_option == 0 else COLOR_LIGHT_GRAY
        play_text_shadow = PIXEL_FONT_MEDIUM.render("GRAJ", True, COLOR_BLACK)
        play_text = PIXEL_FONT_MEDIUM.render("GRAJ", True, play_color)
        play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        if selected_option == 0:
            indicator = PIXEL_FONT_MEDIUM.render(">", True, COLOR_YELLOW)
            window.blit(indicator, (play_rect.x - 40, play_rect.y))
        window.blit(play_text_shadow, (play_rect.x + 2, play_rect.y + 2))
        window.blit(play_text, play_rect)
        quit_color = COLOR_YELLOW if selected_option == 1 else COLOR_LIGHT_GRAY
        quit_text_shadow = PIXEL_FONT_MEDIUM.render("WYJDŹ", True, COLOR_BLACK)
        quit_text = PIXEL_FONT_MEDIUM.render("WYJDŹ", True, quit_color)
        quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
        if selected_option == 1:
            indicator = PIXEL_FONT_MEDIUM.render(">", True, COLOR_YELLOW)
            window.blit(indicator, (quit_rect.x - 40, quit_rect.y))
        window.blit(quit_text_shadow, (quit_rect.x + 2, quit_rect.y + 2))
        window.blit(quit_text, quit_rect)
        controls = ["STEROWANIE:", "Strzałki / WASD - ruch",
                    "SPACJA / Strzałka w górę - skok", "ENTER - wybierz"]
        y_offset = HEIGHT // 2 + 180
        for line in controls:
            control_shadow = PIXEL_FONT.render(line, True, COLOR_BLACK)
            control_text = PIXEL_FONT.render(line, True, COLOR_WHITE)
            control_rect = control_text.get_rect(center=(WIDTH // 2, y_offset))
            window.blit(control_shadow,
                        (control_rect.x + 1, control_rect.y + 1))
            window.blit(control_text, control_rect)
            y_offset += 25
        pygame.display.update()
