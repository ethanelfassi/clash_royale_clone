from cr import Troupe, Map, Game
from troupes import TROUPES
import pygame

class Player:
    def __init__(self, deck:list[str], team:int, game:Game):
        self.deck = deck
        self.team = team
        self.game = game
        self.energie = 0
        self.max_energie = 10
        self.step_energie = 0.05

    def place_troupe(self, coords:tuple[int, int], nom_troupe:str, sprites):
        m = self.game.map
        troupe = Troupe(*TROUPES[nom_troupe], coords, m, 1, sprites)
        if self.energie >= troupe.cost:
            self.game.add_entites(troupe)
            self.energie -= troupe.cost
    
    def display(self, screen):
        # afficher bar energie + deck (cartes)
        font = pygame.font.Font(None, 50)  # None = police par défaut
        text = font.render(str(int(self.energie)), True, (255, 255, 255))
        screen.blit(text, (50, 80))

    def update(self, screen):
        self.energie = min(self.energie+self.step_energie, self.max_energie)
        self.display(screen)
