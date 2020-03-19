import typing
from events.event import Event
from data import *
import spells

pygame.init()

snd_folder = path.join(path.dirname(__file__), 'sound')
pick_item_snd = pygame.mixer.Sound(path.join(snd_folder, 'pick_item.wav'))
click_snd = pygame.mixer.Sound(path.join(snd_folder, 'click2.wav'))
wear_item_snd = pygame.mixer.Sound(path.join(snd_folder, 'wear_item.wav'))
drink_snd = pygame.mixer.Sound(path.join(snd_folder, 'drink.wav'))


class Slot:
    def __init__(self, img, szer = 32, wys = 32):
        self.szer = szer
        self.wys = wys
        self.img = pygame.transform.scale(img, (self.szer, self.wys))
        self.rect = self.img.get_rect()
        self.item = False
        self.occ = False
        self.type = False

    def show_slot(self,surface,x,y):
        self.rect.x = x
        self.rect.y = y
        surface.blit(self.img,(self.rect.x, self.rect.y))
        if self.item:
            surface.blit(self.item.b_image,(self.rect.x, self.rect.y))

    def check_if_clicked(self,pos_cl):
        self.pos_cl = pos_cl
        if self.rect.x + self.szer > self.pos_cl[0] > self.rect.x and (self.rect.y + self.wys > self.pos_cl[1] > self.rect.y):
            return True

    def check_itemslot_to_item_corr(self,pos_cl,item_to_check):
        self.item_to_check = item_to_check
        self.pos_cl = pos_cl
        if self.rect.x + self.szer > self.pos_cl[0] > self.rect.x and (self.rect.y + self.wys > self.pos_cl[1] > self.rect.y):
            if self.item_to_check.type == self.type:
                print ("TYP ZGODNY")
                return True

    def define_type(self,type):
        self.type = type

    def put_item(self, item):
        if self.occ == False:
            self.item = item
            self.occ = True
            return True


    def pick_item(self):
        if self.occ == True:
            self.item_picked = self.item
            pygame.mixer.Sound.play(pick_item_snd)
            self.item = False
            self.occ = False
            return self.item_picked


class Inventory:
    def __init__(self, slot_img, width = 8, height = 5):
        self.item_slots = []
        self.width = width
        self.height = height
        self.slot_img = slot_img
        for y in range (self.height):
            for x in range (self.width):
                self.item_slots.append(Slot(self.slot_img))

    def show_inv(self, surface, start_x_pos = 600, start_y_pos = 400):
        self.start_x_pos = start_x_pos
        self.start_y_pos = start_y_pos
        self.surface = surface
        self.counter = 0
        for y in range (self.height):
            for x in range (self.width):
                self.item_slots[self.counter].show_slot(self.surface,self.start_x_pos + (x*32), self.start_y_pos + (y*32))
                self.counter +=1

    def return_no_items(self):
        counter = 0
        for i in self.item_slots:
            if i.item:
                counter += 1
        return counter

    def return_item_list(self):
        item_list = []
        for i in self.item_slots:
            if i.item:
                item_list.append(i.item)
        return item_list

    def find_free_slot(self):
        self.free_slots = []
        for i in self.item_slots:
            if i.item == False:
                self.free_slots.append(i)
        return self.free_slots

    def check_space(self):
        self.space = 0
        for i in self.item_slots:
            if i.item == False:
                self.space += 1
        return self.space

    def find_item(self, item):
        for i in self.item_slots:
            if i.item == item:
                return True

    def put_in_first_free_slot(self, item):
        self.item = item
        self.space = self.check_space()
        if self.space > 0:
            for i in self.item_slots:
                if i.item == False:
                    i.put_item(self.item)
                    return True
        else:
            print ("INV PELNY!")
            return False

    def check_if_clicked(self,pos_cl):
        self.pos_cl = pos_cl
        for i in self.item_slots:
            if i.rect.x + i.szer > self.pos_cl[0] > i.rect.x and (i.rect.y + i.wys > self.pos_cl[1] > i.rect.y):
                return True

    def pick_item_from_inv(self,pos_cl):
        self.pos_cl = pos_cl
        for i in self.item_slots:
            if i.rect.x + i.szer > self.pos_cl[0] > i.rect.x and (i.rect.y + i.wys > self.pos_cl[1] > i.rect.y):
                #print ("NACISKASZ NA ITEM_SLOT z INV")
                #print (str(i.rect.x))
                #print (str(i.rect.y))
                if i.item:
                    self.item_picked = i.pick_item()
                    #print (self.item_picked.name)
                    pygame.mixer.Sound.play(pick_item_snd)
                    return self.item_picked

    def choose_book_from_inv(self,pos_cl):
        self.pos_cl = pos_cl
        for i in self.item_slots:
            if i.rect.x + i.szer > self.pos_cl[0] > i.rect.x and (i.rect.y + i.wys > self.pos_cl[1] > i.rect.y):
                #print("NACISKASZ NA BOOK Z INV MAGIC_G")
                # print (str(i.rect.x))
                # print (str(i.rect.y))
                if i.item:
                    self.item_picked = i.choose_book()
                    pygame.mixer.Sound.play(pick_item_snd)
                    return self.item_picked

    def remove_item(self,item):
        for i in self.item_slots:
            if i.item == item:
                #print ("jest")
                i.item = False
                i.occ = False

    def put_item_to_inv(self,pos_cl,item):
        self.pos_cl = pos_cl
        self.item = item
        for i in self.item_slots:
            if i.rect.x + i.szer > self.pos_cl[0] > i.rect.x and (i.rect.y + i.wys > self.pos_cl[1] > i.rect.y):
                if i.occ == False:
                    #print("ODKLADASZ ITEM na INV")
                    self.item.status = 0
                    pygame.mixer.Sound.play(pick_item_snd)
                    i.put_item(self.item)
                    return True ## DO EWENTTAULNEGO WYJATKU GDY ZAJETY


