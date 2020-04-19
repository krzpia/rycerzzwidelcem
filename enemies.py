import sprites
#import copy


class EnemyGenerator:
    def __init__(self, game, tileset1, tileset2):
        self.game = game
        self.tileset = tileset1
        self.f_set = tileset2
        self.dif = self.game.difficulty
        print (f'EnemyGeneratorInfo: DIFFICULTY FACTOR = {self.dif}')
        self.sprite_images = {}

    def generate_image(self, name, image):
        print(f' Generuje obrazek dla obiektu {name}')
        self.sprite_images[name] = image

    def get_image_by_name(self, key):
        try:
            return self.sprite_images[key]
        except:
            print ("WRONG SPRITE IMAGE KEY!")

    def generate(self, name, x, y, image, item, hp = False):
        if name == "Rat":
            if not hp:
                hp = round(self.dif * 12)
            return sprites.Mob(self.game, name,x, y, image, False,False,
                               100, 40, 1.1, hp, round(self.dif * 2), 200, 2, item)
        if name == "Brown Rat":
            if not hp:
                hp = round(self.dif * 12)
            return sprites.Mob(self.game, name, x, y, image, False,False,
                               110, 45, 1.1, hp, round(self.dif*3), 200, 3, item)
        if name == "Giant Spider":
            if not hp:
                hp = round(self.dif * 10)
            return sprites.Mob(self.game, name, x, y,image, False,False,
                               120, 60, 1, hp, round(self.dif*6), 150, 5, item)
        if name == "Red Snake":
            if not hp:
                hp = round(self.dif * 20)
            return sprites.Mob(self.game, name, x, y,image,False,False,
                               90, 50, 1.2, hp, round(self.dif*10), 130, 8, item)
        if name == "Green Aligator":
            if not hp:
                hp = round(self.dif * 32)
            return sprites.Mob(self.game, name, x, y,image,False,False,
                               120, 20, 1.5, hp, round(self.dif*8), 150, 10, item)
        if name == "Mad Bull":
            if not hp:
                hp = round(self.dif * 42)
            return sprites.Mob(self.game, name, x, y, image, False, False,
                               110, 20, 1.0, hp, round(self.dif*7), 140, 12, item)

        if name == "Green Spider":
            if not hp:
                hp = round(self.dif * 12)
            return sprites.Mob(self.game, name, x, y,image, False,False,
                               130, 60, 1, hp, round(self.dif*8), 150, 7, item)

        if name == "Green Tarantula":
            if not hp:
                hp = round(self.dif * 22)
            return sprites.Mob(self.game, name, x, y, image, False, False,
                               150, 70, 1.0, hp, round(self.dif*10), 140, 12, item)

        if name == "Ent":
            if not hp:
                hp = round(self.dif * 50)
            return sprites.Mob(self.game, name, x, y, image, False, False,
                              50, 10, 1.8, hp, round(self.dif*6), 200, 25, item)

        if name == "Skeleton Warrior":
            if not hp:
                hp = round(self.dif * 26)
            return sprites.Mob(self.game, name, x, y, image, False, False,
                              75, 35, 1.8, hp, round(self.dif*8), 220, 9, item)

        if name == "Wolf Skeleton":
            if not hp:
                hp = round(self.dif * 16)
            return sprites.Mob(self.game, name, x, y, image, False, False,
                              135, 35, 1.2, hp, round(self.dif*7), 240, 8, item)

        if name == "Forest Worm":
            if not hp:
                hp = round(self.dif * 14)
            return sprites.Mob(self.game, name, x, y, image, False, False,
                              95, 35, 1.2, hp, round(self.dif*5),140, 5, item)

        if name == "Goblin":
            if not hp:
                hp = round(self.dif * 32)
            return sprites.Mob(self.game, name, x, y, image, False, False,
                               100, 30, 1.5, hp, round(self.dif * 6), 180, 12, item)

        if name == "Goblin Warrior":
            if not hp:
                hp = round(self.dif * 36)
            return sprites.Mob(self.game, name, x, y, image, False, False,
                               100, 30, 1.5, hp, round(self.dif * 8), 180, 15, item)

        if name == "Two Head Giant":
            if not hp:
                hp = round(self.dif * 65)
            return sprites.Mob(self.game, name, x, y, image, False, False,
                               100, 10, 1.5, hp, round(self.dif * 10), 180, 45, item)


    def generate_s(self, name, x, y, image, sx, sy, item, hp = False):
        if name == "Rat":
            if not hp:
                hp = round(self.dif * 12)
            return sprites.Mob(self.game, name,x, y, image,(sx, sy),False,
                               100, 40, 1.1, hp, round(self.dif*2), 200, 2, item)
        if name == "Brown Rat":
            if not hp:
                hp = round(self.dif * 12)
            return sprites.Mob(self.game, name, x, y,image,(sx, sy), False,
                               110, 45, 1.1, hp, round(self.dif*3), 200, 3, item)
        if name == "Giant Spider":
            if not hp:
                hp = round(self.dif * 10)
            return sprites.Mob(self.game, name, x, y,image,(sx, sy),False,
                               120, 60, 1, hp, round(self.dif*6), 150, 5, item)
        if name == "Red Snake":
            if not hp:
                hp = round(self.dif * 20)
            return sprites.Mob(self.game, name, x, y, image,(sx, sy),False,
                               90, 50, 1.2, hp, round(self.dif*10), 130, 8, item)
        if name == "Killer Bee":
            if not hp:
                hp = round(self.dif * 10)
            return sprites.Mob(self.game,name,x,y,image,(sx,sy),False,
                               160,60,1.8,hp,round(self.dif*2),120,2, item)
        if name == "Small Bat":
            if not hp:
                hp = round(self.dif * 16)
            return sprites.Mob(self.game,name,x,y,image,(sx,sy),False,
                               140,40,0.9,hp,round(self.dif*4),185,3,item)
        if name == "Mad Bat":
            if not hp:
                hp = round(self.dif * 24)
            return sprites.Mob(self.game, name, x, y, image, (sx, sy), False,
                               150, 40, 0.9, hp, round(self.dif*6), 180, 8, item)
        if name == "Big Bug":
            if not hp:
                hp = round(self.dif * 18)
            return sprites.Mob(self.game, name, x, y, image, (sx, sy), False,
                               120, 40, 1.4, hp, round(self.dif*4), 140, 6, item)

        if name == "Dryad":
            if not hp:
                hp = round(self.dif * 25)
            return sprites.Mob(self.game, name, x, y, image, (sx, sy), False,
                               150, 50, 1.0, hp, round(self.dif*12), 210, 15, item)

        if name == "Scorpion":
            if not hp:
                hp = round(self.dif * 26)
            return sprites.Mob(self.game, name, x, y, image, (sx, sy), False,
                               120, 20, 1.0, hp, round(self.dif*10), 200, 18, item)

        if name == "Goblin":
            if not hp:
                hp = round(self.dif * 35)
            return sprites.Mob(self.game, name, x, y, image, (sx, sy), False,
                               100, 30, 1.5, hp, round(self.dif*6), 180, 12, item)

        if name == "Goblin Warrior":
            if not hp:
                hp = round(self.dif * 40)
            return sprites.Mob(self.game, name, x, y, image, (sx, sy), False,
                               100, 30, 1.5, hp, round(self.dif*8), 180, 15, item)



        if name == "Skeleton":
            if not hp:
                hp = round(self.dif * 20)
            return sprites.Mob(self.game,name,x,y,image,(sx,sy),False,
                               max_speed=55,
                               min_speed=35,
                               stun_time=1.8,
                               hp=hp,
                               damage=round(self.dif*5),
                               sleep_radius=320,
                               xp=6,
                               item=item)

    def generate_r(self, name, x, y, image, item, hp=False):
        if name == "Blue Slime":
            if not hp:
                hp = round(self.dif * 18)
            return sprites.Mob(self.game, name, x, y, image, False, ("magic",round(self.dif*5),180,2000),
                               20,10,1.5,hp,round(self.dif*2),120,7, item)
        if name == "Gremlin":
            if not hp:
                hp = round(self.dif * 20)
            return sprites.Mob(self.game, name, x, y, image, False, ("rock",round(self.dif*4),220,2000),
                               25,10,1.0,hp,round(self.dif*4),160,10, item)

        if name == "Forest Goblin":
            if not hp:
                hp = round(self.dif * 26)
            return sprites.Mob(self.game, name, x, y, image, False, ("rock",round(self.dif*5),250,1800),
                               25,15,1.0,hp,round(self.dif*3),160,10, item)

        if name == "Carn Rose":
            if not hp:
                hp = round(self.dif * 36)
            return sprites.Mob(self.game, name, x, y, image, False, ("dart",round(self.dif*4),280,1300),
                               1,1,1.0,hp,round(self.dif*2),160,12, item)

        if name == "Centaur":
            if not hp:
                hp = round(self.dif * 30)
            return sprites.Mob(self.game, name, x, y, image, False, ("dart",round(self.dif*4),280,2200),
                               60,20,1.0,hp,round(self.dif*5),240,10, item)

        if name == "Fire Butterfly":
            if not hp:
                hp = round(self.dif * 8)
            return sprites.Mob(self.game, name, x, y, image, False, ("fire",round(self.dif*12),280,2000),
                               40,20,1.0,hp,round(self.dif*1),200,7, item)

        if name == "Red Mutant":
            if not hp:
                hp = round(self.dif * 100)
            return sprites.Mob(self.game, name, x, y, image, False, ("fire",round(self.dif*20),280,1800),
                               50,25,1.0,hp,round(self.dif*10),280,50, item)

        if name == "Coronavirus":
            if not hp:
                hp = round(self.dif * 250)
            return sprites.Mob(self.game, name, x, y, image, False, ("virus",round(self.dif*50),250,1500),
                               100,25,1.0,hp,round(self.dif*25),285,100, item)




