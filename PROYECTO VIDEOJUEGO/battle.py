import pygame
import os
import sys
import random


def asset(path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, path)
    return os.path.join(os.path.abspath("."), path)


class Battle:
    def __init__(self, player, mode="wild", npc=None):

        self.player = player
        self.mode = mode
        self.npc = npc

        self.player_hp = 100
        self.current_player_eco_index = 0

        self.running = True
        self.finished = False

        self.options = ["Atacar", "Ecos", "Absorber", "Huir"]
        self.selected = 0

        self.messages = []
        self.showing_message = False
        self.pending_finish = False
        self.enemy_turn = False

        self.open_ecos_menu = False

        self.showing_player = True if mode == "trainer" else False
        self.showing_trainer = False

        try:
            self.font = pygame.font.Font(asset("assets/fonts/pokemon.ttf"), 17)
        except:
            self.font = pygame.font.SysFont("arial", 22)

        self.load_assets()

        if self.mode == "trainer" and self.npc:
            self.enemy_team = self.npc.team
            self.current_enemy_index = 0
            self.trainer_img = self.load_trainer_img()
            self.load_enemy_from_team()
        else:
            self.enemy_team = None
            self.trainer_img = None
            self.create_enemy()

        if self.mode == "trainer":
            self.add_message("¡Entraste a una batalla con un entrenador!")
        else:
            self.add_message(f"{self.enemy_name} apareció!")

    def load_trainer_img(self):
        try:
            img_path = self.npc.img_path
            img = pygame.image.load(asset(img_path)).convert_alpha()
            return pygame.transform.scale(img, (180, 180))
        except:
            return None

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

            self.enemy_imgs = [
                pygame.transform.scale(pygame.image.load(asset("assets/battle/eco1.png")).convert_alpha(), (180, 180)),
                pygame.transform.scale(pygame.image.load(asset("assets/battle/eco2.png")).convert_alpha(), (180, 180)),
                pygame.transform.scale(pygame.image.load(asset("assets/battle/eco3.png")).convert_alpha(), (180, 180))
            ]

            self.player_eco_imgs = [
                pygame.transform.scale(pygame.image.load(asset("assets/battle/eco1espalda.png")).convert_alpha(), (180, 180)),
                pygame.transform.scale(pygame.image.load(asset("assets/battle/eco2espalda.png")).convert_alpha(), (180, 180)),
                pygame.transform.scale(pygame.image.load(asset("assets/battle/eco3espalda.png")).convert_alpha(), (180, 180))
            ]

        except Exception as e:
            print("Error cargando assets:", e)
            self.bg = None
            self.box = None
            self.selector = None
            self.player_img = None
            self.enemy_imgs = []
            self.player_eco_imgs = []

    def get_player_eco_img(self):
        if self.mode == "wild":
            return None

        if self.showing_player or self.showing_trainer:
            return None

        if not self.player_eco_imgs or not self.player.team:
            return None

        if self.current_player_eco_index >= len(self.player.team):
            return None

        eco_name = self.player.team[self.current_player_eco_index]["name"]

        if "Phantom" in eco_name:
            return self.player_eco_imgs[0]
        elif "Zabbit" in eco_name:
            return self.player_eco_imgs[1]
        else:
            return self.player_eco_imgs[2]
        
    def create_enemy(self):
        names = ["Phantom", "Zabbit", "Licht"]
        i = random.randint(0, len(names) - 1)
        self.enemy_name = names[i]
        self.enemy_img = self.enemy_imgs[i] if self.enemy_imgs else None
        self.enemy_hp = 100

    def load_enemy_from_team(self):
        eco = self.enemy_team[self.current_enemy_index]
        self.enemy_name = eco["name"]
        self.enemy_hp = eco["hp"]

        if self.enemy_imgs:
            if "Phantom" in self.enemy_name:
                self.enemy_img = self.enemy_imgs[0]
            elif "Zabbit" in self.enemy_name:
                self.enemy_img = self.enemy_imgs[1]
            else:
                self.enemy_img = self.enemy_imgs[2]

    def team_defeated(self):
        if self.mode != "trainer" or not self.enemy_team:
            return self.enemy_hp <= 0
        return all(eco["hp"] <= 0 for eco in self.enemy_team)

    def draw_hp_bar(self, screen, x, y, hp):
        hp = max(hp, 0)
        ratio = hp / 100

        pygame.draw.rect(screen, (0, 0, 0), (x, y, 140, 12))

        color = (0, 255, 0)
        if hp < 50: color = (255, 255, 0)
        if hp < 25: color = (255, 0, 0)

        pygame.draw.rect(screen, color, (x, y, int(140 * ratio), 12))

    def add_message(self, text):
        self.messages.append(text)
        self.showing_message = True

    def next_message(self):
        if self.messages:
            self.messages.pop(0)

        if not self.messages:
            self.showing_message = False

            if self.showing_player:
                self.showing_player = False
                if self.mode == "trainer":
                    self.showing_trainer = True
                    self.add_message(f"¡{self.npc.name} quiere pelear!")
                return

            if self.showing_trainer:
                self.showing_trainer = False
                self.add_message(f"{self.enemy_name} aparece!")
                return

            if self.enemy_hp <= 0:

                if self.mode == "trainer" and self.enemy_team:
                    self.enemy_team[self.current_enemy_index]["hp"] = 0

                    next_index = self.current_enemy_index + 1
                    while next_index < len(self.enemy_team) and self.enemy_team[next_index]["hp"] <= 0:
                        next_index += 1

                    if next_index < len(self.enemy_team):
                        self.current_enemy_index = next_index
                        self.add_message("El entrenador envía otro eco")
                        self.load_enemy_from_team()
                        return

                if self.team_defeated():
                    self.add_message("¡Has derrotado a todo el equipo enemigo!")
                    self.finish_battle()
                    return

            if self.enemy_turn:
                self.do_enemy_attack()
                self.enemy_turn = False

            elif self.pending_finish:
                self.finish_battle()

    def do_enemy_attack(self):
        if self.enemy_hp <= 0:
            return

        damage = random.randint(10, 20)
        self.player_hp -= damage
        self.add_message(f"{self.enemy_name} te atacó (-{damage})")

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
                    dmg = random.randint(15, 25)
                    self.enemy_hp -= dmg
                    self.add_message(f"Atacaste (-{dmg})")

                    if self.enemy_hp > 0:
                        self.enemy_turn = True

                elif choice == "Absorber":
                    if self.mode == "trainer":
                        self.add_message("No puedes absorber ecos de un entrenador")
                    else:
                        new_eco = {
                            "name": self.enemy_name,
                            "hp": 100,
                            "type": "Desconocido"
                        }
                        self.player.team.append(new_eco)
                        self.add_message(f"{self.enemy_name} fue absorbido")
                        self.pending_finish = True

                elif choice == "Huir":
                    if self.mode == "trainer":
                        self.add_message("No puedes huir de un entrenador")
                    else:
                        self.add_message("Huiste del eco")
                        self.pending_finish = True

                elif choice == "Ecos":
                    self.open_ecos_menu = True
    def update(self, events):

        for e in events:
            self.handle_input(e)

        if self.team_defeated() and not self.pending_finish:
            self.add_message("¡Todos los ecos fueron derrotados!")
            self.pending_finish = True

        if self.player_hp <= 0 and not self.pending_finish:
            next_index = self.current_player_eco_index + 1

            if next_index < len(self.player.team):
                self.current_player_eco_index = next_index
                self.player_hp = 100
                eco_name = self.player.team[next_index]["name"]
                self.add_message(f"¡{eco_name} entra al combate!")
            else:
                self.add_message("¡Todos tus ecos fueron derrotados!")
                self.pending_finish = True

    def draw(self, screen):

        w, h = screen.get_size()

        if self.bg:
            screen.blit(pygame.transform.scale(self.bg, (w, h)), (0, 0))
        else:
            screen.fill((120, 180, 255))

        ex, ey = int(w * 0.65), int(h * 0.10)
        px, py = int(w * 0.15), int(h * 0.55)

        if self.showing_trainer and self.trainer_img:
            screen.blit(self.trainer_img, (ex, ey))
        elif not self.showing_player and not self.showing_trainer:
            if self.enemy_img:
                screen.blit(self.enemy_img, (ex, ey))
            self.draw_hp_bar(screen, ex, ey - 20, self.enemy_hp)

        if self.showing_player:
            if self.player_img:
                screen.blit(self.player_img, (px, py))
        else:
            eco_img = self.get_player_eco_img()
            if eco_img:
                screen.blit(eco_img, (px, py))
            elif self.player_img:
                screen.blit(self.player_img, (px, py))

        self.draw_hp_bar(screen, px, py - 20, self.player_hp)

        box_h = 170
        if self.box:
            screen.blit(pygame.transform.scale(self.box, (w, box_h)), (0, h - box_h))
        else:
            pygame.draw.rect(screen, (240, 240, 240), (0, h - box_h, w, box_h))

        if self.showing_message:
            t = self.font.render(self.messages[0], True, (0, 0, 0))
            screen.blit(t, t.get_rect(midleft=(w * 0.12, h - box_h + 40)))
            return

        t = self.font.render("¿Qué deseas hacer?", True, (0, 0, 0))
        screen.blit(t, t.get_rect(midleft=(w * 0.12, h - box_h + 30)))

        sx, sy = int(w * 0.55), int(h - box_h + 70)

        positions = [
            (sx, sy),
            (sx + 160, sy),
            (sx, sy + 45),
            (sx + 160, sy + 45)
        ]

        for i, opt in enumerate(self.options):
            txt = self.font.render(opt, True, (0, 0, 0))
            screen.blit(txt, txt.get_rect(midleft=positions[i]))

        selx, sely = positions[self.selected]

        if self.selector:
            screen.blit(self.selector, (selx - 50, sely - 15))
        else:
            pygame.draw.circle(screen, (0, 0, 255), (selx - 20, sely + 10), 6)

    def finish_battle(self):
        self.finished = True
        self.running = False