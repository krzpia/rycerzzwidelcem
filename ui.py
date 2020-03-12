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


class SpellBook:
    def __init__(self, game):
        self.game = game
        self.spells = []
        self.image = pygame.Surface((MAP_WIDTH, 466), pygame.HWSURFACE | pygame.SRCALPHA)
        self.image.blit(spellbook_bcg_img, (0, 0))
        self.pos = (5,100)
        self.spellgenerator = spells.SpellGenerator()

    def add_spell(self, spell):
        if len(self.spells)<11:
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

    def show(self, screen, pos = (5,100)):
        self.image.blit(spellbook_bcg_img, (0, 0))
        self.pos = pos
        counter = 0
        x_pos = 40
        # na razie tylko 1 strona
        for i in self.spells:
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
            if counter >= 6:
                x_pos = 330
                counter = 0
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


class DialogBox:
    def __init__(self, game):
        self.game = game
        self.pos = (50, 120)
        self.image = dialogbox_img.copy()
        self.ok_button = RadioButton(rad_ok_img,rad_ok_h_img,178,290)
        self.act_line = False
        self.last_line = False
        self.npc = False
        self.step = 0
        #self.write("TEST", 0)

    def find_act_line(self):
        for line in self.npc.dialogs.lines:
            if line.nr == self.step:
                if line.active:
                    self.act_line = line
                    return 1
        print ("CANNOT FIND A LINE")

    def start_conversation(self,npc):
        self.step = 0
        self.clear()
        self.npc = npc
        self.find_act_line()
        self.write_line()

    def write_line(self):
        if self.act_line.speaker == "n":
            self.image.blit(pygame.transform.scale(self.npc.image,(48,48)), (210, 18))
            self.game.s_write(self.npc.name,self.image,(80,35),(WHITE))
        elif self.act_line.speaker == "p":
            self.image.blit(pygame.transform.scale(self.game.player.image, (48, 48)), (210, 18))
            self.game.s_write(self.game.player.name, self.image, (80, 35), (WHITE))
        self.write(self.act_line.txt,0)

    def next(self):
        self.step += 1
        self.last_line = self.act_line
        self.clear()
        self.find_act_line()
        self.write_line()
        if self.last_line:
            print ("LAST LINE: " + self.last_line.txt)
        print ("ACT LINE: " + self.act_line.txt )

    def write(self, txt, ln):
        self.game.s_write(txt,self.image, (35, 100 + ln * 20), (WHITE))

    def clear(self):
        self.image = dialogbox_img.copy()

    def show(self, screen):
        self.ok_button.show_button(self.image)
        screen.blit(self.image, self.pos)

    def update(self, mouse_pos):
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        mouse_x -= self.pos[0]
        mouse_y -= self.pos[1]
        self.mouse_pos = (mouse_x, mouse_y)
        self.ok_button.check_if_highlight(self.mouse_pos)

    def check_buttons(self, mouse_pos):
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        mouse_x -= self.pos[0]
        mouse_y -= self.pos[1]
        self.mouse_pos = (mouse_x, mouse_y)
        if self.ok_button.active:
            if self.ok_button.check_if_clicked(self.mouse_pos):
                if self.act_line.type == "b":
                    self.game.dialog_in_progress = False
                    self.game.paused = False
                else:
                    self.next()

class NpcDialogData:
    def __init__(self, game):
        self.game = game
        self.lines = []
        self.quests = False

    def add_line(self, type, speaker, active, goto, statchange, txt):
        nr = len(self.lines)
        self.lines.append(DialLine(nr,type, speaker,active,goto,statchange, txt))

    def print_lines(self):
        for line in self.lines:
            print(str(line.nr) + line.txt)

    def get_line_txt(self, nr):
        return self.lines[nr].txt

    def get_line(self, nr):
        return self.lines[nr]

class DialLine:
    def __init__(self, nr, type, speaker, active, goto, statchange, txt):
        self.nr = nr
        self.type = type
        self.speaker = speaker
        self.active = active
        self.goto = goto
        self.statchange = statchange
        self.txt = txt







