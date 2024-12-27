import pygame
import random
from plane_settings import *
 
# 初始化 pygame
pygame.init()
screen = pygame.display.set_mode((1371, length))
pygame.display.set_caption("Plane shoot")
clock = pygame.time.Clock() 

# 載圖片
background = pygame.image.load("img/background.png").convert()
background = pygame.transform.scale(background, (1371, length))  # 確保背景大小與視窗一致
rock_image = pygame.image.load("img/rock.png").convert_alpha()
player_image = pygame.image.load("img/player.png").convert_alpha()

# 定義玩家類別
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = player_image  # 使用載入的 rock.png
        self.rect = self.image.get_rect()
        self.rect.centerx = 250
        self.rect.top = 550

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5

        # 確保玩家不會超出視窗邊界
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 1371:
            self.rect.right = 1371
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > length:
            self.rect.bottom = length

# 定義岩石類別
class Rock(pygame.sprite.Sprite):
    def __init__(self):
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
 
# 定義子彈類別
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Bullet, self).__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill((255, 255, 0))  # 黃色，對比度更高
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # 如果子彈超出上邊界，移除它
        if self.rect.bottom < 0:
            self.kill()

# 建立 sprite 群組
all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# 建立玩家物件
player = Player()
all_sprites.add(player)

# 建立岩石物件
for _ in range(rocket_number):  # 生成 8 顆岩石
    rock = Rock()
    all_sprites.add(rock)
    rocks.add(rock)


# 主遊戲循環
running = True
while running:
    clock.tick(fps)  # 控制遊戲速度為 60 FPS
    
    # 事件處理邏輯
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == 27):
            running = False
        elif event.type == pygame.KEYDOWN:
            print("事件捕捉，按鍵值:", event.key)  # 打印捕捉到的按键值
            if event.key == 32:
                print("空白鍵被按下")  # 用於調試
                # 發射子彈
                for i in range(2):
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)


    # 更新所有精靈
    all_sprites.update()

    # 玩家與岩石的碰撞檢測
    player_hits = pygame.sprite.spritecollide(player, rocks, True)
    if player_hits:
        print("玩家與岩石碰撞！")
        running = False  # 玩家死亡或遊戲結束

    # 子彈與岩石的碰撞檢測
    bullet_hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in bullet_hits:
        print("子彈擊中岩石")  # 用於調試
        new_rock = Rock()
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
    if background:
        screen.blit(background, (0, bg_y1))  # 繪製第一張背景
        screen.blit(background, (0, bg_y2))  # 繪製第二張背景
    else:
        screen.fill((0, 0, 0))  # 如果沒有背景圖片，填充黑色背景

    all_sprites.draw(screen)  # 繪製所有精靈
    pygame.display.flip()  # 更新畫面
