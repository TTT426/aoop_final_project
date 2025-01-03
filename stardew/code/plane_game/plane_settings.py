import pygame
import random
            
fps = 60
length = 720

# 初始化背景初始位置
bg_y1 = 0  # 第一張背景起始位置
bg_y2 = -length  # 第二張背景緊接在第一張背景上方

down_offset = 0.5

rocket_number = 10

enemy_bullets = pygame.sprite.Group()  # 公用的敵人子彈群組
all_sprites = pygame.sprite.Group()  # 公用的所有精靈群組

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
screen_width, screen_height = 1280, 720