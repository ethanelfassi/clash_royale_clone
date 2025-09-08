from cr import Troupe

sprites_troupe = {"avant":"assets/1.png",
                  "droite":"assets/2.png",
                  "gauche":"assets/3.png",
                  "arriere":"assets/4.png",
                  "attaque":"assets/5.png"}
# pv, pf, radius_view, radius_attack, cost
# AJOUTER SPRITES
TROUPES = {
    "knight": (150, .8, 100, 30, 2, sprites_troupe),
    "archer": (80, 1.2, 200, 150, 2, sprites_troupe)
}



class Knight(Troupe):
    def __init__(self, coords, map, team):
        super().__init__(*TROUPES["knight"], coords, map, team)

class Archer(Troupe):
    def __init__(self, coords, map, team):
        super().__init__(*TROUPES["archer"], coords, map, team)