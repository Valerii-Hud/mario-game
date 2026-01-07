import pygame
from utils import load_sprite_sheets, get_block


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


class Hearts:
    def __init__(self, x, y, hearts=3):
        self.x = x
        self.y = y
        self.max_hearts = hearts
        self.current_health = hearts * 2
        self.dead = False
        self.sprites = load_sprite_sheets(
            "Menu", "Hearts", None, 32, 32, False, 3)["PixelHeart16"]

    def set_health(self, hp):
        self.current_health = max(0, min(hp, self.max_hearts * 2))

    def draw(self, win):
        for i in range(self.max_hearts):
            heart_x = self.x + i * 40
            heart_value = self.current_health - i * 2
            if heart_value >= 2:
                sprite = self.sprites[0]
            elif heart_value == 1:
                sprite = self.sprites[1]
            else:
                sprite = self.sprites[2]
            win.blit(sprite, (heart_x, self.y))

    def check_death(self):
        self.dead = self.current_health <= 0


class Fire(Object):
    ANIMATION_DELAY = 6

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", None, width, height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        self.mask = pygame.mask.from_surface(self.image)
        if self.animation_count // self.ANIMATION_DELAY >= len(sprites):
            self.animation_count = 0


class Flag(Object):
    ANIMATION_DELAY = 2

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "checkpoint")
        self.checkpoint = load_sprite_sheets(
            "Items", "Checkpoints", "Checkpoint", width, height)
        self.image = self.checkpoint["CheckpointNo"][0]
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.animation_count = 0
        self.animation_name = "CheckpointNo"
        self.activated = False

    def finish(self):
        self.animation_name = "Checkpoint"
        self.animation_count = 0
        self.activated = True

    def loop(self):
        sprites = self.checkpoint[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        if self.animation_count >= 52:
            self.animation_name = "CheckpointYes"
            self.animation_count = 0
        if self.animation_count // self.ANIMATION_DELAY >= len(sprites):
            self.animation_count = 0


class Coin(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "coin")
        self.coin = load_sprite_sheets("Items", "Coins", None, width, height)
        self.animation_name = "coin"
        self.image = self.coin[self.animation_name][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.animation_count = 0

    def loop(self):
        sprites = self.coin[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        self.mask = pygame.mask.from_surface(self.image)
        if self.animation_count // self.ANIMATION_DELAY >= len(sprites):
            self.animation_count = 0


class Portal(Object):
    ANIMATION_DELAY = 6

    def __init__(self, x, y, width, height, target_x, target_y, flip_horizontal=False):
        super().__init__(x, y, width, height, "portal")
        self.portal = load_sprite_sheets(
            "Items", "Portals", None, width, height, False, 8)
        self.image = self.portal["idle"][0]
        self.animation_count = 0
        self.animation_name = "idle"
        self.target_x = target_x
        self.target_y = target_y
        self.flip_horizontal = flip_horizontal
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collision_rect = pygame.Rect(
            self.rect.centerx - 15,
            self.rect.y + 10,
            30,
            self.rect.height - 20
        )

    def appear(self):
        self.animation_name = "appear"

    def disappear(self):
        self.animation_name = "disappear"

    def loop(self):
        sprites = self.portal[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        if self.animation_count // self.ANIMATION_DELAY >= len(sprites):
            self.animation_count = 0
        self.collision_rect.center = self.rect.center


class MovingPlatform(Object):
    def __init__(self, x, y, block_size, path, speed=2):
        width = block_size * 3
        height = block_size
        super().__init__(x, y, width, height, "moving_platform")

        self.path = path
        self.speed = speed
        self.target_index = 0

        self.delta_x = 0
        self.delta_y = 0

        for i in range(3):
            block = get_block(block_size)
            self.image.blit(block, (i * block_size, 0))

        self.mask = pygame.mask.from_surface(self.image)
    def loop(self):
        old_x = self.rect.x
        old_y = self.rect.y

        target_x, target_y = self.path[self.target_index]
        dx = target_x - self.rect.x
        dy = target_y - self.rect.y
        dist = (dx ** 2 + dy ** 2) ** 0.5

        if dist < self.speed or dist == 0:
            self.rect.topleft = (target_x, target_y)
            self.target_index = (self.target_index + 1) % len(self.path)
        else:
            self.rect.x += self.speed * dx / dist
            self.rect.y += self.speed * dy / dist

        self.delta_x = self.rect.x - old_x
        self.delta_y = self.rect.y - old_y


class Spike(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "spike")
        self.image.fill((0, 0, 0, 0))
        points = [(0, height), (width // 2, 0), (width, height)]
        pygame.draw.polygon(self.image, (200, 0, 0), points)
        self.mask = pygame.mask.from_surface(self.image)

