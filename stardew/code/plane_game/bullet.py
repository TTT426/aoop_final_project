from .plane_settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speedx=0, speedy=-10, image=None, color=(255, 255, 255)):
        super().__init__()
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
        if self.rect.bottom < 0 or self.rect.top > length or self.rect.right < 0 or self.rect.left > screen_width:
            self.kill()