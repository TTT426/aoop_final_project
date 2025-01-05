import pygame
from settings import *
from random import randint, choice, uniform
from timer import Timer

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, all_sprites = None, z = LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate((-self.rect.width*0.2, -self.rect.height*0.75))
        self.all_sprites = all_sprites

class Interaction(Generic):
    def __init__(self, pos, size, groups, name) :
        surf = pygame.Surface(size)
        super().__init__(pos, surf, groups)  
        self.name = name

class Water(Generic):
    def __init__(self, pos, frames, groups):
        
        #animation setup
        self.frames = frames
        self.frame_index = 0

        #sprite setup
        super().__init__(
            pos = pos,
            surf = self.frames[self.frame_index],
            groups = groups,
            z = LAYERS['water']
        )

    def animate(self, dt):
        self.frame_index += 10*dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
    
    def update(self, dt):
        self.animate(dt)

class WildFlower(Generic):
    def __init__(self, pos, surf, groups):
        super().__init__(
            pos = pos, 
            surf = surf,
            groups = groups,
        )
        self.hitbox = self.rect.copy().inflate((-20, -self.rect.height*0.9))

class Particle(Generic):
    def __init__(self, pos, surf, groups, z, duration = 200):
        super().__init__(
            pos =pos, 
            surf = surf, 
            groups = groups, 
            z = z
            )
        self.start_time = pygame.time.get_ticks()
        self.duration = duration
        self.z = z

        # white surface
        mask_surf = pygame.mask.from_surface(self.image)
        new_surf = mask_surf.to_surface()
        new_surf.set_colorkey((0, 0, 0)) 
        self.image = new_surf       
    
    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration:
            self.kill()

class Tree(Generic):
    def __init__(self, pos, surf, groups,all_sprites, name, player_add):
        super().__init__(
            pos = pos,
            surf = surf,
            groups = groups,
            all_sprites = all_sprites
        )

        #tree attributes
        self.health = 5
        self.alive = True
        stump_path = f'../graphics/stumps/{"small" if name == "Small" else "large"}.png'
        self.stump_surf = pygame.image.load(stump_path).convert_alpha()

        #apple
        self.apples_surf = pygame.image.load('../graphics/fruit/apple.png')
        self.apple_pos = APPLE_POS[name]
        self.apple_sprites = pygame.sprite.Group()
        self.create_fruit()

        self.player_add = player_add

        #sounds
        self.axe_sound = pygame.mixer.Sound('../audio/axe.mp3')

    def damage(self):

        #damaging tree
        self.health -= 1

        #play sound
        self.axe_sound.play()

        #remove an apple
        if len(self.apple_sprites.sprites()) > 0:
            random_apple = choice(self.apple_sprites.sprites())
            Particle(random_apple.rect.topleft, random_apple.image, random_apple.all_sprites, LAYERS['fruit'])
            self.player_add('apple')
            random_apple.kill()

    def check_death(self):
        if self.health <= 0:
            Particle(self.rect.topleft, self.image, self.all_sprites, LAYERS['fruit'], 350)
            self.image = self.stump_surf
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate((-10, -self.rect.height*0.6)) 
            self.player_add('wood')
            self.alive = False

    def update(self, dt):
        if self.alive == True:
            self.check_death()
    
    def create_fruit(self):
        for pos in self.apple_pos:
            #if randint(0, 10) < 2:
            if uniform(0, 1) < 0.2:
                x = pos[0] + self.rect.left
                y = pos[1] + self.rect.top
                Generic(
                    pos = (x, y), 
                    surf = self.apples_surf, 
                    #groups = [self.apple_sprites, self.groups()[2]],
                    groups = [self.apple_sprites, self.all_sprites],
                    all_sprites = self.all_sprites,
                    z = LAYERS['fruit']
                    ) 

