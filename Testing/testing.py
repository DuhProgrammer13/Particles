from Main import ParticleEmitter

__author__ = 'Kody'

import pygame
import time


pygame.init()
DISPLAYSURF = pygame.display.set_mode((200, 200))

timeTakenWithLoading = []
timeTakenWithoutLoading = []

test_loading = False
test_emitter = True

def main():
    startingTime = time.time()
    for x in range(100):
        DISPLAYSURF.fill((0,0,0))
        DISPLAYSURF.blit(pygame.image.load("snow.png"), (0, 0))
    endingTime = time.time()

    print "With loading : %s" % (endingTime - startingTime)
    timeTakenWithLoading.append(endingTime-startingTime)

    startingTime = time.time()
    image = pygame.image.load("snow.png")
    for x in range(100):
        DISPLAYSURF.fill((0,0,0))
        DISPLAYSURF.blit(image, (0,0))
    endingTime = time.time()

    print "Without loading: %s" % (endingTime - startingTime)
    timeTakenWithoutLoading.append(endingTime-startingTime)
    print "-" * 10

if test_loading:
    for x in range(10):
        main()

    averageWith = 0
    for item in timeTakenWithLoading:
        averageWith += item
    print "Average With = %s" % (averageWith/len(timeTakenWithLoading))

    averageWithout = 0
    for item in timeTakenWithoutLoading:
        averageWithout += item
    print "Average Without = %s" % (averageWithout / len(timeTakenWithoutLoading))

    print "Difference of Average = %s" % (averageWith - averageWithout)

    print "With 5,000 Loads in just 2 minutes that's a difference of %s" % ((averageWith - averageWithout) * 50)

def testing_particles():
    startTime = time.time()
    emitter = ParticleEmitter.ParticleEmitter("particles.pypart", pygame.Rect(0, 0, 800, 600))
    emitter.turn_on()

    for x in range(1):
        emitter.update_particles(1.50001049042,50)
        emitter.draw(DISPLAYSURF)
        pygame.display.update()
    endTime = time.time()

    print "time_taken = %s" % (endTime - startTime)
    startTime = time.time()
    for x in range(500):
        print emitter.attributes[ParticleEmitter.ParticleEmitter.PARTICLE_COUNT]
        emitter.update_particles(1.50001049042, 50)
        emitter.draw(DISPLAYSURF)
        pygame.display.update()
    endTime = time.time()

    print "time_taken = %s" % (endTime - startTime)

if test_emitter:
    testing_particles()