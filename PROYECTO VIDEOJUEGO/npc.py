import pygame
import random
import os
from settings import TILE_SIZE
from eco import Eco

def _find_project_root():
    current = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.basename(current) == "PROYECTO VIDEOJUEGO":
            return current
        parent = os.path.dirname(current)
        if parent == current:
            return os.path.dirname(os.path.abspath(__file__))
        current = parent

BASE_DIR = _find_project_root()

def asset(relative_path):
    return os.path.join(BASE_DIR, relative_path)


class NPC:
    def __init__(self, x, y):
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE

        self.size    = TILE_SIZE
        self.speed   = 2
        self.color   = (255, 0, 0)

        self.vision_range = 5
        self.chasing  = False
        self.defeated = False

        try:
            self.image = pygame.transform.scale(
                pygame.image.load(asset("assets/npc/npc.png")),
                (TILE_SIZE, TILE_SIZE)
            )
            self.use_image = True
        except FileNotFoundError:
            print("No se encontró assets/npc/npc.png")
            self.use_image = False
        except Exception as e:
            print(f"Error cargando NPC: {e}")
            self.use_image = False

        self.ecos = [
            Eco("Eco Sombrío", random.randint(8, 12)),
            Eco("Eco Feroz",   random.randint(10, 15))
        ]
        self.hp = 80

    def can_see_player(self, player):
        dx = abs(player.x - self.x)
        dy = abs(player.y - self.y)
        return dx < self.vision_range * TILE_SIZE and dy < self.vision_range * TILE_SIZE

    def move_towards_player(self, player, world):
        dx = player.x - self.x
        dy = player.y - self.y
        step_x = self.speed if dx > 0 else -self.speed
        step_y = self.speed if dy > 0 else -self.speed

        if abs(dx) > abs(dy):
            if not world.is_blocked(self.x + step_x, self.y):
                self.x += step_x
        else:
            if not world.is_blocked(self.x, self.y + step_y):
                self.y += step_y

    def update(self, player, world):
        if self.defeated:
            return False
        if self.can_see_player(player):
            self.chasing = True
        if self.chasing:
            self.move_towards_player(player, world)
            if abs(player.x - self.x) < TILE_SIZE and abs(player.y - self.y) < TILE_SIZE:
                return True
        return False

    def draw(self, screen, camera):
        screen_x = self.x - camera.offset_x + 400
        screen_y = self.y - camera.offset_y + 300

        if self.use_image:
            screen.blit(self.image, (screen_x, screen_y))
        else:
            pygame.draw.rect(screen, self.color, (screen_x, screen_y, self.size, self.size))