from plane_settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        super(Player, self).__init__()
        self.image = image 
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
