__author__ = 'Kody'

import pygame
from pygame.locals import *

pygame.init()

def main():
    snowSurf = pygame.Surface((300, 300), pygame.SRCALPHA)
    pygame.draw.circle(snowSurf, (255,255,255,255), (150,150), 150, 50)
    #pygame.draw.circle(snowSurf, (255, 255, 255, 255), (100, 100), 100)
    pygame.image.save(snowSurf, "snow.png")
    pygame.quit()
    exit()

main()