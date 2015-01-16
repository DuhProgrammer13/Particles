__author__ = 'Kody'

from pygame.locals import SRCALPHA
import Particle
import pygame
from pygame.sprite import Group
from pygame.rect import Rect
import random

titles = ["PARTICLE", "EMITTER"]
class ParticleEmitter(Group):
    PARTICLE_COUNT = "particle_count"
    PARTICLE_COUNT_MIN = "particle_count_min"
    PARTICLE_COUNT_MAX = "particle_count_max"
    POSITION = "position"
    PARTICLE_EMISSION_AREA = "particle_emission_area"
    PARTICLE_EMISSION_FILL = "particle_emission_fill_area"
    AREA_RECT = "allowed_area_for_particles"

    # TODO needs emitter image for things such as: torch, cursor, fairy, etc.
    # TODO needs emitter timing for things such as
    # TODO needs emitter switch for on or off for things such as bombs/explosions
    # TODO needs emitter FREEZE for slower computers such as the raspberry pi

    def __init__(self, particle, particle_area_allowed=None):
        Group.__init__(self)

        self.newParticleAttributes = {}
        self.attributes = {}
        self.tempAttributes = {}

        self.setup_attributes()
        self.read_particle(particle)
        self.adjust_attributes(particle_area_allowed)

        self.on = False
        self.frozen = False

        if particle_area_allowed != None:
            self.set_position(self.attributes[ParticleEmitter.AREA_RECT].topleft)

    def update_particles(self, delta, target_fps):
        if self.frozen:
            return

        for particle in self.sprites():
            particle.update(delta)
            if (particle.rect.x < self.attributes[ParticleEmitter.AREA_RECT].x and particle.attributes[Particle.GRAVITY_X] <= 0 or
                particle.rect.x > self.attributes[ParticleEmitter.AREA_RECT].right and particle.attributes[Particle.GRAVITY_X] >= 0 or
                particle.rect.y < self.attributes[ParticleEmitter.AREA_RECT].y and particle.attributes[Particle.GRAVITY_Y] <= 0 or
                particle.rect.y > self.attributes[ParticleEmitter.AREA_RECT].bottom and particle.attributes[Particle.GRAVITY_Y] >= 0 or
                particle.attributes[Particle.TOTAL_LIFE] > 0 and particle.attributes[Particle.REMAINING_LIFE] == 0):
                self.remove(particle)
                particle.remove(self)
                self.update_sprite_count()

        if not self.on: # if off skip putting more particles on screen
            return

        if (delta-0.25 > (1.0/target_fps)  * 100 or self.attributes[ParticleEmitter.PARTICLE_COUNT] > self.attributes[ParticleEmitter.PARTICLE_COUNT_MAX]):
            return

        elif self.attributes[ParticleEmitter.PARTICLE_COUNT] < self.attributes[ParticleEmitter.PARTICLE_COUNT_MIN]:
            while self.attributes[ParticleEmitter.PARTICLE_COUNT] < self.attributes[ParticleEmitter.PARTICLE_COUNT_MIN]:
                self.add(Particle.Particle(self.get_available_pos(), self, **self.newParticleAttributes))
                self.update_sprite_count()


        elif (delta + 0.25 < (1.0 / target_fps) * 100):
            while self.attributes[ParticleEmitter.PARTICLE_COUNT] < self.attributes[ParticleEmitter.PARTICLE_COUNT_MIN]:
                self.add(Particle.Particle(self.get_available_pos(), self, **self.newParticleAttributes))
                self.attributes[ParticleEmitter.PARTICLE_COUNT] = len(self.sprites())
            return

        for _ in range(1, (self.attributes[ParticleEmitter.PARTICLE_COUNT_MAX] / (target_fps/2) if (
                    self.attributes[ParticleEmitter.PARTICLE_COUNT_MAX] / target_fps) > 1 else 2)):
            self.add(Particle.Particle(self.get_available_pos(), self, **self.newParticleAttributes))
            self.update_sprite_count()

    def update_sprite_count(self):
        self.attributes[ParticleEmitter.PARTICLE_COUNT] = len(self.sprites())

    def get_available_pos(self):
        randomSide = random.randint(1, 4)
        if self.attributes[ParticleEmitter.PARTICLE_EMISSION_FILL]:
            randomSide = 5
        x = self.attributes[ParticleEmitter.PARTICLE_EMISSION_AREA].x
        y = self.attributes[ParticleEmitter.PARTICLE_EMISSION_AREA].y
        if randomSide == 1:
            x = random.randint(self.attributes[ParticleEmitter.PARTICLE_EMISSION_AREA].x,
                               self.attributes[ParticleEmitter.PARTICLE_EMISSION_AREA].x+self.attributes[ParticleEmitter.PARTICLE_EMISSION_AREA].width)
        elif randomSide == 2:
            x = self.attributes[ParticleEmitter.PARTICLE_EMISSION_AREA].x + self.attributes[ParticleEmitter.PARTICLE_EMISSION_AREA].width
            y = random.randint(self.attributes[ParticleEmitter.PARTICLE_EMISSION_AREA].y,
                               self.attributes[ParticleEmitter.PARTICLE_EMISSION_AREA].y+self.attributes[ParticleEmitter.PARTICLE_EMISSION_AREA].height)
        elif randomSide == 3:
            x = random.randint(self.attributes[ParticleEmitter.PARTICLE_EMISSION_AREA].x,
                               self.attributes[ParticleEmitter.PARTICLE_EMISSION_AREA].x+self.attributes[ParticleEmitter.PARTICLE_EMISSION_AREA].width)
            y = self.attributes[ParticleEmitter.PARTICLE_EMISSION_AREA].y + self.attributes[ParticleEmitter.PARTICLE_EMISSION_AREA].height
        elif randomSide == 4:
            y = random.randint(self.attributes[ParticleEmitter.PARTICLE_EMISSION_AREA].y,
                               self.attributes[ParticleEmitter.PARTICLE_EMISSION_AREA].y+self.attributes[ParticleEmitter.PARTICLE_EMISSION_AREA].height)
        elif randomSide == 5:
            x = random.randint(self.attributes[ParticleEmitter.PARTICLE_EMISSION_AREA].x,
                               self.attributes[ParticleEmitter.PARTICLE_EMISSION_AREA].x+self.attributes[ParticleEmitter.PARTICLE_EMISSION_AREA].width)
            y = random.randint(self.attributes[ParticleEmitter.PARTICLE_EMISSION_AREA].y,
                               self.attributes[ParticleEmitter.PARTICLE_EMISSION_AREA].y+self.attributes[ParticleEmitter.PARTICLE_EMISSION_AREA].height)

        return (x, y)

    def setup_attributes(self):
        self.attributes[ParticleEmitter.PARTICLE_COUNT] = 0
        self.attributes[ParticleEmitter.PARTICLE_COUNT_MIN] = 0
        self.attributes[ParticleEmitter.PARTICLE_COUNT_MAX] = 0
        self.attributes[ParticleEmitter.POSITION] = (0, 0)
        self.attributes[ParticleEmitter.PARTICLE_EMISSION_AREA] = Rect(0, 0, 1, 1)
        self.attributes[ParticleEmitter.PARTICLE_EMISSION_FILL] = True
        self.attributes[ParticleEmitter.AREA_RECT] = Rect(0, 0, 1, 1)

    def read_particle(self, particle):
        f = open(particle)
        particle_content = f.readlines()
        content_area = None
        for content in particle_content:
            content = content.strip("\n")
            if content in titles:
                content_area = content
                continue
            if content_area == None:
                continue
            if content == None:
                continue
            if content_area == titles[0]:
                self.newParticleAttributes[content.split(":")[0]] = content.split(":")[1]
            elif content_area == titles[1]:
                self.tempAttributes[content.split(":")[0]] = content.split(":")[1]

    def set_position(self, pos):
        self.attributes[ParticleEmitter.POSITION] = pos
        self.attributes[ParticleEmitter.PARTICLE_EMISSION_AREA].x = pos[0]
        self.attributes[ParticleEmitter.PARTICLE_EMISSION_AREA].y = pos[1]

    def get_position(self):
        return self.attributes[ParticleEmitter.POSITION]

    def adjust_attributes(self, area_rect_allowed):
        if (ParticleEmitter.PARTICLE_EMISSION_AREA in self.tempAttributes.keys()):
            self.attributes[ParticleEmitter.PARTICLE_EMISSION_AREA] = Rect(eval(self.tempAttributes[ParticleEmitter.PARTICLE_EMISSION_AREA]))
        if (ParticleEmitter.PARTICLE_EMISSION_FILL in self.tempAttributes.keys()):
            self.attributes[ParticleEmitter.PARTICLE_EMISSION_FILL] = eval(self.tempAttributes[ParticleEmitter.PARTICLE_EMISSION_FILL])
        if (ParticleEmitter.PARTICLE_COUNT in self.tempAttributes.keys()):
            self.attributes[ParticleEmitter.PARTICLE_COUNT] = int(self.tempAttributes[ParticleEmitter.PARTICLE_COUNT])
        if (ParticleEmitter.PARTICLE_COUNT_MIN in self.tempAttributes.keys()):
            self.attributes[ParticleEmitter.PARTICLE_COUNT_MIN] = int(self.tempAttributes[ParticleEmitter.PARTICLE_COUNT_MIN])
        if (ParticleEmitter.PARTICLE_COUNT_MAX in self.tempAttributes.keys()):
            self.attributes[ParticleEmitter.PARTICLE_COUNT_MAX] = int(self.tempAttributes[ParticleEmitter.PARTICLE_COUNT_MAX])
        if (ParticleEmitter.POSITION in self.tempAttributes.keys()):
            self.attributes[ParticleEmitter.POSITION] = eval(self.tempAttributes[ParticleEmitter.POSITION])
        if area_rect_allowed != None:
            self.attributes[ParticleEmitter.AREA_RECT] = Rect(area_rect_allowed)
        for key, value in self.newParticleAttributes.items():
            if key == "image":
                self.newParticleAttributes[key] = self.draw_image()
            else:
                self.newParticleAttributes[key] = eval(value)

    def draw_image(self):
        print "draw?"
        returnImage = pygame.Surface((200, 200), SRCALPHA)
        if self.newParticleAttributes[Particle.IMAGE] != None:
            try:
                print self.newParticleAttributes[Particle.IMAGE]
                new_image = pygame.image.load(self.newParticleAttributes[Particle.IMAGE])
                new_image = new_image.convert_alpha()
                returnImage = pygame.Surface(new_image.get_size(), SRCALPHA)
                returnImage.blit(new_image, (0, 0))
            except:
                # Draw on sprite
                pygame.draw.circle(returnImage, (255, 0, 255, 100), (200 / 2, 200 / 2), 200 / 2, 1)
                pygame.draw.circle(returnImage, (255, 255, 255, 100), (200 / 2, 200 / 2), 200 / 2 - 2)
        else:
            pygame.draw.rect(returnImage, (200, 0, 255), (0, 0, 200, 200))
            pygame.draw.rect(returnImage, (200, 0, 0, 100), (2, 2, 200 - 4, 200 - 4))

        return returnImage

    def turn_on(self):
        self.on = True
    def turn_off(self):
        self.on = False
    def toggle_on(self):
        self.on = not self.on

    def freeze(self):
        self.frozen = True
    def unfreeze(self):
        self.frozen = False
    def toggle_freeze(self):
        self.frozen = not self.frozen
