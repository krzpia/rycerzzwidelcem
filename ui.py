import typing
import sys
from events.event import Event
from npcs import QuestGenerator
from data import *
import spells
import random
import sprites
pygame.init()

if getattr(sys, 'frozen', False): # PyInstaller adds this attribute
    # Running in a bundle
    CurrentPath = sys._MEIPASS
else:
    # Running in normal Python environment
    CurrentPath = path.dirname(__file__)

snd_folder = path.join(CurrentPath, 'sound')
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
                #print ("TYP ZGODNY")
                return True

    def define_type(self,type):
        self.type = type

    def put_item(self, item):
        if self.occ == False:
            self.item = item
            self.occ = True
            return True

    def clear(self):
        self.item = False
        self.occ = False

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

    def return_item_namecond_list(self):
        list = []
        for i in self.item_slots:
            if i.item:
                name = i.item.name
                if isinstance(i.item,sprites.Armor) or isinstance(i.item,sprites.Weapon):
                    cond = i.item.condition
                elif isinstance(i.item,sprites.Key):
                    cond = i.item.key
                elif isinstance(i.item, sprites.Gold_Item):
                    cond = i.item.gold
                elif isinstance(i.item, sprites.Arrow_Item):
                    cond = i.item.number
                else:
                    cond = False
                list.append((name,cond))
        return list

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
            print ("ERROR - INV PELNY!")
            return False

    def check_if_clicked(self,pos_cl):
        self.pos_cl = pos_cl
        for i in self.item_slots:
            if i.rect.x + i.szer > self.pos_cl[0] > i.rect.x and (i.rect.y + i.wys > self.pos_cl[1] > i.rect.y):
                #print("ITEM SLOT on INVENTORY")
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
                    #print ("ODKLADASZ PRZEDMIOT")
                    #print (self.item_picked.name)
                    pygame.mixer.Sound.play(pick_item_snd)
                    return self.item_picked

    def remove_item(self,item):
        for i in self.item_slots:
            if i.item == item:
                #print ("jest")
                i.item = False
                i.occ = False

    def remove_all(self):
        for i in self.item_slots:
            if i.item:
                i.clear()

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


