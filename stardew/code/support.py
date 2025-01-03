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

def import_folder_size(path, animal):
    surface_list = []

    for folder_name, sub_folder, img_files in walk(path):
        img_files = sorted(img_files) # correct amimation order
        for img in img_files:
            full_path = path + '/' + img
            if animal == 'chicken':
                image = pygame.image.load(full_path)
                sized_image = pygame.transform.scale(image, (64,64))
            image_surface = sized_image.convert_alpha()
            surface_list.append(image_surface)
            
    return surface_list

def import_folder_dict(path):
    surface_dict = {}

    for folder_name, sub_folder, img_files in walk(path):   
        for img in img_files:
            full_path = path + '/' + img
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_dict[img.split('.')[0]] = image_surface
        
    return surface_dict



