import pygame
import os
import sys

from world import World
from player import Player
from battle import Battle
from ecos_menu import EcosMenu

def asset(path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, path)
    return os.path.join(os.path.abspath("."), path)

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Echo World: Shadows Rise")

try:
    icon = pygame.image.load(asset("assets/icon.png"))
    pygame.display.set_icon(icon)
except:
    print("No se pudo cargar icono")

clock = pygame.time.Clock()

world = World()
player = Player(*world.get_player_start())

battle = None
ecos_menu = None
running = True

while running:
    screen.fill((0,0,0))

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q and not battle and not ecos_menu:
                ecos_menu = EcosMenu(player)

    keys = pygame.key.get_pressed()

    if ecos_menu:
        ecos_menu.update(events)

        world.draw(screen, player)
        player.draw(screen, player)
        ecos_menu.draw(screen)

        if not ecos_menu.running:
            ecos_menu = None

    elif not battle:

        player.update(keys, world)

        npc_encounter = world.check_npc_encounter(player)

        if npc_encounter:
            if len(player.team) == 3:
                npc_encounter.defeated = True
                battle = Battle(player, "trainer", npc_encounter)
            else:
                print("Necesitas 3 ecos para pelear")

        else:
            encounter = world.check_encounter(player)

            if encounter == "wild":
                battle = Battle(player, "wild")

        world.draw(screen, player)
        player.draw(screen, player)

    else:
        battle.update(events)
        battle.draw(screen)

        if battle.open_ecos_menu:
            ecos_menu = EcosMenu(player)
            battle.open_ecos_menu = False
            continue  

        if battle.finished:
            battle = None

    pygame.display.flip()
    clock.tick(60)

pygame.quit()