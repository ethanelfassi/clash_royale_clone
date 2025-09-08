import pygame
from settings import WIN_RES
from clickable import Clickable

pygame.init()

screen = pygame.display.set_mode((WIN_RES*720, WIN_RES*1280))

class Menu:
    def __init__(self):
        self.button_play = Clickable((100,100), (200,200))
        self.button_quit = Clickable((100, 300), (200, 200))

    def display(self, screen):
        # dessiner les boutons et faire tout avec WIN_RES en coeff
        font = pygame.font.Font(None, 50*WIN_RES)  # None = police par défaut
        text = font.render("CR", True, (255, 255, 255))
        screen.blit(text, (50, 80))

    def update(self, screen):
        # verif les boutons et faire action associée
        self.display(screen)

menu = Menu()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    menu.update(screen)
    pygame.display.flip()