import pygame
import os
import sys

from world import World
from player import Player
from battle import Battle
def asset(path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, path)
    return os.path.join(os.path.abspath("."), path)

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("EchoWorld: Shadows Rise")

try:
    icon = pygame.image.load(asset("assets/icon.png"))
    pygame.display.set_icon(icon)
except Exception as e:
    print("No se pudo cargar el icono:", e)

clock = pygame.time.Clock()

world = World()
player = Player(*world.get_player_start())

battle = None
running = True

while running:
    screen.fill((0,0,0))

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if not battle:
        player.update(keys, world)

        encounter = world.check_encounter(player)

        if encounter == "wild":
            battle = Battle(player, "wild")

        elif encounter == "trainer":
            battle = Battle(player, "trainer")

        world.draw(screen, player)
        player.draw(screen, player)

    else:
        battle.update(events)
        battle.draw(screen)

        if battle.finished:
            battle = None

    pygame.display.flip()
    clock.tick(60)

pygame.quit()