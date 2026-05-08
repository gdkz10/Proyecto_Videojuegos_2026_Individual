import pygame
import os
from settings import TILE_SIZE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def asset(path):
    return os.path.join(BASE_DIR, path)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.target_x = x
        self.target_y = y

        self.speed = 4
        self.moving = False

        self.team = []

        self.direction = "down"

        self.load_sprites()

    def load_sprites(self):
        try:
            self.sprites = {
                "up": pygame.transform.scale(
                    pygame.image.load(asset("assets/player/up.png")).convert_alpha(),
                    (TILE_SIZE, TILE_SIZE)
                ),
                "down": pygame.transform.scale(
                    pygame.image.load(asset("assets/player/down.png")).convert_alpha(),
                    (TILE_SIZE, TILE_SIZE)
                ),
                "left": pygame.transform.scale(
                    pygame.image.load(asset("assets/player/left.png")).convert_alpha(),
                    (TILE_SIZE, TILE_SIZE)
                ),
                "right": pygame.transform.scale(
                    pygame.image.load(asset("assets/player/right.png")).convert_alpha(),
                    (TILE_SIZE, TILE_SIZE)
                ),
            }
            self.use_sprites = True
            print("Sprites del jugador cargados correctamente")
        except Exception as e:
            print("Error cargando sprites del jugador:", e)
            self.use_sprites = False

    def update(self, keys, world):

        if not self.moving:

            dx, dy = 0, 0

            if keys[pygame.K_w] or keys[pygame.K_UP]:
                dy = -TILE_SIZE
                self.direction = "up"
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                dy = TILE_SIZE
                self.direction = "down"
            elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                dx = -TILE_SIZE
                self.direction = "left"
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                dx = TILE_SIZE
                self.direction = "right"

            new_x = self.x + dx
            new_y = self.y + dy

            if not world.is_blocked(new_x, new_y):
                self.target_x = new_x
                self.target_y = new_y
                self.moving = True

        else:
            if self.x < self.target_x:
                self.x += self.speed
            if self.x > self.target_x:
                self.x -= self.speed
            if self.y < self.target_y:
                self.y += self.speed
            if self.y > self.target_y:
                self.y -= self.speed

            if abs(self.x - self.target_x) < self.speed:
                self.x = self.target_x
            if abs(self.y - self.target_y) < self.speed:
                self.y = self.target_y

            if self.x == self.target_x and self.y == self.target_y:
                self.moving = False

    def draw(self, screen, player):

        w, h = screen.get_size()

        px = w // 2
        py = h // 2

        if self.use_sprites:
            sprite = self.sprites[self.direction]
            screen.blit(sprite, (px, py))
        else:
            pygame.draw.rect(screen, (255, 0, 0), (px, py, TILE_SIZE, TILE_SIZE))