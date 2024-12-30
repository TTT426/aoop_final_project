# import pygame
from plane_settings import *

# from plane import *
class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, player):
        super(Enemy, self).__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 1371 - self.rect.width)  # 隨機位置
        self.rect.y = random.randint(-100, 300)  # 在螢幕上方外生成
        self.speedx = random.choice([-2, 2])  # 左右移動
        self.speedy = 2  # 向下移動速度
        self.player = player  # 傳入玩家對象
        self.last_shoot_time = pygame.time.get_ticks()

    def update(self):
        # 更新敵人位置
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # 碰到邊界反向
        if self.rect.right >= 1371 or self.rect.left <= 0:
            self.speedx = -self.speedx

        # 超出螢幕重新生成
        if self.rect.top > length:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, 1371 - self.rect.width)

        # 發射子彈
        now = pygame.time.get_ticks()
        if now - self.last_shoot_time > 1000:  # 每 1 秒發射一顆子彈
            self.shoot()
            self.last_shoot_time = now

    def shoot(self):
        # 生成敵人的子彈，追蹤玩家位置
        bullet = Bullet(self.rect.centerx, self.rect.bottom, speedy=5, color=(255, 0, 0))  # 紅色子彈
        all_sprites.add(bullet)
        enemy_bullets.add(bullet)
        

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super(EnemyBullet, self).__init__()
        self.image = pygame.Surface((8, 16))  # 子彈大小
        self.image.fill((255, 0, 0))  # 子彈顏色（紅色）
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.direction = direction

    def update(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        # 如果子彈超出螢幕，刪除
        if self.rect.bottom < 0 or self.rect.top > length or self.rect.right < 0 or self.rect.left > 1371:
            self.kill()
