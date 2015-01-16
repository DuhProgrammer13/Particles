__author__ = 'Kody'

class Gravity:
    def __init__(self, gravity):
        self.gravity = gravity
    def applyGravity(self, speedY, speedX, delta):
        return speedY + self.gravity * delta, speedX
    def set_gravity(self, gravity):
        self.gravity = gravity