import pygame

class Timer:
    
    def __init__(self, duration, func = None):
        self.duration = duration
        self.func = func
        self.start_time = 0
        self.active = False

    def activate(self):
        self.start_time = pygame.time.get_ticks()
        self.active = True
    
    def deactivate(self):
        self.start_time = 0
        self.active = False

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration:
            if(self.func and self.start_time != 0):
                self.func()
            self.deactivate()
    
