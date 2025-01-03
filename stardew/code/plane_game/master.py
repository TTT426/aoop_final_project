from .plane_settings import *

class Master(pygame.sprite.Sprite):
    def __init__(self, image):
        super(Master, self).__init__()
        self.image = image 
        self.rect = self.image.get_rect()
        self.rect.centerx = 250
        self.rect.top = 550
        self.health = 5  # 初始血量設為 5 格
        self.invincible = False  # 是否處於無敵狀態
        self.last_hit_time = pygame.time.get_ticks()  # 上次受傷時間
        
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
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > length:
            self.rect.bottom = length
        now = pygame.time.get_ticks()
        if self.invincible and now - self.last_hit_time > 500:  # 無敵時間結束
            self.invincible = False
    
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
