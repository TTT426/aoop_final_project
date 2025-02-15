import pygame, sys, settings
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, WildFlower, Tree, Interaction, Particle, Chicken, Cow, ChickenHouse
from pytmx.util_pygame import load_pygame
from support import *
from transition import Transition
from soil import SoilLayer
from sky import Rain, Sky
from random import randint, choice
from menu import Menu


class Level:
    def __init__(self):

        #get the display surface
        self.display_surface = pygame.display.get_surface()

        #sprite groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.animal_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()
        self.meat_sprites = pygame.sprite.Group()
        self.milk_sprites = pygame.sprite.Group()

        self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)
        self.setup()
        self.overlay = Overlay(self.player)
        self.transition = Transition(self.reset, self.player)

        #sky
        self.rain = Rain(self.all_sprites)
        self.raining = False
        self.soil_layer.raining = self.raining
        self.sky = Sky()

        #shop
        self.menu = Menu(self.player, self.toggle_shop)
        self.shop_active = False

        #music
        self.success = pygame.mixer.Sound('../audio/success.wav')
        self.success.set_volume(0.3)
        
        self.backgound_music = pygame.mixer.Sound('../audio/bg.mp3')
        self.backgound_music.set_volume(0.05)
        self.backgound_music.play(loops = -1)

        #animal
        self.chiken_num = len(ANIMAL_POS['chicken'])
        self.cow_num = len(ANIMAL_POS['cow'])

    def setup(self):
        tmx_data = load_pygame('../data/map.tmx')

        #house 
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic(
                    pos = (x * TILE_SIZE, y * TILE_SIZE),
                    surf = surf,
                    groups=self.all_sprites,
                    z = LAYERS['house bottom']
                )

        for layer in ['HouseWalls', 'HouseFurnitureTop']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic(
                    pos = (x * TILE_SIZE, y * TILE_SIZE),
                    surf = surf,
                    groups=self.all_sprites,
                    z = LAYERS['main']
                )

        #Fence
        
        for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
            Generic(
                pos = (x * TILE_SIZE, y * TILE_SIZE),
                surf = surf,
                groups=[self.all_sprites, self.collision_sprites],
                z = LAYERS['main']
            )

        #water
        water_frames = import_folder('../graphics/water')
        for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
            Water(
                pos = (x * TILE_SIZE, y * TILE_SIZE),
                frames = water_frames,
                groups=self.all_sprites
            )

        #trees
        for obj in tmx_data.get_layer_by_name('Trees'):
            Tree(
                pos = (obj.x, obj.y),
                surf = obj.image,
                groups = [self.all_sprites, self.collision_sprites, self.tree_sprites],
                all_sprites = self.all_sprites,
                name = obj.name,
                player_add = self.player_add
            )

        #wildflowers
        for obj in tmx_data.get_layer_by_name('Decoration'):
            WildFlower(
                pos = (obj.x, obj.y),
                surf = obj.image,
                groups = [self.all_sprites, self.collision_sprites]
            )

        Generic(
            pos = (0,0),
            surf = pygame.image.load('../graphics/world/ground.png').convert_alpha(),
            groups=self.all_sprites,
            z = LAYERS['ground']
        )
        
        #collision tiles
        for x,y, surf in tmx_data.get_layer_by_name('Collision').tiles():
            Generic(
                pos = (x * TILE_SIZE, y * TILE_SIZE),
                surf = pygame.Surface((TILE_SIZE, TILE_SIZE)),
                groups = self.collision_sprites
            )

        # #chikens
        self.chiken_frames_dict = import_folder_dict_resize('../graphics/animals/chicken', 'chicken')
        for  pos in ANIMAL_POS['chicken']:
            Chicken(
                #pos = (30*64, 30*64),
                pos = (pos[0]*TILE_SIZE, pos[1]*TILE_SIZE),
                #frames = chiken_frames,
                frames_dict = self.chiken_frames_dict,
                #groups = [self.all_sprites],
                groups = [self.all_sprites, self.animal_sprites],
                all_sprites = self.all_sprites,
                collision_sprites = self.collision_sprites,
                meat_sprites = self.meat_sprites,
                name = 'chicken'
            )
        
        #chicken house
        self.chiken_house = ChickenHouse([self.all_sprites, self.collision_sprites], self.animal_sprites)
        #cows
        self.cow_frames_dict = import_folder_dict_resize('../graphics/animals/cow', 'cow')
        #self.CowCluster = []
        for  pos in ANIMAL_POS['cow']:
            Cow(
                pos = (pos[0]*TILE_SIZE, pos[1]*TILE_SIZE),
                frames_dict = self.cow_frames_dict,
                groups = [self.all_sprites, self.animal_sprites],
                all_sprites = self.all_sprites,
                collision_sprites = self.collision_sprites,
                meat_sprites = self.meat_sprites,
                milk_sprites=self.milk_sprites,
                name = 'cow'
            )
            #self.CowCluster.append(c)
        #print(self.CowCluster)


        #Player
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == 'Start':
                self.player = Player(
                    pos =(obj.x, obj.y),
                    group =  [self.all_sprites], 
                    collision_sprites=self.collision_sprites,
                    animal_sprites = self.animal_sprites,
                    tree_sprites = self.tree_sprites,
                    interation = self.interaction_sprites,
                    soil_layer = self.soil_layer,
                    toggle_shop = self.toggle_shop
                    )
                
            if obj.name == 'Bed':
                Interaction(
                    (obj.x, obj.y),
                    (obj.width, obj.height),
                    self.interaction_sprites,
                    obj.name
                )
            
            if obj.name == 'Trader':
                Interaction(
                    (obj.x, obj.y),
                    (obj.width, obj.height),
                    self.interaction_sprites,
                    obj.name
                )

    def player_add(self, item):

        self.player.item_inventory[item] += 1
        self.success.play()

    def toggle_shop(self):
        self.shop_active = not self.shop_active

    def reset(self):
        #plants
        self.soil_layer.update_plants()

        #soil
        self.soil_layer.remove_water()
        #randomize raining
        self.raining = randint(0,10) > 7
        self.soil_layer.raining = self.raining
        if self.raining == True:
            self.soil_layer.water_all()

        #apples on the trees
        for tree in self.tree_sprites.sprites():
            if tree.health > 0:
                for apple in tree.apple_sprites.sprites():
                    apple.kill()
                tree.create_fruit()

        #sky
        self.sky.start_color = [255,255,255]

        #animals
        for animal in self.animal_sprites.sprites():
            if animal.name == 'cow':
                animal.update_milk()
        self.breed_animal()

    def plant_collision(self):
        #harvesting plants
        if self.soil_layer.plant_sprites:
            for plant in self.soil_layer.plant_sprites.sprites():
                if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
                    self.player_add(plant.plant_type)
                    plant.kill()
                    Particle( plant.rect.topleft, plant.image, self.all_sprites, LAYERS['main'])
                    x = plant.rect.centerx // TILE_SIZE 
                    y = plant.rect.centery // TILE_SIZE
                    self.soil_layer.grid[y][x].remove('P')

    def egg_collison(self):
        #pick up eggs
        for nest in self.chiken_house.nests:
            if nest.has_egg and nest.rect.colliderect(self.player.hitbox):
                self.player_add('egg')
                nest.pick_egg()
                #print(self.player.item_inventory)

    def meat_collison(self):
        #pick up meat
        for meat in self.meat_sprites.sprites():
            if meat.rect.colliderect(self.player.hitbox):
                #self.player_add('meat')
                self.player.item_inventory[meat.name] += 1
                meat.kill()
                #print(self.player.item_inventory)

    def milk_collison(self):
        #pick up milk
        # for cow in self.CowCluster:
        #     for milk in cow.milk_list:
        #         if milk.rect.colliderect(self.player.hitbox):
        #             self.player_add('milk')
        #             cow.milk_list.remove(milk)
        #             milk.kill()
        #             #print(self.player.item_inventory)
        # for animal in self.animal_sprites.sprites():
        #     if animal.name == 'cow':
        #         for milk in animal.milk_list:
        #             if milk.rect.colliderect(self.player.hitbox):
        #                 self.player_add('milk')
        #                 animal.milk_list.remove(milk)
        #                 milk.kill()
        #                 #print(self.player.item_inventory
        for milk in self.milk_sprites.sprites():
            if milk.rect.colliderect(self.player.hitbox):
                        self.player_add('milk')
                        milk.kill()


    def get_milk(self):
        # for cow in self.CowCluster:
        #     if cow.has_milk and cow.rect.colliderect(self.player.hitbox):
        #         #self.player_add('milk')
        #         #print(self.player.item_inventory)
        #         cow.generate_milk(self.player.rect.center)
        #         cow.has_milk = False
        for animal in self.animal_sprites.sprites():
            if animal.name == 'cow':
                if animal.has_milk and animal.rect.colliderect(self.player.hitbox):
                    #self.player_add('milk')
                    #print(self.player.item_inventory)
                    animal.generate_milk(self.player.rect.center)
                    animal.has_milk = False

    def breed_animal(self):
        chicken_num = 0
        cow_num = 0
        for animal in self.animal_sprites.sprites():
            if animal.name == 'chicken':
                chicken_num += 1
            if animal.name == 'cow':
                cow_num += 1
        chicken_pos = choice(AVAILABLE_POS)
        cow_pos = choice(AVAILABLE_POS)        
        if chicken_num >= 2:
            Chicken(
                #pos = (30*64, 30*64),
                pos = (chicken_pos[0]*TILE_SIZE, chicken_pos[1]*TILE_SIZE),
                #frames = chiken_frames,
                frames_dict = self.chiken_frames_dict,
                #groups = [self.all_sprites],
                groups = [self.all_sprites, self.animal_sprites],
                all_sprites = self.all_sprites,
                collision_sprites = self.collision_sprites,
                meat_sprites = self.meat_sprites,
                name = 'chicken'
            )
        if cow_num >= 2:
            Cow(
                pos = (cow_pos[0]*TILE_SIZE, cow_pos[1]*TILE_SIZE),
                frames_dict = self.cow_frames_dict,
                groups = [self.all_sprites, self.animal_sprites],
                all_sprites = self.all_sprites,
                collision_sprites = self.collision_sprites,
                meat_sprites = self.meat_sprites,
                milk_sprites = self.milk_sprites,
                name = 'cow'
            )
    
    def run(self, dt):

        #drawing logic
        self.display_surface.fill('black')
        self.all_sprites.custom_draw(self.player)  

        #update
        if self.shop_active:
            self.menu.update()
        else:
            self.all_sprites.update(dt)
            self.plant_collision()
            self.egg_collison()
            self.get_milk()
            self.milk_collison()
            self.meat_collison()

        #weather
        self.overlay.display()
        #raining
        if self.raining == True and not self.shop_active:
            self.rain.update(dt)
        #daytime
        self.sky.display(dt)

        #transition overlay
        if self.player.sleep:
            self.transition.play()

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2(0, 0)
    
    def custom_draw(self, player):  
        self.offset.x = player.rect.centerx - SCREEN_WIDTH /2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT /2

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(),key = lambda sprite:sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    #self.display.blit(sprite.image, sprite.rect)
                    self.display_surface.blit(sprite.image, offset_rect)

                    # #anaylatics
                    # if sprite == chicken:
                    #     pygame.draw.rect(self.display_surface, 'red', offset_rect, 5)
                    #     hitbox_rect = player.hitbox.copy()
                    #     hitbox_rect.center = offset_rect.center
                    #     pygame.draw.rect(self.display_surface, 'green', hitbox_rect, 5)
                    #     target_pos = offset_rect.center + PLAYER_TOOL_OFFSET[player.status.split('_')[0]]
                    #     pygame.draw.circle(self.display_surface, 'blue', target_pos, 5)