import pygame
import random
from .plane_settings import *

class Rock(pygame.sprite.Sprite):
    def __init__(self, rock_image):
        super(Rock, self).__init__()
        if rock_image:
            self.image = rock_image  # 使用載入的 rock.png
        else:
            self.image = pygame.Surface((30, 30))
            self.image.fill((255, 0, 0))  # 紅色
        self.rect = self.image.get_rect()

        # 隨機生成岩石的初始位置
        self.rect.x = random.randint(0, 1371 - self.rect.width)  # 與螢幕寬度一致
        self.rect.y = random.randint(-100, -40)  # 出現在螢幕上方外
        self.speedy = random.randint(3, 8)  # 縱向速度
        self.speedx = random.randint(-2, 2)  # 橫向速度

    def update(self):
        # 移動岩石
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        # 檢查橫向邊界，讓岩石反彈
        if self.rect.left < 0:  # 左邊界
            self.rect.left = 0
            self.speedx *= -1
        if self.rect.right > 1371:  # 右邊界
            self.rect.right = 1371
            self.speedx *= -1

        # 如果岩石超出下邊界，重新生成在上方
        if self.rect.top > 900:  # 視窗高度為 900
            self.rect.x = random.randint(0, 1371 - self.rect.width)  # 隨機橫向位置
            self.rect.y = random.randint(-100, -40)  # 重置到螢幕上方外
            self.speedy = random.randint(3, 8)  # 重新生成縱向速度
            self.speedx = random.randint(-2, 2)  # 重新生成橫向速度
 