import pygame
import os
import random
from settings import TILE_SIZE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def asset(path):
    return os.path.join(BASE_DIR, path)

class NPC:
    def __init__(self, x, y, sprite_path):

        self.x = x
        self.y = y
        self.size = TILE_SIZE
        self.img_path = sprite_path
        self.name = "Entrenador"

        self.defeated = False

        self.team = self.generate_team()

        try:
            self.image = pygame.transform.scale(
                pygame.image.load(asset(sprite_path)).convert_alpha(),
                (self.size, self.size)
            )
        except:
            self.image = None

    def generate_team(self):
        ecos = ["Phantom", "Zabbit", "Licht"]  # 👈

        return [{
            "name": random.choice(ecos),
            "hp": 100,
            "type": "Desconocido"
        } for _ in range(3)]

    def draw(self, screen, offset_x, offset_y):
        draw_x = self.x - offset_x
        draw_y = self.y - offset_y

        if self.image:
            screen.blit(self.image, (draw_x, draw_y))
        else:
            pygame.draw.rect(screen, (255,0,0), (draw_x, draw_y, self.size, self.size))

    def check_collision(self, player):
        player_tile_x = player.x // self.size
        player_tile_y = player.y // self.size

        npc_tile_x = self.x // self.size
        npc_tile_y = self.y // self.size

        return player_tile_x == npc_tile_x and player_tile_y == npc_tile_y