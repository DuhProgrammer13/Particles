__author__ = 'Kody'

import ParticleTools
import pygame
import sys
import ParticleEmitter
from Particle import Particle
from pygame.locals import *

SCREEN_SIZE = (800, 600)
FPS = 50

class Main:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        self.DISPLAY_SURF = pygame.display.set_mode(SCREEN_SIZE)
        self.CLOCK = pygame.time.Clock()

        self.torchSelected = True
        self.snowing = False

        self.fairy = pygame.image.load("Images/navi.png")
        self.fairy = pygame.transform.scale(self.fairy, (50, 50))
        self.unlit_torch = pygame.image.load("Images/unlit_torch.png")
        self.unlit_torch = pygame.transform.rotate(self.unlit_torch, 90)
        self.unlit_torch = pygame.transform.scale(self.unlit_torch, (50, 200))
        self.flames = ParticleEmitter.ParticleEmitter("ParticlesFile/torch.pypart", (0, 0, 800, 600))
        self.flames.turn_on()
        self.fairy_trail = ParticleEmitter.ParticleEmitter("ParticlesFile/fairy.pypart", (0, 0, 800, 600))
        self.fairy_trail.turn_on()
        self.explosion = ParticleEmitter.ParticleEmitter("ParticlesFile/explosion.pypart", (0, 0, 800, 600))
        self.snow = ParticleEmitter.ParticleEmitter("ParticlesFile/snow.pypart", (0, 0, 800, 600))

        self.main_loop()

    def main_loop(self):
        while True:
            deltaTime = ParticleTools.getTime()
            self.update(deltaTime)
            self.draw()



    def update(self, dt):
        self.CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                if self.torchSelected:
                    self.flames.set_position(event.pos)
                    self.explosion.set_position(event.pos)
                else:
                    self.fairy_trail.set_position(event.pos)
            elif event.type == KEYDOWN:
                if event.key == K_f:
                    self.flames.toggle_on()
                elif event.key == K_i:
                    self.flames.toggle_freeze()
                elif event.key == K_e:
                    self.explosion.turn_on()
                elif event.key == K_t:
                    self.switch()
                elif event.key == K_s:
                    self.toggle_snow()

        self.snow.update_particles(dt, FPS)
        self.flames.update_particles(dt, FPS)
        self.explosion.update_particles(dt, FPS)
        self.fairy_trail.update_particles(dt, FPS)

        self.explosion.turn_off()
        #self.snowGroup.update_particles(dt, FPS)

    def draw(self):
        self.DISPLAY_SURF.fill((0,0,0))
        self.DISPLAY_SURF.blit(self.unlit_torch, (self.flames.get_position()[0]+10, self.flames.get_position()[1]+10))
        self.flames.draw(self.DISPLAY_SURF)
        self.explosion.draw(self.DISPLAY_SURF)
        self.fairy_trail.draw(self.DISPLAY_SURF)
        self.DISPLAY_SURF.blit(self.fairy, (self.fairy_trail.get_position()[0]-25, self.fairy_trail.get_position()[1]-25))
        self.snow.draw(self.DISPLAY_SURF)
        #self.snowGroup.draw(self.DISPLAY_SURF)

        pygame.display.update()

    def switch(self):
        self.torchSelected = not self.torchSelected

    def toggle_snow(self):
        self.snow.toggle_on()

if __name__ == "__main__":
    Main()
