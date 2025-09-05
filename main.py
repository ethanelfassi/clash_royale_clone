import pygame
from settings import WIN_RES
from cr import Map, Troupe, Tour, Game
from troupes import TROUPES
from player import Player, Carte

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
tour1 = Tour(1000, 10, 200, 200, (100, 220), m, 3, sprites_tour)

game = Game([knight, archer, tour1], m)

carte = Carte((100, 620), (70, 80), None)
player = Player([carte], 1, game)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_coords = pygame.mouse.get_pos()
            player.place_troupe(click_coords, "knight", sprites_troupe)
           
    game.update()
    player.update(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()


"""
todo:
- selection des cartes 
- gerer collisions, (chaque perso est un cercle tu repousses selon la normale)
- try except partt ou ca peut chier

amelioration:
- faire de l'heritage bien -> classe generique qui a (pv, pf, team, spirtes etc....)
- sprite diagonales, animations
- cooldown d'attaque
"""