# levels.py
import pygame
from sprites import Platform, Enemy
from settings import TILE_SIZE

def create_level_1():
    """
    创建一个简单的关卡布局
    返回: platforms_group, enemies_group
    """
    platforms = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    # 地面
    ground_y = SCREEN_HEIGHT - TILE_SIZE * 2
    # 生成一段长地面
    for i in range(0, 2000, TILE_SIZE):
        p = Platform(i, ground_y, TILE_SIZE, TILE_SIZE * 2)
        platforms.add(p)

    # 一些悬浮平台
    platform_data = [
        (300, ground_y - 100, 3),
        (500, ground_y - 200, 2),
        (700, ground_y - 100, 4),
        (1000, ground_y - 150, 2),
        (1200, ground_y - 250, 3),
    ]

    for x, y, width_tiles in platform_data:
        p = Platform(x, y, TILE_SIZE * width_tiles, TILE_SIZE)
        platforms.add(p)

    # 添加敌人
    e1 = Enemy(400, ground_y - 32)
    e2 = Enemy(800, ground_y - 32)
    enemies.add(e1, e2)

    return platforms, enemies
