from sprites import *
import sys
import pickle
from ui import *
from settings import *
import tilemap
from os import path
from data import *
import levels
from items import ItemGenerator
from events.events_manager import EventManager


class Level:
    def __init__(self):
        self.explored = False
        #### ALL SPRITES (BEZ GRACZA!)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        ### MURY / tylko odbijanie od obiektu Rect z TMX MAPS
        self.walls = pygame.sprite.LayeredUpdates()
        ### PRZESZKODY / odbijaja sie za pomoca hit_rect.
        self.hr_obstacles = pygame.sprite.LayeredUpdates()
        ### NIEWIDZIALNE POLE ZABIERAJACE HP
        self.lavas = pygame.sprite.LayeredUpdates()
        ### PRZECIWNICY
        self.mobs = pygame.sprite.LayeredUpdates()
        ### STRZALY ranged
        self.arrows = pygame.sprite.LayeredUpdates()
        ### Sprite ataku wręcz
        self.melle_swing = pygame.sprite.LayeredUpdates()
        ### PRZEDMIOTY NA MAPIE DO PODNIESIENIA
        self.items_to_pick = pygame.sprite.LayeredUpdates()
        ### COLLECTING_SPRITES:
        self.collecting_sprites = pygame.sprite.LayeredUpdates()
        ### ZLOTE MONETY DO PODNIESIENIA
        self.gold_to_pick = pygame.sprite.LayeredUpdates()
        ### STRZALY DO PODNIESIENIA
        self.arrows_to_pick = pygame.sprite.LayeredUpdates()
        ### DRZWI
        self.doors = pygame.sprite.LayeredUpdates()
        ### SKRZYNIE
        self.chest_to_open = pygame.sprite.LayeredUpdates()
        ### TELEPORTS
        self.teleports = pygame.sprite.LayeredUpdates()
        ### SHOPS
        self.shops = pygame.sprite.LayeredUpdates()

