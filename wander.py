import pygame
from pygame.math import Vector2
import random
from settings import *
from creature import *

# 初始化 Pygame
pygame.init()

# 创建屏幕
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Moving to New Target Example")

# 创建精灵组、创建自定义精灵对象
sheeps = [Sheep(initial_position=(random.randint(0, SCREEN_WIDTH // 2), random.randint(0, SCREEN_HEIGHT // 2))) for _ in range(SHEEP_NUMS)]

# 创建狼群，生成头狼位置，围绕头狼生成狼群
alpha_wolf_position = (random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH), random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT))

alpha_wolf = AlphaWolf(initial_position=alpha_wolf_position,)

normal_wolves = [NormalWolf(initial_position=(min(alpha_wolf_position[0]+random.randint(-WOLVES_RADIUS, WOLVES_RADIUS), SCREEN_WIDTH), min(alpha_wolf_position[1]+random.randint(-WOLVES_RADIUS, WOLVES_RADIUS), SCREEN_HEIGHT))) for _ in range(WOLVES_NUMS)]

wolves = normal_wolves+[alpha_wolf]

all_sprites = pygame.sprite.Group(sheeps + wolves)

# 游戏主循环
running = True
clock = pygame.time.Clock()
selected_sprites = []
dragging = False
drag_start = None
drag_end = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # 左键按下
            dragging = True
            drag_start = pygame.mouse.get_pos()
            drag_end = drag_start
            selected_sprites.clear()
            for sprite in all_sprites:
                sprite.selected = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if event.pos:
                right_click_position = Vector2(event.pos)
                for wolf in wolves:
                    if wolf.selected:
                        wolf.target = right_click_position
                        wolf.focus_move = True
                
        
        if event.type == pygame.MOUSEMOTION:
            if dragging:
                drag_end = pygame.mouse.get_pos()


        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            dragging = False
            for sprite in all_sprites:
                if sprite.rect.colliderect(pygame.Rect(drag_start, drag_end)):
                    sprite.selected = True
                    selected_sprites.append(sprite)
    
    # 更新头狼
    alpha_wolf.update(sheeps=sheeps, wolves=normal_wolves, alpha_wolf=alpha_wolf)

    # 更新其他狼
    for wolf in normal_wolves:
        wolf.update(sheeps=sheeps, wolves=normal_wolves, alpha_wolf=alpha_wolf)

    # 更新羊
    for sheep in sheeps:
        sheep.update()
    
    # 清空屏幕
    screen.fill(GREEN)
    
    for sprite in all_sprites:
        pygame.draw.line(screen, BLUE, sprite.position, sprite.target, 2)

    # 绘制精灵
    all_sprites.draw(screen)
    
    if dragging:
        pygame.draw.rect(screen, WHITE, (drag_start[0], drag_start[1], drag_end[0] - drag_start[0], drag_end[1] - drag_start[1]), 1)


    # 刷新屏幕
    pygame.display.flip()
    
    clock.tick(FPS)

# 退出 Pygame
pygame.quit()
