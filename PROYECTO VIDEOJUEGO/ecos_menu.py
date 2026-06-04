import pygame
import os
import sys

def asset(path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, path)
    return os.path.join(os.path.abspath("."), path)

class EcosMenu:
    def __init__(self, player):

        self.player = player
        self.selected = 0
        self.running = True

        try:
            self.font = pygame.font.Font(asset("assets/fonts/pokemon.ttf"), 16)
        except:
            self.font = pygame.font.SysFont("arial", 22)

        self.ecos = self.player.team

    def handle_input(self, event):

        if event.type == pygame.KEYDOWN:

            if len(self.ecos) == 0:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                return

            if event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.ecos)

            elif event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.ecos)

            elif event.key == pygame.K_ESCAPE:
                self.running = False

    def draw(self, screen):

        w, h = screen.get_size()

        overlay = pygame.Surface((w,h))
        overlay.set_alpha(180)
        overlay.fill((0,0,0))
        screen.blit(overlay,(0,0))

        pygame.draw.rect(screen,(240,240,240),(50,50,300,400))
        pygame.draw.rect(screen,(255,255,255),(380,50,350,400))

        if len(self.ecos) == 0:
            text = self.font.render("No tienes ecos aún", True, (0,0,0))
            screen.blit(text,(80,80))
            return

        for i, eco in enumerate(self.ecos):

            color = (0,0,0)

            if i == self.selected:
                pygame.draw.rect(screen,(200,200,255),(60,60 + i*40,280,35))
                color = (0,0,150)

            text = self.font.render(eco["name"], True, color)
            screen.blit(text,(70,65 + i*40))

        eco = self.ecos[self.selected]

        screen.blit(self.font.render(f"Nombre: {eco['name']}", True, (0,0,0)), (400,100))
        screen.blit(self.font.render(f"HP: {eco['hp']}", True, (0,0,0)), (400,140))
        screen.blit(self.font.render(f"Tipo: {eco['type']}", True, (0,0,0)), (400,180))

    def update(self, events):
        for e in events:
            self.handle_input(e)