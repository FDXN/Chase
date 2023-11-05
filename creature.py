import pygame
from pygame.math import Vector2
import random
from settings import *

# 自定义精灵类
class Creature(pygame.sprite.Sprite):
    def __init__(self, initial_position):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.rect = self.image.get_rect()
        self.velocity = Vector2(0, 0)
        if initial_position:
            self.position = Vector2(initial_position)
        else:
            self.position = Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.wander_radius = 10  # 徘徊半径
        self.target = self.position
        self.current_time = pygame.time.get_ticks()
        self.change_target_interval = self.get_random_interval()  # 时间间隔（毫秒）
        self.last_target_change = 0
        self.actual_speed = Vector2(0, 0)
        self.first_update = True
        self.hunger = 0
        self.food = 0
        self.speed = 0
        self.is_wandering = True
        self.selected = False

    def get_random_interval(self):
        return random.randint(3000, 4500)
    
    def time_check(self):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.last_target_change > self.change_target_interval:
            return True
        else:
            return False
    
    def wandering(self):
        # 检查是否需要更换目标
        if self.time_check():
            self.target = self.get_random_target()
            self.last_target_change = self.current_time
            self.change_target_interval = self.get_random_interval()
    
    def get_random_target(self):
        # 获得随机目标
        x = random.randint(max(0, int(self.position.x - self.wander_radius)), min(SCREEN_WIDTH, int(self.position.x + self.wander_radius)))
        y = random.randint(max(0, int(self.position.y - self.wander_radius)), min(SCREEN_HEIGHT, int(self.position.y + self.wander_radius)))
        return Vector2(x, y)

    def move2target(self):
        # 更新位置
        self.position += self.velocity
        self.rect.topleft = (int(self.position.x), int(self.position.y))
        
        # 移动到目标位置
        self.actual_speed = self.target - self.position
        if self.actual_speed.length() != 0:
            self.actual_speed.normalize_ip()
        self.velocity = self.actual_speed * self.speed

        # 计算朝向新目标的速度向量
        direction = self.target - self.position

        if direction.length() < self.actual_speed.length():
            # 当精灵非常接近目标时，直接设置为目标位置，避免抖动
            self.position = self.target
            self.velocity = Vector2(0, 0)

    def update(self):
        # 生物始终移动到目标位置
        self.move2target()
        self.food -= self.speed * 0.01

class Sheep(Creature):
    def __init__(self, initial_position):
        super().__init__(initial_position)
        self.position = Vector2(initial_position)
        self.image = pygame.image.load(SHEEP_IMAGE_PATH)
        self.speed = SHEEP_SPEED

    def update(self):
        super().update()
        if self.is_wandering:
            self.wandering()
           

class Wolf(Creature):
    def __init__(self, initial_position):
        super().__init__(initial_position)
        self.is_hunting = False
        self.focus_move = False
        self.speed = WOLF_SPEED

    def wandering_around_alpha(self, alpha_wolf):
        # 计算狼到头狼的距离和方向
        direction = alpha_wolf.position - self.position
        distance_to_alpha_wolf = direction.length()

        if distance_to_alpha_wolf > WOLVES_RADIUS:
            self.target = alpha_wolf.position
        else:
            if self.time_check():
                self.wandering()
    
    def check_collision_with_sheep(self, sheeps, wolves, alpha_wolf):
        for sheep in sheeps:
            if pygame.sprite.collide_rect(self, sheep):
                self.food += 1
                alpha_wolf.food += 2
                sheeps.remove(sheep)  # 从羊的精灵组中移除被碰到的羊
                sheep.kill()  # 从精灵组中移除并删除羊的图像
                for wolf in wolves:
                    wolf.is_hunting = False
                    wolf.food += (SHEEP_MEAT - 3)/len(wolves)
    
    def update(self, sheeps, wolves, alpha_wolf):
        super().update()
        self.check_collision_with_sheep(sheeps, wolves, alpha_wolf)
        # 速度为零时即抵达位置，强制位移取消
        if self.velocity == (0, 0):
            self.focus_move = False

class NormalWolf(Wolf):
    def __init__(self, initial_position):
        self.position = Vector2(initial_position)
        super().__init__(initial_position)
        self.image = pygame.image.load(WOLVES_IMAGE_PATH)
        
    def update(self, alpha_wolf, sheeps, wolves):
        super().update(sheeps, wolves, alpha_wolf)
        if not self.focus_move:
            if self.is_hunting:
                self.target = alpha_wolf.target
            else:
                self.wandering_around_alpha(alpha_wolf)
        if self.selected:
            self.image = pygame.image.load(WOLVES_SELECTED_IMAGE_PATH)
        else:
            self.image = pygame.image.load(WOLVES_IMAGE_PATH)
        
class AlphaWolf(Wolf):
    def __init__(self, initial_position):
        super().__init__(initial_position)
        self.position = Vector2(initial_position)
        self.image = pygame.image.load(ALPHA_WOLF_IMAGE_PATH)
    
    def locate_sheep(self, sheeps):
        closest_sheep = min(sheeps, key=lambda sheep: (self.position - sheep.position).length())
        self.target = closest_sheep.position
    
    def start_hunting(self, sheeps, wolves):
        if sheeps:
            self.is_hunting = True
            for wolf in wolves:
                wolf.is_hunting = True
            self.locate_sheep(sheeps)
            
    def update(self, sheeps, wolves, alpha_wolf):
        super().update(sheeps=sheeps, wolves=wolves, alpha_wolf=alpha_wolf)
        if not self.focus_move:
            self.wandering()
            if self.food < 0:
                self.start_hunting(sheeps, wolves)
            else:
                self.is_hunting = False
        if self.selected:
            self.image = pygame.image.load(ALPHA_WOLF_SELECTED_IMAGE_PATH)
        else:
            self.image = pygame.image.load(ALPHA_WOLF_IMAGE_PATH)