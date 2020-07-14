# Made by Lytix 01.01.2020
import pygame
from random import randint, uniform, choice
import math

vector = pygame.math.Vector2
gravity = vector(0, 0.3)
DISPLAY_WIDTH = DISPLAY_HEIGHT = 800


class Firework:

    def __init__(self):
        self.colour = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.colours = ((randint(0, 255), randint(0, 255), randint(0, 255)), (randint(0, 255), randint(0, 255), randint(0, 255)), (randint(0, 255), randint(0, 255), randint(0, 255)))
        self.firework = Particle(randint(0, DISPLAY_WIDTH), DISPLAY_HEIGHT, True, self.colour)  # Creates the firework particle
        self.exploded = False
        self.particles = []

        # variable constants
        self.min_max_particles = vector(75, 200)

    def update(self, win):  # called every frame
        if not self.exploded:
            self.firework.apply_force(gravity)
            self.firework.move()
            self.show(win)

            if self.firework.vel.y >= 0:
                self.exploded = True
                self.explode()
        else:
            for particle in self.particles:
                particle.apply_force(gravity)
                particle.move()
                particle.show(win)

    def explode(self):
        amount = randint(self.min_max_particles.x, self.min_max_particles.y)
        for i in range(amount):
            self.particles.append(Particle(self.firework.pos.x, self.firework.pos.y, False, self.colours))

    def show(self, win):
        pygame.draw.circle(win, self.colour, (int(self.firework.pos.x), int(self.firework.pos.y)), self.firework.size)

    def remove(self):
        if self.exploded:
            for p in self.particles:
                if p.remove is True:
                    self.particles.remove(p)

            if len(self.particles) == 0:
                return True
            else:
                return False


class Particle:

    def __init__(self, x, y, firework, colour):
        self.firework = firework
        self.pos = vector(x, y)
        self.origin = vector(x, y)
        # self.colour = colour
        # colours = [(0, 255, 255), (0, 255, 255), (195, 255, 0)]

        self.radius = 20
        self.remove = False
        self.explosion_radius = randint(8, 12)
        self.life = 0
        self.acc = vector(0, 0)

        if self.firework:
            self.vel = vector(0, -randint(16, 19))
            self.size = 3
            self.colour = colour
        else:
            self.vel = vector(uniform(-1, 1), uniform(-1, 1))
            self.vel.x *= randint(12, 15)
            self.vel.y *= randint(12, 15)
            self.size = randint(1, 3)
            self.colour = choice(colour)

    def apply_force(self, force):
        self.acc += force

    def move(self):
        if not self.firework:
            self.vel.x *= 0.8
            self.vel.y *= 0.8

        self.vel += self.acc
        self.pos += self.vel
        self.acc *= 0

        if self.life == 0 and not self.firework:  # check if particle is outside explosion radius
            distance = math.sqrt((self.pos.x - self.origin.x) ** 2 + (self.pos.y - self.origin.y) ** 2)
            if distance > self.explosion_radius:
                self.remove = True

        self.decay()

        self.life += 1

    def show(self, win):
        pygame.draw.circle(win, (self.colour[0], self.colour[1], self.colour[2], 0), (int(self.pos.x), int(self.pos.y)), self.size)

    def decay(self):  # random decay of the particles
        if 50 > self.life > 10:  # early stage their is a small chance of decay
            ran = randint(0, 30)
            if ran == 0:
                self.remove = True
        elif self.life > 50:
            ran = randint(0, 5)
            if ran == 0:
                self.remove = True


def play_sound():
    # pygame.mixer.music.play()
    pass


def update(win, fireworks):
    for fw in fireworks:
        fw.update(win)
        if fw.exploded is True and fw.particles[0].life == 0:
            play_sound()
        if fw.remove():
            fireworks.remove(fw)

    pygame.display.update()


def main():
    sound_file = 'firework_sound.mp3'
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.display.set_caption("Fireworks in Pygame")
    win = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    clock = pygame.time.Clock()

    fireworks = [Firework() for i in range(1)]  # create the first fireworks
    running = True

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        win.fill((20, 20, 30))  # draw background

        if randint(0, 20) == 1:  # create new firework
            fireworks.append(Firework())

        update(win, fireworks)

    pygame.quit()
    quit()


main()