class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 2048)
        pygame.init()
        #### USTAWIC POZNIEJ SILE DZWIEKU!
        #print(pygame.mixer.Channel(1).get_volume())
        ######
        self.clock = pygame.time.Clock()
        global font
        font = font_16
        global font20
        font20 = font_20
        global font48
        font48 = font_48
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.map_surface = pygame.Surface((MAP_WIDTH, MAP_HEIGHT), pygame.HWSURFACE | pygame.SRCALPHA| pygame.DOUBLEBUF)
        pygame.display.set_caption(TITLE)
        pygame.key.set_repeat(300, 100)
        ######## ZMIENNE DO DEBUOWANIA #######
        self.unlock_updates = False
        self.fpss = []
        print ("STARTING GAME MODULE - Correct. Version alfa 0.1")

    def get_tile(self, tileset, x, y):
        surface = pygame.Surface((32, 32)).convert_alpha()
        surface.blit(tileset, (0, 0), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        return surface

    def blit_alpha(self, target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)
        target.blit(temp, location)

    def write(self, text, location, color=(255, 255, 255)):
        self.screen.blit(font.render(text, True, color), location)

    def big_write(self, text, location, color=(255, 255, 255)):
        self.screen.blit(font20.render(text, True, color), location)

    def title_write(self, text, location, color=(255, 255, 255)):
        self.screen.blit(font48.render(text, True, color), location)

    def s_write(self, text, surface, location, color=(WHITE)):
        surface.blit(font.render(text, True, color), location)

    def intro(self):
        self.intro_screen = True
        self.to_char_chose = False
        self.class_selected = False
        self.dif_list = (DIF_KID,DIF_EASY,DIF_NOR,DIF_HARD,DIF_ULTIMATE)
        self.difficulty = self.dif_list[2]
        ### CREATE CLASESS
        self.knight_class = CharClass("Knight", pl_knight_image, knight_death_anim, ["sword", "spear", "axe"],
                                      ["staff", "dagger"],
                                      ["plate"], ["robe"], 4, 4, 1, 2, 3, 1, ["Heroism"])
        self.wizard_class = CharClass("Wizard", pl_wizard_image, knight_death_anim, ["staff"], ["sword", "axe", "bow"],
                                      ["robe"],
                                      ["chain", "plate"], 2, 1, 4, 5, 2, 2, ["Firebolt"])
        self.thief_class = CharClass("Thief", pl_thief_image, knight_death_anim, ["dagger", "bow"], ["axe", "spear"],
                                     ["leather"],
                                     ["plate"], 2, 2, 2, 2, 4, 5, ["Haste"])
        ################
        pygame.mixer.music.stop()
        self.incr_diff_button = RadioButton(rad_add_img,rad_add_h_img,INCR_DIF_BUT[0],INCR_DIF_BUT[1])
        self.decr_diff_button = RadioButton(rad_subs_img, rad_subs_h_img, DECR_DIF_BUT[0], DECR_DIF_BUT[1])
        self.new_game_button = Button(intro_but_img, intro_but_h_img, 128, 32, "New Game", SCREEN_WIDTH / 2 - 64, 370)
        self.load_game_button = Button(intro_but_img,intro_but_h_img,128,32,"Load Game",
                                       SCREEN_WIDTH/2 - 64,320)
        self.quit_game_button = Button(intro_but_img, intro_but_h_img, 128, 32, "Quit", SCREEN_WIDTH / 2 - 64, 420)
        self.start_game_button = Button(intro_but_img, intro_but_h_img, 150, 32, "Start Game", SCREEN_WIDTH / 2 - 64,650)
        self.knight_class_button = Button(intro_but_img, intro_but_h_img, 128, 32, "Knight", 170, 365)
        self.wizard_class_button = Button(intro_but_img, intro_but_h_img, 128, 32, "Wizard", 170, 415)
        self.thief_class_button = Button(intro_but_img, intro_but_h_img, 128, 32, "Thief", 170, 465)
        self.intro_buttons = [self.new_game_button, self.quit_game_button, self.load_game_button]
        self.class_buttons = [self.knight_class_button, self.wizard_class_button,
                              self.thief_class_button, self.start_game_button]

        while self.intro_screen:
            self.dt = self.clock.tick(FPS) / 1000
            self.intro_events()
            self.intro_update()
            self.intro_draw()

    def intro_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                if event.key == pygame.K_n:
                    self.new()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.new_game_button.check_if_clicked(mouse_pos):
                        if not self.to_char_chose:
                            self.to_char_chose = True
                            self.new_game_button.deactivate()
                            self.quit_game_button.deactivate()
                    if self.start_game_button.check_if_clicked(mouse_pos):
                        self.new(self.class_selected, self.difficulty)
                    if self.knight_class_button.check_if_clicked(mouse_pos):
                        self.class_selected = self.knight_class
                    if self.wizard_class_button.check_if_clicked(mouse_pos):
                        self.class_selected = self.wizard_class
                    if self.thief_class_button.check_if_clicked(mouse_pos):
                        self.class_selected = self.thief_class
                    if self.quit_game_button.check_if_clicked(mouse_pos):
                        self.quit()
                    if self.load_game_button.check_if_clicked(mouse_pos):
                        #try:
                        self.load_game()
                        #except:
                        #    print ("Load Not Succesfull")
                        #else:
                        #    self.quit()
                    if self.incr_diff_button.check_if_clicked(mouse_pos):
                        a = self.dif_list.index(self.difficulty)
                        if a < 4:
                            self.difficulty = self.dif_list[(a+1)]
                    if self.decr_diff_button.check_if_clicked(mouse_pos):
                        a = self.dif_list.index(self.difficulty)
                        if a > 0:
                            self.difficulty = self.dif_list[(a-1)]

    def intro_update(self):
        mouse_pos = pygame.mouse.get_pos()
        #### HIGHLIGHT BUTTONS #####
        if self.to_char_chose:
            for button in self.class_buttons:
                button.check_if_highlight(mouse_pos)
            self.incr_diff_button.check_if_highlight(mouse_pos)
            self.decr_diff_button.check_if_highlight(mouse_pos)
        else:
            for button in self.intro_buttons:
                button.check_if_highlight(mouse_pos)

        if self.class_selected:
            self.start_game_button.activate()
        else:
            self.start_game_button.deactivate()

    def intro_draw(self):
        self.credits_text1 = "My dear wife Monika, Piotr Kopalko, Zuza and Magda for inspiration and superb sound effects"
        self.credits_text2 = "Chris Bradfield for his amazing tutorials on www.kidscancode.org"
        self.credits_text3 = "Thanks to Thorbjørn Lindeijer for great tool TiledMapEditor"
        self.credits_text4 = "Music by: HorrorPen, Alexandr Zhelanov. Font by Dieter Steffmann"
        self.credits_text5 = "www.opengameart.org: DungeonCrawler, Lorc, Adrix89, gargargarrick and many more"
        self.author_text = "Author: K.J.Piatkowski"
        self.screen.fill(BGCOLOR)
        if self.to_char_chose:
            self.screen.blit(setup_img, (0, 0))
            self.title_write(TITLE,T_POS,PURPLE)
            self.big_write("Choose your class:",CTXT,PURPLE)
            self.knight_class_button.show_button(self.screen, font20)
            self.wizard_class_button.show_button(self.screen, font20)
            self.thief_class_button.show_button(self.screen, font20)
            self.start_game_button.show_button(self.screen, font20)
            self.incr_diff_button.show_button(self.screen)
            self.decr_diff_button.show_button(self.screen)
            if self.difficulty == DIF_NOR:
                dif_txt = "Normal"
            elif self.difficulty == DIF_EASY:
                dif_txt = "Easy. For beginers"
            elif self.difficulty == DIF_KID:
                dif_txt = "Very Easy. For kids"
            elif self.difficulty == DIF_HARD:
                dif_txt = "Hard. For skilled players"
            elif self.difficulty == DIF_ULTIMATE:
                dif_txt = "Extreme. For super masters!"
            else:
                print ("ERROR NO DIFF LVL!")
            self.write(f'Difficulty: {dif_txt}', (DECR_DIF_BUT[0]-40, INCR_DIF_BUT[1] - 25), WHITE)
            self.decr_diff_button.show_button(self.screen)
            if self.class_selected:
                if self.class_selected == self.knight_class:
                    self.screen.blit(self.class_selected.image, TIMGPOS)
                    self.big_write("Knight", NTXT, WHITE)
                    self.write("Dedicated do melle fight, starts with strength and stamina bonus", ADTXT, WHITE)
                    self.write("No penalty using plate armors", (ADTXT[0], ADTXT[1] + 25), WHITE)
                if self.class_selected == self.wizard_class:
                    self.screen.blit(self.class_selected.image, TIMGPOS)
                    self.big_write("Wizard", NTXT, WHITE)
                    self.write("Weak in direct fight, but able to make severe damage by magic powers", ADTXT, WHITE)
                    self.write("Bonus x1.5 power of offensive spells", (ADTXT[0], ADTXT[1] + 25), WHITE)
                if self.class_selected == self.thief_class:
                    self.screen.blit(self.class_selected.image, TIMGPOS)
                    self.big_write("Thief", NTXT, WHITE)
                    self.write("Fast and able to sneak, powerful with bow and dagger combination", ADTXT, WHITE)
                    self.write("Bonus x1.3 Hit Rate with ranged weapons, and additional barter bonus",(ADTXT[0],ADTXT[1]+25), WHITE)
                self.screen.blit(i_str_ico, (IDX - 30, IDY + 0))
                self.screen.blit(i_sta_ico, (IDX - 30, IDY + 20))
                self.screen.blit(i_int_ico, (IDX - 30, IDY + 40))
                self.screen.blit(i_wis_ico, (IDX - 30, IDY + 60))
                self.screen.blit(i_spe_ico, (IDX - 30, IDY + 80))
                self.screen.blit(i_ste_ico, (IDX - 30, IDY + 100))
                self.write("Strength: " + str(self.class_selected.str), (IDX, IDY + 0))
                self.write("Stamina: " + str(self.class_selected.sta), (IDX, IDY + 20))
                self.write("Intellect: " + str(self.class_selected.int), (IDX, IDY + 40))
                self.write("Wisdom: " + str(self.class_selected.wis), (IDX, IDY + 60))
                self.write("Speed: " + str(self.class_selected.spe), (IDX, IDY + 80))
                self.write("Stealth: " + str(self.class_selected.ste), (IDX, IDY + 100))
                self.write("Favourite weapons: ", (IADX,IADY + 0), WHITE)
                weapon_txt = ""
                for weapon in self.class_selected.favourite_weapons:
                    weapon_txt += weapon
                    weapon_txt += ","
                self.write(weapon_txt, (IADX + 120, IADY + 0), WHITE)
                armor_txt = ""
                self.write("Favourite armors: ", (IADX,IADY + 20), WHITE)
                for armor in self.class_selected.favourite_armors:
                    armor_txt += armor
                    armor_txt += ","
                self.write(armor_txt, (IADX + 120, IADY + 20), WHITE)
                self.write("Disliked weapons: ", (IADX,IADY + 40), WHITE)
                weapon_txt = ""
                for weapon in self.class_selected.disliked_weapons:
                    weapon_txt += weapon
                    weapon_txt += ","
                self.write(weapon_txt, (IADX + 120, IADY + 40), WHITE)
                armor_txt = ""
                self.write("Disliked armors: ", (IADX,IADY + 60), WHITE)
                for armor in self.class_selected.disliked_armors:
                    armor_txt += armor
                    armor_txt += ","
                self.write(armor_txt, (IADX + 120, IADY + 60), WHITE)

        else:
            self.screen.blit(intro_img, (0, 0))
            self.title_write(TITLE,(280,250),PURPLE)
            self.big_write(self.author_text,(200,500),PURPLE)
            self.write("Special thanks to:",(200,575),PURPLE)
            self.write(self.credits_text1,(200,600),PURPLE)
            self.write(self.credits_text2,(200,620),PURPLE)
            self.write(self.credits_text3,(200,640), PURPLE)
            self.write(self.credits_text4,(200,660), PURPLE)
            self.write(self.credits_text5, (200, 680), PURPLE)
            self.new_game_button.show_button(self.screen, font20)
            self.load_game_button.show_button(self.screen, font20)
            self.quit_game_button.show_button(self.screen, font20)
        self.write(str(self.clock.get_fps()), (0, 0))
        #### FLIP
        pygame.display.flip()

    def save_game(self):
        print ("saving...")
        saveGame = open('savegame.txt', 'wb')
        print ("looking for act_lvl...")
        for key in self.levels:
            if self.levels[key] == self.act_lvl:
                act_level_name = key
        print ("looking for spells in spellbook:")
        spell_name_list = []
        for spell in self.player.spell_book.spells:
            spell_name_list.append(spell.name)
        print ("looking for quests in questbook:")
        quest_name_list = []
        for quest in self.player.quest_book.quests:
            quest_name_list.append(quest.name)
        print ("packing player_data...")
        score_data = [self.player.score_killed_enemies,
                      self.player.score_swings,
                      self.player.score_swing_enemy_hits,
                      self.player.score_arrows,
                      self.player.score_arrow_enemy_hits,
                      self.player.score_spell_bullets,
                      self.player.score_off_spell_damage,
                      self.player.score_inflicted_damage,
                      self.player.score_blocks,
                      self.player.score_time_played,
                      self.player.score_chest_opened,
                      self.player.score_barrels_destroyed]
        player_data = {'char_name': self.player.char_name,
                       'name': self.player.name,
                       'act_lvl_name': act_level_name,
                       'x': self.player.pos.x,
                       'y': self.player.pos.y,
                       'pos_x': int(self.player.pos.x / TILE_SIZE),
                       'pos_y': int(self.player.pos.y / TILE_SIZE),
                       'act_hp':self.player.act_hp,
                       'act_mana':self.player.act_mana,
                       'gold': self.player.gold,
                       'level': self.player.level,
                       'attribute_points': self.player.attribute_points,
                       'xp': self.player.xp,
                       'arrows': self.player.arrows,
                       'base_str':self.player.base_strength,
                       'base_sta':self.player.base_stamina,
                       'base_int':self.player.base_intellect,
                       'base_wis':self.player.base_wisdom,
                       'base_spe':self.player.base_speed,
                       'base_ste':self.player.base_stealth,
                       'inventory_namecond_list' : self.player.inventory.return_item_namecond_list(),
                       'active_slots_item_namecond_list': self.player.return_active_slots_item_namecond_list(),
                       'spell_list':spell_name_list,
                       'quest_list':quest_name_list,
                       'score_data':score_data}
        print (player_data)
        print ("-------------------------------")
        print ("packing levels_data...")
        levels_data = {}
        for level_name in self.levels:
            levels_data[level_name] = self.levelgen.save_objects(self.levels[level_name])
        print ("packing shops data...")
        shops_data = self.levelgen.shop_gen.save_shops_data()
        saveValues = (self.difficulty, self.events_manager, player_data, levels_data, shops_data, score_data)
        pickle.dump(saveValues, saveGame)
        saveGame.close()

    def load_game(self):
        print("load")
        with open('savegame.txt', 'rb') as f:
            loadValues = pickle.load(f)
        difficulty = loadValues[0]
        events_manager = loadValues[1]
        player_data = loadValues[2]
        levels_data = loadValues[3]
        shops_data = loadValues[4]
        score_data = loadValues[5]
        print("--LOAD OBJECTS--")
        print("----------------")
        print(levels_data)
        print("----------------")
        print("---LOAD PLAYER--")
        print(difficulty)
        print(events_manager.history())
        print(player_data['char_name'])
        print(player_data['name'])
        pos = vec(player_data['x'],player_data['y'])
        print(pos)
        for item in player_data['inventory_namecond_list']:
            print (item[0])
        for item in player_data['active_slots_item_namecond_list']:
            print (item[0])
        print (player_data['quest_list'])
        self.shops_data = shops_data
        self.player_data = player_data
        self.loaded_events_manager = events_manager
        self.saved_levels_data = levels_data
        self.score_data = score_data
        print("LOAD DATA DESARIALISED")
        print("STARTING GAME with LOADED")
        if self.player_data['char_name'] == "Knight":
            self.new(self.knight_class,difficulty,True)
        if self.player_data['char_name'] == "Wizard":
            self.new(self.wizard_class,difficulty,True)
        if self.player_data['char_name'] == "Thief":
            self.new(self.thief_class,difficulty,True)

    def load_inventory_from_namecond_list(self, nc_list):
        ## TO UNPACK ITEMS FOR PLAYER INVENTORY
        self.itemgen = ItemGenerator(self, tileset_image,full_tileset_image)
        for tuple in nc_list:
            #if tuple[1]:
            item = self.itemgen.load_item_by_name(tuple[0], tuple[1])
            self.player.inventory.put_in_first_free_slot(item)
            #else:
            #item = self.itemgen.load_item_by_name(tuple[0], tuple[1])
            #self.player.inventory.put_in_first_free_slot(item)

    def new_player(self, name, class_selected):
        print("CREATING PLAYER...")
        self.name = name
        self.player = Player(self, name, class_selected)

    def load_player(self, player_data, class_selected):
        print ("### TWORZE PLAYERA")
        self.player = Player(self, player_data['name'], class_selected)
        print("###### POZYCJA")
        self.player.put_in_pos(player_data['pos_x'],player_data['pos_y'])
        print("###### INVENTARZ")
        self.player.inventory.remove_all()
        self.load_inventory_from_namecond_list(player_data['inventory_namecond_list'])
        self.player.load_active_slots_from_item_namecond_list(player_data['active_slots_item_namecond_list'],self.itemgen)
        print("###### ZASOBY i SKILLe")
        self.player.act_mana = player_data['act_mana']
        self.player.act_hp = player_data['act_hp']
        self.player.gold = player_data['gold']
        self.player.arrows = player_data['arrows']
        self.player.xp = player_data['xp']
        self.player.attribute_points = player_data['attribute_points']
        self.player.level = player_data['level']
        self.player.xp_step = 10 * self.player.level + ((self.player.level - 1) * 2 * self.player.level)
        self.player.base_strength = player_data['base_str']
        self.player.base_stamina = player_data['base_sta']
        self.player.base_intellect = player_data['base_int']
        self.player.base_wisdom = player_data['base_wis']
        self.player.base_stealth = player_data['base_ste']
        self.player.base_speed = player_data['base_spe']
        print("####### CZARY")
        spell_list = player_data['spell_list']
        for spell in spell_list:
            self.player.spell_book.add_spell_by_name(spell)
        print("####### QUESTY")
        quest_list = player_data['quest_list']
        self.player.quest_book.load_quests_by_name_list(quest_list)
        print("####### GAME SCORE and TIME")
        print (self.score_data[0])
        self.player.score_killed_enemies = self.score_data[0]
        self.player.score_swings = self.score_data[1]
        self.player.score_swing_enemy_hits = self.score_data[2]
        self.player.score_arrows = self.score_data[3]
        self.player.score_arrow_enemy_hits = self.score_data[4]
        self.player.score_spell_bullets = self.score_data[5]
        self.player.score_off_spell_damage = self.score_data[6]
        self.player.score_inflicted_damage = self.score_data[7]
        self.player.score_blocks = self.score_data[8]
        self.player.score_time_played = self.score_data[9]
        self.player.score_chest_opened = self.score_data[10]
        self.player.score_barrels_destroyed = self.score_data[11]
        ### UPDATING STATS!
        self.player.update_stats()
        self.update_game_enviroment()

    def new(self, class_selected, difficulty, loaded = False):
        self.game_accomplished = False
        #### LOADING LEVELS ####
        self.difficulty = difficulty
        print("LOADING LEVELS...")
        self.rem_objects = []
        self.levels = {}
        self.map_levels = {}
        self.level_01 = Level()
        self.map_level_01 = tilemap.TiledMap(path.join(map_folder, 'mapa1.tmx'))
        self.level_02 = Level()
        self.map_level_02 = tilemap.TiledMap(path.join(map_folder, 'mapa2.tmx'))
        self.level_03 = Level()
        self.map_level_03 = tilemap.TiledMap(path.join(map_folder, 'mapa3.tmx'))
        self.level_04 = Level()
        self.map_level_04 = tilemap.TiledMap(path.join(map_folder, 'mapa4.tmx'))
        self.level_05 = Level()
        self.map_level_05 = tilemap.TiledMap(path.join(map_folder, 'mapa5.tmx'))
        self.level_06 = Level()
        self.map_level_06 = tilemap.TiledMap(path.join(map_folder, 'mapa6.tmx'))
        self.level_07 = Level()
        self.map_level_07 = tilemap.TiledMap(path.join(map_folder, 'mapa7.tmx'))
        self.level_08 = Level()
        self.map_level_08 = tilemap.TiledMap(path.join(map_folder, 'mapa8.tmx'))
        self.level_09 = Level()
        self.map_level_09 = tilemap.TiledMap(path.join(map_folder, 'mapa9.tmx'))
        #####
        self.levels['level01'] = self.level_01
        self.levels['level02'] = self.level_02
        self.levels['level03'] = self.level_03
        self.levels['level04'] = self.level_04
        self.levels['level05'] = self.level_05
        self.levels['level06'] = self.level_06
        self.levels['level07'] = self.level_07
        self.levels['level08'] = self.level_08
        self.levels['level09'] = self.level_09
        #####
        self.map_levels['level01'] = self.map_level_01
        self.map_levels['level02'] = self.map_level_02
        self.map_levels['level03'] = self.map_level_03
        self.map_levels['level04'] = self.map_level_04
        self.map_levels['level05'] = self.map_level_05
        self.map_levels['level06'] = self.map_level_06
        self.map_levels['level07'] = self.map_level_07
        self.map_levels['level08'] = self.map_level_08
        self.map_levels['level09'] = self.map_level_09
        #### CREATE ##########################################
        ### SPRITE GROUPS NALEZACE DO GAME a nie DO LEVEL! ###
        ######################################################
        self.player_group = pygame.sprite.LayeredUpdates()
        self.small_items = pygame.sprite.LayeredUpdates()
        ######################
        ### IN GAME OBJECTS #
        #####################
        ### CREATE EFFECTS
        self.e_favourite_weapon = ActiveEffect("favourite weapon", e_fav_wea_ico, False, False)
        self.e_disliked_weapon = ActiveEffect("disliked weapon", e_dis_wea_ico, False, False)
        self.e_favourite_armor = ActiveEffect("favourite armor", e_fav_arm_ico, False, False)
        self.e_disliked_armor = ActiveEffect("disliked armor", e_dis_arm_ico, False, False)
        #####################
        ### CREATE PLAYER ###
        #####################
        if not loaded:
            self.new_player("Adventurer", class_selected)
        else:
            self.load_player(self.player_data, class_selected)
        ### CREATE EVENTS MANAGER
        if not loaded:
            self.events_manager = EventManager()
        else:
            self.events_manager = self.loaded_events_manager
        print ("INITIALIZING USER INTERFACE...")
        ### DIALOG BOX
        self.dialog_box = DialogBox(self)
        self.message_box  = MessageBox(self)
        self.q_box = QuestionBox(self)
        self.shop_dialog_box = ShopDialogBox(self)
        ### UI BUTTONS
        self.inv_use_button = RadioButton(rad_use_img, rad_use_h_img,
                                          INV_POS[0] + 140, INV_POS[1] + 80)
        self.inv_open_door_button = RadioButton(rad_open_img, rad_open_h_img,
                                                INV_POS[0] + 120, INV_POS[1] + 20)
        self.pause_button = RadioButton(rad_pause_img, rad_pause_h_img, INV_POS[0]+200, 680)
        #self.save_button = RadioButton(rad_but_img,rad_but_h_img,INV_POS[0]+280, 740)
        self.spell_book_button = RadioButton(sbb_img, sbb_h_img, INV_POS[0], 680)
        self.quest_book_button = RadioButton(qbb_img,qbb_h_img,INV_POS[0]+100, 680)
        self.cast_button = RadioButton(rad_cast_img, rad_cast_h_img, MAP_WIDTH / 2 - 72, MAP_HEIGHT - 96)
        #### AD BUTTONS
        self.str_ad_button = RadioButton(rad_but_img, rad_but_h_img,
                                         ST_POS[0] + 2, ST_POS[1] + 40)
        self.sta_ad_button = RadioButton(rad_but_img, rad_but_h_img,
                                         ST_POS[0] + 2, ST_POS[1] + 60)
        self.int_ad_button = RadioButton(rad_but_img, rad_but_h_img,
                                         ST_POS[0] + 2, ST_POS[1] + 80)
        self.wis_ad_button = RadioButton(rad_but_img, rad_but_h_img,
                                         ST_POS[0] + 2, ST_POS[1] + 100)
        self.spe_ad_button = RadioButton(rad_but_img, rad_but_h_img,
                                         ST_POS[0] + 2, ST_POS[1] + 120)
        self.ste_ad_button = RadioButton(rad_but_img, rad_but_h_img,
                                         ST_POS[0] + 2, ST_POS[1] + 140)
        ####
        self.all_buttons = [self.inv_use_button, self.inv_open_door_button,
                            self.str_ad_button, self.sta_ad_button, self.int_ad_button,
                            self.wis_ad_button, self.spe_ad_button, self.ste_ad_button,
                            self.spell_book_button, self.pause_button,
                            self.cast_button, self.quest_book_button]
        self.att_buttons = [self.str_ad_button, self.sta_ad_button, self.int_ad_button,
                            self.wis_ad_button, self.spe_ad_button, self.ste_ad_button]
        ####### START LEVEL
        print ("STARTING LEVEL...")
        self.levelgen = levels.LevelGen(self)
        if not loaded:
            self.levelgen.load_level_01(False)
            self.levelgen.load_level_02(False)
            self.levelgen.load_level_03(False)
            self.levelgen.load_level_04(False)
            self.levelgen.load_level_05(False)
            self.levelgen.load_level_06(False)
            self.levelgen.load_level_07(False)
            self.levelgen.load_level_08(False)
            self.levelgen.load_level_09(False)
        else:
            self.levelgen.load_level_01(self.saved_levels_data['level01'])
            self.levelgen.load_level_02(self.saved_levels_data['level02'])
            self.levelgen.load_level_03(self.saved_levels_data['level03'])
            self.levelgen.load_level_04(self.saved_levels_data['level04'])
            self.levelgen.load_level_05(self.saved_levels_data['level05'])
            self.levelgen.load_level_06(self.saved_levels_data['level06'])
            self.levelgen.load_level_07(self.saved_levels_data['level07'])
            self.levelgen.load_level_08(self.saved_levels_data['level08'])
            self.levelgen.load_level_09(self.saved_levels_data['level09'])
            self.levelgen.shop_gen.load_shops_data(self.shops_data)
        if not loaded:
            self.levelgen.go_to_level("level01", 2, 2)
        else:
            self.levelgen.go_to_level(self.player_data["act_lvl_name"], self.player_data["pos_x"], self.player_data["pos_y"])
            ### AKTUALIZUJE wyglad gracza:
            for slot in self.player.active_slots:
                if slot.item:
                    if isinstance(slot.item, Armor) or isinstance(slot.item, Weapon):
                        self.player_group.add(slot.item)
            self.player.update_stats()
            self.update_game_enviroment()
        print ("INITIALIZING CAMERA...")
        ##### CAMERA INIT
        self.camera = tilemap.Camera(self.map.width, self.map.height)
        self.draw_debug = False
        #### RUN
        self.run()
        #### GAME OVER
        self.game_over()

    def game_over(self):
        self.game_over_screen = True
        #########################################
        pygame.mixer.music.load(path.join(music_folder, 'Path to Lake Land.ogg'))
        pygame.mixer.music.play(loops=-1)
        ########################################
        self.overall_melle_hits = 0
        self.melle_accuracy = 0
        self.overall_arrow_hits = 0
        self.arrow_accuracy = 0
        self.overall_spell_hits = 0
        self.spell_accuracy = 0
        self.inflicted_damage = 0
        self.block_efficiency = 0
        self.time_played = int(self.player.score_time_played)
        self.killed_enemies = len(self.player.score_killed_enemies)
        if self.killed_enemies > 0:
            biggest_hp = 0
            most_powerful_enemy = False
            for enemy in self.player.score_killed_enemies:
                if enemy[1] > biggest_hp:
                    biggest_hp = enemy[1]
                    most_powerful_enemy = enemy[0]
            self.most_powerful_enemy = most_powerful_enemy
        else:
            self.most_powerful_enemy = False
        # MELLE
        if self.player.score_swings > 0:
            for hits in self.player.score_swing_enemy_hits:
                self.overall_melle_hits += hits
            self.melle_accuracy = len(self.player.score_swing_enemy_hits) / self.player.score_swings
            self.melle_accuracy = int(self.melle_accuracy * 100)
        else:
            self.melle_accuracy = 0
        ## RANGED
        if self.player.score_arrows > 0:
            for hits in self.player.score_arrow_enemy_hits:
                self.overall_arrow_hits += hits
            self.arrow_accuracy = len(self.player.score_arrow_enemy_hits) / self.player.score_arrows
            self.arrow_accuracy = int(self.arrow_accuracy * 100)
        else:
            self.arrow_accuracy = 0
        # MAGIC
        if self.player.score_spell_bullets > 0:
            for hits in self.player.score_off_spell_damage:
                self.overall_spell_hits += hits
            self.spell_accuracy = len(self.player.score_off_spell_damage) / self.player.score_spell_bullets
            self.spell_accuracy = int(self.spell_accuracy * 100)
        else:
            self.spell_accuracy = 0
        if self.player.score_inflicted_damage:
            for i in self.player.score_inflicted_damage:
                self.inflicted_damage += i
            self.block_efficiency = self.player.score_blocks / len(self.player.score_inflicted_damage)
            self.block_efficiency = int(self.block_efficiency * 100)
        self.points = (self.overall_spell_hits + self.overall_melle_hits + self.overall_arrow_hits) + (int(
            self.player.gold / 100)) + self.player.score_barrels_destroyed * 2 + self.player.score_chest_opened * 3 + self.player.score_blocks - self.inflicted_damage

        ########################
        while self.game_over_screen:
            self.dt = self.clock.tick(FPS) / 1000
            self.g_o_events()
            self.g_o_update()
            self.g_o_draw()

    def g_o_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.intro()

    def g_o_update(self):
        pass

    def g_o_draw(self):
        y_pos = 140
        x_pos = 100
        self.screen.fill(BGCOLOR)
        if self.game_accomplished:
            self.screen.blit(winner_img, (0, 0))
            self.big_write("CONGRATULATIONS!", (SCREEN_WIDTH / 2 - 120, 60))
            self.big_write("YOU HAVE ACCOMPLISHED THE GAME!", (SCREEN_WIDTH / 2 - 120, 100))
        else:
            self.screen.blit(game_over_img, (0, 0))
            self.big_write("GAME OVER", (SCREEN_WIDTH / 2 - 120, 60))
        self.big_write("Press Enter to go to Main Menu", (SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT - 100))
        self.big_write("Game time: " + str(self.time_played) + " sec.", (x_pos + 60, y_pos + 50))
        self.big_write("Gold: " + str(self.player.gold), (x_pos + 60, y_pos + 70))
        self.big_write("Killed enemies: " + str(self.killed_enemies), (x_pos + 60, y_pos + 90))
        if self.most_powerful_enemy:
            self.big_write("Most powerful enemy: " + self.most_powerful_enemy, (x_pos + 60, y_pos + 110))
        self.big_write("Melle damage: " + str(self.overall_melle_hits), (x_pos + 60, y_pos + 140))
        self.big_write("Melle accuracy: " + str(self.melle_accuracy) + "%", (x_pos + 60, y_pos + 160))
        self.big_write("Ranged damage: " + str(self.overall_arrow_hits), (x_pos + 60, y_pos + 190))
        self.big_write("Ranged accuracy: " + str(self.arrow_accuracy) + "%", (x_pos + 60, y_pos + 210))
        self.big_write("Magic damage: " + str(self.overall_spell_hits), (x_pos + 60, y_pos + 240))
        self.big_write("Magic accuracy: " + str(self.spell_accuracy) + "%", (x_pos + 60, y_pos + 260))
        self.big_write("Damage recieved: " + str(self.inflicted_damage), (x_pos + 60, y_pos + 290))
        self.big_write("Blocks: " + str(self.player.score_blocks), (x_pos + 60, y_pos + 310))
        self.big_write("Blocks efficiency: " + str(self.block_efficiency) + "%", (x_pos + 60, y_pos + 330))
        self.big_write("Chest opened: " + str(self.player.score_chest_opened), (x_pos + 60, y_pos + 360))
        self.big_write("Barrels destroyed: " + str(self.player.score_barrels_destroyed), (x_pos + 60, y_pos + 380))
        self.big_write("TOTAL POINTS :" + str(self.points), (x_pos + 60, y_pos + 420))
        self.big_write(str(self.clock.get_fps()), (0, 0))
        #### FLIP
        pygame.display.flip()

    def run(self):
        print ("STARTING GAME LOOP...")
        self.playing = True
        ##### FLAGI DO MECHANIKI GRY ############
        self.first_loop = False
        self.paused = False
        ##### FLAGI DO STANU GRY (TREASURE CHEST, SPELL BOOK, SHOP etc..
        self.ph_treasure_inv = False
        self.treasure_inv = False
        self.ph_spell_book = False
        self.ph_shop = False
        self.ph_buy_and_sell = False
        self.ph_repair = False
        self.active_shop = False
        self.ph_quest_book = False
        self.dialog_in_progress = False
        self.message_shown = False
        self.qbox_shown = False
        ##### FLAGI DO OBSLUGI INVENTARZA #######
        self.item_picked = False
        self.toggle_clean_item_picked = False
        self.toggle_open_chest = False
        self.toggle_open_shop = False
        ##### TEXT BOX ###########
        self.line1 = "1"
        self.line2 = "2"
        self.line3 = "3"
        self.line4 = "4"
        self.line5 = "5"
        self.txts = [self.line1, self.line2, self.line3, self.line4, self.line5]
        #########################################
        ### MUSIC
        pygame.mixer.music.load(path.join(music_folder, 'Winds Of Stories.ogg'))
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.4)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
            #### PO TO ABY SIE NIE UPDATEOWALO ZANIM ZE ZALADUJE GRY
            if not self.first_loop:
                # print ("UNLOCKING UPDATES at:")
                # print (str(pygame.time.get_ticks()))
                self.unlock_updates = True
                self.first_loop = True

    def quit(self):
        pygame.quit()
        sys.exit()

    def ad_buttons_check(self, mouse_pos):
        if self.str_ad_button.check_if_clicked(mouse_pos):
            self.player.base_strength += 1
            self.player.attribute_points -= 1
            self.player.update_stats()
        if self.sta_ad_button.check_if_clicked(mouse_pos):
            self.player.base_stamina += 1
            self.player.attribute_points -= 1
            self.player.update_stats()
        if self.int_ad_button.check_if_clicked(mouse_pos):
            self.player.base_intellect += 1
            self.player.attribute_points -= 1
            self.player.update_stats()
        if self.wis_ad_button.check_if_clicked(mouse_pos):
            self.player.base_wisdom += 1
            self.player.attribute_points -= 1
            self.player.update_stats()
        if self.spe_ad_button.check_if_clicked(mouse_pos):
            self.player.base_speed += 1
            self.player.attribute_points -= 1
            self.player.update_stats()
        if self.ste_ad_button.check_if_clicked(mouse_pos):
            self.player.base_stealth += 1
            self.player.attribute_points -= 1
            self.player.update_stats()

    def back_to_game_and_unpause(self):
        self.ph_spell_book = False
        self.ph_quest_book = False
        self.ph_treasure_inv = False
        self.ph_shop = False
        self.ph_buy_and_sell = False
        self.ph_repair = False
        self.active_shop = False
        self.paused = False
        self.update_ui_buttons()
        self.player.update_stats()

    def print_status(self):
        print ("PHASE STATUS:")
        print(f'self.dialog_in_progress = {self.dialog_in_progress}')
        print(f'self.message_shown = {self.message_shown}')
        print(f'self.ph_spell_book = {self.ph_spell_book}')
        print(f'self.ph_quest_book = {self.ph_quest_book}')
        print(f'self.ph_treasure_inv = {self.ph_treasure_inv}')
        print(f'self.ph_shop = {self.ph_shop}')
        print(f'self.ph_buy_and_sell = {self.ph_buy_and_sell}')
        print(f'self.ph_repair = {self.ph_repair}')

        print(f'self.ph_quest_book = {self.ph_quest_book}')
        print(f'self.active_shop = {self.active_shop}')
        if self.active_shop:
            print(f'ACTIVE SHOP LOCAL PH_REPAIR: {self.active_shop.local_ph_repair}')
        print(f'self.paused = {self.paused}')
        print(" FLAGI DO OBSLUGI INVENTARZA ")
        print(f'self.item_picked = {self.item_picked}')
        print(f'self.toggle_clean_item_picked = {self.toggle_clean_item_picked}')
        print("------------- END --------------")

    def events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYUP:
                if self.player.wait_key_pressed:
                    self.player.wait_key_pressed = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                if event.key == pygame.K_p:
                    if self.paused:
                        self.paused = False
                        self.ph_spell_book = False
                        self.ph_treasure_inv = False
                        self.treasure_inv = False
                    else:
                        self.paused = True
                if event.key == pygame.K_F3:
                    self.print_status()
                if event.key == pygame.K_F2:
                    print (f' Events at: {self.player.score_time_played}s of game played')
                    for game_event in self.events_manager.history():
                        print(game_event)
                if event.key == pygame.K_F1:
                    self.draw_debug = not self.draw_debug
                if event.key == pygame.K_c:
                    if self.player.active_spell:
                        self.player.active_spell = False
                        self.player.update_stats()
                    else:
                        self.player.active_spell = self.player.selected_spell
                        self.player.update_stats()
                if event.key == pygame.K_BACKSPACE:
                    if self.item_picked:
                        Item_to_take(self,self.player.pos.x,self.player.pos.y,self.item_picked)
                        self.item_picked = False
                if event.key == pygame.K_e:
                    ####### USE TELEPORT ########
                    teleport_hits = pygame.sprite.spritecollide(self.player, self.act_lvl.teleports, False)
                    for tele_hit in teleport_hits:
                        self.q_box.ask_travel(tele_hit)
                        #self.back_to_game_and_unpause()
                    ####### GATHER COLLECT SPRITE
                    sprites_to_collect = pygame.sprite.spritecollide(self.player, self.act_lvl.collecting_sprites,False,collide_double_hit_rect)
                    for sprite in sprites_to_collect:
                        sprite.gather()
                    ####### WEJDZ DO SKLEPU
                    if not self.ph_shop and not self.paused:
                        shop_doors = pygame.sprite.spritecollide(self.player, self.act_lvl.shops,False,collide_hit_rect)
                        for shop_door in shop_doors:
                            self.ph_shop = True
                            self.active_shop = shop_door.shop
                            self.shop_dialog_box.start_conversation(shop_door.shop)
                            print ("ENTERING SHOP: " + shop_door.shop.name)
                    ####### ROZMAWIAJ Z NPC
                    if not self.dialog_in_progress and not self.paused:
                        npcs_to_talk = pygame.sprite.spritecollide(self.player,self.act_lvl.npcs,False,collide_double_hit_rect)
                        for npc in npcs_to_talk:
                            #print ("TALK")
                            self.paused = True
                            if npc.sound:
                                pygame.mixer.Sound.play(npc.sound)
                            self.dialog_in_progress = True
                            self.dialog_box.start_conversation(npc)
                    ######## PODNIES ZLOTO
                    gold_to_pick = pygame.sprite.spritecollide(self.player, self.act_lvl.gold_to_pick, False)
                    for gold in gold_to_pick:
                        pygame.mixer.Sound.play(coin_snd)
                        self.player.gold += gold.gold
                        gold.kill()
                    ######## PODNIES STRZALY
                    arrow_to_pick = pygame.sprite.spritecollide(self.player, self.act_lvl.arrows_to_pick, False)
                    for arrow in arrow_to_pick:
                        pygame.mixer.Sound.play(bow_snd)
                        self.player.arrows += arrow.number
                        arrow.kill()
                    ######## PODNIES PRZEDMIOT
                    items_to_pick = pygame.sprite.spritecollide(self.player, self.act_lvl.items_to_pick,
                                                                False, collide_double_hit_rect)
                    for item in items_to_pick:
                        ### JEZELI UKRYTY PRZEDMIOT:
                        if isinstance(item,HiddenItem_to_take):
                            item.unhide()
                            item.kill()
                        elif isinstance(item,HiddenGold_to_take):
                            item.unhide()
                            item.kill()
                        ### JEZELI ZWYKLY PRZEDMIOT:
                        else:
                            if self.player.inventory.put_in_first_free_slot(item.item):
                                item.kill()
                                pygame.mixer.Sound.play(pick_item_snd)
                    ######## OTWORZ SKRZYNIE
                    chest_to_open = pygame.sprite.spritecollide(self.player, self.act_lvl.chest_to_open, False,
                                                                collide_double_hit_rect)
                    for chest in chest_to_open:
                        if chest.try_unlock():
                            treasure_inv = chest.open()
                            if treasure_inv.return_no_items() > 0:
                                self.paused = True
                                self.ph_treasure_inv = True
                                self.treasure_inv = treasure_inv
                                # print("OPENING INV MODE")
                            else:
                                self.ph_treasure_inv = False
                                self.treasure_inv = False
                                # print("PUSTO!")
                    ######## ZAMYKANIE OTWARTEJ SKRZYNI klawiszem E
                    if self.toggle_open_chest:
                        self.paused = False
                        self.ph_treasure_inv = False
                        self.treasure_inv = False
                        self.toggle_open_chest = False
                    ######## ZAMYKANIE SKLEPU klawiszem E
                    #if self.toggle_open_shop:
                    #    self.paused = False
                    #    self.ph_shop = False
                    #    self.toggle_open_shop = False
            ##############################################################
            ######## EVENTY MOUSE CONTROL ################################
            ##############################################################
            # # # # # # ############################################ # # #
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.update_ui_buttons()
                    mouse_pos = pygame.mouse.get_pos()
                    dial_pos_x = DIAL_BOX_POS[0]
                    dial_pos_y = DIAL_BOX_POS[1]
                    ### POZYCJONOWANIE Wskaznika myszy dla sklepu
                    shop_mouse_pos = (mouse_pos[0] - dial_pos_x, mouse_pos[1] - dial_pos_y)
                    ### PAUZA
                    if not self.dialog_in_progress or not self.ph_shop:
                        if self.pause_button.check_if_clicked(mouse_pos):
                            if self.paused:
                                self.back_to_game_and_unpause()
                            else:
                                self.paused = True
                        ##### WHILE DEVELOPING SAVE GAME IN GAME
                        #if self.save_button.check_if_clicked(mouse_pos):
                            #self.save_game()
                    ### PRZYCISK QUEST BOOK
                    if not self.dialog_in_progress or not self.ph_shop:
                        if self.quest_book_button.check_if_highlight(mouse_pos):
                            if not self.ph_quest_book:
                                if not self.paused:
                                    self.paused = True
                                    self.ph_quest_book = True
                                else:
                                    self.ph_quest_book = True
                                    self.ph_spell_book = False
                            else:
                                self.back_to_game_and_unpause()
                    ### PRZYCISK SPELL BOOK
                    if not self.dialog_in_progress or not self.ph_shop:
                        if self.spell_book_button.check_if_clicked(mouse_pos):
                            if not self.ph_spell_book:
                                if not self.paused:
                                    self.paused = True
                                    self.ph_spell_book = True
                                else:
                                    self.ph_spell_book = True
                                    self.ph_quest_book = False
                            else:
                                self.back_to_game_and_unpause()
                    ### ADD ATRIBUTES
                    self.ad_buttons_check(mouse_pos)
                    ### PICK UP AND DROP ITEMS on INV
                    if self.item_picked:
                        ##################################
                        # GDY MAM PRZEDMIOT PODNIESIONY  #
                        ##################################
                        # print(f'{self.item_picked.name} owner = {self.item_picked.owner}')
                        # 5. ODKLADAM NA REPAIR SLOT:
                        if self.ph_repair:
                            if self.active_shop.act_inventory.check_if_clicked(shop_mouse_pos):
                                #print ("KLIK REPAIR")
                                if isinstance(self.item_picked,sprites.Armor) or isinstance(self.item_picked,sprites.Weapon):
                                    put_item_success_bool = self.active_shop.act_inventory.put_item_to_inv(shop_mouse_pos,
                                                                                                           self.item_picked)
                                    if put_item_success_bool:
                                        self.toggle_clean_item_picked = True
                        # 1. ODKLADAM DO PLECAKA
                        if self.player.inventory.check_if_clicked(mouse_pos):
                            ## PRZEDMIOTY ZE SKLEPU:
                            if self.item_picked.owner == "shop":
                                if self.player.check_gold(self.item_picked,self.active_shop):
                                    put_item_success_bool = self.player.inventory.put_item_to_inv(mouse_pos,
                                                                                              self.item_picked)
                                    if put_item_success_bool:
                                        #print ("KUPUJE!")
                                        self.active_shop.sell_to_player(self.item_picked)
                                        self.toggle_clean_item_picked = True
                                else:
                                    pygame.mixer.Sound.play(empty_spell_snd)
                            ## PRZEDMIOTY WLASNE LUB NICZYJE:
                            else:
                                put_item_success_bool = self.player.inventory.put_item_to_inv(mouse_pos,
                                                                                          self.item_picked)
                                if put_item_success_bool:  # GDY UDALO SIE ODLOZYC WTEDY OCZYSZCzAM ITEM PICKED
                                    self.toggle_clean_item_picked = True
                        # 2. 0DKLADAM NA AKTYWNY SLOT
                        if not self.ph_buy_and_sell:
                            #print ("PROBUJE ODLOZYC PRZEDMIOT NA AKTYWNY SLOT")
                            for slot in self.player.active_slots:
                                if slot.check_itemslot_to_item_corr(mouse_pos, self.item_picked):
                                    if slot.occ == False:
                                        #print("ODKLADAM PRZEDMIOT NA AKTYWNY SLOT")
                                        self.toggle_clean_item_picked = True
                                    ### POLOZ PRZEDMIOT NA AKTYWNYM SLOCIE i UPDATE STATISTICS
                                    pygame.mixer.Sound.play(wear_item_snd)
                                    if slot.put_item(self.item_picked):
                                        ### TYLKO BRON LUB ZBROJE SA SPRITEAMI DO WYSWIELTENIA NA LUDZIKU
                                        if isinstance(self.item_picked, Armor) or isinstance(self.item_picked, Weapon):
                                            self.player_group.add(self.item_picked)
                                    self.player.update_stats()
                        # 3. ODKLADAM NA TREASURE
                        if self.ph_treasure_inv:
                            if self.treasure_inv.check_if_clicked(mouse_pos):
                                #print ("ODKLADAM NA SKRZYNIE")
                                put_item_success_bool = self.treasure_inv.put_item_to_inv(mouse_pos,
                                                                                          self.item_picked)
                                if put_item_success_bool:  # GDY UDALO SIE ODLOZYC WTEDY OCZYSZCzAM ITEM PICKED
                                    self.toggle_clean_item_picked = True
                        # 4. ODKLADAM NA POLKE SKLEPU
                        if self.ph_buy_and_sell:
                            if self.active_shop.act_inventory.check_if_clicked(shop_mouse_pos):
                                ## PRZEDMIOTY ZE SKLEPU
                                if self.item_picked.owner == "shop":
                                    put_item_success_bool = self.active_shop.act_inventory.put_item_to_inv(
                                        shop_mouse_pos, self.item_picked)
                                    if put_item_success_bool:  # GDY UDALO SIE ODLOZYC WTEDY OCZYSZCzAM ITEM PICKED
                                        self.toggle_clean_item_picked = True
                                ## SPRZEDAJE
                                else:
                                    #print("SELL ITEM")
                                    if self.active_shop.check_gold(self.item_picked):
                                        put_item_success_bool = self.active_shop.act_inventory.put_item_to_inv(
                                            shop_mouse_pos, self.item_picked)
                                        if put_item_success_bool:
                                            #print("SPRZEDAJE!")
                                            self.active_shop.buy_from_player(self.item_picked)
                                            self.toggle_clean_item_picked = True
                        ## PRZEDMIOTY DO UZYCIA
                        ## UZYCIE ELIKSIROW
                        if self.inv_use_button.check_if_clicked(mouse_pos):
                            if self.item_picked.try_use():
                                self.item_picked.use()
                                self.item_picked = False
                                self.player.update_stats()
                            else:
                                pygame.mixer.Sound.play(empty_spell_snd)
                        ## UZYCIE KLUCzA
                        if not self.ph_treasure_inv:
                            if self.inv_open_door_button.check_if_clicked(mouse_pos):
                                self.item_picked.use()
                    if not self.item_picked:
                        ########################################
                        # GDY NIE MAM PRZEDMIOTU PODNIESIONEGO #
                        ########################################
                        # 1. PODNIES ITEM Z INV
                        if self.player.inventory.check_if_clicked(mouse_pos):
                            #print ("KLIKAM PLAYER INVENTORY - podnosze przedmiot")
                            self.item_picked = self.player.inventory.pick_item_from_inv(mouse_pos)
                        # 2. PODNIES ITEM Z SHOP
                        if self.ph_buy_and_sell:
                            if self.active_shop.act_inventory.check_if_clicked(shop_mouse_pos):
                                #print ("KLIKAM SHOP INVENTORY - podnosze przedmiot")
                                self.item_picked = self.active_shop.act_inventory.pick_item_from_inv(shop_mouse_pos)
                        # 2. PODNIES ITEM Z TREASURE INV
                        if self.ph_treasure_inv:
                            if self.treasure_inv.check_if_clicked(mouse_pos):
                                #print("### PODNOSZE ITEM Z TREASURE INV ###")
                                self.item_picked = self.treasure_inv.pick_item_from_inv(mouse_pos)
                                ## wyjątek dla złorych monet
                                if self.item_picked:
                                    if self.item_picked.name == "Gold":
                                        pygame.mixer.Sound.play(coin_snd)
                                        self.player.gold += self.item_picked.gold
                                        self.toggle_clean_item_picked = True
                                    elif self.item_picked.name == "Arrows":
                                        pygame.mixer.Sound.play(bow_snd)
                                        self.player.arrows += self.item_picked.number
                                        self.toggle_clean_item_picked = True
                        # 3. PODNIES ITEM Z AKTYWNYCH SLOTOW
                        for slot in self.player.active_slots:
                            if slot.check_if_clicked(mouse_pos):
                                if slot.item:
                                    #print("### PODNIES PRZEDMIOT Z AKTYWNEGO SLOTU i UPDATE STATYSTYK")
                                    self.player_group.remove(slot.item)
                                    self.item_picked = slot.pick_item()
                                    self.player.update_stats()
                        # 4. REPAIR:
                        if self.ph_repair:
                            if self.active_shop.act_inventory.check_if_clicked(shop_mouse_pos):
                                #print ("REPERUJE PRZEDMIOT")
                                self.item_picked = self.active_shop.act_inventory.pick_item_from_inv(shop_mouse_pos)
                    ############################
                    # UI BUTTONS HANDLONG ######
                    ############################
                    # 1. ZAZNACZ lub ODZNACZ CZAR:
                    if self.ph_spell_book:
                        self.player.spell_book.check_page_buttons(mouse_pos)
                        ## Zaznaczm tylko gdy NIE naciskam guziku cast i spellbook (zeby nie odhaczac bez sensu
                        if not self.spell_book_button.check_if_clicked(mouse_pos) and not self.cast_button.check_if_clicked_even_inactive(mouse_pos):
                            # print ("zaznaczam nowe wskazanie")
                            self.player.active_spell = self.player.spell_book.check_spell(mouse_pos)
                            self.player.selected_spell = self.player.active_spell
                            if self.player.active_spell:
                                if self.player.active_spell.min_int > self.player.intellect:
                                    self.player.active_spell = False
                                    self.player.selected_spell = False
                            self.player.update_stats()
                            # 1a. CZAR DEFENSYWNY
                        if self.cast_button.check_if_clicked(mouse_pos):
                            self.player.active_spell.cast(self.player)
                    # 2. PRZYCISKI DIALOG BOX
                    if self.dialog_in_progress:
                        self.dialog_box.check_buttons(mouse_pos)
                    # 3. PRZYCISKI SHOP DIALOG BOX
                    if self.ph_shop:
                        self.shop_dialog_box.check_buttons(mouse_pos)
                    # 4. PRZYCKISK EXIT SHOP:
                    if self.ph_buy_and_sell:
                        self.active_shop.check_exit_button(mouse_pos)
                    # 5. PRZYCISK REPAIR
                    if self.ph_repair:
                        self.active_shop.check_repair_button(shop_mouse_pos)
                        self.active_shop.check_exit_button(mouse_pos)
                    # 6. PRZYCISKI QUEST BOOK
                    if self.ph_quest_book:
                        self.player.quest_book.check_page_buttons(mouse_pos)
                    # 7. PRZYCISK OK MESSAGE BOX
                    if self.message_shown:
                        self.message_box.check_button(mouse_pos)
                    # 8. PRZYCISKI QBOX
                    if self.qbox_shown:
                        self.q_box.check_button(mouse_pos)

    def get_act_ph(self):
        if self.ph_shop:
            return "ph_shop"
        elif self.ph_buy_and_sell:
            return "ph_buy_and_sell"
        elif self.ph_treasure_inv:
            return "ph_treasure_inv"
        elif self.ph_repair:
            return "ph_repair"
        elif self.dialog_in_progress:
            return "dialog_in_progress"
        elif self.message_shown:
            return "message_shown"
        elif self.qbox_shown:
            return "qbox_shown"
        else:
            print("NOT RECOGNIZED GET ACTUAL PHASE")
            return False

    def update_ui_buttons(self):
        self.quest_book_button.activate()
        self.spell_book_button.activate()
        self.pause_button.activate()
        if self.ph_repair or self.ph_buy_and_sell or self.ph_shop or self.dialog_in_progress or self.message_shown or self.qbox_shown:
            self.quest_book_button.deactivate()
            self.spell_book_button.deactivate()
            self.pause_button.deactivate()

    def update_game_enviroment(self):
        ### REMOVING rem_objects
        for rem_obj in self.rem_objects:
            if rem_obj.check_remove_condition():
                print ("Removing sprite")
                rem_obj.kill()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        #### CZYSZCZE TOGGLE OPEN CHEST
        if self.paused and self.ph_treasure_inv:
            self.toggle_open_chest = True
        else:
            self.toggle_open_chest = False
        #### CZYSZCZE TOGGLE OPEN SHOP
        ## TODO jezeli chce wychodzi ze sklepu literą E
        #### CZYSZCZE ITEM PICKED ####
        if self.toggle_clean_item_picked:
            self.item_picked = False
            self.toggle_clean_item_picked = False
        #### HIGHLIGHT BUTTONS #####
        for button in self.all_buttons:
            button.check_if_highlight(mouse_pos)
        #### HIGLIGHT NEXT PAGE BUTTONS ON SPELL BOOK ###
        if self.ph_spell_book:
            self.player.spell_book.update_buttons(mouse_pos)
        if self.ph_quest_book:
            self.player.quest_book.update_buttons(mouse_pos)
        #### HIGHLIGHT CLOSE SHOP BUTTON
        if self.ph_buy_and_sell or self.ph_repair:
            self.active_shop.update(mouse_pos)
        #### HIGHLIGHT QBOX BUTTONS
        if self.qbox_shown:
            self.q_box.update(mouse_pos)
        ### ACTIVATE ADD BUTTONS ####
        if self.player.attribute_points > 0:
            for button in self.att_buttons:
                button.activate()
        else:
            for button in self.att_buttons:
                button.deactivate()
        #### ACTIVATE CAST BUTTON:
        if self.player.active_spell:
            if self.player.active_spell.type == "defensive":
                self.cast_button.activate()
            else:
                self.cast_button.deactivate()
        else:
            self.cast_button.deactivate()
        #### DIALOG BUTTONS ####
        if self.dialog_in_progress:
            self.dialog_box.update(mouse_pos)
        #### SHOP DIALOG BUTTONS @@@
        if self.ph_shop:
            self.shop_dialog_box.update(mouse_pos)
        #### MESSAGE BOX BUTTON
        if self.message_shown:
            self.message_box.update(mouse_pos)
        #### ACTIVATE INV_USE_BUTTON ####
        if self.item_picked:
            if self.item_picked.type == "potion" or self.item_picked.type == "book":
                self.inv_use_button.activate()
            else:
                self.inv_use_button.deactivate()
        else:
            self.inv_use_button.deactivate()
        #### ACTIVATE OPEN_DOOR_BUTTON ###
        if self.item_picked:
            if self.item_picked.type == "key":
                if self.item_picked.update():
                    self.inv_open_door_button.activate()
                else:
                    self.inv_open_door_button.deactivate()
            else:
                self.inv_open_door_button.deactivate()
        else:
            self.inv_open_door_button.deactivate()
        if not self.paused:
            if self.unlock_updates:
                ###########################
                ####### UPDATE GRY!!! #####
                ###########################
                self.unpaused_dt = self.clock.get_rawtime() / 1000
                self.player.score_time_played += self.unpaused_dt
                # print (self.player.score_time_played)
                self.player.active_effects_lib.update_effects()
                self.player.update()
                self.act_lvl.all_sprites.update()
                self.act_lvl.melle_swing.update()
                self.camera.update(self.player)
                self.mob_attack()
                self.player_melle_attack()
                self.player_ranged_attack()

    def mob_attack(self):
        ### UDERZENIE PRZEZ PRZECIWNIKA ###
        hits = pygame.sprite.spritecollide(self.player, self.act_lvl.mobs, False, collide_hit_rect)
        for hit in hits:
            if not self.player.check_block():
                #### NIE MA BLOKU #####
                Hit_Splash(self, self.player.pos)
                self.player.armor_breakage()
                hit_damage_after_red = math.ceil(hit.damage * (1 - (self.player.hit_reduction / 100)))
                txt = (hit.name + " hits wih strength: " + str(hit.damage) + ". Inflicted damage: " + str(
                    hit_damage_after_red))
                self.put_txt(txt)
                self.player.act_hp -= hit_damage_after_red
                self.player.score_inflicted_damage.append(int(hit_damage_after_red))
                ### PO UDERZENIU PRZEZ PRZECIWNIKA PREDKOSC = 0 i odsuam o 10
                hit.last_hit_moment = (int(self.player.score_time_played * 1000))
                hit.vel = vec(0, 0)
                # hit.acc = vec(0,0)
                rot = (hit.pos - self.player.pos).angle_to(vec(1, 0))
                hit.pos += vec(10, 0).rotate(-rot)
                ### SPRAWDZENIE CZY KONIEC GRY
                self.player.check_live()
            else:
                #### BLOCK ######
                pygame.mixer.Sound.play(block_snd)
                self.player.armor_breakage()
                self.player.score_blocks += 1
                txt = (self.player.name + "blocks!")
                self.put_txt(txt)
                ### PO UDERZENIU PRZEZ PRZECIWNIKA PREDKOSC = 0 i odsuam o 15 i nadaje wsteczna predkosc
                hit.last_hit_moment = (int(self.player.score_time_played * 1000))
                # hit.vel = vec(0, 0)
                rot = (hit.pos - self.player.pos).angle_to(vec(1, 0))
                hit.vel = vec(25, 0).rotate(-rot)
                hit.pos += vec(15, 0).rotate(-rot)
        if hits:
            self.player.pos += vec(10, 0).rotate(-hits[0].rot)

    def player_melle_attack(self):
        ### UDERZENIE W PRZECIWNIKA ### PREDKOSC = 0, odrzucam o 5
        hits = pygame.sprite.groupcollide(self.act_lvl.mobs, self.act_lvl.melle_swing, False, True)
        for mob in hits:
            pygame.mixer.Sound.play(smash_snd)
            Mob_Hit_Splash(self, mob.pos)
            self.player.weapon_breakage()
            txt = str("Melee hit. " + self.player.name + " inflicted " + (str(self.player.hit_dmg)) + " damage.")
            self.put_txt(txt)
            self.player.score_swing_enemy_hits.append(int(self.player.hit_dmg))
            mob.hp -= self.player.hit_dmg
            mob.damaged = True
            mob.damage_alpha = chain(DAMAGE_ALPHA_LIST * 2)
            mob.last_hit_moment = (int(self.player.score_time_played * 1000))
            mob.vel = vec(0, 0)
            if not mob.frozen:
                rot = (self.player.pos - mob.pos).angle_to(vec(-1, 0))
                mob.pos += vec(5, 0).rotate(-rot)
                # hit.vel = hit.vel.rotate(180)

    def player_ranged_attack(self):
        ### STRZALY Z DYSTANSU
        ### ZWiekszaja attention
        arrow_hits = pygame.sprite.groupcollide(self.act_lvl.mobs, self.act_lvl.arrows, False, True)
        for mob in arrow_hits:
            # print (arrow_hits[mob])
            pygame.mixer.Sound.play(smash_snd)
            Mob_Hit_Splash(self, mob.pos)
            for arrow in arrow_hits[mob]:
                if self.player.attack_type_flag == "magic":
                    txt = str("Magic attack. " + self.player.name + " inflicted: " + (str(arrow.damage)) + " damage.")
                    self.put_txt(txt)
                    self.player.score_off_spell_damage.append(int(arrow.damage))
                    mob.attention += 48
                    mob.hp -= arrow.damage
                    if self.player.active_spell.blow_effect:
                        Blow_Spell(self, arrow.pos, arrow.spell.blow_anim_img,
                                   arrow.spell.blow_radius_sizer,
                                   arrow.spell.blow_damage, arrow.spell.blow_duration)
                    if self.player.active_spell.freeze_effect:
                        mob.frozen = self.player.active_spell.freeze_effect
                    mob.damaged = True
                    mob.damage_alpha = chain(DAMAGE_ALPHA_LIST * 2)
                    mob.last_hit_moment = (int(self.player.score_time_played * 1000))
                    mob.vel = vec(0, 0)
                    rot = (self.player.pos - mob.pos).angle_to(vec(-1, 0))
                    mob.pos += vec(5, 0).rotate(-rot)
                elif self.player.attack_type_flag == "ranged":
                    txt = f'Ranged hit. {self.player.name} inflicted  {int(self.player.arrow_damage)} damage.'
                    self.put_txt(txt)
                    self.player.score_arrow_enemy_hits.append(int(self.player.arrow_damage))
                    mob.attention += 48
                    mob.hp -= self.player.arrow_damage
                    mob.damaged = True
                    mob.damage_alpha = chain(DAMAGE_ALPHA_LIST * 2)
                    mob.last_hit_moment = (int(self.player.score_time_played * 1000))
                    mob.vel = vec(0, 0)
                    rot = (self.player.pos - mob.pos).angle_to(vec(-1, 0))
                    mob.pos += vec(5, 0).rotate(-rot)
                    # hit.vel = hit.vel.rotate(180)

    def draw_weapon_picked_info(self, item):
        self.write(("DAMAGE: " + str(round(item.damage))), (INV_POS[0] + 20, INV_POS[1] + 50))
        self.screen.blit(item.breakage_surf, (INV_POS[0] + 180, INV_POS[1] + 20))
        self.write(("Cost: " + str(item.cost)), (INV_POS[0] + 20, INV_POS[1] + 70))
        self.screen.blit(gold_coin, (INV_POS[0] + 80, INV_POS[1] + 75))
        hit_rate = (1000 / item.hit_rate)
        hit_rate = str(hit_rate)
        hit_rate = hit_rate[:3]
        self.write(("Hit rate ratio: " + hit_rate + "/sec"), (INV_POS[0] + 20, INV_POS[1] + 90))
        if item.hit_radius:
            self.write(("Hit radius: " + item.hit_radius), (INV_POS[0] + 20, INV_POS[1] + 110))
        self.draw_item_special_abilities(item)

    def draw_armor_picked_info(self, item):
        self.write(("ARMOR: " + str(round(item.armor))), (INV_POS[0] + 20, INV_POS[1] + 50))
        self.screen.blit(item.breakage_surf, (INV_POS[0] + 180, INV_POS[1] + 20))
        self.write(("Cost: " + str(item.cost)), (INV_POS[0] + 20, INV_POS[1] + 70))
        self.screen.blit(gold_coin, (INV_POS[0] + 80, INV_POS[1] + 75))
        self.write(("Hit rate ratio:" + str(item.hit_rate_mod)), (INV_POS[0] + 20, INV_POS[1] + 90))
        self.draw_item_special_abilities(item)

    def draw_ring_picked_info(self, item):
        self.write(("Cost: " + str(item.cost)), (INV_POS[0] + 20, INV_POS[1] + 50))
        self.screen.blit(gold_coin, (INV_POS[0] + 80, INV_POS[1] + 55))
        self.draw_ring_special_abilities(item)
        self.draw_item_special_abilities(item)

    def draw_item_special_abilities(self, item):
        l_o_t = 0
        if item.str_mod:
            self.write(("Strength +" + str(item.str_mod)), (INV_POS[0] + 120, INV_POS[1] + 45 + (20 * l_o_t)))
            l_o_t += 1
        if item.sta_mod:
            self.write(("Stamina +" + str(item.sta_mod)), (INV_POS[0] + 120, INV_POS[1] + 45 + (20 * l_o_t)))
            l_o_t += 1
        if item.int_mod:
            self.write(("Intellect +" + str(item.int_mod)), (INV_POS[0] + 120, INV_POS[1] + 45 + (20 * l_o_t)))
            l_o_t += 1
        if item.wis_mod:
            self.write(("Wisdom +" + str(item.wis_mod)), (INV_POS[0] + 120, INV_POS[1] + 45 + (20 * l_o_t)))
            l_o_t += 1
        if item.speed_mod:
            self.write(("Speed +" + str(item.speed_mod)), (INV_POS[0] + 120, INV_POS[1] + 45 + (20 * l_o_t)))
            l_o_t += 1
        if item.ste_mod:
            self.write(("Stealth +" + str(item.ste_mod)), (INV_POS[0] + 120, INV_POS[1] + 45 + (20 * l_o_t)))
            l_o_t += 1

    def draw_ring_special_abilities(self, item):
        l_o_t = 0
        hit_rate_bonus = (1 - item.hit_rate_mod) * 100
        hit_rate_bonus = str(hit_rate_bonus)[:3]
        if item.armor_mod > 0:
            self.write(("Armor +" + str(item.armor_mod)), (INV_POS[0] + 20, INV_POS[1] + 70 + (20 * l_o_t)))
            l_o_t += 1
        if item.damage_mod > 0:
            self.write(("Damage +" + str(item.damage_mod)), (INV_POS[0] + 20, INV_POS[1] + 70 + (20 * l_o_t)))
            l_o_t += 1
        if item.arrow_damage_mod > 0:
            self.write(("Ranged dmg +" + str(item.arrow_damage_mod)), (INV_POS[0] + 20, INV_POS[1] + 70 + (20 * l_o_t)))
            l_o_t += 1
        if item.hit_rate_mod < 1:
            self.write(("Hit rate bonus:" + str(hit_rate_bonus) + "%"),
                       (INV_POS[0] + 20, INV_POS[1] + 70 + (20 * l_o_t)))
            l_o_t += 1

    def draw_inventory(self):
        self.player.inventory.show_inv(self.screen, INV_POS[0] + 30, INV_POS[1] + INV_HEIGHT - 170)
        if self.item_picked:
            self.screen.blit(slot_img, (INV_POS[0] + 20, INV_POS[1] + 15))
            self.screen.blit(self.item_picked.b_image, (INV_POS[0] + 20, INV_POS[1] + 15))
            self.write(self.item_picked.name, (INV_POS[0] + 60, INV_POS[1] + 20))
            if self.item_picked.type == "weapon":
                self.draw_weapon_picked_info(self.item_picked)
            if self.item_picked.type == "armor":
                self.draw_armor_picked_info(self.item_picked)
            if self.item_picked.type == "shield":
                self.draw_armor_picked_info(self.item_picked)
            if self.item_picked.type == "helmet":
                self.draw_armor_picked_info(self.item_picked)
            if self.item_picked.type == "boots":
                self.draw_armor_picked_info(self.item_picked)
            if self.item_picked.type == "potion":
                self.write(("Type: " + str(self.item_picked.potion_type)), (INV_POS[0] + 20, INV_POS[1] + 70))
                self.write(("Strength: " + str(self.item_picked.strength)), (INV_POS[0] + 20, INV_POS[1] + 90))
                self.write(("Cost: " + str(self.item_picked.cost)),(INV_POS[0] + 20, INV_POS[1] + 110))
                self.inv_use_button.show_button(self.screen)
            if self.item_picked.type == "book":
                self.write(("Min. intellect: " + str(self.item_picked.min_int)), (INV_POS[0] + 20, INV_POS[1] + 70))
                self.write(("Cost: " + str(self.item_picked.cost)), (INV_POS[0] + 20, INV_POS[1] + 90))
                self.inv_use_button.show_button(self.screen)
            if self.item_picked.type == "key":
                self.write("Keyhole nr: " + str(self.item_picked.key), (INV_POS[0] + 20, INV_POS[1] + 70))
                if self.inv_open_door_button.active:
                    self.inv_open_door_button.show_button(self.screen)
            if self.item_picked.type == "ring" or self.item_picked.type == "necklace":
                self.draw_ring_picked_info(self.item_picked)
        self.player.armor_slot.show_slot(self.screen, INV_POS[0] + INV_WIDTH - 100, INV_POS[1] + 60)
        self.player.weapon_slot.show_slot(self.screen, INV_POS[0] + INV_WIDTH - 140, INV_POS[1] + 60)
        self.player.shield_slot.show_slot(self.screen, INV_POS[0] + INV_WIDTH - 60, INV_POS[1] + 60)
        self.player.helmet_slot.show_slot(self.screen, INV_POS[0] + INV_WIDTH - 100, INV_POS[1] + 20)
        self.player.boots_slot.show_slot(self.screen, INV_POS[0] + INV_WIDTH - 100, INV_POS[1] + 100)
        self.player.ring1_slot.show_slot(self.screen, INV_POS[0] + INV_WIDTH - 140, INV_POS[1] + 100)
        self.player.ring2_slot.show_slot(self.screen, INV_POS[0] + INV_WIDTH - 60, INV_POS[1] + 100)
        self.player.necklace_slot.show_slot(self.screen, INV_POS[0] + INV_WIDTH - 140, INV_POS[1] + 20)
        self.screen.blit(inv_bar, (INV_POS[0] + 20, INV_POS[1] + 410))
        self.screen.blit(gold_coin, (INV_POS[0] + 30, INV_POS[1] + 420))
        self.write(str(self.player.gold), (INV_POS[0] + 55, INV_POS[1] + 414), YELLOW)
        self.screen.blit(arrow_icon, (INV_POS[0] + 114, INV_POS[1] + 407))
        self.write(str(self.player.arrows), (INV_POS[0] + 145, INV_POS[1] + 414), YELLOW)
        self.write(f'ARMOR: {round(self.player.armor)}', (INV_POS[0] + 20, INV_POS[1] + 160))
        block_chance = str(round(self.player.block_chance))
        hit_red = str(round(self.player.hit_reduction))
        self.write("Block: " + block_chance + "%", (INV_POS[0] + 125, INV_POS[1] + 160))
        self.write("Dmg red: " + hit_red + "%", (INV_POS[0] + 225, INV_POS[1] + 160))
        if self.player.attack_type_flag == "magic":
            if self.player.active_spell.subtype == "poison cloud":
                damage = "0"
            else:
                damage = str(self.player.active_spell.damage + int(self.player.intellect * self.player.spell_power_bonus))
            hit_rate = (1000 / self.player.active_spell.hit_rate)
            hit_rate = str(hit_rate)
            hit_rate = hit_rate[:3]
        elif self.player.attack_type_flag == "ranged":
            damage = str(round(self.player.arrow_damage))
            hit_rate = (1000 / self.player.arrow_rate)
            hit_rate = str(hit_rate)
            hit_rate = hit_rate[:3]
        elif self.player.attack_type_flag == "melle":
            damage = str(round(self.player.hit_dmg))
            hit_rate = (1000 / self.player.hit_rate)
            hit_rate = str(hit_rate)
            hit_rate = hit_rate[:3]
        else:
            print("ERROR - dont know which attack type")
            # damage = str(self.player.hit_dmg)
            # hit_rate = (1000 / self.player.hit_rate)
            # hit_rate = str(hit_rate)
            # hit_rate = hit_rate[:3]
        self.write("DAMAGE: " + damage, (INV_POS[0] + 20, INV_POS[1] + 180))
        if self.player.attack_type_flag == "melle":
            if self.player.hit_radius:
                self.write("Damage radius: " + str(self.player.hit_radius),
                           (INV_POS[0] + 125, INV_POS[1] + 180))
        self.write("HIT RATE: " + hit_rate, (INV_POS[0] + 20, INV_POS[1] + 200))
        self.write("HP " + str(int(self.player.act_hp)), (INV_POS[0] + 20, INV_POS[1] + 230))
        self.write("MP " + str(self.player.act_mana), (INV_POS[0] + 20, INV_POS[1] + 250))
        self.screen.blit(bar, (INV_POS[0] + 65, INV_POS[1] + 234))
        self.screen.blit(red_line, (INV_POS[0] + 70, INV_POS[1] + 238),
                         (0, 0, 250 * self.player.act_hp / self.player.max_hp, 5))
        self.screen.blit(bar, (INV_POS[0] + 65, INV_POS[1] + 254))
        self.screen.blit(blue_line, (INV_POS[0] + 70, INV_POS[1] + 258),
                         (0, 0, 250 * self.player.act_mana / self.player.max_mana, 5))
        self.screen.blit(small_bar, (INV_POS[0] + 140, INV_POS[1] + 205))
        self.screen.blit(silver_line, (INV_POS[0] + 140, INV_POS[1] + 205),
                         (0, 0, 80 * self.player.hit_load_percentage / 100, 5))

    def draw_stats(self):
        ######### PASEK XP
        min_xp_c = 10 * (self.player.level - 1) + ((self.player.level - 2) * 2 * (self.player.level - 1))
        # print ("min_xp_c")
        # print (min_xp_c)
        max_xp_c = 10 * self.player.level + ((self.player.level - 1) * 2 * self.player.level)
        # print("max_xp_c")
        # print (max_xp_c)
        xp_dif_c = self.player.xp - min_xp_c
        # print("xp_dif_c")
        # print (xp_dif_c)
        xp_ratio_c = xp_dif_c / (max_xp_c - min_xp_c)
        # print("xp_ratio_c")
        # print (xp_ratio_c)
        # print ("--------")
        self.write("Name :" + self.player.name, (ST_POS[0] + ST_WIDTH / 2 - 40, ST_POS[1] + 10))
        self.write("Skills:", (ST_POS[0] + 10, ST_POS[1] + 10))
        self.write(str(self.player.strength), (ST_POS[0] + 50, ST_POS[1] + 40))
        self.screen.blit(i_str_ico,(ST_POS[0] + 30, ST_POS[1] + 40))
        self.write(str(self.player.stamina), (ST_POS[0] + 50, ST_POS[1] + 60))
        self.screen.blit(i_sta_ico, (ST_POS[0] + 30, ST_POS[1] + 60))
        self.write(str(self.player.intellect), (ST_POS[0] + 50, ST_POS[1] + 80))
        self.screen.blit(i_int_ico, (ST_POS[0] + 30, ST_POS[1] + 80))
        self.write(str(self.player.wisdom), (ST_POS[0] + 50, ST_POS[1] + 100))
        self.screen.blit(i_wis_ico, (ST_POS[0] + 30, ST_POS[1] + 100))
        self.write(str(self.player.speed), (ST_POS[0] + 50, ST_POS[1] + 120))
        self.screen.blit(i_spe_ico, (ST_POS[0] + 30, ST_POS[1] + 120))
        self.write(str(self.player.stealth), (ST_POS[0] + 50, ST_POS[1] + 140))
        self.screen.blit(i_ste_ico, (ST_POS[0] + 30, ST_POS[1] + 140))
        self.write("CLASS :" + str(self.player.char_class.name), (ST_POS[0] + ST_WIDTH - 250, ST_POS[1] + 40))
        self.write("LEVEL " + str(self.player.level), (ST_POS[0] + ST_WIDTH - 250, ST_POS[1] + 60))
        self.write(f'XP: {self.player.xp}/{max_xp_c}', (ST_POS[0] + ST_WIDTH - 100, ST_POS[1] + 60))
        if self.player.attribute_points > 0:
            self.write("Points to spend :" + str(self.player.attribute_points), (ST_POS[0] + 10, ST_POS[1] + 10))
            self.str_ad_button.show_button(self.screen)
            self.sta_ad_button.show_button(self.screen)
            self.int_ad_button.show_button(self.screen)
            self.wis_ad_button.show_button(self.screen)
            self.spe_ad_button.show_button(self.screen)
            self.ste_ad_button.show_button(self.screen)
        self.screen.blit(small_bar, (ST_POS[0] + ST_WIDTH - 100, ST_POS[1] + 45))
        self.screen.blit(silver_line, (ST_POS[0] + ST_WIDTH - 100, ST_POS[1] + 45),
                         (0, 0, 80 * xp_ratio_c, 5))
        ####################
        mov_sp = str(self.player.movement_speed / 100)
        self.write("Active Spell :", (ST_POS[0] + ST_WIDTH - 250, ST_POS[1] + 80))
        if self.player.active_spell:
            self.write(self.player.active_spell.name, (ST_POS[0] + ST_WIDTH - 160, ST_POS[1] + 80))
        self.write("Active Effects :", (ST_POS[0] + ST_WIDTH - 250, ST_POS[1] + 100))
        self.player.active_effects_lib.show(self.screen, (ST_POS[0] + ST_WIDTH - 150, ST_POS[1] + 100))
        self.write("Movement :" + mov_sp, (ST_POS[0] + ST_WIDTH - 250, ST_POS[1] + 120))
        self.write("Avoid mod : " + str(self.player.stealth * 3) + " pix",
                   (ST_POS[0] + ST_WIDTH - 250, ST_POS[1] + 140))

    def draw_info(self):
        lot = 0
        self.screen.blit(info_bcg, (INFO_POS))
        for line in self.txts:
            self.write(line, (INFO_POS[0] + 10, INFO_POS[1] + 20 * lot),
                       (255 - lot * 40, 255 - lot * 40, 255 - lot * 40))
            lot += 1

    def put_txt(self, txt):
        self.txts.insert(0, txt)
        self.txts.pop()

    def draw_death_animation(self):
        pygame.mixer.Sound.play(death_snd)
        animation = True
        frame_counter = 0
        anim_counter = 0
        while animation:
            #in_dt = self.clock.tick(FPS) / 1000
            self.screen.fill(BGCOLOR)
            self.map_surface.blit(self.map_image, self.camera.apply_rect(self.map_rect))
            for sprite in self.act_lvl.all_sprites:
                if isinstance(sprite, Mob):
                    sprite.draw_health()
                ##### RYSOWANIE WSZYSTKIEGO!
                self.map_surface.blit(sprite.image, self.camera.apply(sprite))
            for sprite in self.player_group:
                self.map_surface.blit(sprite.image, self.camera.apply(sprite))
            self.screen.blit(self.map_surface, MAP_TOPLEFT)
            self.screen.blit(inv_bcg_image, (INV_POS), (0, 0, INV_WIDTH, INV_HEIGHT))
            self.screen.blit(inv_bcg_image, (ST_POS), (0, 0, ST_WIDTH, ST_HEIGHT))
            self.draw_inventory()
            self.draw_stats()
            self.pause_button.show_button(self.screen)
            self.spell_book_button.show_button(self.screen)
            frame_counter += 1
            # print ("frame: " + str(frame_counter))
            # print ("dt: " + str(in_dt))
            if frame_counter > 15:
                self.player.image = self.player.char_death_animation_images[anim_counter]
                anim_counter += 1
                frame_counter = 0
                if anim_counter >= len(self.player.char_death_animation_images):
                    animation = False
            pygame.display.flip()
        self.playing = False

    def draw(self):
        self.screen.fill(BGCOLOR)
        if not self.paused:
            if self.player.start_death_animation:
                self.draw_death_animation()
            #### RYSUJEMY MAPE
            self.map_surface.blit(self.map_image, self.camera.apply_rect(self.map_rect))
            # self.draw_grid()
            # pygame.draw.rect(self.screen,WHITE,self.camera.apply(self.player),2)
            for sprite in self.act_lvl.all_sprites:
                if isinstance(sprite, Mob):
                    sprite.draw_health()
                ##### RYSOWANIE WSZYSTKIEGO!
                self.map_surface.blit(sprite.image, self.camera.apply(sprite))
                ##### DEBUG MODE / COLLISIONS
                if self.draw_debug:
                    pygame.draw.rect(self.map_surface, (70, 30, 170), self.camera.apply_rect(sprite.hit_rect), 1)
            ### ODDZIELNIE RYSUJE GRACZA i PRZEDMIOTY
            for sprite in self.player_group:
                self.map_surface.blit(sprite.image, self.camera.apply(sprite))
            ### DEBUG MODE
            if self.draw_debug:
                #### RYSUJEMY TEKST ROBOCZY
                mouse_pos = pygame.mouse.get_pos()
                mouse_pos = pygame.mouse.get_pos()
                self.write(f'Mouse pos: {mouse_pos}', (50, 0))
                self.write(f'Player pos: {self.player.pos}', (200, 0))
                self.write(f'Diff factor: {self.difficulty}',(400,0))
                for mob in self.act_lvl.mobs:
                    mob_rect = self.camera.apply_rect(mob.rect)
                    mob_center = mob_rect.center
                    pygame.draw.circle(self.map_surface,SKYBLUE,mob_center,mob.sleep_radius,1)
                    pygame.draw.circle(self.map_surface,PURPLE,mob_center,int(mob.updated_sleep_radius),1)
                for wall in self.act_lvl.walls:
                    pygame.draw.rect(self.map_surface, (70, 30, 170), self.camera.apply_rect(wall.rect), 1)
                for lava in self.act_lvl.lavas:
                    pygame.draw.rect(self.map_surface, (230, 0, 0), self.camera.apply_rect(lava.rect), 1)
                for player in self.player_group:
                    if isinstance(player, Player):
                        pygame.draw.rect(self.map_surface, (100, 255, 100), self.camera.apply_rect(player.hit_rect), 1)
                for coll_sprite in self.act_lvl.collecting_sprites:
                    pygame.draw.rect(self.map_surface,(180,210,10),self.camera.apply_rect(coll_sprite.rect), 1)
            self.screen.blit(self.map_surface, MAP_TOPLEFT)
        else:
            pygame.draw.rect(self.screen, (200, 240, 120),
                             (MAP_TOPLEFT[0], MAP_TOPLEFT[1], MAP_WIDTH, MAP_HEIGHT), 3)
            self.screen.blit(self.map_surface, MAP_TOPLEFT)
        #### RYSUJE UI
        self.screen.blit(inv_bcg_image, (INV_POS), (0, 0, INV_WIDTH, INV_HEIGHT))
        self.screen.blit(inv_bcg_image, (ST_POS), (0, 0, ST_WIDTH, ST_HEIGHT))
        self.draw_inventory()
        self.draw_stats()
        self.draw_info()
        self.pause_button.show_button(self.screen)
        #self.save_button.show_button(self.screen)
        self.spell_book_button.show_button(self.screen)
        self.quest_book_button.show_button(self.screen)
        self.write(str(int(self.clock.get_fps())), (0, 0))
        if self.paused:
            self.screen.blit(dim_screen, (MAP_TOPLEFT))
            if self.draw_debug:
                #### RYSUJEMY TEKST ROBOCZY
                mouse_pos = pygame.mouse.get_pos()
                self.write(f'(Mouse pos: {mouse_pos}',(150,0))
                self.write(f'(Player pos: {self.player.pos}', (300,0))
            #### STANY SPECJALNE
            ### NEXT LEVEL
            if self.player.attribute_points > 0:
                self.screen.blit(scroll_level_up, (MAP_WIDTH / 2 - 160, MAP_HEIGHT / 2 - 60))
            ### PHASE SHOP
            if self.ph_shop:
                self.shop_dialog_box.show(self.screen)
            ### PHASE BUY SELL OR REPAIR (ta sama funkcja show)
            if self.ph_buy_and_sell or self.ph_repair:
                self.active_shop.show(self.screen)
            ### TREASURE CHEST
            elif self.ph_treasure_inv:
                self.blit_alpha(self.screen, treasure_bcg_img, (MAP_TOPLEFT[0] + 120, MAP_TOPLEFT[1] + 120), 220)
                self.treasure_inv.show_inv(self.screen, MAP_TOPLEFT[0] + 200, MAP_TOPLEFT[1] + 350)
            ### SPELL BOOK
            elif self.ph_spell_book:
                self.player.spell_book.show(self.screen)
                self.cast_button.show_button(self.screen)
            ### QUEST BOOK
            elif self.ph_quest_book:
                self.player.quest_book.show(self.screen)
            # DIALOG BOX
            elif self.dialog_in_progress:
                self.dialog_box.show(self.screen)
            # MESSAGE BOX
            elif self.message_shown:
                self.message_box.show(self.screen)
            # QBOX
            elif self.qbox_shown:
                self.q_box.show(self.screen)

        #### SREDNIA FPS
        # if self.draw_debug:
        #    x = int(self.clock.get_fps())
        #    self.fpss.append(x)
        #    #print (str(len(self.fpss)))
        #    if len(self.fpss) > 1000:
        #        count = 0
        #        for i in self.fpss:
        #            count += i
        #        print ("MEAN FPS: " + str(count/ len(self.fpss)))
        #        self.fpss.clear()

        #### FLIP
        pygame.display.flip()

game = Game()
game.intro()
