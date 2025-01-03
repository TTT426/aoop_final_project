from .plane_settings import *
from .master import Master
from .rock import Rock
from .bullet import Bullet
from .explosion import Explosion

def start_plane_game():
    # 遊戲開始
    game_state = "start"
    coin = 0
    # 遊戲暫停
    paused = False
    # 字體設定
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)
    # 初始化背景位置
    bg_y1 = 0
    bg_y2 = -length  # 假設背景圖片高度為 `length`

    # 初始化 pygame
    pygame.mixer.init()  # 初始化音頻模組
    screen = pygame.display.set_mode((1371, length))
    pygame.display.set_caption("Plane shoot")
    clock = pygame.time.Clock() 

    # 載圖片
    background = pygame.image.load("plane_game/img/background.png").convert()
    background = pygame.transform.scale(background, (1371, length))  # 確保背景大小與視窗一致
    rock_image = pygame.image.load("plane_game/img/rock.png").convert_alpha()
    rock_image = pygame.transform.scale(rock_image, (45, 40))
    Master_image = pygame.image.load("plane_game/img/Master.png").convert_alpha()
    Master_image = pygame.transform.scale(Master_image, (99, 75))
    bullet_image = pygame.image.load("plane_game/img/bullet3.png").convert_alpha()
    enemy_image = pygame.image.load("plane_game/img/ghost.png").convert_alpha()
    enemy_image = pygame.transform.scale(enemy_image, (99, 75))
    explosion_image = pygame.image.load("plane_game/img/explosion.png").convert_alpha()

    # deal with explosion
    explosion_frames = []
    total_width = explosion_image.get_width()
    total_height = explosion_image.get_height()
    
    frame_width = total_width // 16
    frame_height = total_height

    for i in range(5):
        frame_surface = explosion_image.subsurface(
            pygame.Rect(i * frame_width, 0, frame_width, frame_height)
        )
        explosion_frames.append(frame_surface)

    all_sprites = pygame.sprite.Group()
    rocks = pygame.sprite.Group()
    # 建立玩家物件
    Master2 = Master(Master_image)
    all_sprites.add(Master2)
    # 建立石頭物件
    for _ in range(rocket_number):  # 生成 8 顆岩石
        rock = Rock(rock_image)
        all_sprites.add(rock)
        rocks.add(rock)   

    # 建立 sprite 群組
    bullets = pygame.sprite.Group()

    class Enemy(pygame.sprite.Sprite):
        def __init__(self, image, Master):
            super(Enemy, self).__init__()
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.x = random.randint(0, 1371 - self.rect.width)
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
            if self.rect.left <= 0 or self.rect.right >= 1371:
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
            
        def shoot(self):
            direction = pygame.math.Vector2(
                self.Master.rect.centerx - self.rect.centerx,
                self.Master.rect.centery - self.rect.centery
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
                    print("Master is dead!")
                    self.kill()
                # 啟動無敵狀態
                self.invincible = True

    enemy = Enemy(enemy_image, Master2)
    all_sprites.add(enemy)


    def draw_coin(surface, coin):
        font = pygame.font.Font(None, 36)
        coin_text = font.render(f"coin: {coin}", True, (255, 255, 255))  # 白色文字
        surface.blit(coin_text, (10, 10))  # 在左上角顯示分數

    #  主遊戲循環
    running = True
    while running:
        clock.tick(fps)  # 控制遊戲速度為 60 FPS  
        
        # 事件處理邏輯
        for event in pygame.event.get():
            if event.type == pygame.QUIT or Master2.health <= 0 or enemy.health <= 0:
                running = False
                return ("back_to_main", coin)
            elif event.type == pygame.KEYDOWN:
                if game_state == "start" and event.key == pygame.K_RETURN:
                    for countdown in ["3", "2", "1", "Start!"]:
                        # 繪製背景
                        screen.blit(background, (0, bg_y1))
                        screen.blit(background, (0, bg_y2))
                        
                        # 繪製所有靜止的精靈
                        all_sprites.draw(screen)
                        
                        countdown_text = font.render(countdown, True, WHITE)
                        screen.blit(countdown_text, (screen_width // 2 - countdown_text.get_width() // 2, screen_height // 2))
                        pygame.display.flip()  # 更新畫面
                        pygame.time.delay(1000)  # 延遲 1 秒
                    
                    game_state = "playing"  # 切換到遊戲進行狀態
                if event.key == 32:
                    # 發射子彈
                    bullet = Bullet(Master2.rect.centerx, Master2.rect.top, speedy=-10, image=bullet_image) 
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                if event.key == pygame.K_p and game_state == "playing":  # 按下 P 鍵切換暫停狀態
                    paused = not paused

        if game_state == "start":
            # 清空畫面
            screen.fill(BLACK)
            # 開始畫面
            title_text = font.render("Welcome to the Game!", True, WHITE)
            instructions = [
            "Rules:",
            "Use arrow keys to move the character",
            "Press SPACEBAR to shoot bullets",
            "Press P to pause the game",
            "Earn 1 coin for destroying a rock",
            "Earn 10 coins for defeating the Boss",
            "If you die, your coins will be halved",
            "Try to earn as much as you can under the Boss's wrath!",
                "Press ENTER to start your battle!" 
            ]
            screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 50))
            start_y = 150  # 說明文字起始的 y 座標
            line_spacing = 40  # 每行文字的間距
            for i, line in enumerate(instructions):
                text_surface = small_font.render(line, True, WHITE)
                screen.blit(
                    text_surface, 
                    (screen_width // 2 - text_surface.get_width() // 2, start_y + i * line_spacing)
                )            
            pygame.display.flip()
        
        elif game_state == "playing":
            # 玩家與岩石的碰撞檢測
            hits = pygame.sprite.spritecollide(Master2, rocks, False)
            for hit in hits:
                Master2.take_damage(1)  # 每次碰撞減少 1 格血
                hit.kill()  # 移除與玩家碰撞的石頭
                explosion = Explosion(hit.rect.centerx, hit.rect.centery, explosion_frames)
                all_sprites.add(explosion)

            # 玩家與敵人子彈
            bullet_hits = pygame.sprite.spritecollide(Master2, enemy_bullets, True)
            for bullet in bullet_hits:
                Master2.take_damage(1)  # 子彈擊中也減少 1 格血
                bullet.kill()
            
            # 子彈與岩石的碰撞檢測
            bullet_hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
            for hit in bullet_hits:
                coin += 1
                new_rock = Rock(rock_image)
                all_sprites.add(new_rock)
                rocks.add(new_rock)
                explosion = Explosion(hit.rect.centerx, hit.rect.centery, explosion_frames)
                all_sprites.add(explosion)

            # 玩家子彈和敵人
            attack = pygame.sprite.spritecollide(enemy, bullets, False)
            for a in attack:
                enemy.take_damage(1)
                a.kill()
                if enemy.health <= 0:
                    explosion = Explosion(hit.rect.centerx, hit.rect.centery, explosion_frames)
                    all_sprites.add(explosion)
                    coin += 10  # 打倒敵人加10分
            
            # 玩家跟敵人
            if pygame.sprite.collide_rect(Master2, enemy):
                Master2.take_damage(1)
                if Master2.health <= 0:
                    Master2.kill() 

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
                Master2.update()
                Master2.draw_health_bar(screen)
                enemy.update()
                enemy.draw_health_bar(screen)
                draw_coin(screen, coin)
                pygame.display.flip()  # 更新畫面
            else:
                # 顯示暫停文字
                pause_text = font.render("Game Paused", True, WHITE)
                screen.blit(pause_text, (screen_width // 2 - pause_text.get_width() // 2, screen_height // 2))
                # 刷新屏幕
                pygame.display.flip()

            if Master2.health <= 0:
                pygame.mixer.music.load("plane_game/sound/ghost_win.ogg")
                pygame.mixer.music.play(loops=2)
                pygame.mixer.music.set_volume(1)
                while True:
                    # 顯示暫停文字
                    lose_text = font.render("You are destoryed!", True, WHITE)
                    restart_text = small_font.render("Press ESC to Return the main game", True, WHITE)
                    screen.blit(lose_text, (screen_width // 2 - lose_text.get_width() // 2, screen_height // 2))
                    screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + 50))
                    
                    # 刷新屏幕
                    pygame.display.flip()

                    # 事件處理
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                            return ("back_to_main", coin)
                            
            elif enemy.health <= 0:
                sound_effect = pygame.mixer.Sound("plane_game/sound/ghost_lose.wav")
                sound_effect.play(loops=2)
                sound_effect.set_volume(1)
                while True:
                    restart_text = small_font.render("Press ESC to Return the main game", True, WHITE)
                    win_text = font.render("You Win!", True, WHITE)
                    screen.blit(win_text, (screen_width // 2 - win_text.get_width() // 2, screen_height // 2))
                    screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + 50))
                    # 刷新屏幕
                    pygame.display.flip()

                    # 事件處理
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                            return ("back_to_main", coin)
    return "back_to_main"  # 結束子遊戲時返回主遊戲

