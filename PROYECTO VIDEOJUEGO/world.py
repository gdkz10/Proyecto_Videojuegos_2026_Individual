import pygame
import random
import os
from settings import TILE_SIZE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def asset(path):
    return os.path.join(BASE_DIR, path)

class World:
    def __init__(self):
        self.seed = 777
        self.chunk_size = 16
        self.last_encounter_time = 0

        self.tiles = {}
        self.load_assets()

    def load_assets(self):
        files = {
            0: "assets/tiles/grass.png",
            1: "assets/tiles/tree.png",
            2: "assets/tiles/path.png",
            3: "assets/tiles/tall_grass.png",
            4: "assets/tiles/wall.png",
        }

        self.use_images = True

        for k, path in files.items():
            full = asset(path)

            if not os.path.exists(full):
                print("Falta:", full)
                self.use_images = False
                continue

            img = pygame.image.load(full).convert_alpha()
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            self.tiles[k] = img

    def get_chunk_type(self, cx, cy):
        random.seed(cx * 9999 + cy * 5555 + self.seed)
        r = random.random()

        if r < 0.15:
            return "city"
        elif r < 0.5:
            return "route"
        return "wild"

    def has_vertical_road(self, cx):
        random.seed(cx * 1234 + self.seed)
        return random.random() < 0.7

    def has_horizontal_road(self, cy):
        random.seed(cy * 5678 + self.seed)
        return random.random() < 0.7

    def get_tile(self, x, y):

        cx = x // self.chunk_size
        cy = y // self.chunk_size

        lx = x % self.chunk_size
        ly = y % self.chunk_size

        chunk = self.get_chunk_type(cx, cy)
        center = self.chunk_size // 2

        if self.has_vertical_road(cx) and lx == center:
            return 2

        if self.has_horizontal_road(cy) and ly == center:
            return 2

        if chunk == "city":

            if lx == 0 or ly == 0 or lx == self.chunk_size-1 or ly == self.chunk_size-1:
                return 4

            if lx == center or ly == center:
                return 2

            return 0

        elif chunk == "route":

            if ly == center:
                return 2
            if abs(ly - center) <= 3:
                return 3
            if ly == center - 4 or ly == center + 4:
                return 1
            return 0
        else:
            random.seed(x * 888 + y * 444)

            if random.random() < 0.1:
                return 1

            if random.random() < 0.6:
                return 3

            return 0

    def draw(self, screen, player):
        w, h = screen.get_size()

        cam_x = player.x - w // 2
        cam_y = player.y - h // 2

        tiles_x = w // TILE_SIZE + 2
        tiles_y = h // TILE_SIZE + 2

        start_x = int(cam_x // TILE_SIZE)
        start_y = int(cam_y // TILE_SIZE)

        for y in range(tiles_y):
            for x in range(tiles_x):

                wx = start_x + x
                wy = start_y + y

                tile = self.get_tile(wx, wy)

                sx = x * TILE_SIZE - (cam_x % TILE_SIZE)
                sy = y * TILE_SIZE - (cam_y % TILE_SIZE)

                if self.use_images and tile in self.tiles:
                    screen.blit(self.tiles[tile], (sx, sy))
                else:
                    color = (100,180,100)
                    if tile == 1: color = (30,100,30)
                    elif tile == 2: color = (200,180,120)
                    elif tile == 3: color = (20,130,20)
                    elif tile == 4: color = (100,100,100)

                    pygame.draw.rect(screen, color, (sx, sy, TILE_SIZE, TILE_SIZE))

    def is_blocked(self, x, y):
        tile = self.get_tile(x // TILE_SIZE, y // TILE_SIZE)

        return tile in (1, 4)  # árbol y muro bloquean

    def check_encounter(self, player):
        current_time = pygame.time.get_ticks()
        tile = self.get_tile(player.x // TILE_SIZE, player.y // TILE_SIZE)

        if tile == 2:
            return None

        if not hasattr(player, "steps"):
            player.steps = 0
            player.last_pos = (player.x, player.y)

        if (player.x, player.y) != player.last_pos:
            player.steps += 1
            player.last_pos = (player.x, player.y)

        if tile == 3:
            chance = 0.9
            cooldown = 15000
            steps_needed = 2
        else:
            chance = 0.2
            cooldown = 60000
            steps_needed = 6

        if current_time - self.last_encounter_time < cooldown:
            return None

        if player.steps < steps_needed:
            return None

        player.steps = 0

        if random.random() < chance:
            self.last_encounter_time = current_time
            return "wild"

        if len(player.team) == 3 and random.random() < 0.25:
            self.last_encounter_time = current_time
            return "trainer"

        return None

    def get_player_start(self):
        return 0, 0