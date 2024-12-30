from os import walk
import pygame 

def import_folder(path):
    surface_list = []

    for folder_name, sub_folder, img_files in walk(path):

        img_files = sorted(img_files) # correct amimation order

        for img in img_files:
            full_path = path + '/' + img
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)
        

    return surface_list 