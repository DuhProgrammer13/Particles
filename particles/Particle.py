__author__ = 'Kody'
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.locals import SRCALPHA
import time
from pygame import transform
import random


# Constants used to make code more readable and easier to edit
IMAGE = "image"
MAX_SIZE = "maxsize"
MIN_SIZE = "minsize"
ROTATE = "rotate"
GRAVITY_X = "gravity_x"
GRAVITY_Y = "gravity_y"
GRAVITY_X_RANGE = "gravity_x_range"
GRAVITY_Y_RANGE = "gravity_y_range"
SPEED_X = "speed_x"
SPEED_Y = "speed_y"
SPEED_X_RANGE = "speed_x_range"
SPEED_Y_RANGE = "speed_y_range"
ZERO_OUT_X = "zero_x"
SLOWLY_DISAPPEAR = "slowly_disappear"
TOTAL_LIFE = "total_life"
REMAINING_LIFE = "remaining_life"
MAX_LIFE = "max_life"
MIN_LIFE = "min_life"


class Particle(Sprite):
    def __init__(self, pos, group, **kwargs):
        # Use the key word args to add more depth to the particle (i.e. Color tinting, Min Size, Max Size, etc)
        self.attributes = {}
        self.setup_attributes()
        self.use_kwargs(**kwargs)
        self.setup_speed()
        self.setup_gravity()

        # Init sprite
        Sprite.__init__(self, group)

        if self.attributes[ROTATE]:
            self.rotationAmount = random.randint(-90, 90)
            self.rotationSpeed = random.randint(-10, 10)
        else:
            self.rotationAmount = 0
            self.rotationSpeed0 = 0

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        rand_size = random.randint(self.attributes[MIN_SIZE], self.attributes[MAX_SIZE])
        self.image = Surface((rand_size, rand_size), SRCALPHA)
        self.originalImage = self.image

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        # Create Speed for acceleration and physics
        self.speedY = -2.0

        # Draw on the sprite
        self.draw_image()

        self.adjust_as_necessary()

    def update(self, delta):
        if self.attributes[ROTATE]:
            self.image = transform.rotate(self.originalImage, self.rotationAmount)
            # self.rect.width = self.image.get_width()
            #self.rect.height = self.image.get_height()
            self.rotationAmount += self.rotationSpeed * delta

        self.rect.y += int(self.attributes[SPEED_Y] * delta)
        self.rect.x += int(self.attributes[SPEED_X] * delta)

        self.update_alpha(delta)
        self.update_gravity(delta)
        self.update_life(delta)

    def use_kwargs(self, **kwargs):
        for key, value in kwargs.items():
            if key not in self.attributes.keys():
                continue
            self.attributes[key] = value

        self.image = self.attributes["image"]

    def setup_attributes(self):
        self.attributes[IMAGE] = None
        self.attributes["color"] = None
        self.attributes[MIN_SIZE] = 5
        self.attributes[MAX_SIZE] = 20
        self.attributes[SPEED_X] = 0
        self.attributes[SPEED_Y] = 0
        self.attributes[SPEED_X_RANGE] = []
        self.attributes[SPEED_Y_RANGE] = []
        self.attributes[GRAVITY_X] = 0
        self.attributes[GRAVITY_Y] = 0
        self.attributes[GRAVITY_X_RANGE] = []
        self.attributes[GRAVITY_Y_RANGE] = []
        self.attributes[ROTATE] = False
        self.attributes[ZERO_OUT_X] = False
        self.attributes[SLOWLY_DISAPPEAR] = False
        self.attributes[REMAINING_LIFE] = 0
        self.attributes[TOTAL_LIFE] = 0

    def setup_speed(self):
        if len(self.attributes[SPEED_Y_RANGE]) == 2:
            while int(self.attributes[SPEED_Y] * 10) == 0:
                self.attributes[SPEED_Y] = random.randint(self.attributes[SPEED_Y_RANGE][0] * 100,
                                                      self.attributes[SPEED_Y_RANGE][1] * 100) / 100.0
        if len(self.attributes[SPEED_X_RANGE]) == 2:
            while int(self.attributes[SPEED_X] * 10) == 0:
                self.attributes[SPEED_X] = random.randint(self.attributes[SPEED_X_RANGE][0] * 100,
                                                      self.attributes[SPEED_X_RANGE][1] * 100) / 100.0

        return

    def setup_gravity(self):
        """Used to spread the gravity over the range given by GRAVITY_X_RANGE"""
        if len(self.attributes[GRAVITY_X_RANGE]) == 2:
            self.attributes[GRAVITY_X] = random.randint(self.attributes[GRAVITY_X_RANGE][0] * 100,
                                                        self.attributes[GRAVITY_X_RANGE][1] * 100) / 100.0
            if self.attributes[ZERO_OUT_X]:
                if self.attributes[GRAVITY_X] < 0 and self.attributes[SPEED_X] < 0:
                    self.attributes[GRAVITY_X] = self.attributes[GRAVITY_X_RANGE][0] if self.attributes[GRAVITY_X_RANGE][1] > 0 else 0.1
                elif self.attributes[GRAVITY_X] == 0:
                    self.attributes[GRAVITY_X] = - self.attributes[SPEED_X] / 10.0
        if len(self.attributes[GRAVITY_Y_RANGE]) == 2:
            self.attributes[GRAVITY_Y] = random.randint(self.attributes[GRAVITY_Y_RANGE][0] * 100,
                                                        self.attributes[GRAVITY_Y_RANGE][1] * 100) / 100.0

    def update_gravity(self, delta):
        # UPDATE VERTICAL SPEED BASED ON VERTICAL GRAVITY
        self.attributes[SPEED_Y] += self.attributes[GRAVITY_Y] * delta

        # UPDATE HORIZONTAL SPEED BASED ON HORIZONTAL GRAVITY
        # IF HORIZONTAL GRAVITY IS PULLING TOWARDS THE RIGHT
        if self.attributes[SPEED_X] > 0:
            if self.attributes[ZERO_OUT_X]:  # IF THE HORIZONTAL SPEED SHOULD SLOW DOWN
                if self.attributes[SPEED_X] + self.attributes[GRAVITY_X] * delta < 0:  # IF SPEED AFTER TAKING AWAY IS LESS THAN 0
                    self.attributes[SPEED_X] = 0  # SET SPEED TO AVOID JIGGLING MOTION OR OVERSHOT
                else:
                    self.attributes[SPEED_X] += self.attributes[GRAVITY_X] * delta  # GET CLOSER TO ZERO HORIZONTAL SPEED
            else:
                self.attributes[SPEED_X] += self.attributes[GRAVITY_X] * delta  # UPDATE HORIZONTAL SPEED BASED ON HORIZONTAL GRAVITY
        # IF HORIZONTAL GRAVITY IS PULLING TOWARDS THE LEFT
        elif self.attributes[SPEED_X] < 0:
            if self.attributes[ZERO_OUT_X]:  # IF THE HORIZONTAL SPEED SHOULD SLOW DOWN
                if self.attributes[SPEED_X] + self.attributes[GRAVITY_X] * delta > 0:  # IF SPEED AFTER TAKING AWAY IS GREATER THAN 0
                    self.attributes[SPEED_X] = 0  # SET SPEED TO AVOID JIGGLING MOTION OR OVERSHOT
                else:
                    self.attributes[SPEED_X] += self.attributes[GRAVITY_X] * delta  # GET CLOSER TO ZERO HORIZONTAL SPEED
            else:
                self.attributes[SPEED_X] += self.attributes[GRAVITY_X] * delta  # UPDATE HORIZONTAL SPEED BASED ON HORIZONTAL GRAVITY
        elif not self.attributes[ZERO_OUT_X]:  # IF NOT ZEROING OUT AT HORIZONTAL SPEED OF ZERO
            self.attributes[SPEED_X] += self.attributes[GRAVITY_X] * delta  # ACCELERATE HORIZONTALLY

    def update_alpha(self, delta):
        if self.attributes[SLOWLY_DISAPPEAR]:
            self.image.set_alpha((self.attributes[REMAINING_LIFE]/self.attributes[TOTAL_LIFE]) * 255)

    def update_life(self, delta):
        if self.attributes[TOTAL_LIFE] > 0 and self.attributes[REMAINING_LIFE] > 0:
            self.attributes[REMAINING_LIFE] -= 10 * delta
        else:
            self.attributes[REMAINING_LIFE] = 0

    def draw_image(self):
        self.image = transform.scale(self.attributes[IMAGE], (self.rect.width, self.rect.height))

    def adjust_as_necessary(self):
        if self.attributes[GRAVITY_X] == 0 and self.attributes[GRAVITY_Y] == 0:
            if len(self.attributes[GRAVITY_Y_RANGE]) != 0:
                if (self.attributes[GRAVITY_Y_RANGE][1] - self.attributes[GRAVITY_Y_RANGE][0]) != 0:
                    self.attributes[GRAVITY_Y] = 0.1
            if len(self.attributes[GRAVITY_X_RANGE]) != 0:
                if (self.attributes[GRAVITY_X_RANGE][1] - self.attributes[GRAVITY_X_RANGE][0]) != 0:
                    self.attributes[GRAVITY_X] = 0.1