import pygame
import sys

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0.0

    font = pygame.font.Font(None, 35)

    # Load background image and create shade
    bg_image = pygame.image.load("background.jpg").convert()
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    shade_bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    shade_bg.set_alpha(100)

    # pygame grouping
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, drawable, updatable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    # Main game loop
    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # set background and apply shading
        screen.blit(bg_image, (0, 0))
        screen.blit(shade_bg, (0, 0))

        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                if player.shield_duration > 0:
                    continue
                log_event("player_hit")
                player.lives -=1
                if player.lives <= 0:
                    print(f"Game over! Your score: {player.score}")
                    sys.exit()
                player.shield_duration = 2
                player.rotation = 0
                player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    shot.kill()
                    player.score += asteroid.value
                    asteroid.split()

        for sprite in drawable:
            sprite.draw(screen)

        top_bar = font.render(f"Lives: {player.lives} Score: {int(player.score)}", True, "white")
        screen.blit(top_bar, (10, 10)) 

        pygame.display.flip()

        # Limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