class RepairInventory:
    def __init__(self, slot_img):
        self.item_slot = Slot(slot_img)

    def show_inv(self, surface, start_x_pos = 600, start_y_pos = 400):
        self.start_x_pos = start_x_pos
        self.start_y_pos = start_y_pos
        self.surface = surface
        self.item_slot.show_slot(self.surface,self.start_x_pos, self.start_y_pos)

    def return_item(self):
        if self.item_slot.item:
            return self.item_slot.item

    def check_free(self):
        if self.item_slot.item:
            #print ("Check free: False")
            return False
        else:
            #print("Check free: True")
            return True

    def put_in_slot(self, item):
        if self.check_free():
            self.item_slot.put_item(item)
            return True
        else:
            print ("ERROR - REPAIR SLOT PELNY!")
            return False

    def check_if_clicked(self,pos_cl):
        self.pos_cl = pos_cl
        if self.item_slot.rect.x + self.item_slot.szer > self.pos_cl[0] > self.item_slot.rect.x and (self.item_slot.rect.y + self.item_slot.wys > self.pos_cl[1] > self.item_slot.rect.y):
            return True

    def pick_item_from_inv(self,pos_cl):
        self.pos_cl = pos_cl
        if self.item_slot.rect.x + self.item_slot.szer > self.pos_cl[0] > self.item_slot.rect.x and (self.item_slot.rect.y + self.item_slot.wys > self.pos_cl[1] > self.item_slot.rect.y):
            #print ("NACISKASZ NA ITEM_SLOT z REPAIR INV")
            #print (str(i.rect.x))
            #print (str(i.rect.y))
            if self.item_slot.item:
                self.item_picked = self.item_slot.pick_item()
                #print (self.item_picked.name)
                pygame.mixer.Sound.play(pick_item_snd)
                return self.item_picked

    def remove_item(self,item):
        if self.item_slot.item == item:
            print ("USUWAM DANY PRZEDMIOT ZE SLOTU REPAIR")
            self.item_slot.item = False
            self.item_slot.occ = False

    def put_item_to_inv(self,pos_cl,item):
        self.pos_cl = pos_cl
        self.item = item
        if self.item_slot.rect.x + self.item_slot.szer > self.pos_cl[0] > self.item_slot.rect.x and (self.item_slot.rect.y + self.item_slot.wys > self.pos_cl[1] > self.item_slot.rect.y):
            if self.item_slot.occ == False:
                print("ODKLADASZ ITEM na SLOT REPAIR")
                self.item.status = 0
                pygame.mixer.Sound.play(pick_item_snd)
                self.item_slot.put_item(self.item)
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
    def __init__(self, img, img_h, szer, wys, text, x, y):
        self.text = text
        self.szer = szer
        self.wys = wys
        self.img = pygame.transform.scale(img, (self.szer,self.wys))
        self.img_h = pygame.transform.scale(img_h, (self.szer, self.wys))
        self.rect = self.img.get_rect()
        self.active = True
        self.highlighted = False
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    def show_button(self,surface, font):
        self.act_color = BLACK
        self.text_surface = font.render(self.text, True, self.act_color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.topleft = (self.rect.x + 20, self.rect.y + 4)
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
        self.quest_generator = QuestGenerator(self.game)

    def add_quest(self, quest):
        if len(self.quests)<50:
            self.quests.append(quest)
        else:
            print ("za dużo questow")

    def add_quest_by_name(self, quest_name):
        if len(self.quests)<50:
            self.quests.append(self.quest_generator.return_quest_by_name(quest_name))
        else:
            print ("za dużo questow")

    def remove(self, quest):
        self.quests.remove(quest)

    def remove_by_name(self, quest_name):
        for i in self.quests:
            if i.name == quest_name:
                self.quests.remove(i)

    def return_quest_name_list(self):
        quest_list = []
        for i in self.quests:
            quest_list.append(i.name)
        return quest_list

    def load_quests_by_name_list(self, quest_name_list):
        if quest_name_list:
            quest_list = self.quest_generator.return_quest_list_by_name_list(quest_name_list)
            for quest in quest_list:
                self.add_quest(quest)

    def get_quest_by_name(self, quest_name):
        for i in self.quests:
            if i.name == quest_name:
                return i

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
            i.show_quest_icon(self.image,x_pos + 6, 40 + counter * 64)
            self.game.s_write(f'Quest {i.name}', self.image, (x_pos + 80, 40 + counter * 64),(BLACK))
            if len(i.goal_descr) <= 30:
                text_line_01 = i.goal_descr
                text_line_02 = ""
            else:
                text_line_01 = i.goal_descr[:30]
                text_line_02 = i.goal_descr[30:]
            self.game.s_write(text_line_01, self.image, (x_pos + 80, 58 + counter * 64), BLACK)
            self.game.s_write(text_line_02, self.image, (x_pos + 80, 76 + counter * 64), BLACK)
            #self.game.s_write(f'Reward {i.reward_xp} XP,  {i.reward_gold} gold.', self.image ,(x_pos + 80, 70 + counter * 64),(BLACK))
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
        if not self.check_duplicate_by_name(name):
            self.spells.append(self.spellgenerator.get_spell_by_name(name))

    def check_duplicate(self, spell):
        for i in self.spells:
            if i.name == spell.name:
                return True

    def check_duplicate_by_name(self, spell_name):
        for i in self.spells:
            if i.name == spell_name:
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
                if i.subtype == "heroism":
                    self.game.s_write("Strength bonus: " + str(5 + self.game.player.intellect),
                                      self.image, (x_pos + 80, 55 + counter * i.width), (BLACK))
                    self.game.s_write("Duration: " + str(15 + (2 * self.game.player.intellect)) + "s",
                                      self.image, (x_pos + 80, 85 + counter * i.width), (BLACK))
            if i.type == "offensive":
                if i.bullet_nr > 1:
                    self.game.s_write("Damage: " + str(i.bullet_nr) + "x " + str(i.damage + int(self.game.player.intellect * self.game.player.spell_power_bonus)), self.image, (x_pos + 80, 55 + counter * i.width),(BLACK))
                else:
                    if i.subtype == "poison cloud":
                        self.game.s_write("Damage: 0",
                                          self.image, (x_pos + 80, 55 + counter * i.width), (BLACK))
                    else:
                        self.game.s_write("Damage: " + str(i.damage + int(self.game.player.intellect * self.game.player.spell_power_bonus)),
                                      self.image, (x_pos + 80, 55 + counter * i.width), (BLACK))
                if i.blow_effect:
                    self.game.s_write("Blow Dmg: " + str(i.blow_damage + self.game.player.intellect * self.game.player.spell_power_bonus) + "/s",self.image, (x_pos + 180, 55 + counter * i.width),(BLACK))
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
                if self.subtype == "heroism":
                    player.active_effects_lib.add_effect(ActiveEffect("heroism",e_heroism_ico,
                                                                      5 + player.intellect,15 + (2 * player.intellect)))
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
            #print (f' Efekt {self.name} duration: {self.duration}')
            self.effect_time += unpaused_dt
            #print (f' Czas efektu: {self.effect_time}')
            if self.effect_time >= self.duration:
                #print ("KONIEC TRWANIA EFEKTU")
                self.effect_time = 0
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
                #print ("EFEKT JUZ BYL, nadaje NOWY celem zerowania czasu trwania")
                self.active_effects.remove(act_effect)
        #print ("NADAJE NOWY EFFECT")
        self.active_effects.append(effect)
        #self.game.player.update_stats()

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
        self.dialog_dict = {}
        self.conversation = []
        self.blocked_threads = []
        self.threads_to_block_by_event = {}
        self.threads_to_unblock_by_event = {}
        self.threads_to_late_unblock_by_event = {}
        self.text_returned = False

    #### DODAJE SILNIK BLOKOWANIA I ODBLOKOWANIA WATKOW W ZALEZNOSCI OD PRZYPISANIA I EVENT MANAGERA
    def add_blocked_thread(self, blocked_thread):
        if blocked_thread not in self.blocked_threads:
            self.blocked_threads.append(blocked_thread)

    def remove_blocked_thread(self, blocked_thread):
        if blocked_thread in self.blocked_threads:
            self.blocked_threads.remove(blocked_thread)
        else:
            print ("ERROR ! DONT HAVE THREAD, YOU WISH TO REMOVE FROM BLOCKED!")

    def check_thread_if_blocked(self, thread_to_check) -> bool:
        if thread_to_check in self.blocked_threads:
            return True
        else:
            return False

    def thread_block_with_event(self, thread, events):
        for game_event in events:
            self.threads_to_block_by_event[game_event] = thread
        # print (self.threads_to_block_by_event)

    def thread_unblock_with_event(self, thread, events):
        for game_event in events:
            self.threads_to_unblock_by_event[game_event] = thread
        #print (self.threads_to_unblock_by_event)

    def thread_late_unblock_with_event(self, thread, game_event):
        print ("adding late unblock formula")
        self.threads_to_late_unblock_by_event[game_event] = thread

    def setup_blocked_threads(self):
        ## EVENTY TO WARUNKI DO SPELNIENIA. WYSTARCZY 1 SPELNIONY z wielu mozliwych..
        ## TE KTORE SA DO ODBLOKOWANIA SA PER SE ZABLOKOWANE:
        for thread in self.threads_to_unblock_by_event.values():
            self.add_blocked_thread(thread)
        ## TE KTORE SA ZABLOKOWANE I MAJA EVENT spelniony ODBLOKOWUJE:
        for event, thread in self.threads_to_unblock_by_event.items():
            if self.game.events_manager.search_event(event):
                self.remove_blocked_thread(thread)
        ## TE KTORE SA DO ZABLOKOWANIA I MAJA EVENT spelniony:
        for event, thread in self.threads_to_block_by_event.items():
            if self.game.events_manager.search_event(event):
                self.add_blocked_thread(thread)
        ## LATE UNBLOCK
        for event, thread in self.threads_to_late_unblock_by_event.items():
            if self.game.events_manager.search_event(event):
                print ("late removing")
                self.remove_blocked_thread(thread)

        ############
        print ("BLOCKED THREADS:")
        print (self.blocked_threads)
        print ("----------------")

    def find_branch_in_thread(self, branch_to_find, active_thread):
        for text in self.conversation:
            if text.thread == active_thread:
                if text.branch == branch_to_find:
                    if text.step == 0:
                        return text

    def reset(self):
        self.text_returned = False

    def decode_bool(self, input_string):
        if input_string == "False":
            return False
        elif input_string == "True":
            return True
        elif input_string == False:
            return False
        elif input_string == True:
            return True
        else:
            print ("DECODE ERROR")
            return False

    def decode_next_thread(self, input_string):
        if input_string == "False":
            #print("DECODE NEXT THREAD - bool False")
            return False
        elif input_string == "True":
            #print("DECODE NEXT THREAD - bool True")
            return True
        elif input_string == "Next":
            #print("DECODE NEXT THREAD - NEXT convert into bool True")
            return True
        elif input_string == False:
            return False
        elif input_string == True:
            return True
        else:
            #print("DECODE NEXT THREAD - STRING")
            return input_string

    def decode_int(self, input_string):
        if input_string == False:
            return False
        elif input_string != "False":
            return int(input_string)
        else:
            return False

    def decode_event(self, input_string):
        if input_string == "False":
            return False
        if input_string == False:
            return False
        #print ("PASSING EVENT "+ input_string)
        return input_string

    def decode_ask(self, input_string):
        if input_string == False:
            return False
        if input_string == "False":
            return False
        ask_text = ""
        ask_quest = ""
        ask_goto_step = ""
        ask_goto_branch = ""
        ###############
        counter = 0
        #print(input_string)
        for case in input_string:
            if case != ">":
                counter += 1
                ask_text = ask_text + case
            else:
                break
        counter += 1
        input_string = input_string[counter:]
        #print(input_string)
        ###############
        counter = 0
        for case in input_string:
            if case != ">":
                counter += 1
                ask_quest = ask_quest + case
            else:
                break
        counter += 1
        input_string = input_string[counter:]
        #print(input_string)
        ################
        counter = 0
        for case in input_string:
            if case != ",":
                counter += 1
                ask_goto_branch = ask_goto_branch + case
            else:
                break
        counter += 1
        input_string = input_string[counter:]
        #print(input_string)
        for case in input_string:
            ask_goto_step = ask_goto_step + case
        #print("Result")
        #print("ask_text: " + ask_text)
        #print("ask_quest: " + ask_quest)
        #print("ask_goto_branch: " + ask_goto_branch)
        #print("ask_goto_step: " + ask_goto_step)
        #############
        ##############
        if ask_quest == "False":
            ask_quest = False
        elif ask_quest[:5] == "quest":
            ask_quest = self.quest_gen.return_quest_by_name(ask_quest[6:])
        ask_goto_step = int(ask_goto_step)
        ask_goto_branch = int(ask_goto_branch)
        return (ask_text, ask_quest, (ask_goto_branch, ask_goto_step))

    def load_from_dict(self, dialog_dict, quest_gen):
        self.dialog_dict = dialog_dict
        self.quest_gen = quest_gen
        for row in self.dialog_dict:
            ifnpc = self.decode_bool(row['Npc'])
            thread = row['Thread']
            branch = self.decode_int(row['Branch'])
            step = self.decode_int(row['Step'])
            text = row['Text']
            ask1 = self.decode_ask(row['Ask1'])
            ask2 = self.decode_ask(row['Ask2'])
            ask3 = self.decode_ask(row['Ask3'])
            ask4 = self.decode_ask(row['Ask4'])
            next_thread = self.decode_next_thread(row['Next_Thread'])
            goto_branch = self.decode_int(row['Goto_Branch'])
            goto_step = self.decode_int(row['Goto_Step'])
            event = self.decode_event(row['Event'])
            self.conversation.append(
                Text(ifnpc, thread, branch, step, text, ask1, ask2, ask3, ask4,
                     next_thread, (goto_branch, goto_step), event))

    def load_text(self,ifnpc,thread,branch,step,text,ask1,ask2,ask3,ask4,next_thread,goto, event):
        self.conversation.append(Text(ifnpc,thread,branch,step,text,ask1,ask2,ask3,ask4,next_thread,goto, event))

    def find_first_step(self, encounter):
        if not encounter:
            for act_txt in self.conversation:
                if act_txt.thread == "welcome" and act_txt.branch == 0 and act_txt.step == 0:
                    self.text_returned = act_txt
                    #print ("FOUND WELCOME TXT")
                    return act_txt
        else:
            for act_txt in self.conversation:
                if act_txt.thread == "welcome" and act_txt.branch == 1 and act_txt.step == 0:
                    self.text_returned = act_txt
                    #print("FOUND WELCOME AGAIN TXT")
                    return act_txt

        print ("ERROR DID NOT FIND next welcome TXT, SO SENDING welcome branch 0 step 0")
        for act_txt in self.conversation:
            if act_txt.thread == "welcome" and act_txt.branch == 0 and act_txt.step == 0:
                self.text_returned = act_txt
                # print ("FOUND WELCOME TXT")
                return act_txt
        print("ERROR DID NOT FOUND ANY WELCOME BRANCH")

    def check_goto(self) -> bool:
        if self.text_returned.goto:
            branch = self.text_returned.goto[0]
            step = self.text_returned.goto[1]
            if branch or step:
                return True
            else:
                return False
        else:
            print ("Error, couldnt decode goto")
            return False

    def find_next_step(self):
        ###NAJPIERW SPRAWDZAM CZY NIE MA ZMIANY WATKU (next_thread = False)
        ## JEZELI NIE TO:
        if not self.text_returned.next_thread:
            print (f' Text returned.oto: {self.text_returned.goto}')
            if not self.check_goto():
                next_step = self.text_returned.step + 1
                for text in self.conversation:
                    if text.thread == self.text_returned.thread:
                        if text.branch == self.text_returned.branch:
                            if text.step == next_step:
                                print("FOUND NEXT STEP")
                                self.text_returned = text
                                return text
            else:
                for text in self.conversation:
                    if text.thread == self.text_returned.thread:
                        if text.branch == self.text_returned.goto[0] and text.step == self.text_returned.goto[1]:
                            print("FOUND NEXT STEP BY GOTO")
                            self.text_returned = text
                            return text
        print ("DID NOT FIND NEXT STEP - GO TO NEXT THREAD")
        ### TERAZ SPRAWDZAM CZY JEST ZMIANA WATKU (next_thread = "string"
        if isinstance(self.text_returned.next_thread, str):
            print ("FOUND NEXT THREAD BY NEXT TRHEAD STRING")
            thread_name = self.text_returned.next_thread
            #print (f'Thread will be - {thread_name}')
        ### SPRAWDZAM NOWY WATEK (next_thread = True lub next_thread = False ale nie znaleziono next step ani goto)
        else:
            thread_name = self.next_thread(self.text_returned.thread)
        ### JEZELI ZNALAZLEM NOWA GALAZ:
        if thread_name:
            ### DODAJE EVENT ZE ZNAM JUZ WATEK
            if not self.game.events_manager.find_thread_read_event(thread_name):
                if thread_name != "bye":
                    self.game.events_manager.emit(Event(id=f'thread {thread_name} has been read'))
            ### JEZELI TO QUEST TO SILNIK ROZDZIELI GALEZIE WG Eventów WLASCICIEL QUESTA GO DAJE I OCENIA POSTEP:
            if thread_name[:5] == "quest":
                print ("NEXT THREAD IS A QUEST THREAD, SEARCHING FOR A NEXT BRANCH AND STEP:")
                if self.game.events_manager.find_got_quest_event(thread_name[6:]):
                    print (f'FOUND {thread_name[6:]} quest in event manager - Branch 1,2,3')
                    if self.game.events_manager.find_quest_compl_event(thread_name[6:]):
                        print("BRANCH 3 or 4 = quest completed")
                        if self.game.events_manager.find_quest_rewarded_event(thread_name[6:]):
                            print ("BRANCH 3 = quest completed and rewarded")
                            text = self.find_branch_in_thread(3, thread_name)
                            self.text_returned = text
                            return text
                        else:
                            print("BRANCH 4 = qust completed but not rewarded")
                            text = self.find_branch_in_thread(4, thread_name)
                            self.text_returned = text
                            return text
                    else:
                        ## Tu male peligro jezeli nie bedzie questu w ksiazce a bedzie
                        # sytuacja w ktorej Event_manager nie znajdzie quest_compl o danej nazwie [6:]!!
                        quest_to_check = self.game.player.quest_book.get_quest_by_name(thread_name[6:])
                        if quest_to_check:
                            if quest_to_check.check_if_fulfiled():
                                print ("BRANCH 2 = quest fulfiled and not completed")
                                text = self.find_branch_in_thread(2, thread_name)
                                self.text_returned = text
                                return text
                            else:
                                print ("BRANCH 1 = quest not fulfiled and not completed")
                                text = self.find_branch_in_thread(1, thread_name)
                                self.text_returned = text
                                return text
                        else:
                            print (f'ERROR - No quest {thread_name[6:]} in quest book')
                else:
                    print(f'DID NOT FIND {thread_name[6:]} quest in event manager - NEXT BRANCH 0')
                    text = self.find_branch_in_thread(0, thread_name)
                    self.text_returned = text
                    return text
            ### UWAGA JEZELI BEDA INNE WATKI TRZEBA JE TUTAJ UWZGLEDNIC CZY NIE WYMAGAJA SPECJALNEJ LOGIKI!
            else: #thread_name == "bye":
                text = self.find_branch_in_thread(0, thread_name)
                self.text_returned = text
                return text
        else:
        ### NIE MA KOLEJNEJ GALEZI - KONIEC DIALOGU:
            return 0

    def find_next_step_by_goto(self, goto):
        act_thread = self.text_returned.thread
        for text in self.conversation:
            if text.thread == act_thread:
                if text.branch == goto[0] and text.step == goto[1]:
                    print("FOUND NEXT STEP BY RECIVING ANSWER")
                    self.text_returned = text
                    return text
        print ("ERROR, DID NOT FIND NEXT BRANCH and STEP by GOTO")

    def next_thread(self, act_thread):
        threads = []
        for text in self.conversation:
            if text.thread not in threads:
                threads.append(text.thread)
        #print (f'found threads: {threads}')
        blocked_threads = self.blocked_threads.copy()
        #print (f'removing blocked Threads from list: {blocked_threads}')
        ## LIST SUBSTACTION you silly kris!
        result_threads = [i for i in threads if not i in blocked_threads or blocked_threads.remove(i)]
        #print(f'SEARCHING FOR A NEXT THREAD. AVAIBLE Threads: {result_threads}')
        threads = iter(result_threads)
        while True:
            try:
                thread = next(threads)
                #print (f'THREAD: {thread} to search')
                #print (f'THREAD: {act_thread} was active')
                if thread == act_thread:
                    try:
                        next_thread = next(threads)
                        print (f'WILL RETURN NEXT THREAD: {next_thread}')
                        return next_thread
                    except:
                        print("LAST THREAD, END DIALOG")
                        break
            except:
                print("No more threads!")
                break


class Text:
    def __init__(self, ifnpc, thread, branch, step, text, ask1,ask2,ask3,ask4,next_thread, goto, event):
        ### ZAWIERAC BEDZIE CALA WYPOWIEDZ
        ### PODZIELIMY NA linijki tekstu
        self.ifnpc = ifnpc
        self.thread = thread
        self.branch = branch
        self.step = step
        self.text = text
        self.ask1 = ask1
        self.ask2 = ask2
        self.ask3 = ask3
        self.ask4 = ask4
        self.next_thread = next_thread
        self.goto = goto
        self.event = event
        self.welcome = False
        if self.thread == "welcome" and self.branch == 0 and self.step == 0:
            self.welcome = True


class ShopDialogBox:
    def __init__(self,game):
        self.game = game
        self.shop = False
        self.pos = DIAL_BOX_POS
        self.image = dialogbox_img_2.copy()
        self.ok_button = RadioButton(rad_exit_img, rad_exit_h_img, 178, 290)
        self.resp_but_1 = RadioButton(rad_but_img, rad_but_h_img, 55, 150)
        self.resp_but_2 = RadioButton(rad_but_img, rad_but_h_img, 55, 175)
        self.resp_but_3 = RadioButton(rad_but_img, rad_but_h_img, 55, 200)
        self.resp_but_4 = RadioButton(rad_but_img, rad_but_h_img, 55, 225)
        self.resp_buttons = [self.resp_but_1, self.resp_but_2, self.resp_but_3, self.resp_but_4]

    def clear(self):
        self.image = dialogbox_img_2.copy()
        self.shop = False
        for button in self.resp_buttons:
            button.deactivate()

    def activate_and_write_ask(self):
        if self.shop.shop_ask1.text:
            self.resp_but_1.activate()
            self.write(self.shop.shop_ask1.text, 2)
        if self.shop.shop_ask2.text:
            self.resp_but_2.activate()
            self.write(self.shop.shop_ask2.text, 3)
        if self.shop.shop_ask3.text:
            self.resp_but_3.activate()
            self.write(self.shop.shop_ask3.text, 4)
        if self.shop.shop_ask4.text:
            self.resp_but_4.activate()
            self.write(self.shop.shop_ask4.text, 5)

    def start_conversation(self, shop):
        self.clear()
        self.game.paused = True
        self.shop = shop
        self.game.put_txt(f'You are in {self.shop.shop_name}')
        self.game.ph_shop = True
        self.game.update_ui_buttons()
        print("START SPEAKING WITH SHOP OWNER")
        print(f'ph_shop: {self.game.ph_shop}')
        print(f'ph_buy and sell: {self.game.ph_buy_and_sell}')
        print(f'ph_repair: {self.game.ph_repair}')
        self.activate_and_write_ask()
        self.draw_upper_part()

    def draw_upper_part(self) -> None:
        self.image.blit(self.shop.owner_image, DB2_IMG_POS)
        self.game.s_write(self.shop.owner_name, self.image, DB2_TXT_POS, WHITE)
        self.write(self.shop.welcome_text, 0)

    def write(self, txt, ln):
        self.game.s_write(txt, self.image, (85, 100 + ln * 24), (WHITE))

    def check_buttons(self, mouse_pos):
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        mouse_x -= self.pos[0]
        mouse_y -= self.pos[1]
        self.mouse_pos = (mouse_x, mouse_y)
        if self.ok_button.active:
            if self.ok_button.check_if_clicked(self.mouse_pos):
                print ("OK CLICKED - EXIT SHOP DIALOG")
                self.game.active_shop = False
                self.game.back_to_game_and_unpause()
        if self.resp_but_1.active:
            if self.resp_but_1.check_if_clicked(self.mouse_pos):
                self.shop.activate_ask(self.shop.shop_ask1)
        if self.resp_but_2.active:
            if self.resp_but_2.check_if_clicked(self.mouse_pos):
                self.shop.activate_ask(self.shop.shop_ask2)
        if self.resp_but_3.active:
            if self.resp_but_3.check_if_clicked(self.mouse_pos):
                self.shop.activate_ask(self.shop.shop_ask3)
        if self.resp_but_4.active:
            if self.resp_but_4.check_if_clicked(self.mouse_pos):
                self.shop.activate_ask(self.shop.shop_ask4)

    def update(self, mouse_pos):
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        mouse_x -= self.pos[0]
        mouse_y -= self.pos[1]
        self.mouse_pos = (mouse_x, mouse_y)
        self.ok_button.check_if_highlight(self.mouse_pos)
        for i in self.resp_buttons:
            i.check_if_highlight(self.mouse_pos)

    def show_buttons(self):
        for i in self.resp_buttons:
            if i.active:
                i.show_button(self.image)
        self.ok_button.show_button(self.image)

    def show(self, screen):
        self.show_buttons()
        screen.blit(self.image, self.pos)


class MessageBox:
    def __init__(self, game):
        self.game = game
        self.pos = DIAL_BOX_POS
        self.image = dialogbox_img_2.copy()
        self.rew_image = scroll_160_img.copy()
        self.rew_pos = (140,240)
        self.ok_button = RadioButton(rad_ok_img, rad_ok_h_img, 178, 290)
        self.rew_scroll_show = False
        self.ok_button.deactivate()

    def clear(self):
        self.image = dialogbox_img_2.copy()
        self.rew_image = scroll_160_img.copy()

    def update(self, mouse_pos):
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        mouse_x -= self.pos[0]
        mouse_y -= self.pos[1]
        self.mouse_pos = (mouse_x, mouse_y)
        self.ok_button.activate()
        self.ok_button.check_if_highlight(self.mouse_pos)

    def check_button(self, mouse_pos):
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        mouse_x -= self.pos[0]
        mouse_y -= self.pos[1]
        self.mouse_pos = (mouse_x, mouse_y)
        if self.ok_button.active:
            if self.ok_button.check_if_clicked(self.mouse_pos):
                print ("OK CLICKED - EXIT MESSAGE BOX")
                self.rew_scroll_show = False
                self.game.message_shown = False
                self.ok_button.deactivate()
                self.game.back_to_game_and_unpause()

    def show_title(self, text):
        self.game.s_write(text, self.image,DB2_TXT_POS,WHITE)
        #self.write(text,0)

    def show_text(self, text):
        self.game.s_write(text, self.image,(120,150),WHITE)
        #self.write(text,0)

    def show_button_ok(self):
        self.ok_button.show_button(self.image)

    def show_reward_image(self, reward_gold, reward_xp, reward_item):
        self.rew_scroll_show = True
        print("REW SCROLL SHOW = True")
        self.game.s_write(f'You have recieved a reward:', self.rew_image, (80, 10), BLACK)
        g_l_m = 10 * (len(str(reward_gold)) - 1)
        e_l_m = 10 * (len(str(reward_xp)) - 1)
        if reward_gold > 0:
            self.rew_image.blit(gold_coin, (95 + g_l_m, 45))
            self.game.s_write(str(reward_gold), self.rew_image, (80, 35), BLACK)
        if reward_xp > 0:
            self.rew_image.blit(xp_icon, (95 + e_l_m, 60))
            self.game.s_write(str(reward_xp), self.rew_image, (80, 60), BLACK)
        if reward_item:
            self.game.s_write(f'You get {reward_item.name}', self.rew_image, (120, 85), BLACK)
            self.rew_image.blit(reward_item.image, (80, 80))

    def show(self, screen):
        self.show_button_ok()
        screen.blit(self.image, self.pos)
        if self.rew_scroll_show:
            screen.blit(self.rew_image, self.rew_pos)

    def show_message(self, title, text):
        self.clear()
        self.game.message_shown = True
        self.game.paused = True
        print ("akukukuku")
        self.game.update_ui_buttons()
        self.show_title(title)
        self.show_text(text)

    def show_message_quest_reward(self, text, reward_gold, reward_xp, reward_item):
        print ("show message quest reward")
        self.clear()
        self.game.message_shown = True
        self.game.paused = True
        self.game.update_ui_buttons()
        self.show_title(text)
        self.show_reward_image(reward_gold, reward_xp, reward_item)


class QuestionBox:
    def __init__(self, game):
        self.game = game
        self.pos = DIAL_BOX_POS
        self.image = dialogbox_img_2.copy()
        self.ok_button = RadioButton(rad_ok_img, rad_ok_h_img, 100, 290)
        self.back_button = RadioButton(rad_back_img,rad_back_h_img,240,290)
        self.text = ""

    def update(self, mouse_pos):
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        mouse_x -= self.pos[0]
        mouse_y -= self.pos[1]
        self.mouse_pos = (mouse_x, mouse_y)
        self.ok_button.check_if_highlight(self.mouse_pos)
        self.back_button.check_if_highlight(self.mouse_pos)

    def check_button(self, mouse_pos):
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        mouse_x -= self.pos[0]
        mouse_y -= self.pos[1]
        self.mouse_pos = (mouse_x, mouse_y)
        if self.ok_button.check_if_clicked(self.mouse_pos):
            print ("OK CLICKED - Q BOX")
            self.game.qbox_shown = False
            if self.gobackph:
                self.game.paused = True
            else:
                self.game.paused = False
            self.ok_button.deactivate()
            self.back_button.deactivate()
            self.game.update_ui_buttons()
            self.ok_function()

        if self.back_button.check_if_clicked(self.mouse_pos):
            print ("BACK CLICKED QBOX")
            self.game.qbox_shown = False
            if self.gobackph:
                self.game.paused = True
            else:
                self.game.paused = False
            self.ok_button.deactivate()
            self.back_button.deactivate()
            self.game.update_ui_buttons()

    def void_function(self):
        pass

    ## MOZNA ZROBIC TYPY PYTAN - narazie 1 o podróż.
    def ask_travel(self, teleport):
        self.image = dialogbox_img_2.copy()
        self.game.paused = True
        self.game.qbox_shown = True
        self.gobackph = False
        self.ok_button.activate()
        self.back_button.activate()
        self.game.update_ui_buttons()
        self.show_text(f'Are you sure you want to travel to {teleport.name}?')
        self.show_title("Travel")
        self.ok_function = teleport.activate_teleport

    def ask_save_game(self, save_game):
        self.image = dialogbox_img_2.copy()
        self.game.paused = True
        self.game.qbox_shown = True
        self.gobackph = self.game.ph_shop
        self.ok_button.activate()
        self.back_button.activate()
        self.game.update_ui_buttons()
        self.show_text(f'Are you sure?')
        self.show_title("Tavern")
        self.ok_function = save_game

    def show_title(self, text):
        self.game.s_write(text, self.image,DB2_TXT_POS,WHITE)
        #self.write(text,0)

    def show_text(self, text):
        self.game.s_write(text, self.image,(40,150),WHITE)
        #self.write(text,0)

    def show_buttons(self):
        self.ok_button.show_button(self.image)
        self.back_button.show_button(self.image)

    def show(self, screen):
        self.show_buttons()
        screen.blit(self.image, self.pos)


class DialogBox:
    def __init__(self, game):
        self.game = game
        self.pos = DIAL_BOX_POS
        self.image = dialogbox_img_2.copy()
        self.rew_image = scroll_160_img.copy()
        self.rew_scroll_show = False
        self.rew_pos = REW_BOX_POS
        self.ok_button = RadioButton(rad_ok_img,rad_ok_h_img,178,290)
        self.resp_but_1 = RadioButton(rad_but_img,rad_but_h_img,55,150)
        self.resp_but_2 = RadioButton(rad_but_img, rad_but_h_img, 55, 175)
        self.resp_but_3 = RadioButton(rad_but_img, rad_but_h_img, 55, 200)
        self.resp_but_4 = RadioButton(rad_but_img, rad_but_h_img, 55, 225)
        self.resp_buttons = [self.resp_but_1,self.resp_but_2,self.resp_but_3,self.resp_but_4]
        self.npc = False
        self.actual_text = False
        self.dialog_data = False

    def start_conversation(self,npc):
        print ("STARTING CONVERSATION")
        ### WYLACZAM GUZIKI NA MAIN SCREEN
        self.game.update_ui_buttons()
        ### SENDING INFO
        self.game.put_txt(f'Speaking with {npc.name}')
        ### PUT NPC DATA
        self.npc = npc
        self.dialog_data = self.npc.dialog_data
        ### CLEaR IMAGES
        self.rew_image = scroll_160_img.copy()
        self.dialog_data.reset()
        ### BLOKUJE WATKI
        self.dialog_data.setup_blocked_threads()
        #### SZUKAM POCZATKU DIALOGU:
        encounter = self.game.events_manager.find_npc_encounter_event(self.npc.name)
        self.actual_text = self.dialog_data.find_first_step(encounter)
        self.write_actual_text()

    def next_ask_step(self, goto):
        self.actual_text = self.dialog_data.find_next_step_by_goto(goto)
        self.configure_text()

    def next_step(self):
        #### POBIERAM NOWY TEXT Z MASZYNY DIALOG
        self.actual_text = self.dialog_data.find_next_step()
        #### SPRAWDZAM CZY ACTUAL TEKST MA EVENT I GO DODAJE
        if self.actual_text:
            if self.actual_text.event:
                self.game.events_manager.emit(Event(id=self.actual_text.event))
                #### SPRAWDZAM CZY EVENT WYMAGA DZIALANIA teraz (Np. COLLECT REWARD)
                if self.actual_text.event[-17:] == "has been rewarded":
                    ## wycinam nazwe questa z Event.id
                    lastcutstr = self.actual_text.event[:-18]
                    quest_name = lastcutstr[6:]
                    quest = self.game.player.quest_book.get_quest_by_name(quest_name)
                    self.show_reward(quest)
                    quest.collect_reward()
        #### KONFIGURUJE I WYSWIETLAM TEXT
        self.configure_text()

    def show_reward(self, quest):
        self.rew_scroll_show = True
        print ("REW SCROLL SHOW = True")
        self.game.s_write(f'You have recieved a reward:', self.rew_image,(80,10),BLACK)
        g_l_m = 10 * (len(str(quest.reward_gold)) - 1)
        e_l_m = 10 * (len(str(quest.reward_xp)) - 1)
        if quest.reward_gold > 0:
            self.rew_image.blit(gold_coin,(95 + g_l_m,35))
            self.game.s_write(str(quest.reward_gold), self.rew_image,(80,30),BLACK)
        if quest.reward_xp > 0:
            self.rew_image.blit(xp_icon,(95 + e_l_m,50))
            self.game.s_write(str(quest.reward_xp), self.rew_image, (80, 50),BLACK)
        if quest.reward_item:
            self.game.s_write(f'You get {quest.reward_item}', self.rew_image, (80, 70),BLACK)
            #self.rew_image.blit(quest.reward_item.image,(80,80))

    def configure_text(self):
        ################################################################
        ### KONFIGURACJA UKLADU - NOWY AKTUALNY TEKST DO WYSWIETLENIA! #
        ################################################################
        # Czyszcze zmienne i dodatki #
        self.resp_but_1.deactivate()
        self.resp_but_2.deactivate()
        self.resp_but_3.deactivate()
        self.resp_but_4.deactivate()
        if self.actual_text:
            ## JEZELI JEST TO PYTANIE AKTYWUJE PRZYCISKI ODPOWIEDZI I PISZE ODPOWIEDZI:
            how_many_answers = 0
            if self.actual_text.ask1:
                print(self.actual_text.ask1)
                how_many_answers +=1
            if self.actual_text.ask2:
                print(self.actual_text.ask2)
                how_many_answers +=1
            if self.actual_text.ask3:
                print(self.actual_text.ask3)
                how_many_answers += 1
            if self.actual_text.ask4:
                print(self.actual_text.ask4)
                how_many_answers += 1
            #print (how_many_answers)
            if how_many_answers >=1:
                self.write_actual_text()
                self.ok_button.deactivate()
                if how_many_answers == 1:
                    self.resp_but_1.activate()
                    #print(self.actual_text.ask[0][0])
                    self.write(self.actual_text.ask1[0], 2)
                elif how_many_answers == 2:
                    self.resp_but_1.activate()
                    self.resp_but_2.activate()
                    #print(self.actual_text.ask[0][0])
                    #print(self.actual_text.ask[1][0])
                    self.write(self.actual_text.ask1[0], 2)
                    self.write(self.actual_text.ask2[0], 3)
                elif how_many_answers == 3:
                    self.resp_but_1.activate()
                    self.resp_but_2.activate()
                    self.resp_but_3.activate()
                    #print(self.actual_text.ask[0][0])
                    #print(self.actual_text.ask[1][0])
                    #print(self.actual_text.ask[2][0])
                    self.write(self.actual_text.ask1[0], 2)
                    self.write(self.actual_text.ask2[0], 3)
                    self.write(self.actual_text.ask3[0], 4)
                elif how_many_answers == 4:
                    self.resp_but_1.activate()
                    self.resp_but_2.activate()
                    self.resp_but_3.activate()
                    self.resp_but_4.activate()
                    self.write(self.actual_text.ask1[0], 2)
                    self.write(self.actual_text.ask2[0], 3)
                    self.write(self.actual_text.ask3[0], 4)
                    self.write(self.actual_text.ask4[0], 5)
            ## JEZELI ZWYKLY TEKST
            else:
                self.ok_button.activate()
                for i in self.resp_buttons:
                    i.deactivate()
                self.write_actual_text()
        ### JEZELI NIE MA JUZ AKTULANEGO TESKTU KONCZE DIALOG I ZAPISUJE ZE ODNALEZIONY NPC
        else:
            self.clear()
            self.game.dialog_in_progress = False
            self.game.paused = False
            self.game.update_ui_buttons()
        ### NA ZAKONCZENIE DIALOGU> zapisuje NPC jako spotkany
            if not self.npc.encountered:
                self.game.events_manager.emit(Event(id=f'{self.npc.name} has been encountered'))
                self.npc.encountered = True
                ### SPRAWDZANIE DLA QUESTOW SAMOKONCZACYCH SIE< ZE ODNALEZIONO NPC - czyli auto fulfil and reward quest
                for quest in self.game.player.quest_book.quests:
                    if quest.auto_checking:
                        print("ZNALAZLEM W KSIAZCE QUESTOW quest Z AUTOSPRAWDZENIEM")
                        if quest.check_if_fulfiled():
                            self.game.put_txt(f'{quest.name} has been completed')
                            quest.collect_reward()
                        else:
                            print ("ALE NIE WYKONANO WARUNKOW DO SPELNIENIA questu z autosprawdzeniem")
            ### wyswietlam wiadomosc po dialogu jezeli zakonczono quest
            if self.game.message_shown:
                print ("Message shown = True")
                self.game.paused = True
            ### jezeli next level, pauzuje gre po dialogu
            if self.game.player.check_next_level():
                self.game.paused = True
            ### jezeli koniec gry:
            if self.game.events_manager.check_game_accomplished():
                self.game.game_accomplished = True
                self.game.playing = False

    def write_actual_text(self):
        if self.actual_text.ifnpc:
            speaker = self.npc
        else:
            speaker = self.game.player
        self.write_line(speaker, self.actual_text.text)
        #except:
        #   print ("ERROR DONT HAVE ACTUAL TEXT TO BLIT")

    def write_line(self, speaker, text) -> None:
        self.clear()
        self.image.blit(speaker.image, DB2_IMG_POS)
        self.game.s_write(speaker.name, self.image, DB2_TXT_POS, WHITE)
        text_len = len(text)
        text_line_1 = ""
        text_line_2 = ""
        text_line_3 = ""
        text_line_4 = ""
        text_line_5 = ""
        text_line_6 = ""
        text_line_7 = ""
        #print (text_len)
        ## MAX LINE LENGTH 350~!
        if text_len < 50:
            text_line_1 = text[:50]
        if text_len >= 50 and text_len <100:
            text_line_1 = text[:50]
            text_line_2 = text[50:100]
        if text_len >=100 and text_len <150:
            text_line_1 = text[:50]
            text_line_2 = text[50:100]
            text_line_3 = text[100:120]
        if text_len >=150 and text_len <200:
            text_line_1 = text[:50]
            text_line_2 = text[50:100]
            text_line_3 = text[100:150]
            text_line_4 = text[150:200]
        if text_len >= 200 and text_len < 250:
            text_line_1 = text[:50]
            text_line_2 = text[50:100]
            text_line_3 = text[100:150]
            text_line_4 = text[150:200]
            text_line_5 = text[200:250]
        if text_len >=250 and text_len <300:
            text_line_1 = text[:50]
            text_line_2 = text[50:100]
            text_line_3 = text[100:150]
            text_line_4 = text[150:200]
            text_line_5 = text[200:250]
            text_line_6 = text[250:300]
        if text_len >=300 and text_len <350:
            text_line_1 = text[:50]
            text_line_2 = text[50:100]
            text_line_3 = text[100:150]
            text_line_4 = text[150:200]
            text_line_5 = text[200:250]
            text_line_6 = text[250:300]
            text_line_7 = text[300:350]
        self.write(text_line_1, 0)
        self.write(text_line_2, 1)
        self.write(text_line_3, 2)
        self.write(text_line_4, 3)
        self.write(text_line_5, 4)
        self.write(text_line_6, 5)
        self.write(text_line_7, 6)

    def write(self, txt, ln):
        self.game.s_write(txt,self.image, (85, 100 + ln * 24), (WHITE))

    def clear(self):
        self.image = dialogbox_img_2.copy()

    def show(self, screen):
        ## Uwaga tu powinienem sprawdzic wszystkie 4 ask (odpowiedzi na pytania)
        # ale to jest nowy draft
        if not self.actual_text.ask1:
            self.ok_button.show_button(self.image)
        else:
            self.show_response_buttons()
        if self.rew_scroll_show:
            screen.blit(self.rew_image, self.rew_pos)
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
                self.rew_scroll_show = False
                self.next_step()
        if self.resp_but_1.active:
            if self.resp_but_1.check_if_clicked(self.mouse_pos):
                if self.actual_text.ask1[1]:
                    self.actual_text.ask1[1].get_quest()
                self.next_ask_step(self.actual_text.ask1[2])
        if self.resp_but_2.active:
            if self.resp_but_2.check_if_clicked(self.mouse_pos):
                if self.actual_text.ask2[1]:
                    self.actual_text.ask2[1].get_quest()
                self.next_ask_step(self.actual_text.ask2[2])
        if self.resp_but_3.active:
            if self.resp_but_3.check_if_clicked(self.mouse_pos):
                if self.actual_text.ask3[1]:
                    self.actual_text.ask3[1].get_quest()
                self.next_ask_step(self.actual_text.ask3[2])
        if self.resp_but_4.active:
            if self.resp_but_4.check_if_clicked(self.mouse_pos):
                if self.actual_text.ask4[1]:
                    self.actual_text.ask4[1].get_quest()
                self.next_ask_step(self.actual_text.ask4[2])


class Quest:
    def __init__(self, game, name, goal_descr, level_req,
                 mobs_to_kill,
                 items_to_collect, item_remove_bool,
                 tiles_to_explore,
                 npcs_to_encounter,
                 reward_xp, reward_gold, reward_item = False):
        self.game = game
        self.name = name
        self.image = quest_bcg_img.copy()
        self.rect = self.image.get_rect()
        self.level_req = level_req
        self.goal_descr = goal_descr
        self.goal = QuestGoal()
        for i in mobs_to_kill:
            self.goal.add_mob_to_kill(i)
        for i in items_to_collect:
            self.goal.add_item_to_collect(i)
        self.item_remove_bool = item_remove_bool
        for i in tiles_to_explore:
            self.goal.add_tile_to_explore(i)
        for i in npcs_to_encounter:
            self.goal.add_npc_to_encounter(i)
        self.reward_xp = reward_xp
        self.reward_gold = reward_gold
        if reward_item:
            self.reward_item = reward_item
        else:
            self.reward_item = False
        self.start_time = 0
        #### JEZELI MA SPRAWDZIC OD RAZU PO ZDARZENIU, uwaga zrobiona narazie opcja z napotkaniem NPC
        #### inne (przedmioty, wrogowie, lub miejsca - do zrobienia sprawdzanie warunku podczas zdarzenia
        #### np po podniesieniu przedmiotu/skrzyni sprawdzam czy nie mam przedmiotów, lub po zabiciu wroga sprawdzam czy nie ma spelnionego questu.
        self.auto_checking = False
        #### PO WYKONANIU QUESTU automatycznie dostaje kolejny! -> object.
        self.auto_next_quest = False

    def put_image(self,image):
        self.image.blit(image,(16,16))

    def put_image_from_tileset(self, x, y, tileset):
        self.image.blit(tileset,(16,16),(x*TILE_SIZE, y*TILE_SIZE,TILE_SIZE,TILE_SIZE))

    def set_to_autochecking(self):
        self.auto_checking = True

    def put_auto_next_quest(self, quest):
        self.auto_next_quest = quest

    def show_quest_icon(self, surface, x, y):
        surface.blit(self.image, (x, y))

    def check_npcs_to_encounter(self) -> bool:
        if len(self.goal.npcs_to_encounter) > 0:
            npc_to_fulfil = []
            print("Sprawdzam czy wykonałes quest. Sprawdzam czy napotkałes npcs")
            npcs_encountered = self.game.events_manager.return_npcs_encountered_names()
            for npc in self.goal.npcs_to_encounter:
                for npc_encountered in npcs_encountered:
                    if npc == npc_encountered:
                        npc_to_fulfil.append(npc)
                        break
            if len(npc_to_fulfil) == len(self.goal.npcs_to_encounter):
                return True
            else:
                return False

    def check_mobs_to_kill(self) -> bool:
        if len(self.goal.mobs_to_kill) > 0:
            mobs_killed_to_fulfil = []
            print("Sprawdzam czy wykonałeś quest. Sprawdzam zabitych przeciwników")
            mobs_killed = self.game.events_manager.return_killed_mobs_names()
            for mob_goal in self.goal.mobs_to_kill:
                for mob_name in mobs_killed:
                    if mob_name == mob_goal:
                        mobs_killed_to_fulfil.append(mob_name)
                        break
            #print("LISTA wykonania z questu " + self.name)
            #print(mobs_killed_to_fulfil)
            #print("LISTA goal.mobs_to_kill:")
            #print(self.goal.mobs_to_kill)
            #print("SPRAWDZAM CZY SIE ZGADZA LICZBA OBIEKTOW!")
            if len(mobs_killed_to_fulfil) == len(self.goal.mobs_to_kill):
                return True
            else:
                return False
        return False

    def check_quest_items(self) -> list:
        if len(self.goal.items_to_collect) > 0:
            collected_quest_items = []
            quest_items_to_fulfil = []
            print ("Sprawdzam czy wykonałeś quest. Sprawdzam przedmioty")
            for slot in self.game.player.inventory.item_slots:
                if slot.item:
                    if slot.item.type == "quest item":
                        #print ("I HAVE QUEST ITEM!!")
                        collected_quest_items.append(slot.item)
            if self.goal.items_to_collect and collected_quest_items:
                for goal_item in self.goal.items_to_collect:
                    #print (goal_item)
                    for quest_item in collected_quest_items:
                        #print (quest_item.name)
                        if quest_item.name == goal_item:
                            quest_items_to_fulfil.append(quest_item)
                            print (f'Masz: {quest_item} i potzebujesz {quest_item.name}! proba OK!')
            print (f'- LISTA FULFIL ITEMS: {quest_items_to_fulfil}')
            print ("removing duplicates....")
            quest_items_to_fulfil = list(dict.fromkeys(quest_items_to_fulfil))
            print(f'- LISTA FULFIL ITEMS AFTER REMOVE DUPL: {quest_items_to_fulfil}')
            print (f'- DLUGOSC LISTY: {len(quest_items_to_fulfil)}')
            print (f'- DLUGOSC LISTY GOAL {len(self.goal.items_to_collect)}')
            ### JEZELI NA LISCIE SA WSZYSTKIE PRZEDMIOTY dopiero wysyłam listę przedmiotów!
            if len(quest_items_to_fulfil) >= len(self.goal.items_to_collect):
                return quest_items_to_fulfil
            else:
                return False
        else:
            return False

    def check_if_fulfiled(self) -> bool:
        ### 1. ITEMS
        quest_items_to_remove = self.check_quest_items()
        if quest_items_to_remove:
            self.emit_the_quest_fulfiled_event()
            ### ZABIERA PRZEDMIOT GDY MA selfi.item_remove_bool
            if self.item_remove_bool: ### czyli czy ma zabierac przedmiot!
                for item in quest_items_to_remove:
                    self.game.player.inventory.remove_item(item)
            return True
        ### 2. NPCs
        npcs_to_encounter = self.check_npcs_to_encounter()
        if npcs_to_encounter:
            self.emit_the_quest_fulfiled_event()
            return True
        ### 3. MOBs to kill
        mobs_to_kill = self.check_mobs_to_kill()
        if mobs_to_kill:
            self.emit_the_quest_fulfiled_event()
            return True
        ### 4. TODO tile(area) to explore

    def emit_the_quest_fulfiled_event(self):
        if not self.game.events_manager.search_event(f'quest {self.name} has been fulfiled'):
            self.game.events_manager.emit(Event(id=f'quest {self.name} has been fulfiled'))

    def collect_reward(self):
        self.game.player.gold += self.reward_gold
        self.game.player.xp += self.reward_xp
        #### GENERUJE PRZEDMIOTY REWARD
        if self.reward_item:
            if self.reward_item[-3:] == "Key":
                item = self.game.levelgen.gen.g_key(self.reward_item,False)
            else:
                item = self.game.levelgen.gen.generate_item_by_name(self.reward_item)
            item_collected = self.game.player.inventory.put_in_first_free_slot(item)
            if not item_collected:
                sprites.Item_to_take(self.game,self.game.player.pos.x, self.game.player.pos.y, item)
        pygame.mixer.Sound.play(coin_snd)
        ### JEZELI AUTO NEXT QUEST - dodaje nowy quest!
        if self.auto_next_quest:
            self.auto_next_quest.get_quest()
        #### SEND INFO
        if not self.game.events_manager.search_event(f'quest {self.name} has been completed'):
            self.game.events_manager.emit(Event(id= f'quest {self.name} has been completed'))
        if not self.game.events_manager.search_event(f'quest {self.name} has been rewarded'):
            self.game.events_manager.emit(Event(id= f'quest {self.name} has been rewarded'))
        pygame.mixer.Sound.play(levelup_snd)
        self.game.put_txt(f'Quest {self.name} finished')
        ### JEZELI AUTO-CHECK i nie prowadzisz rozmowy trzeba nadać informację o zakończeniu questa
        if not self.game.dialog_in_progress:
            self.game.message_box.show_message_quest_reward(f'Quest {self.name} completed!',
                                                            self.reward_gold, self.reward_xp, self.reward_item)
        #### USUWAM ZAKONCZONE QUESTY
        self.game.player.quest_book.remove(self)
        print("NAGRODA ODEBRANA i QUEST ZAPISANY JAKO WYKONANY")

    def get_quest(self):
        print("GOT NEW QUEST")
        self.game.put_txt(f'Got quest {self.name}')
        self.game.events_manager.emit(Event(id=f'got quest {self.name}'))
        self.game.player.quest_book.add_quest(self)
        self.start_time = (int(self.game.player.score_time_played * 1000))


class QuestGoal:
    def __init__(self):
        self.mobs_to_kill = []
        self.items_to_collect = []
        self.tiles_to_explore = []
        self.npcs_to_encounter = []

    def add_mob_to_kill(self,mob_name):
        self.mobs_to_kill.append(mob_name)

    def add_item_to_collect(self,item):
        self.items_to_collect.append(item)

    def add_tile_to_explore(self,tile_pos):
        self.tiles_to_explore.append(tile_pos)

    def add_npc_to_encounter(self,npc):
        self.npcs_to_encounter.append(npc)


class ShopGenerator:
    def __init__(self, game, item_gen):
        self.game = game
        self.item_gen = item_gen
        self.level_02_magic_shop = Shop(self.game, "Magic Shop 02", "magic",
                                        129, 150, "Harold the Alchemist", default_shop_owner_img, self.item_gen)
        self.level_02_smith_shop = Shop(self.game, "Smith 02", "smith",
                                        59, 100, "Jendryk the Smith", default_shop_owner_img, self.item_gen)
        self.level_02_inn = Shop(self.game, "Inn 02", "inn",
                                 99, 50, "Donald the Innkeeper", default_shop_owner_img, self.item_gen)
        self.level_05_inn = Shop(self.game, "Inn 05", "inn",
                                 159,120,"Astrid the Bartender",default_shop_owner_img,self.item_gen)
        self.level_05_magic_shop = Shop(self.game, "Magic Shop 05", "magic",
                                        229, 150, "Aghaton the Wise", default_shop_owner_img, self.item_gen)
        self.level_05_smith_shop = Shop(self.game, "Smith 05", "smith",
                                        259, 100, "Megathon the Smith", default_shop_owner_img, self.item_gen)
        self.level_06_inn = Shop(self.game, "Inn 06", "inn",
                                 159, 120, "Astrid the Bartender", default_shop_owner_img, self.item_gen)

        self.shops = {'Magic Shop 02': self.level_02_magic_shop,
                      'Smith 02': self.level_02_smith_shop,
                      'Inn 02': self.level_02_inn,
                      'Inn 05': self.level_05_inn,
                      'Magic Shop 05': self.level_05_magic_shop,
                      'Smith 05': self.level_05_smith_shop,
                      'Inn 06': self.level_06_inn
                      }

    def generate_shop_by_name(self, name):
        if name == "Magic Shop 02":
            print("shop on level 02 created")
            return self.level_02_magic_shop
        if name == "Smith 02":
            print("shop on level 02 created")
            return self.level_02_smith_shop
        if name == "Inn 02":
            print ("inn on level 02 created")
            return self.level_02_inn
        if name == "Inn 05":
            print ("inn lvl 05 created")
            return self.level_05_inn
        if name == "Magic Shop 05":
            print("shop on level 05 created")
            return self.level_05_magic_shop
        if name == "Smith 05":
            print("shop on level 05 created")
            return self.level_05_smith_shop
        if name == "Inn 06":
            print("inn lvl 06 created")
            return self.level_06_inn
        print ("ERROR IN SHOP GENERATION (name not recognized")

    def load_shops_data(self, shops_data):
        print("SHOPS_DATA:")
        print(shops_data)
        for shop in self.shops:
            print (f'LOADING SHOP {shop}')
            print (f'ACCESING TO {self.shops[shop]}')
            self.shops[shop].set_owner_gold(shops_data[shop]['owner_gold'])
            if shops_data[shop]['ask1_namecond_list']:
                print ("Putting items in INV by namecond list - ask1")
                self.shops[shop].set_ask1_items_by_namecondlist(shops_data[shop]['ask1_namecond_list'])
            if shops_data[shop]['ask2_namecond_list']:
                print("Putting items in INV by namecond list - ask2")
                self.shops[shop].set_ask2_items_by_namecondlist(shops_data[shop]['ask2_namecond_list'])
            if shops_data[shop]['ask3_namecond_list']:
                print("Putting items in INV by namecond list - ask3")
                self.shops[shop].set_ask3_items_by_namecondlist(shops_data[shop]['ask3_namecond_list'])
            if shops_data[shop]['ask4_namecond_list']:
                print("Putting items in INV by namecond list - ask4")
                self.shops[shop].set_ask4_items_by_namecondlist(shops_data[shop]['ask4_namecond_list'])

    def save_shops_data(self):
        self.saved_shops_dic = {}
        for shop in self.shops:
            print(f'SAVING SHOP {shop}')
            print(f'GETTING INFO FROM {self.shops[shop]}')
            owner_gold = self.shops[shop].owner_gold
            ask1_namecond_list = self.shops[shop].shop_ask1.return_inventory_namecond_list()
            ask2_namecond_list = self.shops[shop].shop_ask2.return_inventory_namecond_list()
            ask3_namecond_list = self.shops[shop].shop_ask3.return_inventory_namecond_list()
            ask4_namecond_list = self.shops[shop].shop_ask4.return_inventory_namecond_list()
            self.saved_shops_dic[shop] = {'owner_gold':owner_gold,
                                          'ask1_namecond_list':ask1_namecond_list,
                                          'ask2_namecond_list':ask2_namecond_list,
                                          'ask3_namecond_list':ask3_namecond_list,
                                          'ask4_namecond_list':ask4_namecond_list,
                                          }
        print(self.saved_shops_dic)
        return self.saved_shops_dic


class ShopAsk:
    def __init__(self, shop_type):
        self.shop_type = shop_type
        self.text = ""
        self.activity = False
        self.inventory = False

    def put_inventory(self,x,y):
        self.inventory = Inventory(slot_img,x,y)

    def put_repair_inv(self):
        self.inventory = RepairInventory(slot_img)

    def put_text(self, text):
        self.text = text

    def configure_activity(self, activity):
        self.activity = activity

    def return_inventory_namecond_list(self):
        if self.inventory:
            if isinstance(self.inventory, Inventory):
                return self.inventory.return_item_namecond_list()
            else:
                return False
        else:
            return False


class Shop:
    def __init__(self, game, name, shop_type, quality, owner_gold, owner_name, owner_image, item_gen):
        self.game = game
        self.name = name
        self.item_gen = item_gen
        self.shop_name = name[:-2]
        self.owner_name = owner_name
        self.act_inventory = False
        self.image = dialogbox_img_2.copy()
        self.pos = DIAL_BOX_POS
        ### type - Magical, Smith etc..
        self.shop_type = shop_type
        self.shop_ask1 = ShopAsk(self.shop_type)
        self.shop_ask2 = ShopAsk(self.shop_type)
        self.shop_ask3 = ShopAsk(self.shop_type)
        self.shop_ask4 = ShopAsk(self.shop_type)
        ### quality - Max cost of items...
        self.quality = quality
        self.owner_image = owner_image
        self.owner_attitude = 100
        self.owner_gold = owner_gold
        self.repair_cost = 0
        self.arrow_price = 5
        self.recover_price = 2
        self.arrow_pack = 10
        self.rest_price = 10
        self.open = True
        self.welcome_text = "Welcome adventurer!"
        if self.shop_type == "magic":
            self.shop_ask1.put_text("Can I see your potions?")
            self.shop_ask1.configure_activity("buy and sell")
            self.shop_ask1.put_inventory(10,6)
            self.generate_new_potions(self.shop_ask1.inventory)
            self.shop_ask2.put_text("Can I see your books?")
            self.shop_ask2.configure_activity("buy and sell")
            self.shop_ask2.put_inventory(10, 6)
            self.generate_new_books(self.shop_ask2.inventory)
            self.shop_ask3.put_text("I`d like to see your magic items for sale")
            self.shop_ask3.configure_activity("buy and sell")
            self.shop_ask3.put_inventory(10, 6)
            self.generate_new_magic_items(self.shop_ask3.inventory)
            # W II Czesci gry beda rozdzki...
            #self.shop_ask4.put_text("Please recharge my wand")
            #self.shop_ask4.configure_activity("recharge wand")
        elif self.shop_type == "smith":
            self.shop_ask1.put_text("Can I see your armors?")
            self.shop_ask1.configure_activity("buy and sell")
            self.shop_ask1.put_inventory(10, 6)
            self.generate_new_items("armor",self.shop_ask1.inventory)
            self.shop_ask2.put_text("Can I see yout weapons?")
            self.shop_ask2.configure_activity("buy and sell")
            self.shop_ask2.put_inventory(10, 6)
            self.generate_new_items("weapon",self.shop_ask2.inventory)
            self.shop_ask3.put_text("Please reapir my item")
            self.shop_ask3.configure_activity("repair")
            self.shop_ask3.put_repair_inv()
            self.shop_ask4.put_text("I`d like to buy some arrows (10 arrows for 5 gold)")
            self.shop_ask4.configure_activity("arrows")
        elif self.shop_type == "inn":
            self.shop_ask1.put_text("Have a drink? (Restores HP and MP for 2 gold)")
            self.shop_ask1.configure_activity("recover")
            self.shop_ask2.put_text("Something for takeaway?")
            self.shop_ask2.configure_activity("buy and sell")
            self.shop_ask2.put_inventory(10,6)
            self.generate_new_potions(self.shop_ask2.inventory)
            self.shop_ask3.put_text("Rest (SAVE GAME and restore HP for 10 gold")
            self.shop_ask3.configure_activity("rest")
        else:
            self.shop_ask1.put_text("Wish you trade?")
            self.shop_ask1.configure_activity("buy and sell")
            print ("ERROR IN DECODING SHOP TYPE")
        #### POSIBLE PHASES
        self.local_ph_buy_and_sell = False
        self.local_ph_repair = False
        self.local_ph_charge_wands = False
        self.local_ph_arrows = False
        self.local_ph_rest = False
        self.local_ph_restore = False
        #### EXIT BUTTON
        self.exit_button = RadioButton(rad_back_img, rad_back_h_img, 178,290)
        self.repair_button = RadioButton(repb_img, repb_h_img,345,145)
        ##########
        self.subscribe_owner_to_all_items()

    def generate_new_items(self,item_type,inventory):
        items_no = 0
        items_maxcost = 0
        if 0 < self.quality <= 100:
            items_no = random.randint(5, 10)
            items_maxcost = self.quality
        elif 100 < self.quality:
            items_no = random.randint(5, 25)
            items_maxcost = self.quality
        else:
            print("ERROR 0 or neg number of items in shop while generating shop items")
        if items_no > 0:
            for i in range(items_no):
                inventory.put_in_first_free_slot(
                    self.item_gen.generate_random_item(item_type,items_maxcost))

    def generate_new_smith_items(self,inventory):
        items_no = 0
        items_maxcost = 0
        if 0 < self.quality <= 100:
            items_no = random.randint(8, 16)
            items_maxcost = self.quality
        elif 100 < self.quality:
            items_no = random.randint(10, 25)
            items_maxcost = self.quality
        else:
            print("ERROR 0 or neg number of items in shop while generating shop items")
        if items_no > 0:
            for i in range(items_no):
                inventory.put_in_first_free_slot(
                    self.item_gen.generate_random_item("smith",items_maxcost))

    def generate_new_books(self,inventory):
        items_no = 0
        items_maxcost = 0
        if 0 < self.quality <= 100:
            items_no = random.randint(1, 3)
            items_maxcost = self.quality + 200
        elif 100 < self.quality:
            items_no = random.randint(2, 6)
            items_maxcost = self.quality + 400
        else:
            print("ERROR 0 or neg number of items in shop while generating shop items")
        ## TODO wiecej eliksirow mniej innych, sie zobaczy jak wyskakują
        if items_no > 0:
            for i in range(items_no):
                inventory.put_in_first_free_slot(
                    self.item_gen.generate_random_item("book", items_maxcost))

    def generate_new_potions(self,inventory):
        items_no = 0
        items_maxcost = 0
        if 0 < self.quality <= 100:
            items_no = random.randint(5, 15)
            items_maxcost = self.quality
        elif 100 < self.quality:
            items_no = random.randint(10, 25)
            items_maxcost = self.quality
        else:
            print("ERROR 0 or neg number of items in shop while generating shop items")
        ## TODO wiecej eliksirow mniej innych, sie zobaczy jak wyskakują
        if items_no > 0:
            for i in range(items_no):
                inventory.put_in_first_free_slot(
                    self.item_gen.generate_random_item("potion",items_maxcost))

    def generate_new_magic_items(self,inventory):
        items_no = 0
        items_maxcost = 0
        if 0 < self.quality <= 100:
            items_no = random.randint(2, 5)
            items_maxcost = self.quality
        elif 100 < self.quality:
            items_no = random.randint(4, 10)
            items_maxcost = self.quality
        else:
            print("ERROR 0 or neg number of items in shop while generating shop items")
        ## TODO wiecej eliksirow mniej innych, sie zobaczy jak wyskakują
        if items_no > 0:
            for i in range(items_no):
                inventory.put_in_first_free_slot(
                    self.item_gen.generate_random_item("rings",items_maxcost))

    def set_owner_gold(self, owner_gold):
        self.owner_gold = owner_gold

    def set_ask1_items_by_namecondlist(self, namecond_list):
        if self.shop_ask1.activity == "buy and sell":
            self.shop_ask1.inventory.remove_all()
            for tuple in namecond_list:
                item = self.item_gen.load_item_by_name(tuple[0], tuple[1])
                self.shop_ask1.inventory.put_in_first_free_slot(item)
        self.subscribe_owner_to_all_items()

    def set_ask2_items_by_namecondlist(self, namecond_list):
        if self.shop_ask2.activity == "buy and sell":
            self.shop_ask2.inventory.remove_all()
            for tuple in namecond_list:
                item = self.item_gen.load_item_by_name(tuple[0], tuple[1])
                self.shop_ask2.inventory.put_in_first_free_slot(item)
        self.subscribe_owner_to_all_items()

    def set_ask3_items_by_namecondlist(self, namecond_list):
        if self.shop_ask3.activity == "buy and sell":
            self.shop_ask3.inventory.remove_all()
            for tuple in namecond_list:
                item = self.item_gen.load_item_by_name(tuple[0], tuple[1])
                self.shop_ask3.inventory.put_in_first_free_slot(item)
        self.subscribe_owner_to_all_items()

    def set_ask4_items_by_namecondlist(self, namecond_list):
        if self.shop_ask4.activity == "buy and sell":
            self.shop_ask4.inventory.remove_all()
            for tuple in namecond_list:
                item = self.item_gen.load_item_by_name(tuple[0], tuple[1])
                self.shop_ask4.inventory.put_in_first_free_slot(item)
        self.subscribe_owner_to_all_items()

    def set_owner_attitude(self, attitude):
        self.owner_attitude = attitude

    def subscribe_owner_to_all_items(self):
        if self.shop_ask1.inventory:
            if isinstance(self.shop_ask1.inventory, Inventory):
                for slot in self.shop_ask1.inventory.item_slots:
                    if slot.item:
                        slot.item.owner = "shop"
        if self.shop_ask2.inventory:
            if isinstance(self.shop_ask2.inventory, Inventory):
                for slot in self.shop_ask2.inventory.item_slots:
                    if slot.item:
                        slot.item.owner = "shop"
        if self.shop_ask3.inventory:
            if isinstance(self.shop_ask3.inventory, Inventory):
                for slot in self.shop_ask3.inventory.item_slots:
                    if slot.item:
                        slot.item.owner = "shop"
        if self.shop_ask4.inventory:
            if isinstance(self.shop_ask4.inventory, Inventory):
                for slot in self.shop_ask4.inventory.item_slots:
                    if slot.item:
                        slot.item.owner = "shop"

    def check_gold(self, item) -> bool:
        price = self.calculate_buy_from_player_price(item)
        if self.owner_gold >= price:
            return True
        else:
            return False

    def sell_to_player(self, item):
        price = self.calculate_sell_to_player_price(item)
        print (price)
        pygame.mixer.Sound.play(coin_snd)
        self.owner_gold += price
        self.game.player.gold -= price
        item.owner = "player"

    def buy_from_player(self, item):
        price = self.calculate_buy_from_player_price(item)
        print(price)
        pygame.mixer.Sound.play(coin_snd)
        self.owner_gold -= price
        self.game.player.gold += price
        item.owner = "shop"

    def local_ph_deactivate(self):
        self.local_ph_buy_and_sell = False
        self.local_ph_repair = False
        self.local_ph_charge_wands = False
        self.local_ph_arrows = False
        self.act_inventory = False
        #self.exit_button.deactivate()

    def activate_ask(self, ask):
        print ("Function activate ask with ask.activity: " + ask.activity)
        if ask.activity == "buy and sell":
            self.game.ph_shop = False
            self.game.ph_buy_and_sell = True
            self.activate_buy_and_sell(ask.inventory)
        elif ask.activity == "repair":
            self.game.ph_shop = False
            self.game.ph_repair = True
            self.activate_repair(ask.inventory)
        elif ask.activity == "recharge wand":
            pass
            ## TODO
        elif ask.activity == "arrows":
            ## FOR KNOW NO SPECIAL PHASE< DIRECT pack to buy wih price. arrows unlimited.
            self.buy_arrows()
        elif ask.activity == "rest":
            self.rest()
        elif ask.activity == "recover":
            self.recover()
        else:
            print ("ERROR couldnt encode ask1 activity")

    def buy_arrows(self):
        if self.game.player.gold >= self.arrow_price:
            self.game.player.gold -= self.arrow_price
            self.game.player.arrows += self.arrow_pack
            self.owner_gold += self.arrow_price
            pygame.mixer.Sound.play(coin_snd)
        else:
            pygame.mixer.Sound.play(empty_spell_snd)
        self.back_to_shop_dialog()

    def recover(self):
        if self.game.player.gold >= self.recover_price:
            self.game.player.gold -= self.recover_price
            self.game.player.act_hp = self.game.player.max_hp
            self.game.player.act_mana = self.game.player.max_mana
            self.owner_gold += self.recover_price
            pygame.mixer.Sound.play(drink_snd)
        else:
            pygame.mixer.Sound.play(empty_spell_snd)
        self.back_to_shop_dialog()

    def rest(self):
        if self.game.player.gold >= self.rest_price:
            if not self.game.item_picked:
                self.game.q_box.ask_save_game(self.tavern_save_game)
            else:
                pygame.mixer.Sound.play(empty_spell_snd)
                self.game.put_txt("Please remove your item to inventory before saving game")
        else:
            pygame.mixer.Sound.play(empty_spell_snd)
            self.game.put_txt("Not enough gold")
        self.game.paused = True
        self.back_to_shop_dialog()

    def tavern_save_game(self):
        print("Tavern save game funccion")
        self.game.player.gold -= self.rest_price
        self.owner_gold += self.rest_price
        pygame.mixer.Sound.play(coin_snd)
        self.game.save_game()
        self.game.ph_shop = False
        self.game.paused = True
        self.game.message_box.show_message("Tavern","Game Saved. You wake up next morning..")

    def activate_repair(self, inventory):
        self.act_inventory = inventory
        self.local_ph_repair = True
        self.local_ph_buy_and_sell = False
        self.blit_upper_part()
        self.exit_button.activate()
        self.repair_button.activate()

    def activate_buy_and_sell(self, inventory):
        print ("ENTERING INVENTORY (ph buy_and_sell")
        ### ENTER THE SHOP`S INVENTRORY
        self.act_inventory = inventory
        self.local_ph_repair = False
        self.local_ph_buy_and_sell = True
        self.blit_upper_part()
        self.exit_button.activate()
        self.repair_button.deactivate()

    def clear_image(self):
        self.image = dialogbox_img_2.copy()

    def blit_upper_part(self):
        self.image.blit(self.owner_image, DB2_IMG_POS)
        self.game.s_write(self.owner_name, self.image, DB2_TXT_POS, WHITE)

    def show(self, screen):
        if self.local_ph_buy_and_sell:
            self.clear_image()
            self.blit_upper_part()
            self.act_inventory.show_inv(self.image,MAP_TOPLEFT[0] + 60,MAP_TOPLEFT[1]+70)
            self.exit_button.show_button(self.image)
            self.image.blit(gold_coin,(85,315))
            self.game.s_write(str(self.owner_gold),self.image,(102,310),YELLOW)
            self.game.s_write("OWNER GOLD:",self.image,(75,290),YELLOW)
            if self.game.item_picked:
                if self.game.item_picked.owner == "shop":
                    self.image.blit(gold_coin,(315,315))
                    self.game.s_write("SELL PRICE:",self.image,(310,290),YELLOW)
                    self.game.s_write(str(self.calculate_sell_to_player_price(self.game.item_picked)),
                                      self.image,(332,310),YELLOW)
                else:
                    self.image.blit(gold_coin, (315, 315))
                    self.game.s_write("BUY PRICE:",self.image,(310,290),YELLOW)
                    self.game.s_write(str(self.calculate_buy_from_player_price(self.game.item_picked)),
                                      self.image,(332,310),YELLOW)
            screen.blit(self.image, (self.pos))
        elif self.local_ph_repair:
            self.clear_image()
            self.blit_upper_part()
            self.act_inventory.show_inv(self.image,160,125)
            self.exit_button.show_button(self.image)
            self.repair_button.show_button(self.image)
            self.image.blit(gold_coin, (85, 315))
            self.game.s_write(str(self.owner_gold), self.image, (102, 310), YELLOW)
            self.game.s_write("OWNER GOLD:",self.image,(75,290),YELLOW)
            self.game.s_write("PUT ITEM HERE:",self.image,(130,100),WHITE)
            if not self.act_inventory.check_free():
                if isinstance(self.act_inventory.item_slot.item, sprites.Armor) or\
                        isinstance(self.act_inventory.item_slot.item, sprites.Weapon):
                    item_condition = int(self.act_inventory.item_slot.item.condition)
                    item_repair_cost = int(self.calculate_repair_cost(self.act_inventory.item_slot.item))
                    self.game.s_write(self.act_inventory.item_slot.item.name,self.image, (195,130))
                    self.game.s_write(f'Item condition: {item_condition}',self.image,(160,170),WHITE)
                    self.game.s_write(f'Item durability: {self.act_inventory.item_slot.item.durability}',self.image,(160,195),WHITE)
                    self.game.s_write(f'COST TO REPAIR: {item_repair_cost}',self.image,(160,220),WHITE)
            if self.game.item_picked:
                if isinstance (self.game.item_picked, sprites.Weapon) or isinstance(self.game.item_picked, sprites.Armor):
                    # TODO jaks strzalke wskazujaca gdzie polozyc
                    pygame.draw.rect(self.image,RED,(160,125,32,32),3)
            screen.blit(self.image, (self.pos))
        else:
            print ("ERROR DONT KNOW WHAT ACTIVITY OF THE SHOP I HAVE TO SHOW")

    def calculate_repair_cost(self, item):
        #print ("calculating repair cost")
        max_cost = item.cost
        condition_percentage = item.condition/100
        durability_factor = 1 + item.durability/100
        repair_cost = (max_cost - (max_cost * condition_percentage)) * durability_factor
        self.repair_cost = int(repair_cost)
        return repair_cost

    def calculate_sell_to_player_price(self, item):
        owner_attitude = self.calculate_owner_attitude()
        ## NA WYPADEK BLEDU, owner attitude powinien byc w zakresie (0:200)
        if owner_attitude <= 0:
            owner_attitude = 0
        elif owner_attitude >200:
            owner_attitude = 200
        ## obliczam:
        item_cost = round(1.5 * item.cost - (owner_attitude / 200 * item.cost) + item.cost * 0.5, 0)
        ## zużyte kosztują mniej!
        if isinstance(item, sprites.Armor) or isinstance(item, sprites.Weapon):
            item_cost = 0.25 * item_cost + (0.75 * item_cost * item.condition / 100)
        return int(item_cost)

    def calculate_buy_from_player_price(self, item):
        owner_attitude = self.calculate_owner_attitude()
        ## NA WYPADEK BLEDU, owner attitude powinien byc w zakresie (0:200)
        if owner_attitude <= 0:
            owner_attitude = 0
        elif owner_attitude > 200:
            owner_attitude = 200
        if owner_attitude == 100:
            item_cost = 0.5 * item.cost
        elif 100 < owner_attitude < 200:
            item_cost = 0.5 * item.cost + (item.cost * (owner_attitude - 100) / 200)
        elif owner_attitude < 100:
            item_cost = 0.25 * item.cost + (0.25 * item.cost * owner_attitude / 100)
        else:
            print ("ERROR Calc shopping price")
            return 0.5 * item.cost
        ## zuzyte kosztuja mniej!
        if isinstance(item, sprites.Armor) or isinstance(item, sprites.Weapon):
            item_cost = 0.25 * item_cost + (0.75 * item_cost * item.condition / 100)
        return int(round(item_cost,0))

    def calculate_owner_attitude(self):
        owner_attitude = self.owner_attitude + 5 * self.game.player.stealth + self.game.player.barter_bonus
        #print ("owner attitude" + str(owner_attitude))
        return owner_attitude

    def update(self, mouse_pos):
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        mouse_x -= self.pos[0]
        mouse_y -= self.pos[1]
        self.mouse_pos = (mouse_x, mouse_y)
        if self.game.item_picked:
            self.exit_button.deactivate()
            self.repair_button.deactivate()
        else:
            self.exit_button.activate()
            self.repair_button.activate()
        if self.game.ph_repair:
            if self.act_inventory.item_slot.item:
                self.repair_button.activate()
                self.repair_button.check_if_highlight(self.mouse_pos)
                self.exit_button.deactivate()
            else:
                self.exit_button.activate()
                self.repair_button.deactivate()
        # print ("mod_mouse a (%d, %d)" % self.mouse_pos)
        self.exit_button.check_if_highlight(self.mouse_pos)


    def check_exit_button(self, mouse_pos):
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        mouse_x -= self.pos[0]
        mouse_y -= self.pos[1]
        self.mouse_pos = (mouse_x, mouse_y)
        if self.exit_button.check_if_clicked(self.mouse_pos):
            print("EXIT SHOP INV CLICKED")
            self.back_to_shop_dialog()
            #self.exit_shop()

    def check_repair_button(self, mouse_pos):
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        mouse_x -= self.pos[0]
        mouse_y -= self.pos[1]
        self.mouse_pos = (mouse_x, mouse_y)
        if not self.act_inventory.check_free():
            if self.repair_button.check_if_clicked(mouse_pos):
                print ("Repair. button clicked.")
                if self.repair_cost <= self.game.player.gold and self.repair_cost > 0:
                    print ("Repair" + self.act_inventory.item_slot.item.name)
                    self.owner_gold += self.repair_cost
                    pygame.mixer.Sound.play(smith_snd)
                    self.act_inventory.item_slot.item.repair(100)
                    self.game.player.gold -= self.repair_cost
                    self.game.player.update_stats()
                else:
                    print ("NO GOLD on WEAPON IN GOOD SHAPE")
        else:
            print ("NO ITEM ON REPAIR SLOT")

    def exit_shop(self):
        print ("Exit SHOP function")
        self.local_ph_deactivate()
        self.clear_image()
        self.repair_button.deactivate()
        self.game.ph_buy_and_sell = False
        self.game.ph_shop = False
        self.game.ph_repair = False
        self.repair_cost = 0
        self.game.back_to_game_and_unpause()

    def back_to_shop_dialog(self):
        print ("Back to shop dialog function")
        self.local_ph_deactivate()
        self.clear_image()
        self.repair_button.deactivate()
        self.game.ph_buy_and_sell = False
        self.game.ph_repair = False
        self.repair_cost = 0
        self.ph_shop = True
        self.game.shop_dialog_box.start_conversation(self)