class Animal(Generic):
    def __init__(self, pos, frames_dict, groups, collision_sprites, name):

        #general setup
        self.name = name
        
        #animation setup
        self.frame_index = 0
        self.frames_dict = frames_dict

        #movement setup
        #self.direction = pygame.math.Vector2(-1,0)
        self.direction = pygame.math.Vector2(-1,0)
        self.speed = ANIMAL_SPEED[self.name]
        self.run = True
        self.pos = pygame.math.Vector2(pos)
        self.timer = Timer(3000)
        self.status = 'left_run'
        
        super().__init__(
            pos = pos, 
            surf = self.frames_dict[self.status][self.frame_index], 
            groups = groups,
            z = LAYERS['main']
        )

        #collision setup
        self.collision_sprites = collision_sprites
        self.rect = self.image.get_rect(bottomleft = pos)
        self.hitbox = self.rect.copy()
        
    def move(self,dt):
        if self.run == True:
            if self.direction.length() > 0:
                direction_normalized = self.direction.normalize()
            else:
                direction_normalized = pygame.math.Vector2(0,0)
            #horizontal movement
            self.pos.x += direction_normalized.x * self.speed * dt
            self.hitbox.centerx = round(self.pos.x)
            self.rect.centerx = round(self.pos.x)
            self.collision('horizontal')

            #vertical movement
            self.pos.y += direction_normalized.y * self.speed * dt
            self.hitbox.centery = round(self.pos.y)
            self.rect.centery= round(self.pos.y)
            self.collision('vertical')

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if self.hitbox.colliderect(sprite.hitbox):
                    if direction == 'horizontal':
                        if self.direction.x > 0: #moving right
                            self.run = False
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0: #moving left
                            self.run = False
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                    
                    if direction == 'vertical':
                        if self.direction.y > 0: #moving down
                            self.direction.y = 0
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0: #moving up
                            self.direction.y = 0
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    def get_status(self):
        if self.run and self.direction.x == -1:
            self.status = 'left_run'
        elif self.run and self.direction.x == 1:
            self.status = 'right_run'
        elif not self.run and self.direction.x == -1:
            self.status = 'left_idle' 
        elif not self.run and self.direction.x == 1:
            self.status = 'right_idle'

    def movement_update(self):
        if self.timer.active == False:
            if randint(0,10) < 5:
            #if randint(0,10) < 0:
                self.run = not self.run
                self.frame_index = 0
                if self.run  ==  True:
                    self.direction.x = choice([-1,1])
                    self.direction.y = choice([-1,0,1])
                    self.timer.duration = 3000
                else:
                    self.timer.duration = 10000
                self.timer.activate()
     
    def animate(self, dt):
        if self.run == True:
            self.frame_index += 4*dt
        else :
            self.frame_index += 0.5*dt
        if self.frame_index >= len(self.frames_dict[self.status]):
            self.frame_index = 0
        self.image = self.frames_dict[self.status][int(self.frame_index)]

    def update(self, dt):
        self.movement_update()
        self.get_status()
        self.move(dt)
        self.timer.update()
        self.animate(dt) 


class Chicken(Animal):
    def __init__(self, pos, frames_dict, groups, collision_sprites, name):
        super().__init__(
            pos = pos, 
            frames_dict = frames_dict, 
            groups = groups,
            collision_sprites = collision_sprites,
            name = name
        )

class ChickenHouse(Generic):
    def __init__(self, groups):

        img = pygame.image.load('../graphics/animals/chicken/house/house.png')
        resized_img = pygame.transform.scale(img, (img.get_width()*4, img.get_height()*4))
        
        self.surf = resized_img.convert_alpha()
        self.pos = (TILE_SIZE*30, TILE_SIZE*23)

        super().__init__(
            pos = self.pos, 
            surf = self.surf, 
            groups = groups
        )      
        #nest
        self.nests = [ChickenNest(groups, (30*TILE_SIZE, 26*TILE_SIZE)),
        ChickenNest(groups, (31*TILE_SIZE, 26*TILE_SIZE)),
        ChickenNest(groups, (32*TILE_SIZE, 26*TILE_SIZE))]
        self.timer = Timer(5000)

        #num
        self.chicken_num = len(ANIMAL_POS['chicken'])
    
    def lay_egg(self):
        if self.timer.active == False:
            self.timer.activate()
            for chik_nest in self.nests:
                if randint(0, 100) < self.chicken_num:
                #if randint(0, 100) < 100:
                    chik_nest.egg()
    def update(self, dt):
        self.lay_egg()
        self.timer.update()
    

class ChickenNest(Generic):
    def __init__(self, groups, pos):

        egg_img = pygame.image.load('../graphics/animals/chicken/nest/0.png')
        resized_img = pygame.transform.scale(egg_img, (egg_img.get_width()*4, egg_img.get_height()*4))
        egg_surf = resized_img.convert_alpha()
        empty_img = pygame.image.load('../graphics/animals/chicken/nest/1.png')
        resized_img = pygame.transform.scale(empty_img, (empty_img.get_width()*4, empty_img.get_height()*4))
        empty_surf = resized_img.convert_alpha()

        #self.hitbox = resized_img.get_rect(topleft = pos).inflate((-20, -resized_img.get_height()*0.6))

        self.frames = [empty_surf, egg_surf]
        self.frame_index = 0
        self.pos = pos

        #egg
        self.has_egg = False



        super().__init__(
            pos = self.pos, 
            surf = self.frames[self.frame_index], 
            groups = groups
        ) 

    def egg(self):
        if self.frame_index == 0:
            self.frame_index = 1
            self.has_egg = True
            self.image = self.frames[self.frame_index]
    
    def pick_egg(self):
        if self.frame_index == 1:
            self.frame_index = 0
            self.has_egg = False
            self.image = self.frames[self.frame_index]
        

        
class Cow(Animal):
    def __init__(self, pos, frames_dict, groups, collision_sprites, name):
        super().__init__(
            pos = pos, 
            frames_dict = frames_dict, 
            groups = groups,
            collision_sprites = collision_sprites,
            name = name
            )
        self.hitbox = self.image.get_rect(topleft = pos).inflate((-20, -self.rect.height*0.6))

        

