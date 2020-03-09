from sprites import *
from ui import *
import sys
from settings import *
import tilemap
from os import path
from data import *
import levels


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
        ### PRZEDMIOTY NA UI
        self.items = pygame.sprite.LayeredUpdates()
        ### PRZEDMIOTY NA MAPIE DO PODNIESIENIA
        self.items_to_pick = pygame.sprite.LayeredUpdates()
        ### ZLOTE MONETY DO PODNIESIENIA
        self.gold_to_pick = pygame.sprite.LayeredUpdates()
        ### STRZALY DO PODNIESIENIA
        self.arrows_to_pick = pygame.sprite.LayeredUpdates()
        ### DRZWI
        self.doors = pygame.sprite.LayeredUpdates()
        ### SKRZYNIE
        self.chest_to_open = pygame.sprite.LayeredUpdates()
        ### CHYBA NIC..
        self.active_items = pygame.sprite.LayeredUpdates()
        ### TELEPORTS
        self.teleports = pygame.sprite.LayeredUpdates()


class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 2048)
        pygame.init()
        #### USTAWIC POZNIEJ SILE DZWIEKU!
        print(pygame.mixer.Channel(1).get_volume())
        ######
        self.clock = pygame.time.Clock()
        self.font_arial = pygame.font.match_font("arial")
        global font
        font = pygame.font.Font(self.font_arial, 16)
        global font20
        font20 = pygame.font.Font(self.font_arial, 20)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.map_surface = pygame.Surface((MAP_WIDTH, MAP_HEIGHT), pygame.HWSURFACE | pygame.SRCALPHA)
        pygame.display.set_caption(TITLE)
        pygame.key.set_repeat(300, 100)
        ######## ZMIENNE DO DEBUOWANIA #######
        self.unlock_updates = False
        self.fpss = []

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

    def s_write(self, text, surface, location, color=(WHITE)):
        surface.blit(font.render(text, True, color), location)

    def h_write(self, text, location, h_font, size, color):
        h_font_type = pygame.font.match_font(h_font)
        h_font_r = pygame.font.Font(h_font_type, size)
        self.screen.blit(h_font_r.render(text, True, color, ), location)

    def new(self, class_selected):
        #### LOADING LEVELS ####
        self.levels = {}
        self.map_levels = {}
        self.level_01 = Level()
        self.map_level_01 = tilemap.TiledMap(path.join(map_folder, 'mapa1.tmx'))
        self.level_02 = Level()
        self.map_level_02 = tilemap.TiledMap(path.join(map_folder, 'mapa2.tmx'))
        #####
        self.levels['level01'] = self.level_01
        self.levels['level02'] = self.level_02
        #####
        self.map_levels['level01'] = self.map_level_01
        self.map_levels['level02'] = self.map_level_02
        #### CREATE ##########################################
        ### SPRITE GROUPS NALEZACE DO GAME a nie DO LEVEL! ###
        ######################################################
        self.player_group = pygame.sprite.LayeredUpdates()
        self.small_items = pygame.sprite.LayeredUpdates()
        ### STARTING WITH LEVEL 01 #######
        self.act_lvl = self.level_01
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
        self.player = Player(self, "Kris", class_selected)
        ### DIALOG BOX
        self.dialog_box = DialogBox(self)
        ### UI BUTTONS
        self.inv_use_button = RadioButton(rad_use_img, rad_use_h_img,
                                          INV_POS[0] + 140, INV_POS[1] + 80)
        self.inv_open_door_button = RadioButton(rad_open_img, rad_open_h_img,
                                                INV_POS[0] + 120, INV_POS[1] + 20)
        self.pause_button = RadioButton(rad_pause_img, rad_pause_h_img, 780, 690)
        self.spell_book_button = RadioButton(sbb_img, sbb_h_img, INV_POS[0], 680)
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
                            self.spell_book_button, self.pause_button, self.cast_button]
        self.att_buttons = [self.str_ad_button, self.sta_ad_button, self.int_ad_button,
                            self.wis_ad_button, self.spe_ad_button, self.ste_ad_button]
        ####### START LEVEL
        self.levelgen = levels.LevelGen(self)
        self.levelgen.load_level_01()
        self.levelgen.load_level_02()
        self.levelgen.go_to_level("level01", 2, 2)
        ##### CAMERA INIT
        self.camera = tilemap.Camera(self.map.width, self.map.height)
        self.draw_debug = False
        #### RUN
        self.run()
        #### GAME OVER
        self.game_over()

    def intro(self):
        self.intro_screen = True
        self.to_char_chose = False
        self.class_selected = False
        ### CREATE CLASESS
        self.knight_class = CharClass("Knight", pl_knight_image, knight_death_anim, ["sword", "spear", "axe"],
                                      ["staff", "dagger"],
                                      ["plate"], ["robe"], 4, 4, 1, 2, 3, 1, [])
        self.wizard_class = CharClass("Wizard", pl_wizard_image, knight_death_anim, ["staff"], ["sword", "axe", "bow"],
                                      ["robe"],
                                      ["chain", "plate"], 2, 1, 4, 5, 2, 2, ["Firebolt"])
        self.thief_class = CharClass("Thief", pl_thief_image, knight_death_anim, ["dagger", "bow"], ["axe", "spear"],
                                     ["leather"],
                                     ["plate"], 2, 2, 2, 2, 4, 5, [])
        ################
        pygame.mixer.music.stop()
        self.new_game_button = Button(intro_but_img, intro_but_h_img, 128, 32, "New Game", SCREEN_WIDTH / 2 - 64, 270,
                                      20)
        self.quit_game_button = Button(intro_but_img, intro_but_h_img, 128, 32, "Quit", SCREEN_WIDTH / 2 - 64, 320, 20)
        self.start_game_button = Button(intro_but_img, intro_but_h_img, 150, 32, "Start Game", SCREEN_WIDTH / 2 - 64,
                                        650, 20)
        self.knight_class_button = Button(intro_but_img, intro_but_h_img, 128, 32, "Knight", 140, 200, 20)
        self.wizard_class_button = Button(intro_but_img, intro_but_h_img, 128, 32, "Wizard", 140, 250, 20)
        self.thief_class_button = Button(intro_but_img, intro_but_h_img, 128, 32, "Thief", 140, 300, 20)
        self.intro_buttons = [self.new_game_button, self.quit_game_button]
        self.class_buttons = [self.knight_class_button, self.wizard_class_button, self.thief_class_button,
                              self.start_game_button]

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
                        self.new(self.class_selected)
                    if self.knight_class_button.check_if_clicked(mouse_pos):
                        self.class_selected = self.knight_class
                    if self.wizard_class_button.check_if_clicked(mouse_pos):
                        self.class_selected = self.wizard_class
                    if self.thief_class_button.check_if_clicked(mouse_pos):
                        self.class_selected = self.thief_class
                    if self.quit_game_button.check_if_clicked(mouse_pos):
                        self.quit()

    def intro_update(self):
        mouse_pos = pygame.mouse.get_pos()
        #### HIGHLIGHT BUTTONS #####
        if self.to_char_chose:
            for button in self.class_buttons:
                button.check_if_highlight(mouse_pos)
        else:
            for button in self.intro_buttons:
                button.check_if_highlight(mouse_pos)
        if self.class_selected:
            self.start_game_button.activate()
        else:
            self.start_game_button.deactivate()

    def intro_draw(self):
        self.screen.fill(BGCOLOR)
        # self.h_write("GRA RYCERZ Z WIDELCEM",(200,50),"monotype corsiva",40,(200,0,200))
        if self.to_char_chose:
            self.screen.blit(game_over_img, (0, 0))
            self.h_write("Choose your character class:", (360, 120), "arial", 26, (WHITE))
            self.knight_class_button.show_button(self.screen, font)
            self.wizard_class_button.show_button(self.screen, font)
            self.thief_class_button.show_button(self.screen, font)
            self.start_game_button.show_button(self.screen, font)
            if self.class_selected:
                if self.class_selected == self.knight_class:
                    self.screen.blit(pygame.transform.scale(self.class_selected.image, (64, 64)), (400, 240))
                    self.h_write("Knight", (400, 200), "arial", 26, (WHITE))
                    self.write("Dedicated do melle fight, starts with strength and stamina bonus", (340, 340), (WHITE))
                if self.class_selected == self.wizard_class:
                    self.screen.blit(pygame.transform.scale(self.class_selected.image, (64, 64)), (400, 240))
                    self.h_write("Wizard", (400, 200), "arial", 26, (WHITE))
                    self.write("Weak in direct fight, but able to make severe damage by magic powers", (340, 340),
                               (WHITE))
                if self.class_selected == self.thief_class:
                    self.screen.blit(pygame.transform.scale(self.class_selected.image, (64, 64)), (400, 240))
                    self.h_write("Thief", (400, 200), "arial", 26, (WHITE))
                    self.write("Fast and able to sneak, powerful with his favourite bow and dagger combination",
                               (340, 340),
                               (WHITE))
                self.write("Strength: " + str(self.class_selected.str), (500, 160 + 40))
                self.write("Stamina: " + str(self.class_selected.sta), (500, 160 + 60))
                self.write("Intellect: " + str(self.class_selected.int), (500, 160 + 80))
                self.write("Wisdom: " + str(self.class_selected.wis), (500, 160 + 100))
                self.write("Speed: " + str(self.class_selected.spe), (500, 160 + 120))
                self.write("Stealth: " + str(self.class_selected.ste), (500, 160 + 140))
                self.write("Favourite weapons: ", (340, 360), (WHITE))
                weapon_txt = ""
                for weapon in self.class_selected.favourite_weapons:
                    weapon_txt += weapon
                    weapon_txt += ","
                self.write(weapon_txt, (480, 360), (WHITE))
                armor_txt = ""
                self.write("Favourite armors: ", (340, 380), (WHITE))
                for armor in self.class_selected.favourite_armors:
                    armor_txt += armor
                    armor_txt += ","
                self.write(armor_txt, (480, 380), (WHITE))
                self.write("Disliked weapons: ", (340, 400), (WHITE))
                weapon_txt = ""
                for weapon in self.class_selected.disliked_weapons:
                    weapon_txt += weapon
                    weapon_txt += ","
                self.write(weapon_txt, (480, 400), (WHITE))
                armor_txt = ""
                self.write("Disliked armors: ", (340, 420), (WHITE))
                for armor in self.class_selected.disliked_armors:
                    armor_txt += armor
                    armor_txt += ","
                self.write(armor_txt, (480, 420), (WHITE))
                self.write("Strength: " + str(self.class_selected.str), (500, 160 + 40))
                self.write("Stamina: " + str(self.class_selected.sta), (500, 160 + 60))
                self.write("Intellect: " + str(self.class_selected.int), (500, 160 + 80))
                self.write("Wisdom: " + str(self.class_selected.wis), (500, 160 + 100))
                self.write("Speed: " + str(self.class_selected.spe), (500, 160 + 120))
                self.write("Stealth: " + str(self.class_selected.ste), (500, 160 + 140))


        else:
            self.screen.blit(intro_img, (0, 0))
            self.new_game_button.show_button(self.screen, font)
            self.quit_game_button.show_button(self.screen, font)
        self.write(str(self.clock.get_fps()), (0, 0))
        #### FLIP
        pygame.display.flip()

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
                if enemy.max_hp > biggest_hp:
                    biggest_hp = enemy.max_hp
                    most_powerful_enemy = enemy
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
        self.screen.blit(game_over_img, (0, 0))
        self.h_write("GAME OVER", (SCREEN_WIDTH / 2 - 120, 60), "monotype corsiva", 42, (WHITE))
        self.h_write("Press Enter to go to Main Menu", (SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT - 100),
                     "monotype corsiva", 32, (WHITE))
        self.h_write("Czas gry: " + str(self.time_played) + " sekund", (x_pos + 60, y_pos + 50), "monotype corsiva", 20,
                     (WHITE))
        self.h_write("Posiadane złoto: " + str(self.player.gold), (x_pos + 60, y_pos + 70), "monotype corsiva", 20,
                     (WHITE))
        self.h_write("Zabici przeciwnicy: " + str(self.killed_enemies), (x_pos + 60, y_pos + 90), "monotype corsiva",
                     20, (WHITE))
        if self.most_powerful_enemy:
            self.h_write("Najpotężniejszy przeciwnik: " + str(self.most_powerful_enemy.name), (x_pos + 60, y_pos + 110),
                         "monotype corsiva", 20, (WHITE))
        self.h_write("Wartość zadanych obrażeń wręcz: " + str(self.overall_melle_hits), (x_pos + 60, y_pos + 140),
                     "monotype corsiva", 20, (WHITE))
        self.h_write("Celność ciosów wręcz: " + str(self.melle_accuracy) + "%", (x_pos + 60, y_pos + 160),
                     "monotype corsiva", 20, (WHITE))
        self.h_write("Wartość zadanych obrażeń z łuku: " + str(self.overall_arrow_hits), (x_pos + 60, y_pos + 190),
                     "monotype corsiva", 20,
                     (WHITE))
        self.h_write("Celność z łuku: " + str(self.arrow_accuracy) + "%", (x_pos + 60, y_pos + 210), "monotype corsiva",
                     20, (WHITE))
        self.h_write("Wartość obrażeń magicznych: " + str(self.overall_spell_hits), (x_pos + 60, y_pos + 240),
                     "monotype corsiva", 20,
                     (WHITE))
        self.h_write("Celność magii: " + str(self.spell_accuracy) + "%", (x_pos + 60, y_pos + 260), "monotype corsiva",
                     20, (WHITE))
        self.h_write("Otrzymane obrażenia: " + str(self.inflicted_damage), (x_pos + 60, y_pos + 290),
                     "monotype corsiva", 20, (WHITE))
        self.h_write("Bloki: " + str(self.player.score_blocks), (x_pos + 60, y_pos + 310), "monotype corsiva", 20,
                     (WHITE))
        self.h_write("Efektywność bloków: " + str(self.block_efficiency) + "%", (x_pos + 60, y_pos + 330),
                     "monotype corsiva", 20, (WHITE))
        self.h_write("Otworzone skrzynie: " + str(self.player.score_chest_opened), (x_pos + 60, y_pos + 360),
                     "monotype corsiva", 20, (WHITE))
        self.h_write("Zniszczone beczki: " + str(self.player.score_barrels_destroyed), (x_pos + 60, y_pos + 380),
                     "monotype corsiva", 20, (WHITE))
        self.h_write("PUNKTY :" + str(self.points), (x_pos + 60, y_pos + 420), "monotype corsiva", 26, (WHITE))
        self.write(str(self.clock.get_fps()), (0, 0))
        #### FLIP
        pygame.display.flip()

    def run(self):
        self.playing = True
        ##### FLAGI DO MECHANIKI GRY ############
        self.first_loop = False
        self.paused = False
        ##### FLAGI DO STANU GRY (TREASURE CHEST, SPELL BOOK, SHOP etc..
        self.ph_treasure_inv = False
        self.treasure_inv = False
        self.ph_spell_book = False
        self.ph_shop = False
        self.dialog_in_progress = False
        ##### FLAGI DO OBSLUGI INVENTARZA #######
        self.item_picked = False
        self.toggle_clean_item_picked = False
        self.toggle_open_chest = False
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
                if event.key == pygame.K_F1:
                    self.draw_debug = not self.draw_debug
                if event.key == pygame.K_c:
                    if self.player.active_spell:
                        self.player.active_spell = False
                        self.player.update_stats()
                    else:
                        self.player.active_spell = self.player.selected_spell
                        self.player.update_stats()
                if event.key == pygame.K_e:
                    ######## PODNIES PRZEDMIOT
                    items_to_pick = pygame.sprite.spritecollide(self.player, self.act_lvl.items_to_pick, False,
                                                                collide_double_hit_rect)
                    for item in items_to_pick:
                        if self.player.inventory.put_in_first_free_slot(item.item):
                            item.kill()
                            pygame.mixer.Sound.play(pick_item_snd)
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
                    ######## ZAMYKANIE OTWARTEJ SKRZYNI
                    if self.toggle_open_chest:
                        self.paused = False
                        self.ph_treasure_inv = False
                        self.treasure_inv = False
                        self.toggle_open_chest = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    ### PAUZA
                    if self.pause_button.check_if_clicked(mouse_pos):
                        if self.paused:
                            self.paused = False
                            ##### ZAMYKAM STANY SPECJALNE
                            self.ph_treasure_inv = False
                            self.ph_spell_book = False
                            self.treasure_inv = False
                            self.player.update_stats()
                        else:
                            self.paused = True
                    ### PRZYCISK SPELL BOOK
                    if self.spell_book_button.check_if_clicked(mouse_pos):
                        if not self.ph_spell_book:
                            if not self.paused:
                                self.paused = True
                                self.ph_spell_book = True
                            else:
                                self.ph_spell_book = True
                        else:
                            self.ph_spell_book = False
                            self.ph_treasure_inv = False
                            self.paused = False
                            self.player.update_stats()
                    ### ADD ATRIBUTES
                    self.ad_buttons_check(mouse_pos)
                    ### PICK UP AND DROP ITEMS on INV
                    if self.item_picked:
                        ##################################
                        # GDY MAM PRZEDMIOT PODNIESIONY  #
                        ##################################
                        # 1. ODKLADAM DO PLECAKA
                        if self.player.inventory.check_if_clicked(mouse_pos):
                            put_item_success_bool = self.player.inventory.put_item_to_inv(mouse_pos,
                                                                                          self.item_picked)
                            if put_item_success_bool:  # GDY UDALO SIE ODLOZYC WTEDY OCZYSZCzAM ITEM PICKED
                                self.toggle_clean_item_picked = True
                        # 2. 0DKLADAM NA AKTYWNY SLOT
                        for slot in self.player.active_slots:
                            if slot.check_itemslot_to_item_corr(mouse_pos, self.item_picked):
                                if slot.occ == False:
                                    self.toggle_clean_item_picked = True
                                ### POLOZ PRZEDMIOT NA AKTYWNYM SLOCIE i UPDATE STATISTICS
                                pygame.mixer.Sound.play(wear_item_snd)
                                if slot.put_item(self.item_picked):
                                    ### TYLKO BRON LUB ZBROJE SA SPRITEAMI DO WYSWIELTENIA NA LUDZIKU
                                    if isinstance(self.item_picked, Armor) or isinstance(self.item_picked, Weapon):
                                        self.player_group.add(self.item_picked)
                                self.player.update_stats()
                        # 3. ODKLADAM NA TREASURE
                        if self.treasure_inv:
                            if self.treasure_inv.check_if_clicked(mouse_pos):
                                put_item_success_bool = self.treasure_inv.put_item_to_inv(mouse_pos,
                                                                                          self.item_picked)
                                if put_item_success_bool:  # GDY UDALO SIE ODLOZYC WTEDY OCZYSZCzAM ITEM PICKED
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
                            self.item_picked = self.player.inventory.pick_item_from_inv(mouse_pos)
                        # 2. PODNIES ITEM Z TREASURE INV
                        if self.treasure_inv:
                            if self.treasure_inv.check_if_clicked(mouse_pos):
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
                                    ### PODNIES PRZEDMIOT Z AKTYWNEGO SLOTU i UPDATE STATYSTYK
                                    self.player_group.remove(slot.item)
                                    self.item_picked = slot.pick_item()
                                    self.player.update_stats()
                        # 4. ZAZNACZ lub ODZNACZ CZAR:
                        if self.ph_spell_book:
                            ## Zaznaczm tylko gdy NIE naciskam guziku cast i spellbook (zeby nie odhaczac bez sensu
                            if not self.spell_book_button.check_if_clicked(
                                    mouse_pos) and not self.cast_button.check_if_clicked_even_inactive(mouse_pos):
                                # print ("zaznaczam nowe wskazanie")
                                self.player.active_spell = self.player.spell_book.check_spell(mouse_pos)
                                self.player.selected_spell = self.player.active_spell
                                if self.player.active_spell:
                                    if self.player.active_spell.min_int > self.player.intellect:
                                        self.player.active_spell = False
                                        self.player.selected_spell = False
                                self.player.update_stats()
                                # 5. CZAR DEFENSYWNY
                            if self.cast_button.check_if_clicked(mouse_pos):
                                self.player.active_spell.cast(self.player)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        #### CZYSZCZE TOGGLE OPEN CHEST
        if self.paused and self.ph_treasure_inv:
            self.toggle_open_chest = True
        else:
            self.toggle_open_chest = False
        #### CZYSZCZE ITEM PICKED ####
        if self.toggle_clean_item_picked:
            self.item_picked = False
            self.toggle_clean_item_picked = False
        #### HIGHLIGHT BUTTONS #####
        for button in self.all_buttons:
            button.check_if_highlight(mouse_pos)
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
        #### ACTIVATE DIALOG BUTTONS ####
        #
        #
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
                    txt = str(
                        "Ranged hit. " + self.player.name + " inflicted " + (str(self.player.hit_dmg)) + " damage.")
                    self.put_txt(txt)
                    self.player.score_arrow_enemy_hits.append(int(self.player.arrow_damage))
                    mob.hp -= self.player.arrow_damage
                    mob.damaged = True
                    mob.damage_alpha = chain(DAMAGE_ALPHA_LIST * 2)
                    mob.last_hit_moment = (int(self.player.score_time_played * 1000))
                    mob.vel = vec(0, 0)
                    rot = (self.player.pos - mob.pos).angle_to(vec(-1, 0))
                    mob.pos += vec(5, 0).rotate(-rot)
                    # hit.vel = hit.vel.rotate(180)

    def draw_weapon_picked_info(self, item):
        self.write(("DAMAGE: " + str(item.damage)), (INV_POS[0] + 20, INV_POS[1] + 50))
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
        self.write(("ARMOR: " + str(item.armor)), (INV_POS[0] + 20, INV_POS[1] + 50))
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
            self.screen.blit(slot_img, (INV_POS[0] + 40, INV_POS[1] + 15))
            self.screen.blit(self.item_picked.b_image, (INV_POS[0] + 40, INV_POS[1] + 15))
            self.write(self.item_picked.name, (INV_POS[0] + 80, INV_POS[1] + 20))
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
        self.write(str(self.player.gold), (INV_POS[0] + 55, INV_POS[1] + 414), (255, 255, 0))
        self.screen.blit(arrow_icon, (INV_POS[0] + 114, INV_POS[1] + 407))
        self.write(str(self.player.arrows), (INV_POS[0] + 145, INV_POS[1] + 414), (255, 255, 0))
        self.write("ARMOR: " + str(self.player.armor), (INV_POS[0] + 20, INV_POS[1] + 160))
        block_chance = str(self.player.block_chance)[:3]
        hit_red = str(self.player.hit_reduction)[:3]
        self.write("Block: " + block_chance + "%", (INV_POS[0] + 125, INV_POS[1] + 160))
        self.write("Dmg red: " + hit_red + "%", (INV_POS[0] + 225, INV_POS[1] + 160))
        if self.player.attack_type_flag == "magic":
            if self.player.active_spell.subtype == "poison cloud":
                damage = "0"
            else:
                damage = str(self.player.active_spell.damage + self.player.intellect)
            hit_rate = (1000 / self.player.active_spell.hit_rate)
            hit_rate = str(hit_rate)
            hit_rate = hit_rate[:3]
        elif self.player.attack_type_flag == "ranged":
            damage = str(self.player.arrow_damage)
            hit_rate = (1000 / self.player.arrow_rate)
            hit_rate = str(hit_rate)
            hit_rate = hit_rate[:3]
        elif self.player.attack_type_flag == "melle":
            damage = str(self.player.hit_dmg)
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
        self.write("HIT RATE: " + hit_rate + "\s", (INV_POS[0] + 20, INV_POS[1] + 200))
        self.write("HP " + str(int(self.player.act_hp)), (INV_POS[0] + 20, INV_POS[1] + 230))
        self.write("MP " + str(self.player.act_mana), (INV_POS[0] + 20, INV_POS[1] + 250))
        self.screen.blit(bar, (INV_POS[0] + 65, INV_POS[1] + 234))
        self.screen.blit(red_line, (INV_POS[0] + 70, INV_POS[1] + 238),
                         (0, 0, 250 * self.player.act_hp / self.player.max_hp, 5))
        self.screen.blit(bar, (INV_POS[0] + 65, INV_POS[1] + 254))
        self.screen.blit(blue_line, (INV_POS[0] + 70, INV_POS[1] + 258),
                         (0, 0, 250 * self.player.act_mana / self.player.max_mana, 5))
        self.screen.blit(small_bar, (INV_POS[0] + 125, INV_POS[1] + 205))
        self.screen.blit(silver_line, (INV_POS[0] + 125, INV_POS[1] + 205),
                         (0, 0, 80 * self.player.hit_load_percentage / 100, 5))

    def draw_stats(self):
        self.write("Name :" + self.player.name, (ST_POS[0] + ST_WIDTH / 2 - 40, ST_POS[1] + 10))
        self.write("Strength: " + str(self.player.strength), (ST_POS[0] + 25, ST_POS[1] + 40))
        self.write("Stamina: " + str(self.player.stamina), (ST_POS[0] + 25, ST_POS[1] + 60))
        self.write("Intellect: " + str(self.player.intellect), (ST_POS[0] + 25, ST_POS[1] + 80))
        self.write("Wisdom: " + str(self.player.wisdom), (ST_POS[0] + 25, ST_POS[1] + 100))
        self.write("Speed: " + str(self.player.speed), (ST_POS[0] + 25, ST_POS[1] + 120))
        self.write("Stealth: " + str(self.player.stealth), (ST_POS[0] + 25, ST_POS[1] + 140))
        self.write("CLASS :" + str(self.player.char_class.name), (ST_POS[0] + ST_WIDTH - 220, ST_POS[1] + 40))
        self.write("Lvl: " + str(self.player.level), (ST_POS[0] + ST_WIDTH - 220, ST_POS[1] + 60))
        self.write("XP: " + str(self.player.xp), (ST_POS[0] + ST_WIDTH - 160, ST_POS[1] + 60))
        if self.player.attribute_points > 0:
            self.write("Points to spend :" + str(self.player.attribute_points), (ST_POS[0] + 10, ST_POS[1] + 10))
            self.str_ad_button.show_button(self.screen)
            self.sta_ad_button.show_button(self.screen)
            self.int_ad_button.show_button(self.screen)
            self.wis_ad_button.show_button(self.screen)
            self.spe_ad_button.show_button(self.screen)
            self.ste_ad_button.show_button(self.screen)
        ######### PASEK XP
        min_xp_c = 10 * (self.player.level - 1) + ((self.player.level - 2) * (self.player.level - 1))
        # print ("min_xp_c")
        # print (min_xp_c)
        max_xp_c = 10 * self.player.level + ((self.player.level - 1) * self.player.level)
        # print("max_xp_c")
        # print (max_xp_c)
        xp_dif_c = self.player.xp - min_xp_c
        # print("xp_dif_c")
        # print (xp_dif_c)
        xp_ratio_c = xp_dif_c / (max_xp_c - min_xp_c)
        # print("xp_ratio_c")
        # print (xp_ratio_c)
        # print ("--------")
        self.screen.blit(small_bar, (ST_POS[0] + ST_WIDTH - 100, ST_POS[1] + 65))
        self.screen.blit(silver_line, (ST_POS[0] + ST_WIDTH - 100, ST_POS[1] + 65),
                         (0, 0, 80 * xp_ratio_c, 5))
        ####################
        mov_sp = str(self.player.movement_speed / 100)
        self.write("Active Spell :", (ST_POS[0] + ST_WIDTH - 220, ST_POS[1] + 80))
        if self.player.active_spell:
            self.write(self.player.active_spell.name, (ST_POS[0] + ST_WIDTH - 140, ST_POS[1] + 80))
        self.write("Active Effects :", (ST_POS[0] + ST_WIDTH - 220, ST_POS[1] + 100))
        self.player.active_effects_lib.show(self.screen, (ST_POS[0] + ST_WIDTH - 120, ST_POS[1] + 100))
        self.write("Movement :" + mov_sp, (ST_POS[0] + ST_WIDTH - 220, ST_POS[1] + 120))
        self.write("Avoid mod : " + str(self.player.stealth * 3) + " pix",
                   (ST_POS[0] + ST_WIDTH - 220, ST_POS[1] + 140))

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
            in_dt = self.clock.tick(FPS) / 1000
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
                for wall in self.act_lvl.walls:
                    pygame.draw.rect(self.map_surface, (70, 30, 170), self.camera.apply_rect(wall.rect), 1)
                for lava in self.act_lvl.lavas:
                    pygame.draw.rect(self.map_surface, (230, 0, 0), self.camera.apply_rect(lava.rect), 1)
                for player in self.player_group:
                    if isinstance(player, Player):
                        pygame.draw.rect(self.map_surface, (100, 255, 100), self.camera.apply_rect(player.hit_rect), 1)
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
        self.spell_book_button.show_button(self.screen)
        if self.paused:
            self.screen.blit(dim_screen, (MAP_TOPLEFT))
            #### STANY SPECJALNE
            ### NEXT LEVEL
            if self.player.attribute_points > 0:
                self.h_write("NEXT LEVEL", (MAP_WIDTH / 2 - 100, MAP_HEIGHT / 2 - 10), "gothic", 36, (WHITE))
            ### TREASURE CHEST
            if self.ph_treasure_inv:
                self.blit_alpha(self.screen, treasure_bcg_img, (MAP_TOPLEFT[0] + 120, MAP_TOPLEFT[1] + 120), 220)
                self.treasure_inv.show_inv(self.screen, MAP_TOPLEFT[0] + 200, MAP_TOPLEFT[1] + 350)
            ### SPELL BOOK
            elif self.ph_spell_book:
                self.player.spell_book.show(self.screen)
                self.cast_button.show_button(self.screen)
            # DIALOG BOX
            elif self.dialog_in_progress:
                self.active_dialog.show(self.screen)
        #### RYSUJEMY TEKST ROBOCZY
        self.write(str(self.clock.get_fps()), (0, 0))
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
