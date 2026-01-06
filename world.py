from player import Player
from objects import Block, Fire, Coin, Portal, Flag, Hearts
from utils import get_block


def generate_world(width, height, block_size):
    player = Player(20, 600, 50, 50)
    fire = Fire(100, height - block_size - 64, 16, 32)
    fire.on()
    coins = [Coin(400, height - block_size * 3 - 64, 16, 16),
             Coin(700, height - block_size * 2 - 80, 16, 16)]
    portal1 = Portal(475, height - block_size * 2 - 30,
                     60, 80, 800, height - block_size * 5)
    portal2 = Portal(650, height - block_size * 5 - 30,
                     60, 80, 400, height - block_size * 2)
    floor = [Block(i * block_size, height - block_size, block_size)
             for i in range(-width // block_size, (width * 2) // block_size)]
    vertical_blocks = [
        Block(block_size*6, height - block_size*n, block_size) for n in range(2, 10)]
    additional_objects = [*floor, Block(0, height - block_size * 2, block_size),
                          Block(block_size * 3, height -
                                block_size * 4, block_size),
                          Block(block_size * 7, height -
                                block_size * 4, block_size),
                          Block(block_size * 8, height -
                                block_size * 4, block_size),
                          Block(block_size * 12, height - block_size * 3, block_size), fire]
    objects = vertical_blocks + additional_objects + coins + [portal1, portal2]
    flag = Flag(width * 2 - 100, height - (block_size * 1.65) - 64, 64, 64)
    objects.append(flag)
    return player, objects, portal1, portal2


def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if obj.name != "coin" and player.rect.colliderect(obj.rect):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()
            collided_objects.append(obj)
    return collided_objects


def collide(player, objects, dx):
    player.move(dx, 0)
    collided_object = next(
        (obj for obj in objects if player.rect.colliderect(obj.rect)), None)
    player.move(-dx, 0)
    return collided_object


def handle_move(player, objects, portal1, portal2, hearts, PLAYER_VEL):
    import pygame
    keys = pygame.key.get_pressed()
    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not collide_left:
        player.move_left(PLAYER_VEL)
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not collide_right:
        player.move_right(PLAYER_VEL)
    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]
    for obj in to_check:
        if obj:
            if obj.name == "fire" and not player.hit:
                player.make_hit()
                hearts.set_health(hearts.current_health - 1)
                hearts.check_death()
            elif obj.name == "portal" and not player.disappearing and not player.appearing:
                player.start_teleport(obj)
            elif obj.name == "checkpoint" and not obj.activated:
                obj.finish()


def collect_coins(player, objects):
    import pygame
    to_remove = []
    collected = 0
    for obj in objects:
        if getattr(obj, "name", None) == "coin" and getattr(obj, "mask", None) and getattr(player, "mask", None):
            if pygame.sprite.collide_mask(player, obj):
                to_remove.append(obj)
                collected += 1
    for obj in to_remove:
        if obj in objects:
            objects.remove(obj)
    return collected
