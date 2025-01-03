import pygame, sys
from settings import *
from level import Level
from plane_game.plane import start_plane_game  # 引入 plane_game 的函數

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('NYCU VALLEY')
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.state = "main_game"  # 當前狀態：main_game 或 plane_game
        self.main_game_background = None  # 保存主遊戲的背景畫面

    def run(self):
        while True:
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
                if event.key == pygame.K_p:  # 按下 'P' 鍵
                    print("Switching to Plane Game")
                    self.main_game_background = self.screen.copy()
                    self.state = "plane_game"  # 切換到子遊戲
            
        dt = self.clock.tick() / 1000.0 
        self.level.run(dt)
        pygame.display.update()

    def plane_game(self):
        result, coin_value = start_plane_game()  # 執行子遊戲
        print("Returning to Main Game with coin =", coin_value)
        pygame.display.set_caption('NYCU VALLEY')
        self.state = "main_game"  # 子遊戲結束後返回主遊戲


if __name__ == '__main__':
    game = Game()
    game.run()
