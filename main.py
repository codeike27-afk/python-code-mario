# main.py
import pygame
import sys
from settings import *
from sprites import Player
from levels import create_level_1

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Super Mario Clone")
    clock = pygame.time.Clock()

    # 创建游戏对象
    player = Player(50, SCREEN_HEIGHT - 150)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # 加载关卡
    platforms, enemies = create_level_1()
    all_sprites.add(platforms)
    all_sprites.add(enemies)

    # 摄像机偏移量
    camera_offset_x = 0

    running = True
    while running:
        # 1. 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # 2. 更新逻辑
        player.update(keys, platforms)
        enemies.update()

        # 简单的敌人碰撞检测
        hits = pygame.sprite.spritecollide(player, enemies, False)
        if hits:
            # 简单处理：碰到敌人就重置
            player.rect.x = 50
            player.rect.y = SCREEN_HEIGHT - 150
            player.vel_y = 0
            camera_offset_x = 0

        # 摄像机跟随逻辑 (当玩家超过屏幕中间时移动摄像机)
        if player.rect.x > SCREEN_WIDTH / 2:
            diff = player.rect.x - SCREEN_WIDTH / 2
            camera_offset_x += diff
            player.rect.x = SCREEN_WIDTH / 2 # 保持玩家在屏幕相对位置
            
            # 移动所有其他物体以产生摄像机效果
            for sprite in all_sprites:
                if sprite != player:
                    sprite.rect.x -= diff

        # 3. 绘制
        screen.fill(SKY_BLUE)
        
        # 绘制所有精灵
        for sprite in all_sprites:
            # 只有当精灵在屏幕可见范围内才绘制（优化性能，可选）
            if sprite.rect.x + sprite.rect.width > 0 and sprite.rect.x < SCREEN_WIDTH:
                screen.blit(sprite.image, sprite.rect)

        # 绘制UI信息
        font = pygame.font.SysFont(None, 24)
        info_text = font.render(f"Pos: {int(player.rect.x + camera_offset_x)}, Use Arrows to Move, Space to Jump", True, BLACK)
        screen.blit(info_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
