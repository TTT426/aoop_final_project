from .plane_settings import *
from .master import Master
from .rock import Rock
from .bullet import Bullet
from .explosion import Explosion
from .parent_enemy import Parent_Enemy
from .ResourceManager import ResourceManager

def start_plane_game():
    # 遊戲開始
    game_state = "start"
    coin = 0
    # 遊戲暫停
    paused = False

    
    # 初始化背景位置
    bg_y1 = 0
    bg_y2 = -length  # 假設背景圖片高度為 `length`

    # 初始化 pygame
    pygame.mixer.init()  # 初始化音頻模組
    screen = pygame.display.set_mode((screen_width, length))
    pygame.display.set_caption("Plane shoot")
    clock = pygame.time.Clock() 

    # 載入字體與圖片
    resource_manager = ResourceManager(screen_width, length)
    resource_manager.load_resources()
    font = resource_manager.get_font("large")
    small_font = resource_manager.get_font("small")
    background = resource_manager.get_image("background")
    rock_image = resource_manager.get_image("rock")
    Master_image = resource_manager.get_image("master")
    bullet_image = resource_manager.get_image("bullet")
    enemy_image = resource_manager.get_image("enemy")
    explosion_image = resource_manager.get_image("explosion")

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

    class Enemy(Parent_Enemy):
        def __init__(self, image, Master, all_sprites, enemy_bullets):
            super().__init__(image, Master)
            self.all_sprites = all_sprites
            self.enemy_bullets = enemy_bullets
            
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
            
    enemy = Enemy(enemy_image, Master2, all_sprites, enemy_bullets)
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
            if event.type == pygame.KEYDOWN:
                if game_state == "start" and event.key == pygame.K_ESCAPE:
                    running = False
                    return ("2back_to_main", coin)
                
                elif game_state == "start" and event.key == pygame.K_RETURN:
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
            "Earn 1 coin for destroying a rock (only use by the bullets)",
            "Earn 10 coins for defeating the Boss",
            "Colliding with the enemy, asteroids, or enemy bullets",
            "will cause you to lose one health point.",
            "And if you die, your coins will be halved",
            "Try to earn as much as you can under the Boss's wrath!",
                "Submit 20 dollars and Press ENTER to start your battle!", 
                "or Press ESC to Left!" 
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
            notices_y = start_y + len(instructions) * line_spacing  # 計算 Notices 的 y 座標
            Notices = font.render("You Can not Left during the game!", True, RED)
            screen.blit(Notices, (screen_width // 2 - Notices.get_width() // 2, notices_y))
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
                    explosion = Explosion(a.rect.centerx, a.rect.centery, explosion_frames)
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

                # 調整 y 座標，將文字往上移動
                pause_y = 100 # 原本是在螢幕正中央，往上移動 100 像素
                screen.blit(pause_text, (screen_width // 2 - pause_text.get_width() // 2, pause_y))
                instructions = [
                "Rules:",
                "Use arrow keys to move the character",
                "Press SPACEBAR to shoot bullets",
                "Press P to pause the game",
                "Earn 1 coin for destroying a rock (only use by the bullets)",
                "Earn 10 coins for defeating the Boss",
                "Colliding with the enemy, asteroids, or enemy bullets",
                "will cause you to lose one health point.",
                "And if you die, your coins will be halved",
                "Try to earn as much as you can under the Boss's wrath!",
                    "Press P to return your battle!", 
                ]

                start_y = 200  # 說明文字起始的 y 座標
                line_spacing = 40  # 每行文字的間距
                for i, line in enumerate(instructions):
                    text_surface = small_font.render(line, True, WHITE)
                    screen.blit(
                        text_surface, 
                        (screen_width // 2 - text_surface.get_width() // 2, start_y + i * line_spacing)
                    )            
                # 刷新屏幕
                pygame.display.flip()

            if Master2.health <= 0:
                pygame.mixer.music.load(resource_manager.get_music("ghost_win"))
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
                            return ("Lose", coin)
                            
            elif enemy.health <= 0:
                sound_effect = pygame.mixer.Sound(resource_manager.get_sound("ghost_lose"))
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
                            return ("Win", coin)
    return "back_to_main"  # 結束子遊戲時返回主遊戲
