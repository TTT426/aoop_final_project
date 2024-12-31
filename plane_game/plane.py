from plane_settings import *
from player import Player
from rock import Rock
from bullet import Bullet

# 遊戲開始
game_state = "start"
# 遊戲暫停
paused = False

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

# 建立 sprite 群組
bullets = pygame.sprite.Group()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, player):
        super(Enemy, self).__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 1371 - self.rect.width)
        self.rect.y = random.randint(0, 500)
        self.speedx = random.uniform(-3, 3)  # 初始化速度
        self.speedy = random.uniform(-3, 3)  # 初始化速度
        self.player = player
        self.last_speed_update = pygame.time.get_ticks()  # 上次更新速度的時間
        self.last_shoot_time = pygame.time.get_ticks()
        self.health = 5  # 初始血量設為 5 格
        self.invincible = False  # 是否處於無敵狀態
        self.last_hit_time = pygame.time.get_ticks()  # 上次受傷時間

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
        if now - self.last_speed_update > 2000:  # 每3秒更新一次速度
            self.speedx = random.uniform(-5, 5)
            self.speedy = random.uniform(-5, 5)
            if abs(self.speedx) < 1:
                self.speedx = random.choice([-1, 1]) * random.uniform(1, 3)
            if abs(self.speedy) < 1:
                self.speedy = random.choice([-1, 1]) * random.uniform(1, 3)
            self.last_speed_update = now

        # 發射子彈
        now = pygame.time.get_ticks()
        if now - self.last_shoot_time > 750:  # 每秒發射一顆子彈
            self.shoot()
            self.last_shoot_time = now

        now = pygame.time.get_ticks()
        if self.invincible and now - self.last_hit_time > 500:  # 無敵時間結束
            self.invincible = False
        
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
    
    def draw_health_bar(self, surface):
        # 設定血量條的寬度和高度
        bar_width = 40
        bar_height = 5
        fill = (self.health / 5) * bar_width  # 根據血量比例填充
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
                print("Player is dead!")
                self.kill()
            # 啟動無敵狀態
            self.invincible = True

enemy = Enemy(enemy_image, player)
all_sprites.add(enemy)

#  主遊戲循環
running = True
while running:
    clock.tick(fps)  # 控制遊戲速度為 60 FPS  
     
    # 事件處理邏輯
    for event in pygame.event.get():
        if enemy.health == 0: print("win!")
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == 27) or player.health <= 0 or enemy.health <= 0:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_state == "start" and event.key == pygame.K_RETURN:
                game_state = "playing"  # 切換到遊戲進行狀態
            if event.key == 32:
                # 發射子彈
                bullet = Bullet(player.rect.centerx, player.rect.top, speedy=-10, image=bullet_image) 
                all_sprites.add(bullet)
                bullets.add(bullet)
            if event.key == pygame.K_p and game_state == "playing":  # 按下 P 鍵切換暫停狀態
                paused = not paused

    if game_state == "start":
        # 清空畫面
        screen.fill(BLACK)
        # 開始畫面
        font = pygame.font.Font(None, 74)
        small_font = pygame.font.Font(None, 36)
        title_text = font.render("Welcome to the Game", True, WHITE)
        instruction_text = small_font.render("Press ENTER to start", True, WHITE)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 200))
        screen.blit(instruction_text, (screen_width // 2 - instruction_text.get_width() // 2, 300))  
        # 刷新屏幕
        pygame.display.flip()
    elif game_state == "playing":
        # 玩家與岩石的碰撞檢測
        hits = pygame.sprite.spritecollide(player, rocks, False)
        for hit in hits:
            player.take_damage(2)  # 每次碰撞減少 1 格血
            hit.kill()  # 移除與玩家碰撞的石頭

        # 玩家與敵人子彈
        bullet_hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
        for bullet in bullet_hits:
            player.take_damage(1)  # 子彈擊中也減少 1 格血
            bullet.kill()
        
        # 子彈與岩石的碰撞檢測
        bullet_hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
        for hit in bullet_hits:
            new_rock = Rock(rock_image)
            all_sprites.add(new_rock)
            rocks.add(new_rock)
        
        # 玩家子彈和敵人
        attack = pygame.sprite.spritecollide(enemy, bullets, False)
        for a in attack:
            enemy.take_damage(1)
            a.kill()
        
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
             
        if not paused:
            all_sprites.update()
            all_sprites.draw(screen)  # 繪製所有精靈 
            # 更新和繪製玩家
            player.update()
            player.draw_health_bar(screen)
            enemy.update()
            enemy.draw_health_bar(screen)
            pygame.display.flip()  # 更新畫面
        else:
            # 顯示暫停畫面
            pause_font = pygame.font.Font(None, 74)
            # 顯示暫停文字
            pause_text = pause_font.render("Game Paused", True, WHITE)
            screen.blit(pause_text, (screen_width // 2 - pause_text.get_width() // 2, screen_height // 2))
            # 刷新屏幕
            pygame.display.flip()