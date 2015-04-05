__author__ = 'Kody'

import pygame

to_size = (200, 200)
file_name = "fire.png"

def main():
    pygame.init()
    image = pygame.image.load(file_name)
    image = pygame.transform.scale(image, to_size)
    pygame.image.save(image, file_name)
    pygame.quit()
    exit()

main()
