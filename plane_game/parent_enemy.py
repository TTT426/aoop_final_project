import pygame
import random
from plane_settings import *

class Parent_Enemy(pygame.sprite.Sprite):
        def __init__(self, image, Master):
            super(Parent_Enemy, self).__init__()
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.x = random.randint(0, screen_width - self.rect.width)
            self.rect.y = random.randint(0, 500)
            self.speedx = random.uniform(-3, 3)  # 初始化速度
            self.speedy = random.uniform(-3, 3)  # 初始化速度
            self.Master = Master
            self.last_speed_update = pygame.time.get_ticks()  # 上次更新速度的時間
            self.last_shoot_time = pygame.time.get_ticks()
            self.health = 8  # 初始血量設為 8 格
            self.max_health = 8  # 設置最大血量為 8
            self.invincible = False  # 是否處於無敵狀態
            self.last_hit_time = pygame.time.get_ticks()  # 上次受傷時間

        def update(self):
            # 更新位置
            self.rect.x += self.speedx
            self.rect.y += self.speedy

            # 邊界檢測與反彈
            if self.rect.left <= 0 or self.rect.right >= screen_width:
                self.speedx = -self.speedx
                self.rect.x += self.speedx
            if self.rect.top <= 0 or self.rect.bottom >= length:
                self.speedy = -self.speedy
                self.rect.y += self.speedy

            now = pygame.time.get_ticks()
            if now - self.last_speed_update > 2000:  # 每2秒更新一次速度
                self.speedx = random.uniform(-5, 5)
                self.speedy = random.uniform(-5, 5)
                if abs(self.speedx) < 1:
                    self.speedx = random.choice([-1, 1]) * random.uniform(1, 3)
                if abs(self.speedy) < 1:
                    self.speedy = random.choice([-1, 1]) * random.uniform(1, 3)
                self.last_speed_update = now

            # 發射子彈
            now = pygame.time.get_ticks()
            if now - self.last_shoot_time > 750:  # 每0.75發射一顆子彈
                self.shoot()
                self.last_shoot_time = now

            now = pygame.time.get_ticks()
            if self.invincible and now - self.last_hit_time > 500:  # 無敵時間結束
                self.invincible = False
            
        def draw_health_bar(self, surface):
            # 設定血量條的寬度和高度
            bar_width = 40
            bar_height = 5
            fill = (self.health / self.max_health) * bar_width  # 根據最大血量比例填充
            border_color = (255, 255, 255)  # 外框顏色
            fill_color = (255, 0, 0)  # 血量條顏色

            # 計算血量條的位置
            bar_x = self.rect.centerx - bar_width // 2
            bar_y = self.rect.top - 10  # 在敵人上方顯示

            # 畫出血量條
            pygame.draw.rect(surface, fill_color, (bar_x, bar_y, fill, bar_height))
            pygame.draw.rect(surface, border_color, (bar_x, bar_y, bar_width, bar_height), 1)

        def take_damage(self, amount):
            now = pygame.time.get_ticks()
            if not self.invincible and now - self.last_hit_time > 500:  # 無敵冷卻 1 秒
                self.health -= amount
                self.last_hit_time = now
                if self.health <= 0:
                    self.health = 0
                    print("Enemy is dead!")
                    self.kill()
                # 啟動無敵狀態
                self.invincible = True