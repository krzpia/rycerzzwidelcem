import sprites
#import copy


class EnemyGenerator:
    def __init__(self, game, tileset1, tileset2):
        self.game = game
        self.tileset = tileset1
        self.f_set = tileset2

    def generate(self, name, x, y):
        if name == "Rat":
            return sprites.Mob(self.game, name,x, y,False,False, self.tileset,
                                        23, 4, 100, 40, 1.1, 12, 2, 200, 2)
        if name == "Brown Rat":
            return sprites.Mob(self.game, name, x, y, False,False,self.tileset,
                                        28, 4, 110, 45, 1.1, 12, 3, 200, 3)
        if name == "Giant Spider":
            return sprites.Mob(self.game, name, x, y,False,False,self.tileset,
                                        29, 4, 120, 60, 1, 10, 6, 150, 5)
        if name == "Red Snake":
            return sprites.Mob(self.game, name, x, y,False,False, self.tileset,
                                        20, 4, 90, 50, 1.2, 20, 10, 130, 8)

    def generate_s(self, name, x, y, sx, sy):
        if name == "Rat":
            return sprites.Mob(self.game, name,x, y,(sx, sy),False, self.tileset,
                                        23, 4, 100, 40, 1.1, 12, 2, 200, 2)
        if name == "Brown Rat":
            return sprites.Mob(self.game, name, x, y,(sx, sy), False,self.tileset,
                                        28, 4, 110, 45, 1.1, 12, 3, 200, 3)
        if name == "Giant Spider":
            return sprites.Mob(self.game, name, x, y,(sx, sy),False, self.tileset,
                                        29, 4, 120, 60, 1, 10, 6, 150, 5)
        if name == "Red Snake":
            return sprites.Mob(self.game, name, x, y, (sx, sy),False,self.tileset,
                                        20, 4, 90, 50, 1.2, 20, 10, 130, 8)
        if name == "Killer Bee":
            return sprites.Mob(self.game,name,x,y,(sx,sy),False,self.f_set,
                                        11,64,160,60,1.8,10,2,120,2)


    def generate_r(self,name,x,y,bullet_type,bullet_dmg,bullet_speed,bullet_hr):
        if name == "Blue Slime":
            return sprites.Mob(self.game,name,x,y,False,(bullet_type,bullet_dmg,bullet_speed,bullet_hr),
                               self.f_set, 31,62,-20,-10,1.5,18,2,120,7)
