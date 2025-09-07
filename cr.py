from settings import WIN_RES
import math
from abc import ABC, abstractmethod
import pygame
from consts import SCALE_TROUPE, SCALE_TOUR, SCALE_MAP

class Map:
    def __init__(self, sprite, screen):
        self.sprite = pygame.transform.scale(pygame.image.load(sprite),
                                                (SCALE_MAP[0]*WIN_RES, SCALE_MAP[1]*WIN_RES))
        self.screen = screen
        self.map = [
            [1] + [0]*13 + [1]*3 + [0]*13 + [1],
            [1] + [0]*14 + [1] + [0]*14 + [1],
            [1] + [0]*29 + [1],
            [1] + [0]*29 + [1],
            [0]*31,
            [0]*15 + [1] + [0]*15,
            [0]*15 + [1] + [0]*15,
            [0]*15 + [1] + [0]*15,
            [0]*15 + [1] + [0]*15,
            ]
        self.map += self.map[::-1]

        self.tailleh = 19.8
        self.taillev = 16.8
        self.offh = 50
        self.offv = 133
        
    def check_pos_in_map(self, click_pos):
        x, y = click_pos
        min_x, max_x = 0, len(self.map)
        min_y, max_y = 0, len(self.map[0])

        indice_x = round((x - self.offh) / self.tailleh)
        indice_y = round((y - self.offv) / self.taillev)
        if (min_x <= indice_x <= max_x) and (min_y <= indice_y <= max_y):
            try:
                return self.map[indice_x][indice_y] == 0
            except: 
                return False
        return False
            
    # taille 18x31
    def display(self):
        self.screen.blit(self.sprite, (0, 0))
        """
        for ligne in range(len(self.map)):
            for col in range(len(self.map[0])):
                x = self.offh + ligne * self.tailleh 
                y = self.offv + col * self.taillev
                c = self.map[ligne][col]
                pygame.draw.circle(self.screen, (255*c, 0, 0), (x, y), 5)
        """ # DEBUG
    """
    def display_path(self, path):
        self.screen.blit(self.sprite, (0, 0))
        for ligne in range(len(self.map)):
            for col in range(len(self.map[0])):
                x = self.offh + ligne * self.tailleh 
                y = self.offv + col * self.taillev
                c = self.map[ligne][col]
                pygame.draw.circle(self.screen, (255*c, 0, 0), (x, y), 5)
                if (ligne, col) in path:
                    pygame.draw.circle(self.screen, (0, 255, 0), (x, y), 5)
    """ # DEBUG