class RadioButton:
    def __init__(self, img, img_h, x, y):
        self.img = img
        self.img_h = img_h
        self.rect = self.img.get_rect()
        self.active = True
        self.highlighted = False
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def show_button(self,surface):
        if not self.highlighted:
            surface.blit(self.img, (self.rect.x, self.rect.y))
        else:
            surface.blit(self.img_h, (self.rect.x, self.rect.y))

    def check_if_highlight(self, pos_hl):
        if self.active:
            if self.rect.x + self.width > pos_hl[0] > self.rect.x and\
                    (self.rect.y + self.height > pos_hl[1] > self.rect.y):
                self.highlighted = True
                return True
            else:
                self.highlighted = False
                return False
        else:
            self.highlighted = False
            return False

    def check_if_clicked(self,pos_cl):
        self.pos_cl = pos_cl
        if self.active:
            if self.rect.x + self.width > self.pos_cl[0] > self.rect.x and\
                    (self.rect.y + self.height > self.pos_cl[1] > self.rect.y):
                pygame.mixer.Sound.play(click_snd)
                return True

    def check_if_clicked_even_inactive(self,pos_cl):
        self.pos_cl = pos_cl
        if self.rect.x + self.width > self.pos_cl[0] > self.rect.x and\
                (self.rect.y + self.height > self.pos_cl[1] > self.rect.y):
            pygame.mixer.Sound.play(click_snd)
            return True

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False


