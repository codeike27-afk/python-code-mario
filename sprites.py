# sprites.py
import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((24, 32))
        self.image.fill(RED)  # 红色代表马里奥
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.facing_right = True

    def update(self, keys, platforms):
        # 水平移动
        self.vel_x = 0
        if keys[pygame.K_LEFT]:
            self.vel_x = -PLAYER_SPEED
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.vel_x = PLAYER_SPEED
            self.facing_right = True

        # 跳跃
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -PLAYER_JUMP_POWER
            self.on_ground = False

        # 应用重力
        self.vel_y += GRAVITY
        
        # 更新位置并处理碰撞
        self.rect.x += self.vel_x
        self.collide_horizontal(platforms)
        
        self.rect.y += self.vel_y
        self.on_ground = False # 假设在空中，除非碰撞检测证明在地面
        self.collide_vertical(platforms)

        # 边界检查
        if self.rect.left < 0:
            self.rect.left = 0
        # 如果掉出屏幕底部，重置位置（简单处理）
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = 50
            self.rect.y = SCREEN_HEIGHT - 150
            self.vel_y = 0

    def collide_horizontal(self, platforms):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        for hit in hits:
            if self.vel_x > 0: # 向右移动
                self.rect.right = hit.rect.left
            elif self.vel_x < 0: # 向左移动
                self.rect.left = hit.rect.right

    def collide_vertical(self, platforms):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        for hit in hits:
            if self.vel_y > 0: # 下落
                self.rect.bottom = hit.rect.top
                self.vel_y = 0
                self.on_ground = True
            elif self.vel_y < 0: # 向上跳撞到顶部
                self.rect.top = hit.rect.bottom
                self.vel_y = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=BROWN):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, range_dist=100):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill(GREEN) # 绿色代表敌人
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.start_x = x
        self.range_dist = range_dist
        self.speed = 2
        self.direction = 1

    def update(self):
        self.rect.x += self.speed * self.direction
        
        # 简单的巡逻逻辑
        if self.rect.x > self.start_x + self.range_dist:
            self.direction = -1
        elif self.rect.x < self.start_x:
            self.direction = 1
