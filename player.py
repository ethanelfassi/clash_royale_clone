from cr import Troupe, Map, Game
from troupes import TROUPES
from settings import WIN_RES, FPS
from consts import SCALE_CARTE
from clickable import Clickable
import pygame

class Carte(Clickable):
    """
    Carte du deck
    """
    def __init__(self, coords: tuple[int], dim: tuple[int], sprite:str, troupe:str):
        super().__init__(coords, dim)
        self.sprite = sprite
        self.troupe = troupe
        self.selected = False
        self.sprite = pygame.transform.scale(pygame.image.load("assets/carte.png"), (SCALE_CARTE[0]*WIN_RES, SCALE_CARTE[1]*WIN_RES))
    
    def display(self, screen):
        x, y = self.coords
        if self.selected:
            y -= 15 * WIN_RES 
        screen.blit(self.sprite, (x, y))

    def update(self,screen):       
        self.display(screen)

class Player:
    def __init__(self, deck:list[Carte], team:int, game:Game):
        self.deck = deck
        self.team = team
        self.game = game
        self.selection = None #selection:Carte
        self.energie = 0
        self.max_energie = 10
        self.step_energie = 1 / FPS

    def place_troupe(self, coords:tuple[int, int], nom_troupe:str, sprites):
        m = self.game.map
        troupe = Troupe(*TROUPES[nom_troupe], coords, m, 1, sprites)
        if self.energie >= troupe.cost:
            self.game.add_entites(troupe)
            self.energie -= troupe.cost
    
    def display(self, screen):
        # afficher bar energie
        font = pygame.font.Font(None, 50*WIN_RES)  # None = police par défaut
        text = font.render(str(int(self.energie)), True, (255, 255, 255))
        screen.blit(text, (50, 80))

    def update(self, screen):
        self.energie = min(self.energie+self.step_energie, self.max_energie)
        for carte in self.deck:
            carte.update(screen)

        self.display(screen)
