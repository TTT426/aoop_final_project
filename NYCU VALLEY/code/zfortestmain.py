import pygame, sys, settings, player
from settings import *
from level import Level
from plane_game.plane import start_plane_game  # 引入 plane_game
import time

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('NYCU VALLEY')
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.state = "main_game"  # 當前狀態：main_game 或 plane_game
        self.main_game_background = None  # 保存主遊戲的背景畫面
        self.font = pygame.font.Font('../font/LycheeSoda.ttf', 30)
        self.display_surface = pygame.display.get_surface()

    def run(self):
        start_time = time.time()
        while True:
            current_time = time.time()
            if current_time - start_time > 10:  # 10 秒後自動退出
                pygame.quit()
                sys.exit()
            if self.state == "main_game":
                self.main_game()
            elif self.state == "plane_game":
                self.plane_game()
    
    def main_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and settings.unlock:  # 按下 'P' 鍵
                    if settings.money < 20:
                        self.display_message("you don't have enough money to enter the game!")
                    else:
                        self.main_game_background = self.screen.copy()
                        self.state = "plane_game"  # 切換到子遊戲
                elif event.key == 109: # 按 M 會跳出menu
                    self.level.shop_active = True
                    settings.look_menu = True

        dt = self.clock.tick() / 1000.0 
        self.level.run(dt)
        pygame.display.update()

    def plane_game(self):
        result, coin_value = start_plane_game()  # 執行子遊戲
        if result == "Win":
            settings.money += coin_value-20
        elif result == "Lose":
            settings.money += round(coin_value//2) - 20
        pygame.display.set_caption('NYCU VALLEY')
        self.state = "main_game"  # 子遊戲結束後返回主遊戲

    def display_message(self, message):
        # 創建文字表面
        message_surf = self.font.render(message, True, 'Black')
        message_rect = message_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        # 畫出文字背景
        pygame.draw.rect(self.display_surface, 'White', message_rect.inflate(10, 10))
        self.display_surface.blit(message_surf, message_rect)

        # 更新顯示
        pygame.display.flip()
        pygame.time.delay(1500)  # 停留 1.5 秒
if __name__ == '__main__':
    game = Game()
    game.run()
