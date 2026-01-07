import pygame
from utils import load_sprite_sheets


class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets(
        "MainCharacters", "MaskDude", None, 32, 32, True)
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__()
        self.sprite = self.SPRITES["idle_right"][0]
        self.rect = self.sprite.get_rect(topleft=(x, y))
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.appearing = False
        self.disappearing = False
        self.fade_alpha = 0
        self.on_platform = False
        self.platform = None


    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        self.hit = True

    def start_teleport(self, portal):
        self.disappearing = True
        self.appearing = False
        self.animation_count = 0
        self.teleport_target = (portal.target_x, portal.target_y)

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.y_vel *= -0.5

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.disappearing:
            sprite_sheet = "disappearing"
        elif self.appearing:
            sprite_sheet = "appearing"
        elif self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            sprite_sheet = "jump" if self.jump_count == 1 else "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
        if self.on_platform and self.platform:
            self.rect.x += self.platform.delta_x
            self.rect.y += self.platform.delta_y

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps:
            self.hit = False
            self.hit_count = 0
        self.fall_count += 1
        if self.disappearing:
            self.fade_alpha = min(255, self.fade_alpha + 15)
            self.animation_count += 1
            if self.animation_count >= 21:
                self.disappearing = False
                self.rect.topleft = self.teleport_target
                self.animation_count = 0
                self.appearing = True
        elif self.appearing:
            self.fade_alpha = max(0, self.fade_alpha - 15)
            self.animation_count += 1
            if self.animation_count >= 21:
                self.appearing = False
                self.animation_count = 0
        else:
            self.fade_alpha = 0
        self.update_sprite()
