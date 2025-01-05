import pygame
import settings
from settings import *
from timer import Timer

class Menu:
    def __init__(self, player, toggle_menu):

        #general setup
        self.player = player
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../font/LycheeSoda.ttf', 30)

        #menu setup
        self.width = 400
        self.space = 10
        self.padding = 8

        #entries
        self.options = list(self.player.item_inventory.keys()) + list(self.player.seed_inventory.keys())
        self.sell_border = len(self.player.item_inventory)-1
        self.setup()

        #movement
        self.choose_index = 0
        self.timer = Timer(200)
    
    def display_money(self):
        text_surf = self.font.render(f'${settings.money}', False, 'Black')
        text_rect = text_surf.get_rect(midbottom = (SCREEN_WIDTH/2, SCREEN_HEIGHT-20))

        pygame.draw.rect(self.display_surface, 'White', text_rect.copy().inflate(10, 10),0, 4)
        self.display_surface.blit(text_surf, text_rect)

    def setup(self):

        #create the text surface
        self.text_surfs = []
        self.total_height = 0

        for item in self.options:
            text_surf = self.font.render(item, False, 'Black')
            self.text_surfs.append(text_surf)
            self.total_height += text_surf.get_height( ) + (self.padding*2)
        self.total_height += (len(self.options)-1)*self.space
        self.menu_top = SCREEN_HEIGHT/2 - self.total_height/2
        self.menu_left = SCREEN_WIDTH/2 - self.width/2
        self.main_rect = pygame.Rect(self.menu_left, self.menu_top, self.width, self.total_height)

        #buy/sell text surface
        self.buy_text = self.font.render('Buy', False, 'Black')
        self.sell_text = self.font.render('Sell(product)', False, 'Black')

    def input(self):

        self.timer.update()

        #if press esc close menu
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()

        if not self.timer.active:
            #switch item
            if keys[pygame.K_UP]:
                self.choose_index -= 1
                self.timer.activate()
            
            if keys[pygame.K_DOWN]:
                self.choose_index += 1
                self.timer.activate()

            if keys[pygame.K_SPACE] and not settings.look_menu:
                self.timer.activate()
                
                #get item
                current_item = self.options[self.choose_index]
                
                #sell
                if self.choose_index <= self.sell_border:
                    if self.player.item_inventory[current_item] > 0:
                        self.player.item_inventory[current_item] -= 1
                        settings.money += SALE_PRICES[current_item]
                #buy
                else:
                    if settings.money >= PURCHASE_PRICES[current_item]:
                        settings.money -= PURCHASE_PRICES[current_item]
                        self.player.seed_inventory[current_item] += 1
                        if current_item == 'plane_game':
                            if not settings.unlock: self.display_message("You got this game forever! Press P to Start")
                            settings.unlock = True
                            
                            if self.player.seed_inventory[current_item] != 1:
                                self.player.seed_inventory[current_item] = 1
                                settings.money += PURCHASE_PRICES[current_item]
                                self.display_message("You had bought this!")       
        if self.choose_index < 0:
            self.choose_index = 0
        if self.choose_index > len(self.options)-1:
            self.choose_index = len(self.options)-1

    def show_entry(self, text_surf, amount, top, selected):

        #background
        bg_rect= pygame.Rect(self.main_rect.left, top, self.width, text_surf.get_height()+self.padding*2)
        pygame.draw.rect(self.display_surface, 'White', bg_rect, 0, 4)

        #text
        text_rect = text_surf.get_rect(midleft = (self.main_rect.left + 20, bg_rect.centery))
        self.display_surface.blit(text_surf, text_rect)

        #amount
        amount_surf = self.font.render(str(amount), False, 'Black')
        amount_rect = amount_surf.get_rect(midright = (self.main_rect.right - 20, bg_rect.centery))
        self.display_surface.blit(amount_surf, amount_rect)

        #selected
        if selected == True and not settings.look_menu:
            pygame.draw.rect(self.display_surface, 'Black', bg_rect, 4, 4)
            if self.choose_index <= self.sell_border: #sell
                pos_rect = self.sell_text.get_rect(midleft = (self.main_rect.left + 150, bg_rect.centery))
                self.display_surface.blit(self.sell_text, pos_rect )
            else : #buy
                pos_x = self.main_rect.left + 200 if 'plane_game' in self.options[self.choose_index] else self.main_rect.left + 150
                pos_rect = self.buy_text.get_rect(midleft=(pos_x, bg_rect.centery))

                if not 'plane_game' in self.options[self.choose_index]:
                    self.buy_text = self.font.render('Buy(seed)', False, 'Black')
                    self.display_surface.blit(self.buy_text,pos_rect)      
                else:
                    self.buy_text = self.font.render('Buy', False, 'Black')
                    self.display_surface.blit(self.buy_text,pos_rect) 
                
        elif selected == True and settings.look_menu:
            pygame.draw.rect(self.display_surface, 'Blue', bg_rect, 4, 4)

            self.buy_text = self.font.render('have(product)', False, 'Black')
            if self.choose_index <= self.sell_border: #sell
                pos_rect = self.sell_text.get_rect(midleft = (self.main_rect.left + 150, bg_rect.centery))
                self.display_surface.blit(self.buy_text, pos_rect )
            else : #buy
                pos_x = self.main_rect.left + 200 if 'plane_game' in self.options[self.choose_index] else self.main_rect.left + 150
                pos_rect = self.buy_text.get_rect(midleft=(pos_x, bg_rect.centery))
                if not 'plane_game' in self.options[self.choose_index]:
                    self.buy_text = self.font.render('have(seed)', False, 'Black')
                    self.display_surface.blit(self.buy_text,pos_rect)      
                else:
                    self.buy_text = self.font.render('have', False, 'Black')
                    self.display_surface.blit(self.buy_text,pos_rect)
    def update(self):
        self.input()
        self.display_money()
       
        for text_index, text_surf in enumerate(self.text_surfs):
            top = self.main_rect.top + text_index*(text_surf.get_height()+self.padding*2 + self.space)
            amount_list = list(self.player.item_inventory.values()) + list(self.player.seed_inventory.values())
            amount = amount_list[text_index]
            item_is_choosed = text_index == self.choose_index
            self.show_entry(text_surf, amount, top, item_is_choosed)
        
    def display_message(self, message):
        # 創建文字表面
        message_surf = self.font.render(message, True, 'Black')
        message_rect = message_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        # 畫出文字背景
        pygame.draw.rect(self.display_surface, 'White', message_rect.inflate(10, 10))
        self.display_surface.blit(message_surf, message_rect)

        # 更新顯示
        pygame.display.flip()
        pygame.time.delay(2000)  # 停留 1.5 秒