import sprites
#import copy


class EnemyGenerator:
    def __init__(self, game, tileset1, tileset2):
        self.game = game
        self.tileset = tileset1
        self.f_set = tileset2

    def generate(self, name, x, y, image):
        if name == "Rat":
            return sprites.Mob(self.game, name,x, y, image, False,False,
                               100, 40, 1.1, 12, 2, 200, 2)
        if name == "Brown Rat":
            return sprites.Mob(self.game, name, x, y, image,False,False,
                               110, 45, 1.1, 12, 3, 200, 3)
        if name == "Giant Spider":
            return sprites.Mob(self.game, name, x, y,image,False,False,
                               120, 60, 1, 10, 6, 150, 5)
        if name == "Red Snake":
            return sprites.Mob(self.game, name, x, y,image,False,False,
                               90, 50, 1.2, 20, 10, 130, 8)

    def generate_s(self, name, x, y, image, sx, sy):
        if name == "Rat":
            return sprites.Mob(self.game, name,x, y,image,(sx, sy),False,
                               100, 40, 1.1, 12, 2, 200, 2)
        if name == "Brown Rat":
            return sprites.Mob(self.game, name, x, y,image,(sx, sy), False,
                               110, 45, 1.1, 12, 3, 200, 3)
        if name == "Giant Spider":
            return sprites.Mob(self.game, name, x, y,image,(sx, sy),False,
                               120, 60, 1, 10, 6, 150, 5)
        if name == "Red Snake":
            return sprites.Mob(self.game, name, x, y, image,(sx, sy),False,
                               90, 50, 1.2, 20, 10, 130, 8)
        if name == "Killer Bee":
            return sprites.Mob(self.game,name,x,y,image,(sx,sy),False,
                               160,60,1.8,10,2,120,2)
        if name == "Skeleton":
            return sprites.Mob(self.game,name,x,y,image,(sx,sy),False,
                               max_speed=55,
                               min_speed=35,
                               stun_time=1.8,
                               hp=20,
                               damage=5,
                               sleep_radius=320,
                               xp=6)

    def generate_r(self, name, x, y, image):
        if name == "Blue Slime":
            return sprites.Mob(self.game, name, x, y, image, False, ("magic",5,180,2000),
                               -20,-10,1.5,18,2,120,7)
