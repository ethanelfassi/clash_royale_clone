class Clickable:
    def __init__(self, coords, dim):
        self.coords = coords
        self.hauteur, self.largeur = dim

    def been_clicked(self, click_pos):
        x, y = self.coords
        min_x, max_x = x, x + self.largeur
        min_y, max_y = y, y + self.hauteur
        click_x, click_y = click_pos
        return (min_x <= click_x <= max_x) and (min_y <= click_y <= max_y)
