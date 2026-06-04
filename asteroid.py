import pygame
import random
from pygame import Surface
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS, ASTEROID_KINDS
from logger import log_event
from circleshape import CircleShape

class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float, velocity: pygame.Vector2) -> None:
        super().__init__(x, y, radius)
        self.velocity = velocity
        # Smaller and faster asteroids score more because they are harder to hit
        self.value = ASTEROID_MIN_RADIUS * ASTEROID_KINDS + ASTEROID_MIN_RADIUS - self.radius + velocity.length()

    def draw(self, screen: Surface) -> None:
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            log_event("asteroid_split")

            split_angle = random.uniform(20, 50)
            first_asteroid_direction = self.velocity.rotate(split_angle)
            second_asteroid_direction = self.velocity.rotate(-split_angle)

            new_radius = self.radius - ASTEROID_MIN_RADIUS

            Asteroid(self.position.x, self.position.y, new_radius, first_asteroid_direction * 1.2)
            Asteroid(self.position.x, self.position.y, new_radius, second_asteroid_direction * 1.2)