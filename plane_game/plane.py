from plane_settings import *
from player import Player
from rock import Rock
# from empty import Enemy
 
# 初始化 pygame
pygame.init()
screen = pygame.display.set_mode((1371, length))
pygame.display.set_caption("Plane shoot")
clock = pygame.time.Clock() 

# 載圖片
background = pygame.image.load("plane_game/img/background.png").convert()
background = pygame.transform.scale(background, (1371, length))  # 確保背景大小與視窗一致
rock_image = pygame.image.load("plane_game/img/rock.png").convert_alpha()
player_image = pygame.image.load("plane_game/img/player.png").convert_alpha()
bullet_image = pygame.image.load("plane_game/img/bullet3.png").convert_alpha()
enemy_image = pygame.image.load("plane_game/img/player.png").convert_alpha()

all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
 
# 建立玩家物件
player = Player(player_image)
all_sprites.add(player)
# 建立石頭物件
for _ in range(rocket_number):  # 生成 8 顆岩石
    rock = Rock(rock_image)
    all_sprites.add(rock)
    rocks.add(rock)   

# 定義子彈類別
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speedx=0, speedy=-10, image=None, color=(255, 255, 255)):
        super(Bullet, self).__init__()
        if image:
            self.image = image
        else:
            self.image = pygame.Surface((8, 16))
            self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speedx = speedx
        self.speedy = speedy

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.bottom < 0 or self.rect.top > length or self.rect.right < 0 or self.rect.left > 1371:
            self.kill()


# 建立 sprite 群組
bullets = pygame.sprite.Group()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, player):
        super(Enemy, self).__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 1371 - self.rect.width)
        self.rect.y = random.randint(-100, 300)
        self.speedx = random.uniform(-3, 3)  # 初始化速度
        self.speedy = random.uniform(-3, 3)  # 初始化速度
        self.player = player
        self.last_speed_update = pygame.time.get_ticks()  # 上次更新速度的時間
        self.last_shoot_time = pygame.time.get_ticks()

    def update(self):
         # 更新位置
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # 邊界檢測與反彈
        if self.rect.left <= 0 or self.rect.right >= 1371:
            self.speedx = -self.speedx
            self.rect.x += self.speedx
        if self.rect.top <= 0 or self.rect.bottom >= length:
            self.speedy = -self.speedy
            self.rect.y += self.speedy

        # 設定速度更新間隔 (3秒)
        now = pygame.time.get_ticks()
        if now - self.last_speed_update > 2500:  # 每3秒更新一次速度
            self.speedx = random.uniform(-5, 5)
            self.speedy = random.uniform(-5, 5)
            if abs(self.speedx) < 1:
                self.speedx = random.choice([-1, 1]) * random.uniform(1, 3)
            if abs(self.speedy) < 1:
                self.speedy = random.choice([-1, 1]) * random.uniform(1, 3)
            self.last_speed_update = now

        # 發射子彈
        now = pygame.time.get_ticks()
        if now - self.last_shoot_time > 500:  # 每秒發射一顆子彈
            self.shoot()
            self.last_shoot_time = now

    def shoot(self):
        direction = pygame.math.Vector2(
            self.player.rect.centerx - self.rect.centerx,
            self.player.rect.centery - self.rect.centery
        ).normalize()
        bullet = Bullet(
            x=self.rect.centerx,
            y=self.rect.centery,
            speedx=direction.x * 5,
            speedy=direction.y * 5,
            color=(255, 0, 0)
        )
        all_sprites.add(bullet)
        enemy_bullets.add(bullet)


enemy = Enemy(enemy_image, player)
all_sprites.add(enemy)


#  主遊戲循環
running = True
while running:
    clock.tick(fps)  # 控制遊戲速度為 60 FPS    
    # 事件處理邏輯
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == 27):
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == 32:
                # 發射子彈
                bullet = Bullet(player.rect.centerx, player.rect.top, speedy=-10, image=bullet_image) 
                all_sprites.add(bullet)
                bullets.add(bullet)

    # 更新所有精靈
    all_sprites.update()

    # 玩家與岩石的碰撞檢測
    player_hits = pygame.sprite.spritecollide(player, rocks, True)
    if player_hits:
        running = False  # 玩家死亡或遊戲結束

    # 子彈與岩石的碰撞檢測
    bullet_hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in bullet_hits:
        new_rock = Rock(rock_image)
        all_sprites.add(new_rock)
        rocks.add(new_rock)
    
    # 更新背景位置
    bg_y1 += down_offset  
    bg_y2 += down_offset  
    if bg_y1 >= length:
        bg_y1 = bg_y2 - length
    if bg_y2 >= length:
        bg_y2 = bg_y1 - length

    # 畫面繪製
    try :
        screen.blit(background, (0, bg_y1))  # 繪製第一張背景
        screen.blit(background, (0, bg_y2))  # 繪製第二張背景
    except:
        screen.fill((0, 0, 0))  # 如果沒有背景圖片，填充黑色背景

    all_sprites.draw(screen)  # 繪製所有精靈
    pygame.display.flip()  # 更新畫面