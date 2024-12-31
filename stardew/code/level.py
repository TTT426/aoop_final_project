import pygame, sys
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, WildFlower, Tree
from pytmx.util_pygame import load_pygame
from support import *


class Level:
    def __init__(self):

        #get the display surface
        self.display_surface = pygame.display.get_surface()

        #sprite groups
        #self.all_sprites = pygame.sprite.Group()
        self.all_sprites = CameraGroup()

        self.setup()
        self.overlay = Overlay(self.player)

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
                groups=self.all_sprites,
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
                groups = self.all_sprites,
                name = obj.name
                
            )

        #wildflowers
        for obj in tmx_data.get_layer_by_name('Decoration'):
            WildFlower(
                pos = (obj.x, obj.y),
                surf = obj.image,
                groups = self.all_sprites
            )

        Generic(
            pos = (0,0),
            surf = pygame.image.load('../graphics/world/ground.png').convert_alpha(),
            groups=self.all_sprites,
            z = LAYERS['ground']
        )
        self.player = Player((640, 360), self.all_sprites)

    def run(self, dt):
        self.display_surface.fill('black')
        #self.all_sprites.draw(self.display_surface)
        self.all_sprites.custom_draw(self.player)  
        self.all_sprites.update(dt)

        self.overlay.display()

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display = pygame.display.get_surface()
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
                    self.display.blit(sprite.image, offset_rect)