class Button:
    def __init__(self, img, img_h, szer, wys, text, x, y, font_size):
        self.text = text
        self.szer = szer
        self.wys = wys
        self.img = pygame.transform.scale(img, (self.szer,self.wys))
        self.img_h = pygame.transform.scale(img_h, (self.szer, self.wys))
        self.rect = self.img.get_rect()
        self.active = True
        self.highlighted = False
        self.font_size = font_size
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    def show_button(self,surface, font):
        self.act_color = (255, 255, 255)
        self.text_surface = font.render(self.text, True, self.act_color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.topleft = (self.rect.x + 15, self.rect.y + 5)
        if not self.highlighted:
            surface.blit(self.img, (self.rect.x, self.rect.y))
            surface.blit(self.text_surface, (self.text_rect.x, self.text_rect.y))
        else:
            surface.blit(self.img_h, (self.rect.x, self.rect.y))
            surface.blit(self.text_surface, (self.text_rect.x, self.text_rect.y))

    def check_if_highlight(self, pos_hl):
        if self.active:
            if self.rect.x + self.szer > pos_hl[0] > self.rect.x and (self.rect.y + self.wys > pos_hl[1] > self.rect.y):
                self.highlighted = True
                return True
            else:
                self.highlighted = False
                return False
        else:
            self.highlighted = False
            return False

    def check_if_clicked(self,pos_cl):
        self.pos_cl = pos_cl
        if self.active:
            if self.rect.x + self.szer > self.pos_cl[0] > self.rect.x and (self.rect.y + self.wys > self.pos_cl[1] > self.rect.y):
                pygame.mixer.Sound.play(click_snd)
                return True

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False


class EButton:
    def __init__(self, img, x, y):
        self.img = pygame.Surface((74, 74), pygame.HWSURFACE | pygame.SRCALPHA)
        self.h_img = img
        self.rect = self.img.get_rect()
        self.active = True
        self.highlighted = False
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def show_button(self,surface):
        self.img.fill((0,0,0,0))
        if self.highlighted:
            self.img.blit(self.h_img,(0,0))
        surface.blit(self.img,(self.rect.x, self.rect.y))

    def check_if_highlight(self, pos_hl):
        if self.active:
            if self.rect.x + self.width > pos_hl[0] > self.rect.x and\
                    (self.rect.y + self.height > pos_hl[1] > self.rect.y):
                self.highlighted = True
                return True
            else:
                self.highlighted = False
                return False
        else:
            self.highlighted = False
            return False

    def check_if_clicked(self,pos_cl):
        self.pos_cl = pos_cl
        if self.active:
            if self.rect.x + self.width > self.pos_cl[0] > self.rect.x and\
                    (self.rect.y + self.height > self.pos_cl[1] > self.rect.y):
                pygame.mixer.Sound.play(click_snd)
                return True

    def check_if_clicked_even_inactive(self,pos_cl):
        self.pos_cl = pos_cl
        if self.rect.x + self.width > self.pos_cl[0] > self.rect.x and\
                (self.rect.y + self.height > self.pos_cl[1] > self.rect.y):
            pygame.mixer.Sound.play(click_snd)
            return True

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False


class QuestBook:
    def __init__(self, game):
        self.game = game
        self.pages = 5
        self.quests = []
        self.image = pygame.Surface((MAP_WIDTH, 466), pygame.HWSURFACE | pygame.SRCALPHA)
        self.image.blit(spellbook_bcg_img, (0, 0))
        self.pos = (5,100)
        self.act_page = 0
        self.next_page_button = EButton(next_page_img,549,377)
        self.prev_page_button = EButton(prev_page_img,18,376)

    def add_quest(self, quest):
        if len(self.quests)<11:
            self.quests.append(quest)
        else:
            print ("za dużo czarów")
            ### TO DO Usuwanie czarów

    def check_duplicate(self, quest):
        for i in self.quests:
            if i.name == quest.name:
                return True

    def update_buttons(self, mouse_pos):
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        mouse_x -= self.pos[0]
        mouse_y -= self.pos[1]
        self.mouse_pos = (mouse_x, mouse_y)
        # print ("mod_mouse a (%d, %d)" % self.mouse_pos)
        self.next_page_button.check_if_highlight(self.mouse_pos)
        self.prev_page_button.check_if_highlight(self.mouse_pos)

    def check_page_buttons(self, mouse_pos):
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        mouse_x -= self.pos[0]
        mouse_y -= self.pos[1]
        self.mouse_pos = (mouse_x, mouse_y)
        if self.next_page_button.check_if_clicked(self.mouse_pos):
            if self.act_page < self.pages:
                self.act_page += 1
        if self.prev_page_button.check_if_clicked(self.mouse_pos):
            if self.act_page > 0:
                self.act_page -= 1

    def show(self, screen, pos = (5,100)):
        self.image.blit(spellbook_bcg_img, (0, 0))
        self.next_page_button.show_button(self.image)
        self.prev_page_button.show_button(self.image)
        self.pos = pos
        x_pos = 40
        ## TWORZE DWUWYMIAROWA TABLICE CZAROW DO ICH WYSWIETLANIA
        pages = [[] * self.pages for i in range(9)]
        page_counter = 0
        quest_counter = 0
        for quest in self.quests:
            quest.active = False
            pages[page_counter].append(quest)
            quest_counter += 1
            if quest_counter > 9:
                page_counter +=1
        counter = 0
        for i in pages[self.act_page]:
            i.active = True
            self.game.s_write(i.name, self.image, (x_pos + 80, 40 + counter * i.width),(BLACK))
            self.game.s_write("Goal: ", (x_pos + 80, 70 + counter * i.width),(BLACK))
            self.game.s_write("Reward: ", self.image,(x_pos + 180, 70 + counter * i.width),(BLACK))
            counter += 1
            if counter >= 5:
                x_pos = 330
                counter = 0
        self.game.s_write((str(self.act_page + 1)),self.image,(160,428),(BLACK))
        self.game.s_write((str(self.act_page + 1)), self.image, (480, 428), (BLACK))
        screen.blit(self.image,(pos))


class SpellBook:
    def __init__(self, game):
        self.game = game
        self.pages = 5
        self.spells = []
        self.image = pygame.Surface((MAP_WIDTH, 466), pygame.HWSURFACE | pygame.SRCALPHA)
        self.image.blit(spellbook_bcg_img, (0, 0))
        self.pos = (5,100)
        self.spellgenerator = spells.SpellGenerator()
        self.act_page = 0
        self.next_page_button = EButton(next_page_img,549,377)
        self.prev_page_button = EButton(prev_page_img,18,376)

    def add_spell(self, spell):
        if len(self.spells) < 50:
            self.spells.append(spell)
        else:
            print ("za dużo czarów")
            ### TO DO Usuwanie czarów

    def add_spell_by_name(self, name):
        self.spells.append(self.spellgenerator.get_spell_by_name(name))

    def check_duplicate(self, spell):
        for i in self.spells:
            if i.name == spell.name:
                return True

    def update_buttons(self, mouse_pos):
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        mouse_x -= self.pos[0]
        mouse_y -= self.pos[1]
        self.mouse_pos = (mouse_x, mouse_y)
        # print ("mod_mouse a (%d, %d)" % self.mouse_pos)
        self.next_page_button.check_if_highlight(self.mouse_pos)
        self.prev_page_button.check_if_highlight(self.mouse_pos)

    def check_page_buttons(self, mouse_pos):
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        mouse_x -= self.pos[0]
        mouse_y -= self.pos[1]
        self.mouse_pos = (mouse_x, mouse_y)
        if self.next_page_button.check_if_clicked(self.mouse_pos):
            if self.act_page < self.pages:
                self.act_page += 1
        if self.prev_page_button.check_if_clicked(self.mouse_pos):
            if self.act_page > 0:
                self.act_page -= 1

    def show(self, screen, pos = (5,100)):
        self.image.blit(spellbook_bcg_img, (0, 0))
        self.next_page_button.show_button(self.image)
        self.prev_page_button.show_button(self.image)
        self.pos = pos
        x_pos = 40
        ## TWORZE DWUWYMIAROWA TABLICE CZAROW DO ICH WYSWIETLANIA
        pages = [[] * self.pages for i in range(9)]
        page_counter = 0
        spell_counter = 0
        for spell in self.spells:
            spell.active = False
            pages[page_counter].append(spell)
            spell_counter += 1
            if spell_counter > 9:
                page_counter +=1
        #print ("pages[1][0]" + pages[1][0].name)
        counter = 0
        for i in pages[self.act_page]:
            i.active = True
            i.show_spell(self.image, x_pos, 40 + counter * i.width)
            if i == self.game.player.selected_spell:
                pygame.draw.rect(self.image,(0,180,0),(x_pos,40+counter*i.width,i.width,i.height),2)
            self.game.s_write(i.name, self.image, (x_pos + 80, 40 + counter * i.width),(BLACK))
            self.game.s_write("Cost: " + str(i.cost) + " MP", self.image, (x_pos + 80, 70 + counter * i.width),(BLACK))
            self.game.s_write("INT: "+ str(i.min_int),self.image,(x_pos + 180, 70 + counter * i.width),(BLACK))
            if i.type == "defensive":
                if i.subtype == "cure":
                    self.game.s_write("Strength: " + str(i.damage + 2 * self.game.player.intellect),
                                      self.image, (x_pos + 80, 55 + counter * i.width), (BLACK))
                if i.subtype == "stone skin":
                    self.game.s_write("Armor: " + str(20 + self.game.player.intellect),
                                      self.image, (x_pos + 80, 55 + counter * i.width), (BLACK))
                    self.game.s_write("Duration: " + str(15 + (3 * self.game.player.intellect)) + "s",
                                      self.image, (x_pos + 80, 85 + counter * i.width), (BLACK))
                if i.subtype == "haste":
                    self.game.s_write("Speed bonus: " + str(5 + self.game.player.intellect),
                                      self.image, (x_pos + 80, 55 + counter * i.width), (BLACK))
                    self.game.s_write("Duration: " + str(15 + (3 * self.game.player.intellect)) + "s",
                                      self.image, (x_pos + 80, 85 + counter * i.width), (BLACK))
                if i.subtype == "iron skin":
                    self.game.s_write("Armor: " + str(20 + (2 * self.game.player.intellect)),
                                      self.image, (x_pos + 80, 55 + counter * i.width), (BLACK))
                    self.game.s_write("Duration: " + str(15 + (3 * self.game.player.intellect)) + "s",
                                      self.image, (x_pos + 80, 85 + counter * i.width), (BLACK))
                if i.subtype == "invisibility":
                    self.game.s_write("Duration: " + str(15 + (3 * self.game.player.intellect)) + "s",
                                      self.image, (x_pos + 80, 55 + counter * i.width), (BLACK))
            if i.type == "offensive":
                if i.bullet_nr > 1:
                    self.game.s_write("Damage: " + str(i.bullet_nr) + "x " + str(i.damage + self.game.player.intellect), self.image, (x_pos + 80, 55 + counter * i.width),(BLACK))
                else:
                    if i.subtype == "poison cloud":
                        self.game.s_write("Damage: 0",
                                          self.image, (x_pos + 80, 55 + counter * i.width), (BLACK))
                    else:
                        self.game.s_write("Damage: " + str(i.damage + self.game.player.intellect),
                                      self.image, (x_pos + 80, 55 + counter * i.width), (BLACK))
                if i.blow_effect:
                    self.game.s_write("Blow Dmg: " + str(i.blow_damage + self.game.player.intellect) + "/s",self.image, (x_pos + 180, 55 + counter * i.width),(BLACK))
                if i.freeze_effect:
                    self.game.s_write("Freeze time: " + str(i.freeze_effect + self.game.player.intellect) + "s", self.image,
                                      (x_pos + 180, 55 + counter * i.width), (BLACK))
            counter += 1
            if counter >= 5:
                x_pos = 330
                counter = 0
        self.game.s_write((str(self.act_page + 1)),self.image,(160,428),(BLACK))
        self.game.s_write((str(self.act_page + 1)), self.image, (480, 428), (BLACK))
        screen.blit(self.image,(pos))

    def check_spell(self, mouse_pos):
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        mouse_x -= self.pos[0]
        mouse_y -= self.pos[1]
        self.mouse_pos = (mouse_x, mouse_y)
        #print ("mod_mouse a (%d, %d)" % self.mouse_pos)
        for spell in self.spells:
            if spell.check_if_clicked(self.mouse_pos):
                #print ("chose spell")
                return spell
        return False


class Spell:
    def __init__(self, name, sb_img, bullet_img, blow_anim_images, type, subtype, cost, min_int,
                 damage, hit_rate, bullet_type, bullet_nr, bullet_speed, bullet_range,
                  blow_effect,  blow_radius_sizer, blow_damage, blow_duration,
                 freeze_effect, slow_effect, burn_effect,
                 cast_sound):
        self.name = name
        self.active = True
        self.image = sb_img
        self.rect = self.image.get_rect()
        self.width = 64
        self.height = 64
        self.bullet_img = bullet_img
        self.blow_anim_img = blow_anim_images
        self.type = type
        self.subtype = subtype
        self.cost = cost
        self.min_int = min_int
        self.damage = damage
        self.hit_rate = hit_rate
        self.bullet_type = bullet_type
        self.bullet_nr = bullet_nr
        self.bullet_speed = bullet_speed
        self.bullet_range = bullet_range
        self.blow_effect = blow_effect
        self.blow_radius_sizer = blow_radius_sizer
        self.blow_damage = blow_damage
        self.blow_duration = blow_duration
        self.freeze_effect = freeze_effect
        self.slow_effect = slow_effect
        self.burn_effect = burn_effect
        self.cast_sound = cast_sound

    def show_spell(self, surface, x, y):
        self.rect.x = x
        self.rect.y = y
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def check_if_clicked(self,pos_cl):
        self.pos_cl = pos_cl
        if self.active:
            if self.rect.x + self.width > self.pos_cl[0] > self.rect.x and\
                    (self.rect.y + self.height > self.pos_cl[1] > self.rect.y):
                pygame.mixer.Sound.play(click_snd)
                return True

    def cast(self, player):
        ### TYLKO DO CZARÓW DEFENSYWNYCH:
        if self.type == "defensive":
            if player.act_mana >= self.cost:
                pygame.mixer.Sound.play(self.cast_sound)
                player.act_mana -= self.cost
                if self.subtype == "cure":
                    player.act_hp += self.damage + (2*player.intellect)
                    if player.act_hp > player.max_hp:
                        player.act_hp = player.max_hp
                if self.subtype == "stone skin":
                    player.active_effects_lib.add_effect(ActiveEffect("stone skin",e_stoneskin_ico,
                                                                      20 + player.intellect,15 + (3 * player.intellect)))
                if self.subtype == "haste":
                    player.active_effects_lib.add_effect(ActiveEffect("haste",e_haste_ico,
                                                                      5 + player.intellect, 15 + 3 * player.intellect))
                if self.subtype == "invisibility":
                    player.active_effects_lib.add_effect(ActiveEffect("invisibility",e_invisibility_ico,
                                                                      1,15 + (3 * player.intellect)))
                if self.subtype == "iron skin":
                    player.active_effects_lib.add_effect(ActiveEffect("iron skin",e_ironskin_ico,
                                                                      20 + (2 * player.intellect),15 + (3 * player.intellect)))
            else:
                pygame.mixer.Sound.play(empty_spell_snd)
                print ("Brak MANA")


class ActiveEffect:
    def __init__(self, name, icon, strength,  duration):
        self.name = name
        self.icon = icon
        self.strength = strength
        self.duration = duration
        self.effect_time = 0

    def update_effect(self, unpaused_dt):
        ### JEZELI EFFEKT MA OGRANICZONY CZAS:
        if self.duration:
            self.effect_time += unpaused_dt
            #print (self.effect_time)
            if self.effect_time >= self.duration:
                return True


class ActiveEffectsLibrary:
    def __init__(self, game):
        self.active_effects = []
        self.game = game

    def show(self, screen, pos):
        counter = 0
        self.pos = pos
        for i in self.active_effects:
            screen.blit(i.icon,(pos[0] + counter * 16, pos[1]))
            counter += 1
        # ZROBIC WARUNEK GDY ZA DUZO EFEKTÓW (za mało miejsca..)

    def update_effects(self):
        ### JEZELI CZAS MINĄL - USUWAM EFEKT
        for effect in self.active_effects:
            if effect.update_effect(self.game.unpaused_dt):
                self.remove_effect(effect)
                self.game.player.update_stats()

    def add_effect(self, effect):
        for act_effect in self.active_effects:
            if act_effect.name == effect.name:
                self.active_effects.remove(act_effect)
        self.active_effects.append(effect)

    def remove_effect(self, effect):
        for act_effect in self.active_effects:
            if act_effect.name == effect.name:
                self.active_effects.remove(act_effect)

    def remove_fav_dis_weapons_effects(self):
        for act_effect in self.active_effects:
            if act_effect.name == "favourite weapon":
                self.active_effects.remove(act_effect)
            if act_effect.name == "disliked weapon":
                self.active_effects.remove(act_effect)

    def remove_fav_dis_armors_effects(self):
        for act_effect in self.active_effects:
            if act_effect.name == "favourite armor":
                self.active_effects.remove(act_effect)
            if act_effect.name == "disliked armor":
                self.active_effects.remove(act_effect)


class Dialog:
    def __init__(self, game, npc):
        self.game = game
        self.npc = npc
        self.conversation = []
        #self.events_that_has_to_happen = []

    def load_text(self,ifnpc,branch,step,text,compl_event,block_event,ask,goto):
        self.conversation.append(Text(ifnpc,branch,step,text,compl_event,block_event,ask,goto))
        #self.events_that_has_to_happen.append(compl_event)
        #if compl_event:
        #    self.game.events_manager.subscribes_by_id(compl_event, self.store_event)

    #def store_event(self, event):
    #    try:
    #        self.events_ids.remove(event.id)
    #    except ValueError:
    #        pass

    def find_next_step(self, act_branch, act_step):
        ##### SORTUJE PO nr GALĘzi
        ##### TWORZE LOKALNA LISTE GALEZI ROZMOW, ODBLOKOWANYCH
        branch_nrs = []
        for text in self.conversation:
            if text.compl_event:
                for game_event in self.game.events_manager.history():
                    if game_event.id == text.compl_event:
                        #print ("EVENT COMPLETED, UNBLOCK DIALOG BRANCH!")
                        branch_nrs.append(text.branch)
            # if text.compl_event not in self.events_that_has_to_happen:
            #        print("EVENT COMPLETED, UNBLOCK DIALOG BRANCH!")
            #        branch_nrs.append(text.branch)
            else:
                branch_nrs.append(text.branch)
        ###### SORTUJE (na wszelki wypadek) ##
        branch_nrs.sort()
        last_branch = branch_nrs[-1]
        branch_nrs = list(dict.fromkeys(branch_nrs))
        ###### TWORZE ITERACJE
        branch_iter = iter(branch_nrs)
        cont_act_branch = True
        ### JEZELI NIE JEST OSTATNI to przegladam kolejne itaracje galezi (branch) dialogu
        if not act_branch == last_branch:
            while cont_act_branch:
                a = next(branch_iter)
                if a == act_branch:
                    next_branch = next(branch_iter)
                    cont_act_branch = False
            ##### GDY JEST TA SAMA GALAZ DODAJE +1 do DIALOG.STEP
            for text in self.conversation:
                if text.branch == act_branch and text.step == (act_step + 1):
                    return text
            ##### GDY NIE MA WIECEJ KROKOW w DANEJ GALEZI ZERUJE STEP i ZMIENIAM NA KOLEJNA GALAZ
            for text in self.conversation:
                if text.branch == next_branch and text.step == 0:
                    return text
        ##### JEZELI OSTATNIA GALAZ DIALOGU:
        else:
            for text in self.conversation:
                if text.branch == act_branch and text.step == (act_step + 1):
                    return text
        ####### JEZELI NIE MA JUZ WIECEJ GALEZI ANI KROKÓW to koniec
        return False

class Text:
    def __init__(self, ifnpc, branch, step, text, compl_event, block_event, ask, goto):
        ### ZAWIERAC BEDZIE CALA WYPOWIEDZ
        ### PODZIELIMY NA linijki tekstu
        self.ifnpc = ifnpc
        self.branch = branch
        self.step = step
        self.text = text
        self.ask = ask
        self.goto = goto
        self.compl_event = compl_event
        self.block_event = block_event
        self.welcome = False
        self.last = False
        #self.goto = (branch, step)

class DialogBox:
    def __init__(self, game):
        self.game = game
        self.pos = (50, 120)
        self.image = dialogbox_img.copy()
        self.ok_button = RadioButton(rad_ok_img,rad_ok_h_img,178,290)
        self.resp_but_1 = RadioButton(rad_but_img,rad_but_h_img,55,125)
        self.resp_but_2 = RadioButton(rad_but_img, rad_but_h_img, 55, 150)
        self.resp_but_3 = RadioButton(rad_but_img, rad_but_h_img, 55, 175)
        self.resp_but_4 = RadioButton(rad_but_img, rad_but_h_img, 55, 200)
        self.resp_buttons = [self.resp_but_1,self.resp_but_2,self.resp_but_3,self.resp_but_4]
        self.npc = False
        self.actual_text = False
        #self.write("TEST", 0)

    def start_conversation(self,npc):
        print ("STARTING CONVERSATION")
        self.npc = npc
        self.dialog_data = self.npc.dialog_data
        #### SZUKAM POCZATKU DIALOGU:
        for text in self.dialog_data.conversation:
            if text.compl_event == f'{self.npc.name} has been encountered.':
                if self.game.events_manager.find_npc_encounter_event(self.npc.name):
                    self.actual_text = text
                    break
            if text.branch == 0 and text.step ==0:
                self.actual_text = text
        self.write_actual_text()

    def write_actual_text(self):
        if self.actual_text.ifnpc:
            speaker = self.npc
        else:
            speaker = self.game.player
        self.write_line(speaker, self.actual_text.text)
        #except:
        #   print ("ERROR DONT HAVE ACTUAL TEXT TO BLIT")

    def next_ask_step(self, goto):
        for text in self.dialog_data.conversation:
            if text.branch == goto[0] and text.step == goto[1]:
                self.actual_text = text
                print("FOUND NEXT STEP BY RECIVING ANSWER")
                break
        self.configure_text()

    def next_d_step(self):
        #print ("next_d_step")
        if self.actual_text.goto:
            print ("this parse has goto with branch:")
            print (self.actual_text.goto[0])
            print("this parse has goto with step:")
            print(self.actual_text.goto[1])
            for text in self.dialog_data.conversation:
                if text.branch == self.actual_text.goto[0] and text.step == self.actual_text.goto[1]:
                    self.actual_text = text
                    print("FOUND NEXT STEP BY GOTO METHOD")
                    break
        else:
            #print ("this parse dont have goto")
            self.actual_text = self.dialog_data.find_next_step(self.actual_text.branch,self.actual_text.step)
        self.configure_text()

    def configure_text(self):
        #####################################################
        ### KONFIGURACJA UKLADU - NOWY AKTUALNY TEKST DO WYSWIETLENIA! #
        if self.actual_text:
            ## JEZELI JEST TO PYTANIE AKTYWUJE PRZYCISKI ODPOWIEDZI I PISZE ODPOWIEDZI:
            if self.actual_text.ask:
                self.write_actual_text()
                how_many_answers = len(self.actual_text.ask)
                self.ok_button.deactivate()
                if how_many_answers == 1:
                    self.resp_but_1.activate()
                    print(self.actual_text.ask[0][0])
                    self.write(self.actual_text.ask[0][0], 1)
                elif how_many_answers == 2:
                    self.resp_but_1.activate()
                    self.resp_but_2.activate()
                    print(self.actual_text.ask[0][0])
                    print(self.actual_text.ask[1][0])
                    self.write(self.actual_text.ask[0][0], 1)
                    self.write(self.actual_text.ask[1][0], 2)
                elif how_many_answers == 3:
                    self.resp_but_1.activate()
                    self.resp_but_2.activate()
                    self.resp_but_3.activate()
                    print(self.actual_text.ask[0][0])
                    print(self.actual_text.ask[1][0])
                    print(self.actual_text.ask[2][0])
                    self.write(self.actual_text.ask[0][0], 1)
                    self.write(self.actual_text.ask[1][0], 2)
                    self.write(self.actual_text.ask[2][0], 3)
                elif how_many_answers == 4:
                    self.resp_but_1.activate()
                    self.resp_but_2.activate()
                    self.resp_but_3.activate()
                    self.resp_but_4.activate()
                    self.write(self.actual_text.ask[0][0], 1)
                    self.write(self.actual_text.ask[1][0], 2)
                    self.write(self.actual_text.ask[2][0], 3)
                    self.write(self.actual_text.ask[3][0], 4)
            ## JEZELI ZWYKLY TEKST
            else:
                self.ok_button.activate()
                for i in self.resp_buttons:
                    i.deactivate()
                self.write_actual_text()
        ### JEZELI NIE MA JUZ AKTULANEGO TESKTU KONCZE DIALOG I ZAPISUJE ZE ODNALEZIONY NPC
        else:
            self.clear()
            if not self.npc.encountered:
                self.game.events_manager.emit(Event(id=f'{self.npc.name} has been encountered.'))
                self.npc.encountered = True
            self.game.dialog_in_progress = False
            self.game.paused = False

    def add_line(self, text) -> None:
        pass

    def write_line(self, speaker, text) -> None:
        self.clear()
        self.image.blit(pygame.transform.scale(speaker.image, (48, 48)), (210, 18))
        self.game.s_write(speaker.name, self.image, (85, 35), WHITE)
        text_len = len(text)
        text_line_1 = ""
        text_line_2 = ""
        text_line_3 = ""
        text_line_4 = ""
        #print (text_len)
        ## MAX LINE LENGTH 160~!
        if text_len < 40:
            text_line_1 = text[:40]
        if text_len >= 40 and text_len <80:
            text_line_1 = text[:40]
            text_line_2 = text[40:80]
        if text_len >=80 and text_len <120:
            text_line_1 = text[:40]
            text_line_2 = text[40:80]
            text_line_3 = text[80:120]
        if text_len >=120 and text_len <160:
            text_line_1 = text[:40]
            text_line_2 = text[40:80]
            text_line_3 = text[80:120]
            text_line_4 = text[120:160]
        self.write(text_line_1, 0)
        self.write(text_line_2, 1)
        self.write(text_line_3, 2)
        self.write(text_line_4, 3)

    def write(self, txt, ln):
        self.game.s_write(txt,self.image, (85, 100 + ln * 24), (WHITE))

    def clear(self):
        self.image = dialogbox_img.copy()

    def show(self, screen):
        if not self.actual_text.ask:
            self.ok_button.show_button(self.image)
        else:
            self.show_response_buttons()
        screen.blit(self.image, self.pos)

    def show_response_buttons(self):
        for i in self.resp_buttons:
            if i.active:
                i.show_button(self.image)

    def update(self, mouse_pos):
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        mouse_x -= self.pos[0]
        mouse_y -= self.pos[1]
        self.mouse_pos = (mouse_x, mouse_y)
        self.ok_button.check_if_highlight(self.mouse_pos)
        for i in self.resp_buttons:
            i.check_if_highlight(self.mouse_pos)

    def check_buttons(self, mouse_pos):
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        mouse_x -= self.pos[0]
        mouse_y -= self.pos[1]
        self.mouse_pos = (mouse_x, mouse_y)
        if self.ok_button.active:
            if self.ok_button.check_if_clicked(self.mouse_pos):
                self.next_d_step()
        if self.resp_but_1.active:
            if self.resp_but_1.check_if_clicked(self.mouse_pos):
                if self.actual_text.ask[0][1]:
                    self.actual_text.ask[0][1].get_quest()
                self.next_ask_step(self.actual_text.ask[0][2])
        if self.resp_but_2.active:
            if self.resp_but_2.check_if_clicked(self.mouse_pos):
                if self.actual_text.ask[1][1]:
                    self.actual_text.ask[1][1].get_quest()
                self.next_ask_step(self.actual_text.ask[1][2])
        if self.resp_but_3.active:
            if self.resp_but_3.check_if_clicked(self.mouse_pos):
                if self.actual_text.ask[2][1]:
                    self.actual_text.ask[2][1].get_quest()
                self.next_ask_step(self.actual_text.ask[2][2])
        if self.resp_but_4.active:
            if self.resp_but_4.check_if_clicked(self.mouse_pos):
                if self.actual_text.ask[3][1]:
                    self.actual_text.ask[3][1].get_quest()
                self.next_ask_step(self.actual_text.ask[3][2])


class Quest:
    def __init__(self, game, name, level_req, mobs_to_kill,
                 items_to_collect,
                 tiles_to_explore,
                 npcs_to_encounter,
                 reward_xp, reward_gold):
        self.game = game
        self.name = name
        self.level_req = level_req
        self.goal = QuestGoal()
        for i in mobs_to_kill:
            self.goal.add_mob_to_kill(i)
        for i in items_to_collect:
            self.goal.add_item_to_collect(i)
        for i in tiles_to_explore:
            self.goal.add_tile_to_explore(i)
        for i in npcs_to_encounter:
            self.goal.add_npc_to_encounter(i)
        self.reward_xp = reward_xp
        self.reward_gold = reward_gold
        self.completed = False
        self.in_progress = False
        self.visible = False
        self.start_time = 0

    def check_if_completed(self):
        print ("Sprawdzam czy wykonałeś quest")
        if self.goal.mobs_to_kill:
            for i in self.goal.mobs_to_kill:
                for ii in self.game.player.defeated_enemies:
                    if i == ii.name:
                        self.completed = True
                        print ("QUEST WYKONANO")
                        return True
        if self.goal.npcs_to_encounter:
            for i in self.goal.npcs_to_encounter:
                for ii in self.game.player.encountered_npcs:
                    if i == ii.name:
                        self.completed = True
                        self.game.events_manager.emit(Event(id=f'quest {self.name} has been completed.'))
                        print ("ODNALEZIONY NPC, QUEST WYKONANO")
                        return True

    def collect_reward(self):
        if self.completed:
            self.game.player.active_quests.remove(self)
            self.game.player.gold += self.reward_gold
            self.game.player.xp += self.reward_xp
            pygame.mixer.Sound.play(coin_snd)
            #### SEND INFO
            self.game.events_manager.emit(Event(id=f'quest {self.name} reward has been collected.'))
            self.game.player.completed_quests.append(self)
            print("NAGRODA ODEBRANA i QUEST ZAPISANY JAKO WYKONANY")

    def get_quest(self):
        if self not in self.game.player.active_quests:
            self.in_progress = True
            self.game.events_manager.emit(Event(id=f'got quest {self.name}'))
            self.game.player.active_quests.append(self)
            self.start_time = (int(self.game.player.score_time_played * 1000))



class QuestGoal:
    def __init__(self):
        self.mobs_to_kill = []
        self.items_to_collect = []
        self.tiles_to_explore = []
        self.npcs_to_encounter = []

    def add_mob_to_kill(self,mob):
        self.mobs_to_kill.append(mob)

    def add_item_to_collect(self,item):
        self.items_to_collect.append(item)

    def add_tile_to_explore(self,tile_pos):
        self.tiles_to_explore.append(tile_pos)

    def add_npc_to_encounter(self,npc):
        self.npcs_to_encounter.append(npc)










