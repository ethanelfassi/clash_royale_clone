import pygame
from settings import WIN_RES
from cr import Map, Troupe, Tour, Game
from troupes import TROUPES
from player import Player, Carte
from consts import COORDS_CARTE, DIM_CARTE

pygame.init()

screen = pygame.display.set_mode((WIN_RES*720, WIN_RES*1280))
clock = pygame.time.Clock()


sprites_troupe = {"avant":"assets/1.png",
                  "droite":"assets/2.png",
                  "gauche":"assets/3.png",
                  "arriere":"assets/4.png",
                  "attaque":"assets/5.png"}

sprites_tour = {"avant":"assets/tower.png",
                  "droite":"assets/tower.png",
                  "gauche":"assets/tower.png",
                  "arriere":"assets/tower.png",
                  "attaque":"assets/tower.png"}



m = Map("assets/arene.png", screen)

knight = Troupe(*TROUPES["knight"], (400, 300), m, 1,sprites_troupe)
archer = Troupe(*TROUPES["archer"], (200, 580), m, 2,sprites_troupe)
tour1 = Tour(1000, 1, 200, 200, (100, 220), m, 3, sprites_tour)

game = Game([knight, archer, tour1], m)

deck = [Carte((x, y), DIM_CARTE, None, "archer") for x, y in COORDS_CARTE] 
player = Player(deck, 1, game)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_coords = pygame.mouse.get_pos()
            for carte in player.deck:
                carte.selected = False
                if carte.been_clicked(click_coords):
                    carte.selected = True
                    player.selection = carte.troupe
                    break
            
            if player.selection and m.check_pos_in_map(click_coords):
                player.place_troupe(click_coords, player.selection, sprites_troupe)
           
    game.update()
    player.update(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()


"""
todo: 
- gerer collisions, (chaque perso est un cercle tu repousses selon la normale)
- try except partt ou ca peut chier

amelioration:
- faire de l'heritage bien -> classe generique qui a (pv, pf, team, spirtes etc....)
- sprite diagonales, animations
- cooldown d'attaque
- selection des cartes
"""