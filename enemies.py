import sprites
#import copy


class EnemyGenerator:
    def __init__(self, game, tileset1, tileset2):
        self.game = game
        self.tileset = tileset1
        self.f_set = tileset2
        self.dif = self.game.difficulty
        print (f'DIFFICULTY FACTOR = {self.dif}')

    def generate(self, name, x, y, image, item):
        if name == "Rat":
            return sprites.Mob(self.game, name,x, y, image, False,False,
                               100, 40, 1.1, round(self.dif * 12), round(self.dif * 2), 200, 2, item)
        if name == "Brown Rat":
            return sprites.Mob(self.game, name, x, y, image,False,False,
                               110, 45, 1.1, round(self.dif * 12), round(self.dif*3), 200, 3, item)
        if name == "Giant Spider":
            return sprites.Mob(self.game, name, x, y,image,False,False,
                               120, 60, 1, round(self.dif * 10), round(self.dif*6), 150, 5, item)
        if name == "Red Snake":
            return sprites.Mob(self.game, name, x, y,image,False,False,
                               90, 50, 1.2, round(self.dif * 20), round(self.dif*10), 130, 8, item)
        if name == "Green Aligator":
            return sprites.Mob(self.game, name, x, y,image,False,False,
                               120, 20, 1.5, round(self.dif * 30), round(self.dif*8), 150, 10, item)
        if name == "Mad Bull":
            return sprites.Mob(self.game, name, x, y, image, False, False,
                               110, 20, 1.0, round(self.dif * 40), round(self.dif*7), 140, 12, item)

    def generate_s(self, name, x, y, image, sx, sy, item):
        if name == "Rat":
            return sprites.Mob(self.game, name,x, y,image,(sx, sy),False,
                               100, 40, 1.1, round(self.dif * 12), round(self.dif*2), 200, 2, item)
        if name == "Brown Rat":
            return sprites.Mob(self.game, name, x, y,image,(sx, sy), False,
                               110, 45, 1.1, round(self.dif * 12), round(self.dif*3), 200, 3, item)
        if name == "Giant Spider":
            return sprites.Mob(self.game, name, x, y,image,(sx, sy),False,
                               120, 60, 1, round(self.dif * 10), round(self.dif*6), 150, 5, item)
        if name == "Red Snake":
            return sprites.Mob(self.game, name, x, y, image,(sx, sy),False,
                               90, 50, 1.2, round(self.dif * 20), round(self.dif*10), 130, 8, item)
        if name == "Killer Bee":
            return sprites.Mob(self.game,name,x,y,image,(sx,sy),False,
                               160,60,1.8,round(self.dif * 10),round(self.dif*2),120,2, item)
        if name == "Small Bat":
            return sprites.Mob(self.game,name,x,y,image,(sx,sy),False,
                               140,40,0.9,round(self.dif * 16),round(self.dif*4),185,3,item)
        if name == "Mad Bat":
            return sprites.Mob(self.game, name, x, y, image, (sx, sy), False,
                               150, 40, 0.9, round(self.dif * 22), round(self.dif*6), 180, 8, item)
        if name == "Big Bug":
            return sprites.Mob(self.game, name, x, y, image, (sx, sy), False,
                               120, 40, 1.4, round(self.dif * 18), round(self.dif*4), 140, 6, item)

        if name == "Skeleton":
            return sprites.Mob(self.game,name,x,y,image,(sx,sy),False,
                               max_speed=55,
                               min_speed=35,
                               stun_time=1.8,
                               hp=round(self.dif * 20),
                               damage=round(self.dif*5),
                               sleep_radius=320,
                               xp=6,
                               item=item)

    def generate_r(self, name, x, y, image, item):
        if name == "Blue Slime":
            return sprites.Mob(self.game, name, x, y, image, False, ("magic",round(self.dif*5),180,2000),
                               -20,-10,1.5,round(self.dif * 18),round(self.dif*2),120,7, item)
        if name == "Gremlin":
            return sprites.Mob(self.game, name, x, y, image, False, ("rock",round(self.dif*4),220,2000),
                               -20,-10,1.0,round(self.dif * 20),round(self.dif*4),160,10, item)

