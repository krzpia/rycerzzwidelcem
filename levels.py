import pygame
vec = pygame.math.Vector2
from sprites import *
from data import *
from items import ItemGenerator
from enemies import EnemyGenerator
from npcs import NpcGenerator
from ui import ActiveEffect


class LevelGen:
    def __init__(self, game):
        self.game = game
        self.gen = ItemGenerator(self.game,tileset_image,full_tileset_image)
        self.enemy_gen = EnemyGenerator(self.game,tileset_image,full_tileset_image)
        self.npcs_gen = NpcGenerator(self.game,tileset_image,full_tileset_image)
        self.shop_gen = ShopGenerator(self.game)
        self.lava_effect = ActiveEffect("fire",e_fire_ico,5,1)
        self.slow_effect = ActiveEffect("slow",e_slow_ico,50,1.2)

    def load(self,name):
        if name == "level01":
            self.load_level_01()
        elif name == "level02":
            self.load_level_02()
        elif name == "level03":
            self.load_level_03()
        elif name == "level04":
            self.load_level_04()
        elif name == "level05":
            self.load_level_05()
        else:
            print ("ERROR DECODIN LEVELGEN LOAD LEVEL by NAME")

    def go_to_level(self,level,pos_x, pos_y):
        self.game.act_lvl = self.game.levels[level]
        #### PRZEKAZUJE MAPE DO GRY
        self.game.map = self.game.map_levels[level]
        self.game.map_image = self.game.map.make_map()
        self.game.map_rect = self.game.map_image.get_rect()
        self.game.player.put_in_pos(pos_x, pos_y)

    def load_level_05(self):
        self.game.act_lvl = self.game.level_05
        ### ALL SPRITES (BEZ GRACZA!)
        self.game.level_05.all_sprites = pygame.sprite.LayeredUpdates()
        ## MURY / tylko odbijanie od obiektu Rect z TMX MAPS
        self.game.level_05.walls = pygame.sprite.LayeredUpdates()
        ## PRZESZKODY / odbijaja sie za pomoca hit_rect.
        self.game.level_05.hr_obstacles = pygame.sprite.LayeredUpdates()
        ## NIEWIDZIALNE POLE ZABIERAJACE HP
        self.game.level_05.lavas = pygame.sprite.LayeredUpdates()
        ## NPCS
        self.game.level_05.npcs = pygame.sprite.LayeredUpdates()
        ## PRZECIWNICY
        self.game.level_05.mobs = pygame.sprite.LayeredUpdates()
        ## STRZALY PRZECIWNIKOW
        self.game.level_05.mob_arrows = pygame.sprite.LayeredUpdates()
        ## STRZALY ranged
        self.game.level_05.arrows = pygame.sprite.LayeredUpdates()
        ## Sprite ataku wręcz
        self.game.level_05.melle_swing = pygame.sprite.LayeredUpdates()
        ## PRZEDMIOTY NA MAPIE DO PODNIESIENIA
        self.game.level_05.items_to_pick = pygame.sprite.LayeredUpdates()
        ## OBIEKTY DO INTERAKCJI (PODNIESIENIA, WYLECZENIA ITP)
        self.game.level_05.collecting_sprites = pygame.sprite.LayeredUpdates()
        ## ZLOTE MONETY DO PODNIESIENIA
        self.game.level_05.gold_to_pick = pygame.sprite.LayeredUpdates()
        ## STRZALY DO PODNIESIENIA
        self.game.level_05.arrows_to_pick = pygame.sprite.LayeredUpdates()
        ## DRZWI
        self.game.level_05.doors = pygame.sprite.LayeredUpdates()
        ## SKRZYNIE
        self.game.level_05.chest_to_open = pygame.sprite.LayeredUpdates()
        ## TELEPORTS
        self.game.level_05.teleports = pygame.sprite.LayeredUpdates()
        ## SHOPS
        self.game.level_05.shops = pygame.sprite.LayeredUpdates()
        #### LOAD TILE OBJECTS
        self.load_objects(self.game.map_level_05.tmxdata.objects)

    def load_level_04(self):
        self.game.act_lvl = self.game.level_04
        ### ALL SPRITES (BEZ GRACZA!)
        self.game.level_04.all_sprites = pygame.sprite.LayeredUpdates()
        ## MURY / tylko odbijanie od obiektu Rect z TMX MAPS
        self.game.level_04.walls = pygame.sprite.LayeredUpdates()
        ## PRZESZKODY / odbijaja sie za pomoca hit_rect.
        self.game.level_04.hr_obstacles = pygame.sprite.LayeredUpdates()
        ## NIEWIDZIALNE POLE ZABIERAJACE HP
        self.game.level_04.lavas = pygame.sprite.LayeredUpdates()
        ## NPCS
        self.game.level_04.npcs = pygame.sprite.LayeredUpdates()
        ## PRZECIWNICY
        self.game.level_04.mobs = pygame.sprite.LayeredUpdates()
        ## STRZALY PRZECIWNIKOW
        self.game.level_04.mob_arrows = pygame.sprite.LayeredUpdates()
        ## STRZALY ranged
        self.game.level_04.arrows = pygame.sprite.LayeredUpdates()
        ## Sprite ataku wręcz
        self.game.level_04.melle_swing = pygame.sprite.LayeredUpdates()
        ## PRZEDMIOTY NA MAPIE DO PODNIESIENIA
        self.game.level_04.items_to_pick = pygame.sprite.LayeredUpdates()
        ## OBIEKTY DO INTERAKCJI (PODNIESIENIA, WYLECZENIA ITP)
        self.game.level_04.collecting_sprites = pygame.sprite.LayeredUpdates()
        ## ZLOTE MONETY DO PODNIESIENIA
        self.game.level_04.gold_to_pick = pygame.sprite.LayeredUpdates()
        ## STRZALY DO PODNIESIENIA
        self.game.level_04.arrows_to_pick = pygame.sprite.LayeredUpdates()
        ## DRZWI
        self.game.level_04.doors = pygame.sprite.LayeredUpdates()
        ## SKRZYNIE
        self.game.level_04.chest_to_open = pygame.sprite.LayeredUpdates()
        ## TELEPORTS
        self.game.level_04.teleports = pygame.sprite.LayeredUpdates()
        ## SHOPS
        self.game.level_04.shops = pygame.sprite.LayeredUpdates()
        #### LOAD TILE OBJECTS
        self.load_objects(self.game.map_level_04.tmxdata.objects)

    def load_level_03(self):
        self.game.act_lvl = self.game.level_03
        ### ALL SPRITES (BEZ GRACZA!)
        self.game.level_03.all_sprites = pygame.sprite.LayeredUpdates()
        ## MURY / tylko odbijanie od obiektu Rect z TMX MAPS
        self.game.level_03.walls = pygame.sprite.LayeredUpdates()
        ## PRZESZKODY / odbijaja sie za pomoca hit_rect.
        self.game.level_03.hr_obstacles = pygame.sprite.LayeredUpdates()
        ## NIEWIDZIALNE POLE ZABIERAJACE HP
        self.game.level_03.lavas = pygame.sprite.LayeredUpdates()
        ## NPCS
        self.game.level_03.npcs = pygame.sprite.LayeredUpdates()
        ## PRZECIWNICY
        self.game.level_03.mobs = pygame.sprite.LayeredUpdates()
        ## STRZALY PRZECIWNIKOW
        self.game.level_03.mob_arrows = pygame.sprite.LayeredUpdates()
        ## STRZALY ranged
        self.game.level_03.arrows = pygame.sprite.LayeredUpdates()
        ## Sprite ataku wręcz
        self.game.level_03.melle_swing = pygame.sprite.LayeredUpdates()
        ## PRZEDMIOTY NA MAPIE DO PODNIESIENIA
        self.game.level_03.items_to_pick = pygame.sprite.LayeredUpdates()
        ## OBIEKTY DO INTERAKCJI (PODNIESIENIA, WYLECZENIA ITP)
        self.game.level_03.collecting_sprites = pygame.sprite.LayeredUpdates()
        ## ZLOTE MONETY DO PODNIESIENIA
        self.game.level_03.gold_to_pick = pygame.sprite.LayeredUpdates()
        ## STRZALY DO PODNIESIENIA
        self.game.level_03.arrows_to_pick = pygame.sprite.LayeredUpdates()
        ## DRZWI
        self.game.level_03.doors = pygame.sprite.LayeredUpdates()
        ## SKRZYNIE
        self.game.level_03.chest_to_open = pygame.sprite.LayeredUpdates()
        ## TELEPORTS
        self.game.level_03.teleports = pygame.sprite.LayeredUpdates()
        ## SHOPS
        self.game.level_03.shops = pygame.sprite.LayeredUpdates()
        #### LOAD TILE OBJECTS
        self.load_objects(self.game.map_level_03.tmxdata.objects)

    def load_level_02(self):
        self.game.act_lvl = self.game.level_02
        ### ALL SPRITES (BEZ GRACZA!)
        self.game.level_02.all_sprites = pygame.sprite.LayeredUpdates()
        ## MURY / tylko odbijanie od obiektu Rect z TMX MAPS
        self.game.level_02.walls = pygame.sprite.LayeredUpdates()
        ## PRZESZKODY / odbijaja sie za pomoca hit_rect.
        self.game.level_02.hr_obstacles = pygame.sprite.LayeredUpdates()
        ## NIEWIDZIALNE POLE ZABIERAJACE HP
        self.game.level_02.lavas = pygame.sprite.LayeredUpdates()
        ## NPCS
        self.game.level_02.npcs = pygame.sprite.LayeredUpdates()
        ## PRZECIWNICY
        self.game.level_02.mobs = pygame.sprite.LayeredUpdates()
        ## STRZALY PRZECIWNIKOW
        self.game.level_02.mob_arrows = pygame.sprite.LayeredUpdates()
        ## STRZALY ranged
        self.game.level_02.arrows = pygame.sprite.LayeredUpdates()
        ## Sprite ataku wręcz
        self.game.level_02.melle_swing = pygame.sprite.LayeredUpdates()
        ## PRZEDMIOTY NA MAPIE DO PODNIESIENIA
        self.game.level_02.items_to_pick = pygame.sprite.LayeredUpdates()
        ## OBIEKTY DO INTERAKCJI (PODNIESIENIA, WYLECZENIA ITP)
        self.game.level_02.collecting_sprites = pygame.sprite.LayeredUpdates()
        ## ZLOTE MONETY DO PODNIESIENIA
        self.game.level_02.gold_to_pick = pygame.sprite.LayeredUpdates()
        ## STRZALY DO PODNIESIENIA
        self.game.level_02.arrows_to_pick = pygame.sprite.LayeredUpdates()
        ## DRZWI
        self.game.level_02.doors = pygame.sprite.LayeredUpdates()
        ## SKRZYNIE
        self.game.level_02.chest_to_open = pygame.sprite.LayeredUpdates()
        ## TELEPORTS
        self.game.level_02.teleports = pygame.sprite.LayeredUpdates()
        ## SHOPS
        self.game.level_02.shops = pygame.sprite.LayeredUpdates()
        #### LOAD TILE OBJECTS
        self.load_objects(self.game.map_level_02.tmxdata.objects)

        #for tile_object in self.game.map_level_02.tmxdata.objects:
        #    object_center = vec(tile_object.x + tile_object.width/2, tile_object.y + tile_object.height/2)
        #    ### MAP ELEMENTS
        #    if tile_object.name == "wall":
        #        Obstacle(self.game, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
        #    if tile_object.name == "teleport":
        #        Teleport(self.game, tile_object.destination, tile_object.pos_x, tile_object.pos_y,
        #                 tile_object.x, tile_object.y, tile_object.width, tile_object.height)

    def load_level_01(self):
        self.game.act_lvl = self.game.level_01
        ### ALL SPRITES (BEZ GRACZA!)
        self.game.level_01.all_sprites = pygame.sprite.LayeredUpdates()
        ## MURY / tylko odbijanie od obiektu Rect z TMX MAPS
        self.game.level_01.walls = pygame.sprite.LayeredUpdates()
        ## PRZESZKODY / odbijaja sie za pomoca hit_rect.
        self.game.level_01.hr_obstacles = pygame.sprite.LayeredUpdates()
        ## NIEWIDZIALNE POLE ZABIERAJACE HP
        self.game.level_01.lavas = pygame.sprite.LayeredUpdates()
        ## NPCS
        self.game.level_01.npcs = pygame.sprite.LayeredUpdates()
        ## PRZECIWNICY
        self.game.level_01.mobs = pygame.sprite.LayeredUpdates()
        ## STRZALY PRZECIWNIKOW
        self.game.level_01.mob_arrows = pygame.sprite.LayeredUpdates()
        ## STRZALY ranged
        self.game.level_01.arrows = pygame.sprite.LayeredUpdates()
        ## Sprite ataku wręcz
        self.game.level_01.melle_swing = pygame.sprite.LayeredUpdates()
        ## PRZEDMIOTY NA MAPIE DO PODNIESIENIA
        self.game.level_01.items_to_pick = pygame.sprite.LayeredUpdates()
        ## OBIEKTY DO INTERAKCJI (PODNIESIENIA, WYLECZENIA ITP)
        self.game.level_01.collecting_sprites = pygame.sprite.LayeredUpdates()
        ## ZLOTE MONETY DO PODNIESIENIA
        self.game.level_01.gold_to_pick = pygame.sprite.LayeredUpdates()
        ## STRZALY DO PODNIESIENIA
        self.game.level_01.arrows_to_pick = pygame.sprite.LayeredUpdates()
        ## DRZWI
        self.game.level_01.doors = pygame.sprite.LayeredUpdates()
        ## SKRZYNIE
        self.game.level_01.chest_to_open = pygame.sprite.LayeredUpdates()
        ## TELEPORTS
        self.game.level_01.teleports = pygame.sprite.LayeredUpdates()
        ## SHOPS
        self.game.level_01.shops = pygame.sprite.LayeredUpdates()
        ### LOAD TILE OBJECTS
        self.load_objects(self.game.map_level_01.tmxdata.objects)

    def load_objects(self, tmx_objects):
        for tile_object in tmx_objects:
            object_center = vec(tile_object.x + tile_object.width/2, tile_object.y + tile_object.height/2)
            ### ENEMIES NEW
            if tile_object.type == "enemy":
                self.enemy_gen.generate(tile_object.name,object_center.x,object_center.y, tile_object.image, tile_object.item)
            if tile_object.type == "enemy s":
                self.enemy_gen.generate_s(tile_object.name,object_center.x,object_center.y, tile_object.image,
                                          tile_object.sx,tile_object.sy, tile_object.item)
            if tile_object.type == "enemy_r":
                self.enemy_gen.generate_r(tile_object.name,object_center.x,object_center.y,tile_object.image, tile_object.item)
            ### NPCS
            if tile_object.type == "npc":
                self.npcs_gen.generate(tile_object.name,tile_object.x,tile_object.y,tile_object.image)
            ### MAP ELEMENTS
            if tile_object.name == "wall":
                Obstacle(self.game,tile_object.x,tile_object.y,tile_object.width,tile_object.height, water=False)
            if tile_object.name == "rem_wall":
                RemObstacle(self.game,tile_object.x,tile_object.y,tile_object.width,
                            tile_object.height, water=False,remove_event=tile_object.event)
            if tile_object.name == "water":
                Obstacle(self.game,tile_object.x,tile_object.y,tile_object.width,tile_object.height, water=True)
            if tile_object.name == "lava":
                Lava(self.game,tile_object.x,tile_object.y,tile_object.width,tile_object.height,self.lava_effect)
            if tile_object.type == "teleport":
                Teleport(self.game,tile_object.name, tile_object.destination, tile_object.pos_x, tile_object.pos_y,
                         tile_object.x,tile_object.y,tile_object.width,tile_object.height)
            if tile_object.type == "shop":
                ShopDoor(self.game,tile_object.name, tile_object.pos_x, tile_object.pos_y,
                         tile_object.x,tile_object.y,tile_object.width,tile_object.height)
            ### MAP DECORATIONS
            if tile_object.name == "torch":
                Torch(self.game,object_center.x,object_center.y)
            if tile_object.name == "fountain":
                Animated_Obstacle(self.game,object_center.x,object_center.y,tile_object.name)
            ### TRAPS
            if tile_object.name == "trap1e":
                Trap(self.game,object_center.x,object_center.y,trap1_img,"E", 4)
            if tile_object.name == "trap1w":
                Trap(self.game,object_center.x,object_center.y,trap1_img,"W", 4)
            if tile_object.name == "trap1n":
                Trap(self.game,object_center.x,object_center.y,trap1_img,"N", 4)
            if tile_object.name == "trap1s":
                Trap(self.game,object_center.x,object_center.y,trap1_img,"S", 4)
            if tile_object.name == "darttrape":
                DartTrap(self.game,object_center.x,object_center.y,vec(1,0),200,5)
            if tile_object.name == "darttrapw":
                DartTrap(self.game,object_center.x,object_center.y,vec(-1,0),200,5)
            if tile_object.name == "pintrap":
                PinTrap(self.game, object_center.x,object_center.y,pintrap_h_img, pintrap_o_img,5)
            if tile_object.name == "spider web":
                EffectObject(self.game,object_center.x,object_center.y,tile_object.image,self.slow_effect)
            #### DOORS
            if tile_object.name == "door":
                Door(self.game,object_center.x,object_center.y,tile_object.key,tile_object.image)
            #### FENCE
            if tile_object.name == "wood fence":
                Fence_Object(self.game,object_center.x,object_center.y,10,tile_object.image,32,32)
            #### TREASURES AND INTERACTIVE SPRITES ########
            if tile_object.name == "sign":
                InfoSprite(self.game,tile_object.name,object_center.x,object_center.y,
                           tile_object.width,tile_object.height,tile_object.text)
            if tile_object.type == "fruit tree":
                CollectingSprite(self.game,tile_object.name,object_center.x,object_center.y,"hp",tile_object.strength,tile_object.no,12,20)
            if tile_object.name == "barrel":
                Treasure_Object(self.game,object_center.x,object_center.y,barrel_img,22,
                                tile_object.item,tile_object.maxcost,20,20)
            if tile_object.name == "gold":
                Gold_to_take(self.game,object_center.x,object_center.y,tile_object.gold)
            if tile_object.name == "hidden gold":
                HiddenGold_to_take(self.game,object_center.x,object_center.y,tile_object.gold)
            if tile_object.name == "arrow":
                Arrow_to_take(self.game,object_center.x,object_center.y,tile_object.number)
            if tile_object.name == "treasure chest":
                Treasure_Chest(self.game,object_center.x,object_center.y,tile_object.key,
                               tile_object.locked,tile_object.treasure_value,tile_object.item,20,18)
            #### ITEMS ############
            if tile_object.type == "quest item":
                #print (f'Generating Quest item name: {tile_object.name}')
                Item_to_take(self.game,object_center.x,object_center.y,
                             self.gen.generate_quest_item_by_name(tile_object.name))
            if tile_object.type == "hidden item":
                HiddenItem_to_take(self.game,object_center.x,object_center.y,
                                   self.gen.generate_item_by_name(tile_object.name))
            #### KEYS #############
            if tile_object.type == "key":
                Item_to_take(self.game,object_center.x,object_center.y,
                             self.gen.g_key(tile_object.name, tile_object.key))
            if tile_object.type == "hidden key":
                HiddenItem_to_take(self.game,object_center.x,object_center.y,
                                   self.gen.g_key(tile_object.name, tile_object.key))
            #### WEAPONS ##########
            if tile_object.type == "weapon":
                Item_to_take(self.game,object_center.x,object_center.y,
                             self.gen.generate_weapon_by_name(tile_object.name))
            #### POTIONS ###########
            if tile_object.type == "potion":
                Item_to_take(self.game, object_center.x, object_center.y,
                             self.gen.generate_potion_by_name(tile_object.name))
            #### ARMORS #########
            if tile_object.type == "armor":
                Item_to_take(self.game,object_center.x,object_center.y,
                             self.gen.generate_armor_by_name(tile_object.name))
