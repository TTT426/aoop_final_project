import pygame

class ResourceManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.images = {}
        self.sounds = {}
        self.music = {}
        self.fonts = {}

    def load_resources(self):
        """
        統一呼叫此函式，載入所有遊戲裡用到的資源。
        """
        self.load_images()
        self.load_sounds()
        self.load_fonts()

    def load_images(self):
        # 例如你的背景
        bg = pygame.image.load("plane_game/img/background.png").convert()
        # 確保背景大小與視窗一致 (這裡用 self.screen_height 代表 length)
        bg = pygame.transform.scale(bg, (self.screen_width, self.screen_height))
        self.images["background"] = bg

        # rock
        rock_img = pygame.image.load("plane_game/img/rock.png").convert_alpha()
        rock_img = pygame.transform.scale(rock_img, (45, 40))
        self.images["rock"] = rock_img

        # master
        master_img = pygame.image.load("plane_game/img/Master.png").convert_alpha()
        master_img = pygame.transform.scale(master_img, (99, 75))
        self.images["master"] = master_img

        # bullet
        bullet_img = pygame.image.load("plane_game/img/bullet3.png").convert_alpha()
        self.images["bullet"] = bullet_img

        # enemy
        enemy_img = pygame.image.load("plane_game/img/ghost.png").convert_alpha()
        enemy_img = pygame.transform.scale(enemy_img, (99, 75))
        self.images["enemy"] = enemy_img

        # explosion
        explosion_img = pygame.image.load("plane_game/img/explosion.png").convert_alpha()
        self.images["explosion"] = explosion_img

    def load_sounds(self):
        # 音效
        self.sounds["ghost_lose"] = pygame.mixer.Sound("plane_game/sound/ghost_lose.wav")
        self.music["ghost_win"] = "plane_game/sound/ghost_win.ogg"

    def load_fonts(self):
        self.fonts["large"] = pygame.font.Font(None, 74)
        self.fonts["small"] = pygame.font.Font(None, 36)

    def get_image(self, name):
        return self.images.get(name)

    def get_sound(self, name):
        return self.sounds.get(name)

    def get_music(self, name):
        return self.music.get(name)

    def get_font(self, name):
        return self.fonts.get(name)