class Entite(ABC):
    def __init__(self, pv:float, pf:float, radius_view:float, radius_attack:float, cost:int, coords:tuple[str, int], map:Map, team:int, sprites:dict[str,str], scale):
        self.max_pv = pv
        self.pv = pv
        self.pf = pf
        self.radius_view = radius_view
        self.radius_attack = radius_attack
        self.cost = cost
        self.x, self.y = coords
        self.map = map
        self.team = team
        self.scale = scale
        self._init_sprites(sprites)
        self.state = "avant"
        self.step = 1
    
    def _init_sprites(self, sprites):
        self.sprites = {cle: pygame.transform.scale(pygame.image.load(valeur), (self.scale[0]*WIN_RES, self.scale[1]*WIN_RES)) for cle, valeur in sprites.items()}

    @abstractmethod
    def update(self, screen, game):
        pass

    def get_position(self):
        posx = (self.x - self.map.offh)//self.map.tailleh
        posy = (self.y - self.map.offv)//self.map.taillev
        return int(posx), int(posy)

    def find_closest_ennemy(self, game):
        closest_troup = None
        closest_tower = None
        closest_dist = self.radius_view 
        
        for entite in game.entites:
            if entite is not self and entite.team != self.team:
                x2, y2 = entite.x, entite.y
                dist = Troupe._get_distance(self.x, self.y, x2, y2)
                if dist <= closest_dist:
                    closest_troup = entite
        if closest_troup:
            return closest_troup
        
        closest_dist =  float('inf')
        for entite in game.entites:
            if isinstance(entite, Tour) and entite.team != self.team:
                x2, y2 = entite.x, entite.y
                dist = Troupe._get_distance(self.x, self.y, x2, y2)
                if dist < closest_dist:
                    closest_tower = entite        
        return closest_tower
    
    def attack(self, target):
        self.state = "attaque"
        target.pv -= self.pf
    
    def _display_health(self, screen):
        rel_health = self.pv / self.max_pv 
        pygame.draw.rect(screen, (0, 0, 0), (self.x-18*WIN_RES, self.y-30*WIN_RES, 36*WIN_RES, 8*WIN_RES))
        pygame.draw.rect(screen, (255, 0, 0), (self.x-17*WIN_RES, self.y-26*WIN_RES, 34*WIN_RES* rel_health, 6*WIN_RES))

    def display(self, screen):
        scale_x, scale_y = self.scale
        screen.blit(self.sprites[self.state], (self.x - (scale_x//2)*WIN_RES, self.y - (scale_y//2)*WIN_RES))
        pygame.draw.circle(screen, (0, 255, 0), (self.x, self.y), self.radius_view, 1)
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius_attack, 1)
        self._display_health(screen)

class Troupe(Entite):
    def __init__(self, pv:float, pf:float, radius_view:float, radius_attack:float, cost:int, coords:tuple[str, int],  map:Map, team:int, sprites:dict[str,str]):
        super().__init__(pv, pf, radius_view, radius_attack, cost, coords, map, team, sprites, SCALE_TROUPE)
    
    def get_path(self, target:Entite):
        grille = self.map.map
        start = self.get_position()
        end = target.get_position()
        directions = [(0,1),(1,0),(0,-1),(-1,0),(1,1),(-1,-1), (1, -1), (-1, 1)]
        file = [(start, [start])]
        visites = {start}
        rows, cols = len(grille), len(grille[0])

        while len(file):
            (x, y), path = file[0]
            file.pop(0)

            if (x,y) == end:
                return path
            
            for dx, dy in directions:
                nx = x + dx
                ny = y + dy

                if (0 <= nx < rows and 0 <= ny < cols) and grille[nx][ny] == 0 and ((nx, ny) not in visites):
                    file.append(((nx, ny), path + [(nx, ny)]))
                    visites.add((nx, ny))
        return None

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    @staticmethod
    def _get_distance(x1, y1, x2, y2):
        return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

    def change_state(self, angle: float) -> str:
        angle = (angle + math.pi) % (2*math.pi) - math.pi  
        
        if -math.pi/4 <= angle < math.pi/4:
            self.state = "droite"
        elif math.pi/4 <= angle < 3*math.pi/4:
            self.state = "avant"
        elif -3*math.pi/4 <= angle < -math.pi/4:
            self.state = "arriere"
        else:
            self.state = "gauche"

    @staticmethod
    def _get_movement(x1, y1, x2, y2, dist):
        angle = math.atan2(y2 - y1, x2 - x1)
        return math.cos(angle)*dist, math.sin(angle)*dist, angle
    
    def _go_to_target(self, target:Entite):
        x2, y2 = target.x, target.y
        path = self.get_path(target)
        if Troupe._get_distance(self.x, self.y, x2, y2) > self.radius_attack:
            self._go_to_point(path[1])
        else:
            self.attack(target)

    def _go_to_point(self, point):
        x1, y1 = self.get_position()
        x2, y2 = point[0], point[1]
        dx, dy, ang = Troupe._get_movement(x1, y1, x2, y2, self.step)
        self.change_state(ang)

        self.move(dx, dy)

    def update(self, screen, game):
        target = self.find_closest_ennemy(game)
        if target:
            self._go_to_target(target)
        self.display(screen)


class Tour(Entite):
    def __init__(self, pv:float, pf:float, radius_view:float, radius_attack:float, coords:tuple[str, int],  map:Map, team:int, sprites:list[str]):
        super().__init__(pv, pf, radius_view, radius_attack, 0, coords, map, team, sprites, SCALE_TOUR)

    def update(self, screen, game):
        self.display(screen)
        target = self.find_closest_ennemy(game)
        if target:
            self.attack(target)   

class Game:
    def __init__(self, entites:list[Entite], map:Map):
        self.entites = entites.copy()
        self.map = map
        self.screen = self.map.screen
    
    def add_entites(self, entite:Entite):
        self.entites.append(entite)

    def display(self):
        self.map.display()

    def update(self):
        self.display()
        dead_entites = []

        for entite in self.entites:
            entite.update(self.screen, self)
            if entite.pv <= 0:
                dead_entites.append(entite)

        for entite in dead_entites:
            self.entites.remove(entite)