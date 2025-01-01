import pygame, os
from settings import *
from support import *
from pathlib import Path
from timer import Timer



class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, tree_sprites):
        super().__init__(group)

        self.import_assets()
        self.status = 'down'
        self.frame_index = 0

        #general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.z = LAYERS['main'] 

        #moverment attributes
        self.direction = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        #collision
        self.hitbox = self.rect.copy().inflate((-126, -70))
        self.collision_sprites = collision_sprites

        #timers
        self.timers = {
            'tool use': Timer(500, self.use_tool),
            'tool switch':Timer(500),
            'seed use':Timer(500, self.use_seed),
            'seed switch':Timer(500)
        }

        #tools
        self.tools = ['hoe', 'axe', 'water']
        self.tools_index = 0
        self.selected_tool = self.tools[self.tools_index]

        #seeds
        self.seeds = ['corn', 'tomato']
        self.seeds_index = 0
        self.selected_seed = self.seeds[self.seeds_index]

        #interaction
        self.tree_sprites = tree_sprites

    def use_tool(self):
        if self.selected_tool == 'hoe':
            pass

        if self.selected_tool == 'axe':
            pass


        if self.selected_tool == 'water':
            pass

    def get_target_pos(self):
        self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split('_')[0]]
    
    def use_seed(self):
        pass

    def import_assets(self):
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
            'up_hoe': [], 'down_hoe': [],  'left_hoe': [], 'right_hoe': [],
            'up_axe': [], 'down_axe': [],  'left_axe': [], 'right_axe': [],
            'up_water': [], 'down_water': [],  'left_water': [], 'right_water': [],
        }
        for animation in self.animations.keys():
            full_path = '../graphics/character/' + animation
            # run main.py in the code directory
            self.animations[animation] = import_folder(full_path)    

    def animate(self, dt):
        self.frame_index += 4*dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers['tool use'].active:

            #movement
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_LEFT]:   
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_RIGHT]:  
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0
            
            #tool use
            if keys[pygame.K_SPACE]:
                self.timers['tool use'].activate()
                self.direction = pygame.math.Vector2(0, 0)
                self.frame_index = 0
            
            #tool switch
            if keys[pygame.K_q] and not self.timers['tool switch'].active:
                self.timers['tool switch'].activate()
                self.tools_index += 1
                if self.tools_index >= len(self.tools):
                    self.tools_index = 0
                self.selected_tool = self.tools[self.tools_index]
                
            #seed use 
            if keys[pygame.K_LCTRL]:
                self.timers['seed use'].activate()
                self.direction = pygame.math.Vector2(0, 0)
                self.frame_index = 0

            #seed switch
            if keys[pygame.K_e] and not self.timers['seed switch'].active:
                self.timers['seed switch'].activate()
                self.seeds_index += 1
                if self.seeds_index >= len(self.seeds):
                    self.seeds_index = 0
                self.selected_seed = self.seeds[self.seeds_index]
            
    def get_status(self):

        #idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        #tool use
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool
    
    def move(self, dt):

        #normalizing a vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        
        #horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = round(self.pos.x)
        self.collision('horizontal')

        #vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery= round(self.pos.y)
        self.collision('vertical')
    
    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if self.hitbox.colliderect(sprite.hitbox):
                    if direction == 'horizontal':
                        if self.direction.x > 0: #moving right
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0: #moving left
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                    
                    if direction == 'vertical':
                        if self.direction.y > 0: #moving down
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0: #moving up
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery


    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.get_target_pos()

        self.move(dt)
        self.animate(dt)
        