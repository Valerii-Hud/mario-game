import pygame
pygame.init()

WIDTH, HEIGHT = 1200, 800
FPS = 60
PLAYER_VEL = 5

PIXEL_FONT = pygame.font.Font("assets/Fonts/pixel.ttf", 16)
PIXEL_FONT_MEDIUM = pygame.font.Font("assets/Fonts/pixel.ttf", 32)
PIXEL_FONT_LARGE = pygame.font.Font("assets/Fonts/pixel.ttf", 48)

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_LIGHT_GRAY = (200, 200, 200)

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Climber")
icon = pygame.image.load("assets/Items/Checkpoints/End/End.png")
pygame.display.set_icon(icon)
