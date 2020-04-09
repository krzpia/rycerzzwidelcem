import pygame
vec = pygame.math.Vector2
from sprites import *
from data import *
from items import ItemGenerator
from enemies import EnemyGenerator
from npcs import NpcGenerator
from npcs import QuestGenerator
from ui import ActiveEffect


class LevelGen:
    def __init__(self, game):
        self.game = game
        self.gen = ItemGenerator(self.game,tileset_image,full_tileset_image)
        self.enemy_gen = EnemyGenerator(self.game,tileset_image,full_tileset_image)
        self.npcs_gen = NpcGenerator(self.game,tileset_image,full_tileset_image)
        self.quest_gen = QuestGenerator(self.game)
        self.shop_gen = ShopGenerator(self.game, self.gen)
        self.lava_effect = ActiveEffect("fire",e_fire_ico,5,1)
        self.slow_effect = ActiveEffect("slow",e_slow_ico,50,1.2)
        self.images_dict = {}

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

    def load_level_05(self, saved_data):
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
        if not saved_data:
            ### 1 URUCHOMIENIE:
            self.load_objects(self.game.map_level_05.tmxdata.objects)
        else:
            ### 2. z LOAD GAME
            print ("MAM DANE, uruchamiam load level from saved data...")
            self.load_enemy_images(self.game.map_level_05.tmxdata.objects)
            self.load_object_images(self.game.map_level_05.tmxdata.objects)
            self.load_objects_from_save_data(self.game.map_level_05.tmxdata.objects, saved_data)

    def load_level_04(self, saved_data):
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
        if not saved_data:
            ### 1 URUCHOMIENIE:
            self.load_objects(self.game.map_level_04.tmxdata.objects)
        else:
            ### 2. z LOAD GAME
            print ("MAM DANE, uruchamiam load level from saved data...")
            self.load_enemy_images(self.game.map_level_04.tmxdata.objects)
            self.load_object_images(self.game.map_level_04.tmxdata.objects)
            self.load_objects_from_save_data(self.game.map_level_04.tmxdata.objects, saved_data)

    def load_level_03(self, saved_data):
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
        if not saved_data:
            ### 1 URUCHOMIENIE:
            self.load_objects(self.game.map_level_03.tmxdata.objects)
        else:
            ### 2. z LOAD GAME
            print ("MAM DANE, uruchamiam load level from saved data...")
            self.load_enemy_images(self.game.map_level_03.tmxdata.objects)
            self.load_object_images(self.game.map_level_03.tmxdata.objects)
            self.load_objects_from_save_data(self.game.map_level_03.tmxdata.objects, saved_data)

    def load_level_02(self, saved_data):
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
        if not saved_data:
            ### 1 URUCHOMIENIE:
            self.load_objects(self.game.map_level_02.tmxdata.objects)
        else:
            ### 2. z LOAD GAME
            print ("MAM DANE, uruchamiam load level from saved data...")
            self.load_enemy_images(self.game.map_level_02.tmxdata.objects)
            self.load_object_images(self.game.map_level_02.tmxdata.objects)
            self.load_objects_from_save_data(self.game.map_level_02.tmxdata.objects, saved_data)

    def load_level_01(self, saved_data):
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
        if not saved_data:
            ### 1 URUCHOMIENIE:
            self.load_objects(self.game.map_level_01.tmxdata.objects)
        else:
            ### 2. z LOAD GAME
            print ("MAM DANE, uruchamiam load level from saved data...")
            self.load_enemy_images(self.game.map_level_01.tmxdata.objects)
            self.load_object_images(self.game.map_level_01.tmxdata.objects)
            self.load_objects_from_save_data(self.game.map_level_01.tmxdata.objects, saved_data)

    def save_objects(self, act_lvl):
        ##### KODUJE WSZYSTKIE PRZEDMIOTY, KTORE MAJA MIEC NADPISANY STAN
        ### HR OBSTACLES:
        treasure_objects_list = []
        door_list = []
        for hrob in act_lvl.hr_obstacles:
            if isinstance(hrob, Treasure_Object):
                if hrob.item:
                    if hrob.item == "gold":
                        hrob_item = "gold"
                        hrob_max_cost = hrob.max_cost
                    elif hrob.item == "random":
                        hrob_item = "random"
                        hrob_max_cost = hrob.max_cost
                    else:
                        hrob_item = hrob.item.name
                        hrob_max_cost = hrob.max_cost
                else:
                    hrob_item = False
                    hrob_max_cost = False
                treasure_objects_list.append((hrob.name, hrob.rect.centerx,hrob.rect.centery,
                                              hrob_item, hrob_max_cost))
            if isinstance(hrob, Door):
                door_list.append((hrob.name, hrob.rect.centerx,hrob.rect.centery,hrob.key))
        ### MOBS:
        mob_list = []
        for mob in act_lvl.mobs:
            if mob.item:
                mob_item_name = mob.item
            else:
                mob_item_name = False
            if mob.s_pos and not mob.bullet_type:
                mob_type = "enemy s"
            elif mob.bullet_type:
                mob_type = "enemy_r"
            else:
                mob_type = "enemy"
            mob_list.append((mob_type, mob.name, mob.start_x, mob.start_y,
                             mob.s_pos, mob_item_name, mob.hp))
        ### ITEMS:
        item_list = []
        hidden_item_list = []
        gold_list = []
        hidden_gold_list = []
        arrow_list = []
        for item in act_lvl.items_to_pick:
            if isinstance(item, Item_to_take):
                if item.item.name[:3] == "Key":
                    item_list.append((item.item.name, item.rect.centerx, item.rect.centery, item.item.key))
                else:
                    item_list.append((item.item.name, item.rect.centerx, item.rect.centery, False))
            elif isinstance(item, HiddenItem_to_take):
                if item.item.name[:3] == "Key":
                    hidden_item_list.append((item.item.name, item.rect.centerx, item.rect.centery, item.item.key))
                else:
                    hidden_item_list.append((item.item.name, item.rect.centerx, item.rect.centery, False))
            elif isinstance(item, HiddenGold_to_take):
                hidden_gold_list.append((item.gold, item.rect.centerx, item.rect.centery))
            else:
                print("ERROR INCODING items_to_pick")
        for item in act_lvl.gold_to_pick:
            if isinstance(item, Gold_to_take):
                gold_list.append((item.gold, item.rect.centerx, item.rect.centery))
        for item in act_lvl.arrows_to_pick:
            if isinstance(item, Arrow_to_take):
                arrow_list.append((item.number,item.rect.centerx, item.rect.centery))
        ### WALLS (Fence objects):
        wall_list = []
        for wall in act_lvl.walls:
            if isinstance(wall, sprites.Fence_Object):
                wall_list.append((wall.name,wall.rect.centerx,wall.rect.centery,wall.hp))
        ### TREASURE CHESTS:
        chest_list = []
        for chest in act_lvl.chest_to_open:
            chest_namecond_list = chest.inventory.return_item_namecond_list()
            chest_list.append((chest.rect.centerx, chest.rect.centery,chest.locked, chest.closed,
                              chest.key, chest_namecond_list))
        ##### UTWORZONO TYMCzASOWE LISTY DWUWYMIAROWE
        print ("OBIEKTY Z DANEGO LEVELU:")
        print (treasure_objects_list)
        print (door_list)
        print ("MOBs..")
        print (mob_list)
        print ("ITEMS On Ground")
        print (item_list)
        print(hidden_item_list)
        print(gold_list)
        print(hidden_gold_list)
        print(arrow_list)
        print ("WALLS..")
        print (wall_list)
        print ("Chest..")
        print (chest_list)
        print ("KONIEC DANYCH")
        obj_data = {'treasure_objects_list':treasure_objects_list,
                      'door_list':door_list,
                      'mob_list':mob_list,
                      'item_list':item_list,
                      'hidden_item_list':hidden_item_list,
                      'gold_list':gold_list,
                      'hidden_gold_list':hidden_gold_list,
                      'arrow_list':arrow_list,
                      'wall_list':wall_list,
                      'chest_list':chest_list,
                      }
        return obj_data

    def load_enemy_images(self, tmx_objects):
    ########## GENERUJE OBRAZKI
        for en_object in tmx_objects:
            if en_object.type == "enemy" or en_object.type == "enemy s" or en_object.type == "enemy_r":
                self.enemy_gen.generate_image(en_object.name,en_object.image)

    def load_object_images(self, tmx_objects):
        for all_objects in tmx_objects:
            if all_objects.name == "door":
                print ("FOUND DOOR IMAGE")
                self.images_dict['door'] = all_objects.image

    def load_objects_from_save_data(self, tmx_objects, obj_data):
        mob_list = obj_data['mob_list']
        ########### WGRYWAM SPRITE`Y ######
        #######   MOBS
        for mob in mob_list:
            if mob[0] == "enemy":
                self.enemy_gen.generate(mob[1],mob[2],mob[3],
                                        self.enemy_gen.get_image_by_name(mob[1]),
                                        mob[5],mob[6])
            if mob[0] == "enemy_r":
                self.enemy_gen.generate_r(mob[1],mob[2],mob[3],
                                          self.enemy_gen.get_image_by_name(mob[1]),
                                          mob[5],mob[6])
            if mob[0] == "enemy s":
                self.enemy_gen.generate_s(mob[1], mob[2], mob[3],
                                          self.enemy_gen.get_image_by_name(mob[1]),
                                          mob[4][0],mob[4][1], mob[5], mob[6])
        ######## TREASURE ITEMS (barrel, doors)
        treasure_obj_list = obj_data['treasure_objects_list']
        for treasure_obj in treasure_obj_list:
            if treasure_obj[0] == "barrel":
                Treasure_Object(self.game, treasure_obj[0], treasure_obj[1], treasure_obj[2], barrel_img, 22,
                                treasure_obj[3], treasure_obj[4], 20, 20)
        door_list = obj_data['door_list']
        for door in door_list:
            if door[0] == "door":
                Door(self.game, door[0], door[1], door[2], door[3], self.images_dict['door'])
        ######### ITEMS
        gold_list = obj_data['gold_list']
        for gold in gold_list:
            Gold_to_take(self.game,gold[1],gold[2],gold[0])
        hidden_gold_list = obj_data['hidden_gold_list']
        for hidden_gold in hidden_gold_list:
            HiddenGold_to_take(self.game,hidden_gold[1],hidden_gold[2],hidden_gold[0])
        item_list = obj_data['item_list']
        for item in item_list:
            Item_to_take(self.game,item[1],item[2],self.gen.load_item_by_name(item[0],item[3]))
        hidden_item_list = obj_data['hidden_item_list']
        for hidden_item in hidden_item_list:
            Item_to_take(self.game,hidden_item[1],hidden_item[2],self.gen.load_item_by_name(hidden_item[0], hidden_item[3]))
        arrow_list = obj_data['arrow_list']
        for arrow in arrow_list:
            Arrow_to_take(self.game,arrow[1],arrow[2],arrow[0])
        ######### CHESTS
        chest_list = obj_data['chest_list']
        for chest in chest_list:
            Treasure_Chest(self.game,chest[0],chest[1],chest[4],chest[2],chest[3],False,False,20,18,chest[5])
        #####################################
        ########### WGRYWAM POZOSTALE DANE
        for tile_object in tmx_objects:
            object_center = vec(tile_object.x + tile_object.width/2, tile_object.y + tile_object.height/2)
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
            #### FENCE
            if tile_object.name == "wood fence":
                Fence_Object(self.game,tile_object.name, object_center.x,object_center.y,10,tile_object.image,32,32)
            #### TREASURES AND INTERACTIVE SPRITES ########
            if tile_object.name == "sign":
                InfoSprite(self.game,tile_object.name,object_center.x,object_center.y,
                           tile_object.width,tile_object.height,tile_object.text)
            if tile_object.type == "fruit tree":
                CollectingSprite(self.game,tile_object.name,object_center.x,object_center.y,"hp",tile_object.strength,tile_object.no,12,20)
            ############## FIN #######################################

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
                Door(self.game,tile_object.name, object_center.x,object_center.y,tile_object.key,tile_object.image)
            #### FENCE
            if tile_object.name == "wood fence":
                Fence_Object(self.game,tile_object.name, object_center.x,object_center.y,10,tile_object.image,32,32)
            #### TREASURES AND INTERACTIVE SPRITES ########
            if tile_object.name == "sign":
                InfoSprite(self.game,tile_object.name,object_center.x,object_center.y,
                           tile_object.width,tile_object.height,tile_object.text)
            if tile_object.type == "fruit tree":
                CollectingSprite(self.game,tile_object.name,object_center.x,object_center.y,"hp",tile_object.strength,tile_object.no,12,20)
            if tile_object.name == "barrel":
                Treasure_Object(self.game,tile_object.name, object_center.x,object_center.y,barrel_img,22,
                                tile_object.item,tile_object.maxcost,20,20)
            if tile_object.name == "gold":
                Gold_to_take(self.game,object_center.x,object_center.y,tile_object.gold)
            if tile_object.name == "hidden gold":
                HiddenGold_to_take(self.game,object_center.x,object_center.y,tile_object.gold)
            if tile_object.name == "arrow":
                Arrow_to_take(self.game,object_center.x,object_center.y,tile_object.number)
            if tile_object.name == "treasure chest":
                Treasure_Chest(self.game,object_center.x,object_center.y,tile_object.key,
                               tile_object.locked,True,tile_object.treasure_value,tile_object.item,20,18)
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
