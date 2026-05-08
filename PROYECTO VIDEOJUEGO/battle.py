import pygame
import os
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def asset(path):
    return os.path.join(BASE_DIR, path)

class Battle:
    def __init__(self, player, mode="wild"):

        self.player = player
        self.mode = mode

        self.player_hp = 100

        self.running = True
        self.finished = False

        self.options = ["Atacar", "Ecos", "Absorber", "Huir"]
        self.selected = 0

        self.messages = []
        self.showing_message = False
        self.pending_finish = False
        self.enemy_turn = False

        try:
            self.font = pygame.font.Font(asset("assets/fonts/pokemon.ttf"), 15)
        except:
            self.font = pygame.font.SysFont("arial", 22)

        self.load_assets()
        self.create_enemies()

        self.add_message(f"{self.enemy_name} apareció!")

    def add_message(self, text, pos_x=0.12, pos_y=40):
        self.messages.append({
            "text": text,
            "x": pos_x,
            "y": pos_y
        })
        self.showing_message = True

    def next_message(self):
        if self.messages:
            self.messages.pop(0)

        if not self.messages:
            self.showing_message = False

            if self.enemy_hp <= 0:
                self.enemy_turn = False
                if self.pending_finish:
                    self.finish_battle()
                return

            if self.enemy_turn:
                self.do_enemy_attack()
                self.enemy_turn = False

            elif self.pending_finish:
                self.finish_battle()

    def draw_text_box(self, screen, message, w, h, box_h):

        text = message["text"]
        pos_x = message["x"]
        pos_y = message["y"]

        words = text.split(" ")
        lines = []
        current_line = ""

        max_width = w * 0.75

        for word in words:
            test_line = current_line + word + " "
            test_surface = self.font.render(test_line, True, (0,0,0))

            if test_surface.get_width() > max_width:
                lines.append(current_line)
                current_line = word + " "
            else:
                current_line = test_line

        lines.append(current_line)

        for i, line in enumerate(lines[:2]):
            text_surface = self.font.render(line.strip(), True, (0,0,0))

            screen.blit(
                text_surface,
                text_surface.get_rect(
                    midleft=(
                        w * pos_x,
                        h - box_h + pos_y + i * 30
                    )
                )
            )

    def draw_hp_bar(self, screen, x, y, hp):

        hp = max(hp, 0)
        ratio = hp / 100

        pygame.draw.rect(screen, (0,0,0), (x, y, 140, 12))

        if hp > 50:
            color = (0,255,0)
        elif hp > 25:
            color = (255,255,0)
        else:
            color = (255,0,0)

        pygame.draw.rect(screen, color, (x, y, int(140 * ratio), 12))

    def do_enemy_attack(self):
        if self.enemy_hp <= 0:
            return

        damage = random.randint(10, 20)
        self.player_hp -= damage
        self.add_message(f"{self.enemy_name} te atacó (-{damage} HP)")

    def load_assets(self):
        try:
            self.bg = pygame.image.load(asset("assets/battle/bg.png")).convert()
            self.box = pygame.image.load(asset("assets/battle/box.png")).convert_alpha()

            self.selector = pygame.transform.scale(
                pygame.image.load(asset("assets/battle/selector.png")).convert_alpha(),
                (40, 40)
            )

            self.player_img = pygame.transform.scale(
                pygame.image.load(asset("assets/battle/player.png")).convert_alpha(),
                (180, 180)
            )

            self.use_assets = True
        except:
            self.use_assets = False

    def create_enemies(self):
        try:
            eco1 = pygame.transform.scale(
                pygame.image.load(asset("assets/battle/eco1.png")).convert_alpha(), (180,180))
            eco2 = pygame.transform.scale(
                pygame.image.load(asset("assets/battle/eco2.png")).convert_alpha(), (180,180))
            eco3 = pygame.transform.scale(
                pygame.image.load(asset("assets/battle/eco3.png")).convert_alpha(), (180,180))

            self.enemies = [
                {"name": "Eco Fuego", "hp": 100, "img": eco1},
                {"name": "Eco Sombra", "hp": 120, "img": eco2},
                {"name": "Eco Trueno", "hp": 90,  "img": eco3},
            ]

            self.enemy = random.choice(self.enemies)
            self.enemy_img = self.enemy["img"]
            self.enemy_hp = self.enemy["hp"]
            self.enemy_name = self.enemy["name"]

        except:
            self.enemy_img = None
            self.enemy_hp = 100
            self.enemy_name = "Eco"

    def handle_input(self, event):

        if event.type == pygame.KEYDOWN:

            if self.showing_message:
                if event.key == pygame.K_RETURN:
                    self.next_message()
                return

            if event.key == pygame.K_RIGHT and self.selected % 2 == 0:
                self.selected += 1
            elif event.key == pygame.K_LEFT and self.selected % 2 == 1:
                self.selected -= 1
            elif event.key == pygame.K_DOWN and self.selected < 2:
                self.selected += 2
            elif event.key == pygame.K_UP and self.selected >= 2:
                self.selected -= 2

            elif event.key == pygame.K_RETURN:

                choice = self.options[self.selected]

                if choice == "Atacar":
                    damage = random.randint(15, 25)
                    self.enemy_hp -= damage

                    self.add_message(
                        f"Atacaste a {self.enemy_name} (-{damage} HP)",
                        0.12, 40
                    )

                    if self.enemy_hp > 0:
                        self.enemy_turn = True

                elif choice == "Absorber":
                    self.add_message("Absorbiste al eco", 0.15, 50)
                    self.pending_finish = True

                elif choice == "Huir":
                    self.add_message("Huiste del eco", 0.15, 60)
                    self.pending_finish = True

                elif choice == "Ecos":
                    self.add_message("Menú no disponible aún", 0.15, 45)

    def draw(self, screen):

        w, h = screen.get_size()

        if self.use_assets:
            screen.blit(pygame.transform.scale(self.bg,(w,h)),(0,0))
        else:
            screen.fill((120,180,255))

        ex, ey = int(w*0.65), int(h*0.12)
        if self.enemy_img:
            screen.blit(self.enemy_img,(ex,ey))

        px, py = int(w*0.15), int(h*0.60)
        if self.use_assets:
            screen.blit(self.player_img,(px,py))

        self.draw_hp_bar(screen, ex, ey - 20, self.enemy_hp)
        self.draw_hp_bar(screen, px, py - 20, self.player_hp)

        box_h = 170
        if self.use_assets:
            screen.blit(pygame.transform.scale(self.box,(w,box_h)),(0,h-box_h))
        else:
            pygame.draw.rect(screen,(240,240,240),(0,h-box_h,w,box_h))

        if self.showing_message and self.messages:
            self.draw_text_box(screen, self.messages[0], w, h, box_h)
            return

        text = self.font.render("¿Qué deseas hacer?", True, (0,0,0))
        screen.blit(text, text.get_rect(midleft=(w*0.15, h-box_h+40)))

        sx, sy = int(w*0.55), int(h-box_h+70)

        positions = [
            (sx,sy),(sx+160,sy),
            (sx,sy+45),(sx+160,sy+45)
        ]

        for i,opt in enumerate(self.options):
            t = self.font.render(opt,True,(0,0,0))
            screen.blit(t, t.get_rect(midleft=positions[i]))

        selx,sely = positions[self.selected]
        screen.blit(self.selector,(selx-50,sely-15))

    # ======================================
    def update(self, events):

        for e in events:
            self.handle_input(e)

        if self.enemy_hp <= 0 and not self.pending_finish:
            self.add_message(f"{self.enemy_name} derrotado", 0.12, 40)
            self.pending_finish = True

        if self.player_hp <= 0 and not self.pending_finish:
            self.add_message("Has sido derrotado", 0.12, 40)
            self.pending_finish = True

    def finish_battle(self):
        self.finished = True
        self.running = False