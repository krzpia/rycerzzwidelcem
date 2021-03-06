import pygame
from settings import *
vec = pygame.math.Vector2
from ui import *
import random
import math
import pytweening as pytw
from os import path
from data import *
from itertools import chain
from events.event import Event

pygame.init()

snd_folder = path.join(path.dirname(__file__), 'sound')
drink_snd = pygame.mixer.Sound(path.join(snd_folder, 'drink.wav'))
pick_item_snd = pygame.mixer.Sound(path.join(snd_folder, 'pick_item.wav'))
chop_snd = pygame.mixer.Sound(path.join(snd_folder, 'chop.wav'))
swing_snd = pygame.mixer.Sound(path.join(snd_folder, 'swing.wav'))
hit_snd = pygame.mixer.Sound(path.join(snd_folder, 'hit.wav'))
win_snd = pygame.mixer.Sound(path.join(snd_folder, 'win.wav'))
ouch_snd = pygame.mixer.Sound(path.join(snd_folder, 'ouch.wav'))

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

def collide_double_hit_rect(one, two):
    return one.hit_rect.colliderect(two.hit_rect)

def collide_hr_obstacle(sprite, group, dir):
    if dir == 'x':
        hits = pygame.sprite.spritecollide(sprite,group,False,collide_double_hit_rect)
        if hits:
            if hits[0].hit_rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].hit_rect.left - sprite.hit_rect.width / 2
            if hits[0].hit_rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].hit_rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pygame.sprite.spritecollide(sprite,group,False,collide_double_hit_rect)
        if hits:
            if hits[0].hit_rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].hit_rect.top - sprite.hit_rect.height / 2
            if hits[0].hit_rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].hit_rect.bottom + sprite.hit_rect.height /2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

def collide_wall(sprite, group, dir):
    if dir == 'x':
        hits = pygame.sprite.spritecollide(sprite,group,False,collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pygame.sprite.spritecollide(sprite,group,False,collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height /2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


class Arrow(pygame.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self._layer = HIT_GRAPHICS_LAYER
        self.groups = game.act_lvl.all_sprites, game.act_lvl.arrows
        pygame.mixer.Sound.play(bow_snd)
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.speed = 400
        self.lifetime = 800
        self.game = game
        self.name = "Arrow"
        self.pos = vec(pos)
        self.vel = dir * self.speed
        self.image = arrow_img
        self.image = pygame.transform.rotate(self.image,dir.angle_to(vec(1,0)))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.hit_rect = self.rect
        self.game.player.score_arrows += 1
        self.spawn_time = (int(self.game.player.score_time_played * 1000))

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        ### KOLIZJA Z MUREM (ale nie wodą!)
        hits = pygame.sprite.spritecollide(self,self.game.act_lvl.walls,False)
        for hit in hits:
            if not hit.water:
                self.kill()
        now = (int(self.game.player.score_time_played * 1000))
        if now - self.spawn_time > self.lifetime:
            self.kill()


class Spell_Bullet(pygame.sprite.Sprite):
    def __init__(self, game, spell, pos, dir):
        self._layer = HIT_GRAPHICS_LAYER
        self.groups = game.act_lvl.all_sprites, game.act_lvl.arrows
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.spell = spell
        pygame.mixer.Sound.play(self.spell.cast_sound)
        self.speed = self.spell.bullet_speed
        self.range = self.spell.bullet_range
        if self.spell.subtype == "poison cloud":
            self.damage = 0
        else:
            self.damage = self.spell.damage + int(self.game.player.intellect * self.game.player.spell_power_bonus)
        self.blow_effect = self.spell.blow_effect
        self.blow_radius_sizer = self.spell.blow_radius_sizer
        self.blow_damage = self.spell.blow_damage
        self.blow_anim = self.spell.blow_anim_img
        self.blow_duration = self.spell.blow_duration
        self.burn_effect = self.spell.burn_effect
        self.freeze_effect = self.spell.freeze_effect
        self.slow_effect = self.spell.slow_effect
        self.bullet_image = self.spell.bullet_img
        self.start_pos = vec(pos)
        self.pos = vec(pos)
        self.vel = dir * self.speed
        self.image = self.bullet_image
        self.image = pygame.transform.rotate(self.image,dir.angle_to(vec(1,0)))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.hit_rect = self.rect
        self.game.player.score_spell_bullets += 1
        self.spawn_time = (int(self.game.player.score_time_played * 1000))

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        distance = vec.length_squared(self.pos - self.start_pos)
        if distance >= self.range ** 2:
            self.blow()
        wall_hits = pygame.sprite.spritecollide(self,self.game.act_lvl.walls,False)
        #print (wall_hits)
        for wall_hit in wall_hits:
            if isinstance(wall_hit,Obstacle):
                if not wall_hit.water:
                    self.blow()

    def blow(self):
        if self.blow_effect:
            if self.spell.subtype == "fire":
                pygame.mixer.Sound.play(fireblow_snd)
            Blow_Spell(self.game, self.pos,self.blow_anim,
                       self.blow_radius_sizer,self.blow_damage, self.blow_duration)
            self.kill()
        else:
            self.kill()


class Blow_Spell(pygame.sprite.Sprite):
    def __init__(self, game, pos, images, size, strength, duration):
        self._layer = HIT_GRAPHICS_LAYER
        self.groups = game.act_lvl.all_sprites, game.act_lvl.lavas
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.strength = strength + int(self.game.player.intellect * self.game.player.spell_power_bonus)
        self.radius_sizer = size
        self.duration = duration
        #### CZAS TRWANIA EFEKTU = DURATION + INT
        if self.duration:
            self.duration += self.game.player.intellect
        self.effect = ActiveEffect("fire", e_fire_ico, self.strength, 1)
        self.images = images
        self.image = self.images[0]
        self.base_size_image = self.images[3]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = (int(self.game.player.score_time_played * 1000))
        self.animation_time = 0
        self.last_animation_time = 0
        self.counter = 0
        self.sizer = 0


    def update(self):
        self.animation_time += self.game.unpaused_dt
        if self.animation_time - self.last_animation_time > 0.1:
            self.counter += 1
            if self.counter > 3:
                #### GDY WYBUCH MA SIE POWIEKSZAC zmienna blow_radius_sizer
                if self.radius_sizer:
                    self.sizer += 5
                    if self.sizer <= self.radius_sizer:
                        #print ("Increasing SIZE by "+ str(self.sizer))
                        self.image = pygame.transform.scale(self.base_size_image,(32+self.sizer,32+self.sizer))
                        self.rect = self.image.get_rect()
                        self.rect.center = self.pos
                        self.hit_rect = self.rect
                        self.last_animation_time = self.animation_time
                    else:
                        self.kill()
                else:
                    self.counter = 0
                    if self.animation_time > self.duration:
                        self.kill()
            else:
                #print ("image nr "+ str(self.counter))
                self.image.fill((0,0,0,0))
                self.image.blit(self.images[self.counter],(0,0))
                self.last_animation_time = self.animation_time


class Swing(pygame.sprite.Sprite):
    def __init__(self, game, pos, dir, size):
        self._layer = HIT_GRAPHICS_LAYER
        self.groups = game.act_lvl.all_sprites, game.act_lvl.melle_swing
        pygame.sprite.Sprite.__init__(self, self.groups)
        pygame.mixer.Sound.play(swing_snd)
        self.game = game
        self.lifetime = 120
        self.pos = vec(pos.x -12,pos.y)
        self.dir = dir
        if size == "small":
            self.base_image = swing_small
        elif size == "medium":
            self.base_image = swing_medium
        elif size == "big":
            self.base_image = swing_big
        else:
            self.base_image = swing_small
        self.image = pygame.transform.rotate(self.base_image,dir.angle_to(vec(-1,0)))
        #print ("Swing Radius :" + size)
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.game.player.score_swings += 1
        self.spawn_time = (int(self.game.player.score_time_played * 1000))

    def update(self):
        #### MELLE SWING SPRITE ma towsarzyszyc Playerowi! w kazdym kierunku
        if self.dir.angle_to(vec(-1,0)) == 0:
            self.pos = vec(self.game.player.pos.x - 13,self.game.player.pos.y)
        elif self.dir.angle_to(vec(-1,0)) == 90:
            self.pos = vec(self.game.player.pos.x,self.game.player.pos.y + 16)
        elif self.dir.angle_to(vec(-1,0)) == 180:
            self.pos = vec(self.game.player.pos.x + 14,self.game.player.pos.y)
        elif self.dir.angle_to(vec(-1,0)) == 270:
            self.pos = vec(self.game.player.pos.x,self.game.player.pos.y - 18)
        elif 0 < self.dir.angle_to(vec(-1,0)) < 90:
            self.pos = vec(self.game.player.pos.x - 5, self.game.player.pos.y + 7)
        elif 90 < self.dir.angle_to(vec(-1,0)) < 180:
            self.pos = vec(self.game.player.pos.x + 5, self.game.player.pos.y + 7)
        elif 180 < self.dir.angle_to(vec(-1,0)) < 270:
            self.pos = vec(self.game.player.pos.x + 5, self.game.player.pos.y - 7)
        elif 270 < self.dir.angle_to(vec(-1,0)) or self.dir.angle_to(vec(-1,0)) < 0:
            self.pos = vec(self.game.player.pos.x - 5, self.game.player.pos.y - 7)
        #### PRZYPISUJE POZYCJE
        self.rect.center = self.pos
        #### I ZNIKA PO PEWNYM (krótkim) czasie
        now = (int(self.game.player.score_time_played * 1000))
        if now - self.spawn_time > self.lifetime:
            self.kill()


class HiddenItem_to_take(pygame.sprite.Sprite):
    def __init__(self, game, x, y, item):
        self._layer = FLOOR_LAYER
        self.groups = game.act_lvl.items_to_pick
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.item = item
        self.image = self.item.b_image
        self.rect = self.image.get_rect()
        self.hit_rect = pygame.Rect(0, 0, TILE_SIZE - 5, TILE_SIZE - 5)
        self.pos = vec(x,y)
        self.rect.center = self.pos
        self.hit_rect.centerx = self.pos.x
        self.hit_rect.centery = self.pos.y
        self.encountered = False
        self.unlocked = True

    def unlock(self):
        self.unlocked = True

    def lock(self):
        self.unlocked = False

    def unhide(self):
        if not self.encountered and self.unlocked:
            pygame.mixer.Channel(0).play(item_dig_snd)
            pygame.mixer.Channel(0).queue(item_found_snd)
            Item_to_take(self.game,self.pos.x, self.pos.y, self.item)
            self.encountered = True


class Item_to_take(pygame.sprite.Sprite):
    def __init__(self, game, x, y, item):
        self._layer = FLOOR_LAYER
        self.groups = game.act_lvl.all_sprites, game.act_lvl.items_to_pick
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.item = item
        self.image = self.item.b_image
        self.rect = self.image.get_rect()
        self.hit_rect = pygame.Rect(0, 0, TILE_SIZE - 5, TILE_SIZE - 5)
        self.pos = vec(x,y)
        self.rect.center = self.pos
        self.hit_rect.centerx = self.pos.x
        self.hit_rect.centery = self.pos.y


class HiddenGold_to_take(pygame.sprite.Sprite):
    def __init__(self, game, x, y, gold):
        self._layer = FLOOR_LAYER
        self.groups = game.act_lvl.items_to_pick
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.gold = gold
        self.image = gold1_img
        self.rect = self.image.get_rect()
        self.hit_rect = pygame.Rect(0, 0, TILE_SIZE - 5, TILE_SIZE - 5)
        self.pos = vec(x, y)
        self.rect.center = self.pos
        self.hit_rect.centerx = self.pos.x
        self.hit_rect.centery = self.pos.y
        self.encountered = False
        self.unlocked = True

    def unlock(self):
        self.unlocked = True

    def lock(self):
        self.unlocked = False

    def unhide(self):
        if not self.encountered and self.unlocked:
            pygame.mixer.Channel(0).play(item_dig_snd)
            pygame.mixer.Channel(0).queue(item_found_snd)
            Gold_to_take(self.game,self.pos.x, self.pos.y, self.gold)
            self.encountered = True


class Gold_to_take(pygame.sprite.Sprite):
    def __init__(self, game, x, y, gold):
        self._layer = FLOOR_LAYER
        self.groups = game.act_lvl.all_sprites, game.act_lvl.gold_to_pick
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.gold = gold
        if self.gold == 0:
            self.gold = random.randint(1,self.game.player.level * 10)
        if 0 < self.gold <= 1:
            self.image = gold1_img
        elif 1 < self.gold <= 9:
            self.image = goldfew_img
        elif 9 < self.gold:
            self.image = goldlots_img
        else:
            self.image = goldlots_img
        self.rect = self.image.get_rect()
        self.hit_rect = pygame.Rect(0, 0, TILE_SIZE - 5, TILE_SIZE - 5)
        self.pos = vec(x,y)
        self.rect.center = self.pos
        self.hit_rect.centerx = self.pos.x
        self.hit_rect.centery = self.pos.y


class Arrow_to_take(pygame.sprite.Sprite):
    def __init__(self, game, x, y, number):
        self._layer = FLOOR_LAYER
        self.groups = game.act_lvl.all_sprites, game.act_lvl.arrows_to_pick
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.number = number
        if 0 < self.number <= 1:
            self.image = arrow_icon
        else:
            self.image = arrows_icon
        self.rect = self.image.get_rect()
        self.hit_rect = pygame.Rect(0, 0, TILE_SIZE - 5, TILE_SIZE - 5)
        self.pos = vec(x,y)
        self.rect.center = self.pos
        self.hit_rect.centerx = self.pos.x
        self.hit_rect.centery = self.pos.y


class Treasure_Object(pygame.sprite.Sprite):
    def __init__(self, game, name, x, y, image, hp, item, max_cost, hit_rect_width, hit_rect_height):
        self._layer = FLOOR_LAYER
        self.groups = game.act_lvl.all_sprites, game.act_lvl.hr_obstacles
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = name
        if item == "random":
            self.item = self.game.levelgen.gen.generate_random_item("all",max_cost)
        elif item == "gold":
            self.item = "gold"
        else:
            self.item = self.game.levelgen.gen.generate_item_by_name(item)
        self.max_cost = max_cost
        self.image = image.copy()
        self.half_damaged = False
        self.hp = hp
        self.max_hp = hp
        self.rect = pygame.Rect(0, 0,TILE_SIZE, TILE_SIZE)
        self.rect.center = (x,y)
        self.hit_rect = pygame.Rect(0, 0,hit_rect_width,  hit_rect_height)
        self.hit_rect.center = (x,y)
        self.last_damage = 0
        self.fire_immune_time = 500


    def update(self):
        #### GDY UDERZENIE OD MELEE (Swing Class)
        hits = pygame.sprite.spritecollide(self,self.game.act_lvl.melle_swing,True,collide_double_hit_rect)
        for hit in hits:
            pygame.mixer.Sound.play(chop_snd)
            self.game.player.weapon_breakage()
            self.hp -= self.game.player.hit_dmg
        #### GDY UDERZENIE OD STRZAL (Arrow Class)
        arrow_hits = pygame.sprite.spritecollide(self,self.game.act_lvl.arrows,False,collide_hit_rect)
        for hit in arrow_hits:
            pygame.mixer.Sound.play(chop_snd)
            if self.game.player.attack_type_flag == "magic":
                self.hp -= hit.damage
                hit.blow()
            elif self.game.player.attack_type_flag == "ranged":
                self.hp -= self.game.player.arrow_damage
                hit.kill()
        #### GDY UDERZENIE FIRE (lava group)
        lava_hits = pygame.sprite.spritecollide(self,self.game.act_lvl.lavas,False,collide_hit_rect)
        for lava_hit in lava_hits:
            if lava_hit.effect.name == "fire":
                now = (int(self.game.player.score_time_played * 1000))
                if now - self.last_damage >= self.fire_immune_time:
                    self.hp -= lava_hit.effect.strength
                    pygame.mixer.Sound.play(chop_snd)
                    self.last_damage = now
        if self.hp < self.max_hp / 2:
            if not self.half_damaged:
                self.image.blit(barrel_damage_mask,(0,0))
                self.half_damaged = True
        if self.hp <=0:
            self.kill()
            self.game.player.score_barrels_destroyed += 1
            #### wyjątek na złoto / jeseli w tilemap pisze gold to maxcost bedzie sie rownało max ilosci złota
            if self.item == "gold":
                random_gold = random.randint(1,self.max_cost)
                Gold_to_take(self.game,self.rect.centerx, self.rect.centery, random_gold)
            elif self.item.name == "Arrows":
                random_arrows = random.randint(1,self.max_cost)
                Arrow_to_take(self.game,self.rect.centerx,self.rect.centery, random_arrows)
            else:
                Item_to_take(self.game,self.rect.centerx, self.rect.centery,self.item)


class Treasure_Chest(pygame.sprite.Sprite):
    def __init__(self, game, x, y, key, locked, closed, treasure_value, special_item,
                 hit_rect_width, hit_rect_height, item_namecond_list = False):
        self._layer = FLOOR_LAYER
        self.groups = game.act_lvl.all_sprites, game.act_lvl.chest_to_open
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.closed = closed
        self.locked = locked
        self.inventory = Inventory(slot_img,8,4)
        self.special_item = special_item
        if treasure_value:
            if 0 < treasure_value <= 10:
                self.gold_coins = random.randint(1,treasure_value)
                self.treasure_items_no = 0
                self.treasure_items_maxcost = 0
            elif 10 < treasure_value <= 100:
                self.gold_coins = random.randint(5,treasure_value)
                self.treasure_items_no = random.randint(1,3)
                self.treasure_items_maxcost = treasure_value + 19
            elif 100 < treasure_value:
                self.gold_coins = random.randint(20,treasure_value)
                self.treasure_items_no = random.randint(2,8)
                self.treasure_items_maxcost = treasure_value
            self.inventory.put_in_first_free_slot(Gold_Item(self.game,"Gold",self.gold_coins))
            if self.treasure_items_no > 0:
                for i in range(self.treasure_items_no):
                    self.inventory.put_in_first_free_slot(
                        self.game.levelgen.gen.generate_random_item("all",self.treasure_items_maxcost))
        if special_item:
            special_item = self.game.levelgen.gen.generate_item_by_name(self.special_item)
            self.inventory.put_in_first_free_slot(special_item)
        self.key = key
        if self.closed:
            self.image = treasure_chest_closed.copy()
        else:
            self.image = treasure_chest_open.copy()
        if item_namecond_list:
            for tuple in item_namecond_list:
                if tuple[0] == "Gold":
                    self.inventory.put_in_first_free_slot(Gold_Item(self.game, "Gold", tuple[1]))
                elif tuple[0] == "Arrows":
                    self.inventory.put_in_first_free_slot(Arrow_Item(self.game, "Arrows", tuple[1]))
                elif tuple[0][:3] == "Key":
                    item = self.game.levelgen.gen.g_key(tuple[0], tuple[1])
                    self.inventory.put_in_first_free_slot(item)
                else:
                    item = self.game.levelgen.gen.load_item_by_name(tuple[0], tuple[1])
                    self.inventory.put_in_first_free_slot(item)
        self.pos = vec(x, y)
        self.rect = pygame.Rect(0, 0,TILE_SIZE, TILE_SIZE)
        self.rect.center = (x,y)
        self.hit_rect = pygame.Rect(0, 0,hit_rect_width,  hit_rect_height)
        self.hit_rect.center = (x,y)

    def update_img(self):
        if self.closed:
            self.image.blit(treasure_chest_closed, (0,0))
        else:
            self.image.blit(treasure_chest_open, (0,0))

    def try_unlock(self):#
        if self.locked:
            if self.game.player.inventory.return_no_items() > 0:
                for item in self.game.player.inventory.return_item_list():
                    if item.type == "key":
                        if item.key == self.key:
                            pygame.mixer.Sound.play(door_open_snd)
                            self.game.put_txt("Chest unlock success!")
                            self.locked = False
                            self.game.player.score_chest_opened += 1
                            self.game.player.inventory.remove_item(item)
                            return True
                        else:
                            self.game.put_txt("WRONG KEY")
            else:
                print ("NO ITEMS IN INV")
            if not pygame.mixer.Channel(1).get_busy():
                pygame.mixer.Channel(1).play(try_unlock_snd)
                self.game.put_txt("Chest locked")
                #print ("UNLOCK FAILED")
            return False
        else:
            #print ("ALREADY UNLOCKED")
            pygame.mixer.Sound.play(door_open_snd)
            return True

    def unlock_with_key(self):
        pygame.mixer.Sound.play(door_open_snd)
        self.game.put_txt("Chest unlock success!")
        self.locked = False
        self.game.item_picked = False
        return True

    def open(self):
        if not self.locked:
            self.image.fill((0,0,0,0))
            self.image.blit(treasure_chest_open,(0,0))
            self.closed = False
            return self.inventory
        else:
            self.try_unlock()


class CollectingSprite(pygame.sprite.Sprite):
    def __init__(self, game, name, x, y, content_type, content_str, content_no, hit_rect_width, hit_rect_height):
        self._layer = FLOOR_LAYER
        self.groups = game.act_lvl.all_sprites, game.act_lvl.collecting_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)
        self.rect.center = (x, y)
        self.hit_rect = pygame.Rect(0, 0, hit_rect_width, hit_rect_height)
        self.hit_rect.center = (x, y)
        self.name = name
        if name == "tomato":
            self.image = tomato_img
            self.empty_image = tomato_empty_img
            self.sound = crunch_snd
        elif name == "paprika":
            self.image = paprika_img
            self.empty_image = paprika_empty_img
            self.sound = crunch_snd
        else:
            self.image = pygame.Surface((32,32),pygame.HWSURFACE | pygame.SRCALPHA)
            self.sound = False
        self.content_type = content_type # HP, MP, QUEST_ITEM, RAND_ITEM
        self.content_str = content_str # for HP, MP, QUEST_ITEM_NAME, RAND_ITEM_MAXCOST
        self.content_no = content_no # for HP, MP, ITEMs
        if self.content_type == "quest item":
            self.item = self.game.levelgen.gen.generate_quest_item_by_name(self.content_str)
        elif self.content_type == "random item":
            self.item = self.game.levelgen.gen.generate_random_item(self.content_str)
        self.active = True
        self.depleted = False

    def update(self):
        if self.content_no <= 0:
            self.depleted = True
        if self.depleted:
            self.image = self.empty_image

    def gather(self):
        if not self.depleted and self.active:
            if self.sound:
                pygame.mixer.Sound.play(self.sound)
            if self.content_type == "hp":
                self.game.player.act_hp += self.content_str
                self.game.put_txt(f'Restored {self.content_str} HP')
                self.content_no -= 1
                if self.game.player.act_hp >= self.game.player.max_hp:
                    self.game.player.act_hp = self.game.player.max_hp
            elif self.content_type == "mana":
                self.game.player.act_mana += self.content_str
                self.game.put_txt(f'Restored {self.content_str} MP')
                if self.game.player.act_mana >= self.game.player.max_mana:
                    self.game.player.act_mana = self.game.player.max_mana
                self.content_no -= 1
            elif self.content_type == "quest item":
                if self.game.player.inventory.put_in_first_free_slot(self.item):
                    self.content_no -= 1
                    self.game.events_manager.emit(Event(id=f'item {self.item.name} collected'))
                    self.game.put_txt(f'Item {self.item.name} collected')
            elif self.content_type == "random item":
                if self.game.player.inventory.put_in_first_free_slot(self.item):
                    self.game.put_txt(f'Item {self.item.name} collected')
                    self.content_no -=1
            else:
                print ("ERROR Decoding content type in CollectingSprite object!")


class InfoSprite(pygame.sprite.Sprite):
    def __init__(self, game, name, x, y,w,h, text):
        self._layer = FLOOR_LAYER
        self.groups = game.act_lvl.collecting_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = name
        self.rect = pygame.Rect(0, 0, w, h)
        self.rect.center = (x, y)
        self.hit_rect = self.rect
        self.hit_rect.center = (x, y)
        self.name = name
        self.sound = False
        self.active = True
        self.text = text

    def gather(self):
        if self.active:
            if self.sound:
                pygame.mixer.Sound.play(self.sound)
            self.game.message_box.show_message(self.name, self.text)
            self.game.put_txt(self.text)


class Fence_Object(pygame.sprite.Sprite):
    def __init__(self, game, name, x, y, hp, image, hit_rect_width, hit_rect_height):
        self._layer = FLOOR_LAYER
        self.groups = game.act_lvl.all_sprites, game.act_lvl.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = name
        self.image = image
        self.hp = hp
        self.rect = pygame.Rect(0, 0,TILE_SIZE, TILE_SIZE)
        self.rect.center = (x,y)
        self.hit_rect = pygame.Rect(0, 0,hit_rect_width,  hit_rect_height)
        self.hit_rect.center = (x,y)
        self.fire_immune_time = 500
        self.last_damage = 0
        self.water = False

    def update(self):
        hits = pygame.sprite.spritecollide(self,self.game.act_lvl.melle_swing,True,collide_double_hit_rect)
        for hit in hits:
            pygame.mixer.Sound.play(chop_snd)
            self.game.player.weapon_breakage()
            self.hp -= self.game.player.hit_dmg
            #print("object hp = " + str(self.hp))
        arrow_hits = pygame.sprite.spritecollide(self, self.game.act_lvl.arrows,False)
        for hit in arrow_hits:
            pygame.mixer.Sound.play(chop_snd)
            if self.game.player.attack_type_flag == "magic":
                self.hp -= hit.damage
                #print("magic damage to fence object")
                #print("object hp = " + str(self.hp))
                hit.blow()
        #### UDERZENIE OD FIRE (group lavas)
        lava_hits = pygame.sprite.spritecollide(self, self.game.act_lvl.lavas, False, collide_hit_rect)
        for lava_hit in lava_hits:
            if lava_hit.effect.name == "fire":
                now = (int(self.game.player.score_time_played * 1000))
                if now - self.last_damage >= self.fire_immune_time:
                    self.hp -= lava_hit.effect.strength
                    print ("lava damage to fence object")
                    print ("object hp = "+ str(self.hp))
                    pygame.mixer.Sound.play(chop_snd)
                    self.last_damage = now
        if self.hp <=0:
            self.kill()


class Door(pygame.sprite.Sprite):
    def __init__(self, game, name, x, y, key, image):
        self._layer = FLOOR_LAYER
        self.groups = game.act_lvl.all_sprites, game.act_lvl.hr_obstacles, game.act_lvl.doors
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = name
        self.open = False
        self.key = key
        self.image = image
        self.pos = vec(x,y)
        self.rect = pygame.Rect(0, 0,TILE_SIZE, TILE_SIZE)
        self.rect.center = (x,y)
        self.hit_rect = self.rect


class Gold_Item:
    ## TYLKO DO TREASURE CHESTÓW / NIE SPRITE!
    def __init__(self, game, name, gold):
        self.game = game
        self.gold = gold
        self.image = pygame.Surface((32,32), pygame.HWSURFACE | pygame.SRCALPHA)
        if 0 < self.gold <= 1:
            self.image = gold1_img
        elif 1 < self.gold <= 9:
            self.image = goldfew_img
        elif 9 < self.gold:
            self.image = goldlots_img
        else:
            self.image = goldlots_img
        self.name = name
        self.b_image = self.image
        self.rect = self.b_image.get_rect()


class Arrow_Item:
    ## TYLKO DO TREASURE CHESTÓW / NIE SPRITE!
    def __init__(self, game, name, number):
        self.game = game
        self.number = number
        self.image = arrows_icon
        self.name = name
        #### TODO zrobic cene strzał oddzielnie?
        self.cost = number
        self.b_image = self.image
        self.rect = self.b_image.get_rect()


class Weapon(pygame.sprite.Sprite):
    def __init__(self, game, name, type,subtype, cost, ranged, damage, hit_rate, hit_radius,
                 str_mod,sta_mod,int_mod,wis_mod,speed_mod,ste_mod, durability,
                 img_x, img_y, s_img_x, s_img_y, tileset = full_tileset_image):
        self._layer = ITEMS_LAYER
        self.groups = game.small_items
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.owner = False
        self.b_image = pygame.Surface((32,32), pygame.HWSURFACE | pygame.SRCALPHA)
        self.s_image = pygame.Surface((32,32), pygame.HWSURFACE | pygame.SRCALPHA)
        self.b_image.blit(tileset,(0,0),(img_x*TILE_SIZE, img_y*TILE_SIZE,TILE_SIZE,TILE_SIZE))
        self.s_image.blit(tileset,(0,0),(s_img_x*TILE_SIZE, s_img_y*TILE_SIZE,TILE_SIZE,TILE_SIZE))
        self.breakage_surf = pygame.Surface((16,16), pygame.HWSURFACE | pygame.SRCALPHA)
        self.breakage_icon = ebroken_armor_img
        self.name = name
        self.type = type
        self.subtype = subtype
        self.cost = cost
        self.ranged = ranged
        self.base_damage = damage
        self.str_mod = str_mod
        self.sta_mod = sta_mod
        self.int_mod = int_mod
        self.wis_mod = wis_mod
        self.speed_mod = speed_mod
        self.ste_mod = ste_mod
        self.durability = durability
        self.condition = 100.0
        self.hit_rate = hit_rate
        self.hit_radius = hit_radius
        self.image = self.s_image
        self.rect = self.s_image.get_rect()
        self.hit_rect = self.rect
        self.damage = round((0.4 * self.base_damage) + (0.6 * self.base_damage * self.condition / 100),0)
        self.breakage_surf.fill((255 - (int(2.5 * self.condition)), (int(2.0 * self.condition)), 0))
        self.breakage_surf.blit(self.breakage_icon, (0, 0))

    def set_condition(self, condition):
        self.condition = condition

    def update(self):
        #### bron bedzie tam gdzie gracz (czyli vector Pos + (4,0)
        self.pos = self.game.player.pos
        self.rect.center = self.pos + (4,0)

    def breakage(self):
        self.condition -= 20 / self.durability
        if self.condition <= 0:
            self.condition = 0
        self.damage = round((0.4 * self.base_damage) + (0.6 * self.base_damage * self.condition / 100), 0)
        print (f'{self.name} condition: {self.condition}')
        self.breakage_surf.fill((255 - (int(2.5 * self.condition)),(int(2.5* self.condition)),0))
        self.breakage_surf.blit(self.breakage_icon,(0,0))

    def repair(self, val):
        self.condition += val
        if self.condition > 100:
            self.condition = 100.0
        self.damage = round((0.4 * self.base_damage) + (0.6 * self.base_damage * self.condition / 100), 0)
        self.breakage_surf.fill((255 - (int(2.5 * self.condition)), (int(2.5 * self.condition)), 0))
        self.breakage_surf.blit(self.breakage_icon, (0, 0))


class Armor(pygame.sprite.Sprite):
    def __init__(self, game, name, type, subtype, cost, armor, hit_rate_mod,
                 str_mod, sta_mod, int_mod, wis_mod, speed_mod, ste_mod, durability,
                 img_x, img_y, s_img_x, s_img_y, tileset = full_tileset_image):
        self._layer = ITEMS_LAYER
        self.groups = game.small_items
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.owner = False
        self.b_image = pygame.Surface((32,32), pygame.HWSURFACE | pygame.SRCALPHA)
        self.s_image = pygame.Surface((32,32), pygame.HWSURFACE | pygame.SRCALPHA)
        self.b_image.blit(tileset,(0,0),(img_x*TILE_SIZE, img_y*TILE_SIZE,TILE_SIZE,TILE_SIZE))
        self.s_image.blit(tileset,(0,0),(s_img_x*TILE_SIZE, s_img_y*TILE_SIZE,TILE_SIZE,TILE_SIZE))
        self.breakage_surf = pygame.Surface((16, 16), pygame.HWSURFACE | pygame.SRCALPHA)
        self.breakage_icon = ebroken_armor_img
        self.name = name
        self.type = type
        self.subtype = subtype
        self.cost = cost
        self.base_armor = armor
        self.hit_rate_mod = hit_rate_mod
        self.str_mod = str_mod
        self.sta_mod = sta_mod
        self.int_mod = int_mod
        self.wis_mod = wis_mod
        self.speed_mod = speed_mod
        self.ste_mod = ste_mod
        self.durability = durability
        self.condition = 100.0
        self.image = self.s_image
        self.rect = self.s_image.get_rect()
        self.rect.center = self.game.player.pos
        self.hit_rect = self.rect
        self.armor = round((0.4 * self.base_armor) + (0.6 * self.base_armor * self.condition / 100), 0)
        self.breakage_surf.fill((255 - (int(2.5 * self.condition)), (int(2.5 * self.condition)), 0))
        self.breakage_surf.blit(self.breakage_icon, (0, 0))

    def set_condition(self, condition):
        self.condition = condition

    def update(self):
        self.pos = self.game.player.pos
        self.rect.center = self.pos

    def breakage(self):
        self.condition -= 15 / self.durability
        if self.condition <= 0:
            self.condition = 0
        self.armor = round((0.4 * self.base_armor) + (0.6 * self.base_armor * self.condition / 100), 0)
        print (f'{self.name} condition: {self.condition}')
        self.breakage_surf.fill((255 - (int(2.5 * self.condition)), (int(2.5 * self.condition)), 0))
        self.breakage_surf.blit(self.breakage_icon, (0, 0))

    def repair(self, val):
        self.condition += val
        if self.condition > 100:
            self.condition = 100.0
        self.armor = round((0.4 * self.base_armor) + (0.6 * self.base_armor * self.condition / 100), 0)
        self.breakage_surf.fill((255 - (int(2.5 * self.condition)), (int(2.5 * self.condition)), 0))
        self.breakage_surf.blit(self.breakage_icon, (0, 0))


class Ring:
    def __init__(self, game, name, cost, str_mod, sta_mod,int_mod,wis_mod,speed_mod,ste_mod,
                 armor_mod,damage_mod,arrow_damage_mod, hit_rate_mod,img_x, img_y, tileset = full_tileset_image):
        self.game = game
        self.owner = False
        self.b_image = pygame.Surface((32,32), pygame.HWSURFACE | pygame.SRCALPHA)
        self.b_image.blit(tileset,(0,0),(img_x*TILE_SIZE, img_y*TILE_SIZE,TILE_SIZE,TILE_SIZE))
        self.image = self.b_image
        self.name = name
        self.type = "ring"
        self.cost = cost
        self.str_mod = str_mod
        self.sta_mod = sta_mod
        self.int_mod = int_mod
        self.wis_mod = wis_mod
        self.speed_mod = speed_mod
        self.ste_mod = ste_mod
        self.barter_mod = 0
        self.armor_mod = armor_mod
        self.damage_mod = damage_mod
        self.arrow_damage_mod = arrow_damage_mod
        self.hit_rate_mod = hit_rate_mod
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect


class Necklace:
    def __init__(self, game, name, cost, str_mod, sta_mod,int_mod,wis_mod,speed_mod,ste_mod,
                 armor_mod,damage_mod,arrow_damage_mod, hit_rate_mod,img_x, img_y, tileset = full_tileset_image):
        self.game = game
        self.owner = False
        self.b_image = pygame.Surface((32,32), pygame.HWSURFACE | pygame.SRCALPHA)
        self.b_image.blit(tileset,(0,0),(img_x*TILE_SIZE, img_y*TILE_SIZE,TILE_SIZE,TILE_SIZE))
        self.image = self.b_image
        self.name = name
        self.type = "necklace"
        self.cost = cost
        self.str_mod = str_mod
        self.sta_mod = sta_mod
        self.int_mod = int_mod
        self.wis_mod = wis_mod
        self.speed_mod = speed_mod
        self.ste_mod = ste_mod
        self.barter_mod = 0
        self.armor_mod = armor_mod
        self.damage_mod = damage_mod
        self.arrow_damage_mod = arrow_damage_mod
        self.hit_rate_mod = hit_rate_mod
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect


class Potion:
    def __init__(self, game, name, potion_type, cost, strength, img_x, img_y, tileset = full_tileset_image):
        self.game = game
        self.owner = False
        self.b_image = pygame.Surface((32,32), pygame.HWSURFACE | pygame.SRCALPHA)
        self.b_image.blit(tileset,(0,0),(img_x*TILE_SIZE, img_y*TILE_SIZE,TILE_SIZE,TILE_SIZE))
        self.image = self.b_image
        self.name = name
        self.type = "potion"
        self.cost = cost
        self.potion_type = potion_type
        self.strength = strength
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect

    def try_use(self):
        if self.owner == "shop":
            return False
        if self.potion_type == "Cure":
            if self.game.player.act_hp == self.game.player.max_hp:
                return False
        elif self.potion_type == "Mana":
            if self.game.player.act_mana == self.game.player.max_mana:
                return False
        elif self.potion_type == "All":
            if self.game.player.act_mana == self.game.player.max_mana and self.game.player.act_hp == self.game.player.max_hp:
                return False
        return True

    def use(self):
        if self.potion_type == "Cure":
            pygame.mixer.Sound.play(drink_snd)
            self.game.player.act_hp += self.strength
            self.game.put_txt("You`ve drink a Cure Potion. " + str(self.strength) + " HP restored.")
            if self.game.player.act_hp >= self.game.player.max_hp:
                self.game.player.act_hp = self.game.player.max_hp
        elif self.potion_type == "Mana":
            pygame.mixer.Sound.play(drink_snd)
            self.game.player.act_mana += self.strength
            self.game.put_txt("You`ve drink a Mana Potion. " + str(self.strength) + " MP restored.")
            if self.game.player.act_mana >= self.game.player.max_mana:
                self.game.player.act_mana = self.game.player.max_mana
        elif self.potion_type == "All":
            pygame.mixer.Sound.play(drink_snd)
            self.game.player.act_mana += self.strength
            self.game.player.act_hp += self.strength
            self.game.put_txt("You`ve drink a Restore Potion. " + str(self.strength) + " HP and MP restored.")
            if self.game.player.act_mana >= self.game.player.max_mana:
                self.game.player.act_mana = self.game.player.max_mana
            if self.game.player.act_hp >= self.game.player.max_hp:
                self.game.player.act_hp = self.game.player.max_hp
        else:
            print ("ERROR POTION TYPE UNKNOWN")


class Book:
    def __init__(self, game, name, cost, min_int, img_x, img_y, tileset = full_tileset_image):
        self.spell_generator = spells.SpellGenerator()
        self.game = game
        self.owner = False
        self.b_image = pygame.Surface((32,32), pygame.HWSURFACE | pygame.SRCALPHA)
        self.b_image.blit(tileset,(0,0),(img_x*TILE_SIZE, img_y*TILE_SIZE,TILE_SIZE,TILE_SIZE))
        self.image = self.b_image
        self.name = name
        self.type = "book"
        self.cost = cost
        self.min_int = min_int
        self.spell = self.spell_generator.get_spell_by_name(name)
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect

    def try_use(self):
        if self.owner == "shop":
            return False
        if self.min_int > self.game.player.intellect:
            return False
        if self.game.player.spell_book.check_duplicate(self.spell):
            return False
        return True

    def use(self):
        pygame.mixer.Sound.play(cure_snd)
        self.game.player.spell_book.add_spell(self.spell)


class Quest_Item:
    def __init__(self, game, name, cost, img_x, img_y, tileset = full_tileset_image):
        self.game = game
        self.owner = False
        self.b_image = pygame.Surface((32,32), pygame.HWSURFACE | pygame.SRCALPHA)
        self.b_image.blit(tileset,(0,0),(img_x*TILE_SIZE, img_y*TILE_SIZE,TILE_SIZE,TILE_SIZE))
        self.image = self.b_image
        self.name = name
        self.type = "quest item"
        self.cost = cost
        self.quest = False
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect


class Key:
    def __init__(self, game, name, key, img_x, img_y, tileset = full_tileset_image):
        self.game = game
        self.owner = False
        self.b_image = pygame.Surface((32,32), pygame.HWSURFACE | pygame.SRCALPHA)
        self.b_image.blit(tileset,(0,0),(img_x*TILE_SIZE, img_y*TILE_SIZE,TILE_SIZE,TILE_SIZE))
        self.image = self.b_image
        self.name = name
        self.type = "key"
        self.key = key
        self.lock_is_close = False
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect

    def update(self):
        for lock in self.game.act_lvl.doors:
            dist = lock.pos - self.game.player.pos
            if dist.length_squared() < 36**2:
                self.lock_is_close = lock
                return True
        for lock in self.game.act_lvl.chest_to_open:
            dist = lock.pos - self.game.player.pos
            if dist.length_squared() < 20**2:
                self.lock_is_close = lock
                if self.lock_is_close.closed:
                    return True
        self.lock_is_close = False

    def use(self):
        if self.lock_is_close.key == self.key:
            if isinstance(self.lock_is_close,Door):
                self.game.put_txt("Open door success")
                pygame.mixer.Sound.play(door_open_snd)
                self.lock_is_close.kill()
                self.game.item_picked = False
            if isinstance(self.lock_is_close,Treasure_Chest):
                #print("OPEN CHEST")
                if self.lock_is_close.unlock_with_key():
                    self.lock_is_close.open()
        else:
            if not pygame.mixer.Channel(1).get_busy():
                pygame.mixer.Channel(1).play(try_unlock_snd)
            self.game.put_txt("Wrong key..")


class CharClass:
    def __init__(self, name, image, death_anim, favourite_weapons, disliked_weapons, favourite_armors, disliked_armors,
                 str, sta, int, wis, spe, ste, spells):
        self.name = name
        self.image = image
        self.death_anim = death_anim
        self.favourite_weapons = favourite_weapons
        self.disliked_weapons = disliked_weapons
        self.favourite_armors = favourite_armors
        self.disliked_armors = disliked_armors
        self.str = str
        self.sta = sta
        self.int = int
        self.wis = wis
        self.spe = spe
        self.ste = ste
        self.spells = spells


class Player(pygame.sprite.Sprite):
    def __init__(self, game, name, char_class):
        self._layer = PLAYER_LAYER
        self.groups = game.player_group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = char_class.image
        self.char_death_animation_images = char_class.death_anim
        #self.image = pygame.Surface((32,32),pygame.HWSURFACE|pygame.SRCALPHA)
        #self.image.blit(player_image, (0, 0))
        self.name = name
        self.char_class = char_class
        self.char_name = char_class.name
        self.favourite_weapons = char_class.favourite_weapons
        self.disliked_weapons = char_class.disliked_weapons
        self.favourite_armors = char_class.favourite_armors
        self.disliked_armors = char_class.disliked_armors
        self.x = 0
        self.y = 0
        self.rect = self.image.get_rect()
        self.hit_rect = pygame.Rect(0,0,PL_HIT_TILE_SIZE - 10,PL_HIT_TILE_SIZE)
        self.hit_rect.center = self.rect.center
        self.vel = vec(0,0)
        self.pos = vec(self.x,self.y)
        self.rect.center = self.pos
        self.hit_rect.centerx = self.pos.x
        self.hit_rect.centery = self.pos.y
        self.inventory = Inventory(slot_img,9,4)
        ## ZDOLNOSCI SPEJALNE
        self.plate_armor_penalty_reduction = 1
        self.spell_power_bonus = 1
        self.bow_hit_rate_bonus = 1
        self.barter_bonus = 0
        self.slow_mod = 0
        ##############################
        if self.char_class.name == "Knight":
            self.inventory.put_in_first_free_slot(Potion(self.game, "Red Potion", "Cure", 15, 30, 26, 42))
            self.inventory.put_in_first_free_slot(Potion(self.game, "Small Red Potion", "Cure",5,15,24,42))
            self.inventory.put_in_first_free_slot(Potion(self.game, "Small Red Potion", "Cure", 5, 15, 24, 42))
            self.inventory.put_in_first_free_slot(Potion(self.game, "Small Red Potion", "Cure", 5, 15, 24, 42))
            self.inventory.put_in_first_free_slot(Weapon(self.game, "Small Sword","weapon","sword",
                                           10,False,2,625,"small",
                                           0,0,0,0,0,0,50,4,45,52,89))
            self.plate_armor_penalty_reduction = 0.75
        if self.char_class.name == "Wizard":
            self.inventory.put_in_first_free_slot(Potion(self.game, "Blue Potion", "Mana",15,30,58,41))
            self.inventory.put_in_first_free_slot(Potion(self.game, "Blue Potion", "Mana", 15, 30, 58, 41))
            self.inventory.put_in_first_free_slot(Potion(self.game, "Red Potion", "Cure", 15, 30, 26, 42))
            self.inventory.put_in_first_free_slot(Potion(self.game, "Small Red Potion", "Cure", 5, 15, 24,42))
            self.inventory.put_in_first_free_slot(Weapon(self.game,"Wood Staff","weapon","staff",
                                           15,False,2,700,"big",
                                           0,0,0,0,0,0,25,3,47,10,89))
            self.spell_power_bonus = 1.5
        if self.char_class.name == "Thief":
            self.inventory.put_in_first_free_slot(Potion(self.game, "Small Blue Potion", "Mana", 5, 15, 23, 42))
            self.inventory.put_in_first_free_slot(Potion(self.game, "Small Red Potion", "Cure", 5, 15, 24, 42))
            self.inventory.put_in_first_free_slot(Potion(self.game, "Small Red Potion", "Cure", 5, 15, 24, 42))
            self.inventory.put_in_first_free_slot(Potion(self.game, "Red Potion", "Cure", 15, 30, 26, 42))
            self.inventory.put_in_first_free_slot(Weapon(self.game, "Knife", "weapon","dagger",
                                           15, False, 1, 500, "small",
                                           0, 0, 0, 0, 0, 0,40, 2, 45, 42, 87))
            self.inventory.put_in_first_free_slot(sprites.Weapon(self.game, "Wood Bow", "weapon", "bow",
                           75, True, 3, 1250, False,
                           0, 0, 0, 0, 0, 0, 25, 38, 49, 26, 87))
            self.bow_hit_rate_bonus = 0.75
            self.barter_bonus = 50
        self.active_effects_lib = ActiveEffectsLibrary(self.game)
        self.quest_book = QuestBook(self.game)
        self.spell_book = SpellBook(self.game)
        if self.char_class.spells:
            for spell in self.char_class.spells:
                self.spell_book.add_spell_by_name(spell)
            #self.spell_book.add_spell_by_name("Fireball")
            #self.spell_book.add_spell_by_name("Tricebolt")
            #self.spell_book.add_spell_by_name("Iron Skin")
            #self.spell_book.add_spell_by_name("Cure")
            #self.spell_book.add_spell_by_name("Freeze")
            #self.spell_book.add_spell_by_name("Invisibility")
            #self.spell_book.add_spell_by_name("Icebolt")
            #self.spell_book.add_spell_by_name("Haste")
            #self.spell_book.add_spell_by_name("Poison Cloud")
            #self.spell_book.add_spell_by_name("Stone Skin")
            #self.spell_book.add_spell_by_name("Heroism")
        self.active_spell = False
        self.selected_spell = False
        self.armor_slot = Slot(slot_a_img)
        self.armor_slot.define_type("armor")
        self.weapon_slot = Slot(slot_w_img)
        self.weapon_slot.define_type("weapon")
        self.shield_slot = Slot(slot_s_img)
        self.shield_slot.define_type("shield")
        self.helmet_slot = Slot(slot_h_img)
        self.helmet_slot.define_type("helmet")
        self.boots_slot = Slot(slot_b_img)
        self.boots_slot.define_type("boots")
        self.ring1_slot = Slot(slot_r_img)
        self.ring1_slot.define_type("ring")
        self.ring2_slot = Slot(slot_r_img)
        self.ring2_slot.define_type("ring")
        self.necklace_slot = Slot(slot_n_img)
        self.necklace_slot.define_type("necklace")
        self.active_slots = [self.armor_slot, self.weapon_slot, self.shield_slot, self.helmet_slot,
                             self.boots_slot, self.ring1_slot, self.ring2_slot, self.necklace_slot]
        self.base_speed = self.char_class.spe
        self.base_stamina = self.char_class.sta
        self.base_strength = self.char_class.str
        self.base_intellect = self.char_class.int
        self.base_wisdom = self.char_class.wis
        self.base_stealth = self.char_class.ste
        self.speed = self.base_speed
        self.stamina = self.base_stamina
        self.strength = self.base_strength
        self.intellect = self.base_intellect
        self.wisdom = self.base_wisdom
        self.stealth = self.base_stealth
        self.max_hp = 15 + self.stamina * 5
        self.act_hp = self.max_hp
        self.max_mana = max(4, self.wisdom * 8 - 15)
        self.act_mana = self.max_mana
        self.gold = 0
        self.arrows = 0
        self.xp = 0
        self.attribute_points = 0
        self.level = 1
        self.xp_step = 10 * self.level + ((self.level - 1) * 2 * self.level)
        self.hit_dmg = self.strength
        self.hit_radius = "small"
        self.armor = 0
        self.block_chance = self.calculate_block_ratio(self.armor)
        self.hit_reduction = self.calculate_hit_reduction(self.armor)
        self.unarmed_hit_rate = 575
        self.hit_rate = self.unarmed_hit_rate
        self.hit_load_percentage = 100
        #### pygame.time moment of attack:
        self.last_hit = 0
        self.last_damage = 0
        #### used for blink red animation
        self.damaged = False
        self.arrow_rate = False
        self.last_shot = 0
        self.last_dir = vec(1,0)
        self.melle_swing = False
        self.last_magic = 0
        self.attack_type_flag = "melle"
        self.movement_speed = self.calculate_movement_speed(self.speed)
        self.fire_immune_time = 500
        self.invisible = False
        #### score values
        self.score_killed_enemies = []
        self.score_swings = 0
        self.score_swing_enemy_hits = []
        self.score_arrows = 0
        self.score_arrow_enemy_hits = []
        self.score_spell_bullets = 0
        self.score_off_spell_damage = []
        self.score_inflicted_damage = []
        self.score_blocks = 0
        self.score_time_played = 0
        self.score_chest_opened = 0
        self.score_barrels_destroyed = 0
        ####
        self.debug_value = 0
        self.wait_key_pressed = False
        self.start_death_animation = False
        self.char_animation_time = 0
        self.last_char_animation_time = 0

    def load_state(self):
        pass

    def return_active_slots_item_namecond_list(self):
        list = []
        for i in self.active_slots:
            if i.item:
                name = i.item.name
                slot = i.type
                if isinstance(i.item, sprites.Armor) or isinstance(i.item, sprites.Weapon):
                    cond = i.item.condition
                else:
                    cond = False
                list.append((name, slot, cond))
        return list

    def load_active_slots_from_item_namecond_list(self, nc_list, itemgen):
        ring1occ = False
        ring2occ = False
        for tuple in nc_list:
            print ("item name: " + tuple[0] + ", item type: " + tuple[1] + ",item_cond: "+ str(tuple[2]))
            if tuple[1] == "armor":
                item = itemgen.load_item_by_name(tuple[0],tuple[2])
                self.armor_slot.put_item(item)
            elif tuple[1] == "weapon":
                item = itemgen.load_item_by_name(tuple[0],tuple[2])
                self.weapon_slot.put_item(item)
            elif tuple[1] == "shield":
                item = itemgen.load_item_by_name(tuple[0], tuple[2])
                self.shield_slot.put_item(item)
            elif tuple[1] == "helmet":
                item = itemgen.load_item_by_name(tuple[0],tuple[2])
                self.helmet_slot.put_item(item)
            elif tuple[1] == "boots":
                item = itemgen.load_item_by_name(tuple[0],tuple[2])
                self.boots_slot.put_item(item)
            elif tuple[1] == "ring" and not ring1occ:
                item = itemgen.load_item_by_name(tuple[0])
                self.ring1_slot.put_item(item)
                ring1occ = True
            elif tuple[1] == "ring" and not ring2occ:
                item = itemgen.load_item_by_name(tuple[0])
                self.ring2_slot.put_item(item)
                ring2occ = True
            elif tuple[1] == "necklace":
                item = itemgen.load_item_by_name(tuple[0],tuple[2])
                self.necklace_slot.put_item(item)

    def put_in_pos(self,x,y):
        self.x = x * TILE_SIZE + TILE_SIZE /2
        self.y = y * TILE_SIZE + TILE_SIZE /2
        self.rect = self.image.get_rect()
        self.hit_rect = pygame.Rect(0, 0, PL_HIT_TILE_SIZE - 10, PL_HIT_TILE_SIZE)
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(self.x, self.y)
        self.rect.center = self.pos
        self.hit_rect.centerx = self.pos.x
        self.hit_rect.centery = self.pos.y

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0,0)
        if not self.wait_key_pressed:
            keys = pygame.key.get_pressed()
            ### RUCH
            if keys[pygame.K_a]:
                self.vel.x = - self.movement_speed
                self.last_dir = vec(-1, 0)
            if keys[pygame.K_d]:
                self.vel.x = self.movement_speed
                self.last_dir = vec(1, 0)
            if keys[pygame.K_w]:
                self.vel.y = - self.movement_speed
                self.last_dir = vec(0, -1)
            if keys[pygame.K_s]:
                self.vel.y = self.movement_speed
                self.last_dir = vec(0, 1)
            ### RUCHY PO SKOSACH
            if self.vel.x > 0 and self.vel.y > 0:
                self.last_dir = vec(0.7071, 0.7071)
            elif self.vel.x < 0 and self.vel.y > 0:
                self.last_dir = vec(-0.7071, 0.7071)
            elif self.vel.x < 0 and self.vel.y < 0:
                self.last_dir = vec(-0.7071, -0.7071)
            elif self.vel.x > 0 and self.vel.y < 0:
                self.last_dir = vec(0.7071, -0.7071)
            if self.vel.x != 0 and self.vel.y != 0:
                self.vel *= 0.7071
            ### ATAK
            if keys[pygame.K_SPACE]:
                if self.attack_type_flag == "melle":
                    self.melle_attack()
                elif self.attack_type_flag == "ranged":
                    self.bow_shot()
                elif self.attack_type_flag == "magic":
                    self.magic_attack()

    def magic_attack(self):
        now = (int(self.score_time_played * 1000))
        if now - self.last_magic > self.active_spell.hit_rate:
            self.last_magic = now
            dir = self.last_dir
            #### SPRAWDZAM MANE #####
            if self.act_mana >= self.active_spell.cost:
                self.act_mana -= self.active_spell.cost
                ###### KIERUNEK POCISKÓW ###########
                if self.active_spell.bullet_nr == 1:
                    Spell_Bullet(self.game, self.active_spell, self.pos, dir)
                elif self.active_spell.bullet_nr == 2:
                    Spell_Bullet(self.game, self.active_spell, self.pos, dir.rotate(-5))
                    Spell_Bullet(self.game, self.active_spell, self.pos, dir.rotate(5))
                elif self.active_spell.bullet_nr == 3:
                    Spell_Bullet(self.game, self.active_spell, self.pos, dir.rotate(-10))
                    Spell_Bullet(self.game, self.active_spell, self.pos, dir.rotate(10))
                    Spell_Bullet(self.game, self.active_spell, self.pos, dir)
                else:
                    for i in range(0,self.active_spell.bullet_nr):
                        Spell_Bullet(self.game, self.active_spell, self.pos, dir)
                        random_dir_mod = random.randint(-20,20)
                        dir = dir.rotate(random_dir_mod)
                        print (dir)
            else:
                pygame.mixer.Sound.play(empty_spell_snd)

    def bow_shot(self):
        if self.arrows > 0:
            now = (int(self.score_time_played * 1000))
            if now - self.last_shot > self.arrow_rate:
                self.last_shot = now
                dir = self.last_dir
                self.weapon_slot.item.breakage()
                Arrow(self.game, self.pos, dir)
                self.arrows -= 1

    def melle_attack(self):
        ### self.score_time_player = czas NIE PAUZOWANEJ gry
        now = (int(self.score_time_played * 1000))
        if now - self.last_hit > self.hit_rate:
            #print (now)
            self.last_hit = now
            dir = self.last_dir
            Swing(self.game, self.pos, dir, self.hit_radius)

    def update_weapon_load_bar(self):
        if self.attack_type_flag == "melle":
            now = (int(self.score_time_played * 1000))
            self.hit_load_percentage = (now - self.last_hit) / self.hit_rate
            self.hit_load_percentage = self.hit_load_percentage * 100
            self.hit_load_percentage = int(self.hit_load_percentage)
            self.hit_load_percentage = min(100, self.hit_load_percentage)
        elif self.attack_type_flag == "ranged":
            now = (int(self.score_time_played * 1000))
            self.hit_load_percentage = (now - self.last_shot) / self.arrow_rate
            self.hit_load_percentage = self.hit_load_percentage * 100
            self.hit_load_percentage = int(self.hit_load_percentage)
            self.hit_load_percentage = min(100, self.hit_load_percentage)
        elif self.attack_type_flag == "magic":
            now = (int(self.score_time_played * 1000))
            self.hit_load_percentage = (now - self.last_magic) / self.active_spell.hit_rate
            self.hit_load_percentage = self.hit_load_percentage * 100
            self.hit_load_percentage = int(self.hit_load_percentage)
            self.hit_load_percentage = min(100, self.hit_load_percentage)

    def update_stats(self):
        temp_str_mod = 0
        temp_sta_mod = 0
        temp_int_mod = 0
        temp_wis_mod = 0
        temp_speed_mod = 0
        temp_ste_mod = 0
        temp_barter_bonus = 0
        temp_armor_mod = 0
        temp_hit_rate_mod = 1
        self.hit_radius = "small"
        temp_hit_rate = 1500
        temp_hit_damage = 0
        temp_arrow_rate = 0
        temp_arrow_damage = 0
        self.armor = 0
        self.invisible = False
        ## ZERUJE IKONY AKTYWNYCH EFEKTOW SPECJALNYCH, EFEKTOW ULUBIONYCH lub NIELUBIANYCH BRONI
        self.slow_mod = 0
        self.active_effects_lib.remove_fav_dis_weapons_effects()
        self.active_effects_lib.remove_fav_dis_armors_effects()
        if self.weapon_slot.item:
            temp_str_mod += self.weapon_slot.item.str_mod
            temp_sta_mod += self.weapon_slot.item.sta_mod
            temp_int_mod += self.weapon_slot.item.int_mod
            temp_wis_mod += self.weapon_slot.item.wis_mod
            temp_speed_mod += self.weapon_slot.item.speed_mod
            temp_ste_mod += self.weapon_slot.item.ste_mod
            if self.weapon_slot.item.ranged:
                if self.weapon_slot.item.subtype in self.favourite_weapons:
                    temp_arrow_damage = math.floor(self.weapon_slot.item.damage * 1.33)
                    self.active_effects_lib.add_effect(self.game.e_favourite_weapon)
                elif self.weapon_slot.item.subtype in self.disliked_weapons:
                    temp_arrow_damage = math.floor(self.weapon_slot.item.damage * 0.51)
                    self.active_effects_lib.add_effect(self.game.e_disliked_weapon)
                else:
                    temp_arrow_damage = self.weapon_slot.item.damage
                temp_arrow_rate = self.weapon_slot.item.hit_rate
                self.hit_radius = False
            else:
                if self.weapon_slot.item.subtype in self.favourite_weapons:
                    temp_hit_damage = math.floor(self.weapon_slot.item.damage * 1.33)
                    self.active_effects_lib.add_effect(self.game.e_favourite_weapon)
                elif self.weapon_slot.item.subtype in self.disliked_weapons:
                    temp_hit_damage = math.floor(self.weapon_slot.item.damage * 0.51)
                    self.active_effects_lib.add_effect(self.game.e_disliked_weapon)
                else:
                    temp_hit_damage = self.weapon_slot.item.damage
                temp_hit_rate = self.weapon_slot.item.hit_rate
                self.hit_radius = self.weapon_slot.item.hit_radius
        else:
            temp_hit_rate = self.unarmed_hit_rate
            temp_hit_damage = 0
        if self.armor_slot.item:
            if self.armor_slot.item.subtype in self.favourite_armors:
                temp_armor_mod += math.floor(self.armor_slot.item.armor * 1.33)
                self.active_effects_lib.add_effect(self.game.e_favourite_armor)
            elif self.armor_slot.item.subtype in self.disliked_armors:
                temp_armor_mod += math.floor(self.armor_slot.item.armor * 0.66)
                self.active_effects_lib.add_effect(self.game.e_disliked_armor)
            else:
                temp_armor_mod += self.armor_slot.item.armor
            if self.armor_slot.item.subtype == "plate":
                #print ("Knight bonus aplied")
                temp_hit_rate_mod *= (self.armor_slot.item.hit_rate_mod * self.plate_armor_penalty_reduction)
            else:
                temp_hit_rate_mod *= self.armor_slot.item.hit_rate_mod
            temp_str_mod += self.armor_slot.item.str_mod
            temp_sta_mod += self.armor_slot.item.sta_mod
            temp_int_mod += self.armor_slot.item.int_mod
            temp_wis_mod += self.armor_slot.item.wis_mod
            temp_speed_mod += self.armor_slot.item.speed_mod
            temp_ste_mod += self.armor_slot.item.ste_mod
        if self.shield_slot.item:
            if self.shield_slot.item.subtype in self.favourite_armors:
                temp_armor_mod += math.floor(self.shield_slot.item.armor * 1.33)
                self.active_effects_lib.add_effect(self.game.e_favourite_armor)
            elif self.shield_slot.item.subtype in self.disliked_armors:
                temp_armor_mod += math.floor(self.shield_slot.item.armor * 0.66)
                self.active_effects_lib.add_effect(self.game.e_disliked_armor)
            else:
                temp_armor_mod += self.shield_slot.item.armor
            temp_hit_rate_mod *= self.shield_slot.item.hit_rate_mod
            temp_str_mod += self.shield_slot.item.str_mod
            temp_sta_mod += self.shield_slot.item.sta_mod
            temp_int_mod += self.shield_slot.item.int_mod
            temp_wis_mod += self.shield_slot.item.wis_mod
            temp_speed_mod += self.shield_slot.item.speed_mod
            temp_ste_mod += self.shield_slot.item.ste_mod
        if self.helmet_slot.item:
            if self.helmet_slot.item.subtype in self.favourite_armors:
                temp_armor_mod += math.floor(self.helmet_slot.item.armor * 1.33)
                self.active_effects_lib.add_effect(self.game.e_favourite_armor)
            elif self.helmet_slot.item.subtype in self.disliked_armors:
                temp_armor_mod += math.floor(self.helmet_slot.item.armor * 0.66)
                self.active_effects_lib.add_effect(self.game.e_disliked_armor)
            else:
                temp_armor_mod += self.helmet_slot.item.armor
            if self.helmet_slot.item.subtype == "plate":
                print ("Knight bonus aplied")
                temp_hit_rate_mod *= (self.helmet_slot.item.hit_rate_mod * self.plate_armor_penalty_reduction)
            else:
                temp_hit_rate_mod *= self.helmet_slot.item.hit_rate_mod
            temp_str_mod += self.helmet_slot.item.str_mod
            temp_sta_mod += self.helmet_slot.item.sta_mod
            temp_int_mod += self.helmet_slot.item.int_mod
            temp_wis_mod += self.helmet_slot.item.wis_mod
            temp_speed_mod += self.helmet_slot.item.speed_mod
            temp_ste_mod += self.helmet_slot.item.ste_mod
        if self.boots_slot.item:
            if self.boots_slot.item.subtype in self.favourite_armors:
                temp_armor_mod += math.floor(self.boots_slot.item.armor * 1.33)
                self.active_effects_lib.add_effect(self.game.e_favourite_armor)
            elif self.boots_slot.item.subtype in self.disliked_armors:
                temp_armor_mod += math.floor(self.boots_slot.item.armor * 0.66)
                self.active_effects_lib.add_effect(self.game.e_disliked_armor)
            else:
                temp_armor_mod += self.boots_slot.item.armor
            if self.boots_slot.item.subtype == "plate":
                print ("Knight bonus aplied")
                temp_hit_rate_mod *= (self.boots_slot.item.hit_rate_mod * self.plate_armor_penalty_reduction)
            else:
                temp_hit_rate_mod *= self.boots_slot.item.hit_rate_mod
            temp_str_mod += self.boots_slot.item.str_mod
            temp_sta_mod += self.boots_slot.item.sta_mod
            temp_int_mod += self.boots_slot.item.int_mod
            temp_wis_mod += self.boots_slot.item.wis_mod
            temp_speed_mod += self.boots_slot.item.speed_mod
            temp_ste_mod += self.boots_slot.item.ste_mod
        if self.ring1_slot.item:
            temp_hit_damage += self.ring1_slot.item.damage_mod
            temp_arrow_damage += self.ring1_slot.item.arrow_damage_mod
            temp_armor_mod += self.ring1_slot.item.armor_mod
            temp_hit_rate_mod *= self.ring1_slot.item.hit_rate_mod
            temp_str_mod += self.ring1_slot.item.str_mod
            temp_sta_mod += self.ring1_slot.item.sta_mod
            temp_int_mod += self.ring1_slot.item.int_mod
            temp_wis_mod += self.ring1_slot.item.wis_mod
            temp_speed_mod += self.ring1_slot.item.speed_mod
            temp_ste_mod += self.ring1_slot.item.ste_mod
            temp_barter_bonus += self.ring1_slot.item.barter_mod
        if self.ring2_slot.item:
            temp_hit_damage += self.ring2_slot.item.damage_mod
            temp_arrow_damage += self.ring2_slot.item.arrow_damage_mod
            temp_armor_mod += self.ring2_slot.item.armor_mod
            temp_hit_rate_mod *= self.ring2_slot.item.hit_rate_mod
            temp_str_mod += self.ring2_slot.item.str_mod
            temp_sta_mod += self.ring2_slot.item.sta_mod
            temp_int_mod += self.ring2_slot.item.int_mod
            temp_wis_mod += self.ring2_slot.item.wis_mod
            temp_speed_mod += self.ring2_slot.item.speed_mod
            temp_ste_mod += self.ring2_slot.item.ste_mod
            temp_barter_bonus += self.ring2_slot.item.barter_mod
        if self.necklace_slot.item:
            temp_hit_damage += self.necklace_slot.item.damage_mod
            temp_arrow_damage += self.necklace_slot.item.arrow_damage_mod
            temp_armor_mod += self.necklace_slot.item.armor_mod
            temp_hit_rate_mod *= self.necklace_slot.item.hit_rate_mod
            temp_str_mod += self.necklace_slot.item.str_mod
            temp_sta_mod += self.necklace_slot.item.sta_mod
            temp_int_mod += self.necklace_slot.item.int_mod
            temp_wis_mod += self.necklace_slot.item.wis_mod
            temp_speed_mod += self.necklace_slot.item.speed_mod
            temp_ste_mod += self.necklace_slot.item.ste_mod
            temp_barter_bonus += self.necklace_slot.item.barter_mod
        ############ EFEKTY ############
        for effect in self.active_effects_lib.active_effects:
            if effect.name == "stone skin" or effect.name == "iron skin":
                temp_armor_mod += effect.strength
            if effect.name == "haste":
                temp_speed_mod += effect.strength
            if effect.name == "invisibility":
                self.invisible = True
            if effect.name == "heroism":
                temp_str_mod += effect.strength
            if effect.name == "barter":
                temp_barter_bonus += effect.strength
            if effect.name == "slow":
                self.slow_mod = effect.strength
        #########################
        self.strength = self.base_strength + temp_str_mod
        self.stamina = self.base_stamina + temp_sta_mod
        self.intellect = self.base_intellect + temp_int_mod
        self.wisdom = self.base_wisdom + temp_wis_mod
        self.speed = self.base_speed + temp_speed_mod
        self.stealth = self.base_stealth + temp_ste_mod
        self.barter_bonus = temp_barter_bonus
        #########################
        self.max_hp = 15 + self.stamina * 5
        self.max_mana = max(4, self.wisdom * 8 - 15)
        self.arrow_damage = self.strength + temp_arrow_damage
        self.hit_dmg = self.strength + temp_hit_damage
        self.armor += temp_armor_mod
        ##########################
        if temp_arrow_rate:
            self.arrow_rate = temp_arrow_rate
            self.arrow_rate *= (temp_hit_rate_mod * self.bow_hit_rate_bonus)
        else:
            self.hit_rate = temp_hit_rate
            self.hit_rate *= temp_hit_rate_mod
        ###########################
        self.block_chance = self.calculate_block_ratio(self.armor) * 100
        self.hit_reduction = self.calculate_hit_reduction(self.armor) * 100
        self.movement_speed = self.calculate_movement_speed(self.speed)
        #print("hit damage: " + str(self.hit_dmg))
        #print("hit rate: " + str(self.hit_rate))
        #print("arrow rate: " + str(self.arrow_rate))
        #print("temp hit rate mod: " + str(temp_hit_rate_mod))
        #print("armor: " + str(self.armor))
        #print("block_chance: " + str(self.block_chance) + "%")
        #print("hit_reduction: " + str(self.hit_reduction) + "%")
        #print("movement speed: " + str(self.movement_speed))
        ############## AKTUALIZACJA FLAGI ATTACK TYPE ###########
        attack_flag_type_done = False
        if self.active_spell:
            if self.active_spell.type == "offensive":
                self.attack_type_flag = "magic"
                attack_flag_type_done = True
        if not attack_flag_type_done:
            if self.weapon_slot.item:
                if self.weapon_slot.item.ranged:
                    self.attack_type_flag = "ranged"
                    attack_flag_type_done = True
        if not attack_flag_type_done:
            self.attack_type_flag = "melle"
        #print ("TYP ATAKU = " + self.attack_type_flag)

    def check_block(self):
        block_seed = random.random()
        block_ratio = self.calculate_block_ratio(self.armor)
        if block_seed < block_ratio:
            print ("block!")
            return True
        else:
            #print ("no block")
            return False

    def calculate_hit_reduction(self, x):
        x += 4
        hit_reduction = (math.log(x/5)* 10)
        hit_reduction = int(hit_reduction + (x/3)) / 100
        return min(0.8,hit_reduction)

    def calculate_block_ratio(self, x):
        ### FUNKCJA ZWRACAJACA PRAWDOPODOBIENSTWO BLOKU
        block_ratio = min(0.5, math.sin(x / 200))
        if x > 106:
            block_ratio += (x - 100) / 500
            block_ratio = min(0.8, block_ratio)
        return block_ratio

    def calculate_movement_speed(self,x):
        result = 80 + (10 * math.log2(x * x / 4))
        result = max(80, int(result))
        if self.slow_mod > 0:
            return result * self.slow_mod / 100
        return result

    def armor_breakage(self):
        if self.armor_slot.item:
            self.armor_slot.item.breakage()
        if self.shield_slot.item:
            self.shield_slot.item.breakage()
        if self.boots_slot.item:
            self.boots_slot.item.breakage()
        if self.helmet_slot.item:
            self.helmet_slot.item.breakage()

    def weapon_breakage(self):
        if self.weapon_slot.item:
            self.weapon_slot.item.breakage()

    def check_live(self):
        if self.act_hp <=0:
            self.start_death_animation = True
        else:
            return True

    def check_gold(self, item, shop) -> bool:
        price = shop.calculate_sell_to_player_price(item)
        if self.gold >= price:
            return True
        else:
            return False

    def check_next_level(self):
        self.xp_step = 10 * self.level + ((self.level - 1) * 2 * self.level)
        while self.xp >= self.xp_step:
            self.level += 1
            self.attribute_points += 1
            self.xp_step = 10 * self.level + ((self.level - 1) * 2 * self.level)
            self.game.events_manager.emit(Event(id=f'level {self.level} achieved'))
        if self.attribute_points > 0:
            pygame.mixer.Sound.play(levelup_snd)
            self.act_hp = self.max_hp
            self.act_mana = self.max_mana
            return self.attribute_points
        else:
            return False

    def go_to_level(self, destination, pos_x, pos_y):
        self.game.levelgen.go_to_level(destination, pos_x, pos_y)
        #self.wait_key_pressed = True

    def update(self):
        ######## OPOZNIAM ROZPOCZECIE CZYTANIA KLAWISZY
        ####### ZEBY UNIKNA BUGA Z PRZEMIESZCENIEM GRACZA ZANIM
        ####### ZALADUJE MAPE
        ### KLAWIATURA ###
        self.get_keys()
        #print(str(self.pos.x) + "," + str(self.pos.y))
        ### ROTACJA ###
        # jesli rotacja - nadaj ROTATION SPEED< popraw klawisze, popraw kolizje i kamerę
        #self.image = pygame.transform.rotate(player_image, self.rot)
        self.image = self.char_class.image.copy()
        ### POZYCJA #############
        #self.rect = self.image.get_rect()
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        ### OBRAZENIA OD STRZAL INNYCH POTWOROW:
        hits = pygame.sprite.spritecollide(self, self.game.act_lvl.mob_arrows, False)
        for hit in hits:
            if not self.check_block():
                reduction = 1 - self.calculate_hit_reduction(self.armor)
                damage = math.ceil(hit.str * reduction)
                #print("Redukcja od zbroji: " + str(reduction))
                self.act_hp -= damage
                #print("Obrażenia od obiektu mob_arrows: " + str(damage))
                self.game.put_txt(self.name + " received " + str(damage) + " damage")
                self.damaged = True
                self.damage_alpha = chain(DAMAGE_ALPHA_LIST * 2)
                if ouch_snd.get_num_channels() > 2:
                    ouch_snd.stop()
                ouch_snd.play()
                self.armor_breakage()
                hit.kill()
                #### SPRAWDZAM CZY ZYJE PO KAZDYM UDERZENIU
                self.check_live()
            else:
                #### BLOCK ######
                pygame.mixer.Sound.play(block_snd)
                self.armor_breakage()
                self.score_blocks += 1
                txt = (self.name + "blocks!")
                self.game.put_txt(txt)
        ### OBRAZENIA(kolizja) OD(z) LAVA - w tym FIRE, SLOW etc..
        hits = pygame.sprite.spritecollide(self,self.game.act_lvl.lavas,False,collide_double_hit_rect)
        for hit in hits:
            if hit.effect.name == "damage":
                ## uderzenie DAMAGE z grupu lava fire immune time = 500 czyli udrz. 1x effect.strength na 0.2s
                now = (int(self.score_time_played * 1000))
                if now - self.last_damage >= self.fire_immune_time:
                    reduction = 1 - self.calculate_hit_reduction(self.armor)
                    damage = math.ceil(hit.effect.strength * reduction)
                    #print ("Redukcja od zbroji: " + str(reduction))
                    print("UDERZENIE OD EFFECTU DAMAGE z GRUPY LAVAS")
                    self.act_hp -= damage
                    #print ("Obrażenia od obiektu lava: " + str(damage))
                    self.game.put_txt(self.name + " received " + str(damage) + " damage")
                    self.damaged = True
                    self.damage_alpha = chain(DAMAGE_ALPHA_LIST * 2)
                    if ouch_snd.get_num_channels() > 2:
                        ouch_snd.stop()
                    ouch_snd.play()
                    self.armor_breakage()
                    self.last_damage = now
            if hit.effect.name == "fire":
                ## uderzenie FIRE z grupu lava fire immune time =500 czyli udrz. 1x effect.strength na 0.2s
                now = (int(self.score_time_played * 1000))
                if now - self.last_damage >= self.fire_immune_time:
                    reduction = 1 - self.calculate_hit_reduction(self.armor)
                    damage = math.ceil(hit.effect.strength * reduction)
                    #print ("Redukcja od zbroji: " + str(reduction))
                    print("UDERZENIE OD EFFECTU FIRE z GRUPY LAVAS")
                    self.act_hp -= damage
                    #print ("Obrażenia od obiektu lava: " + str(damage))
                    self.game.put_txt(self.name + " received " + str(damage) + " damage")
                    self.damaged = True
                    self.damage_alpha = chain(DAMAGE_ALPHA_LIST * 2)
                    if ouch_snd.get_num_channels() > 2:
                        ouch_snd.stop()
                    ouch_snd.play()
                    self.armor_breakage()
                    self.last_damage = now
                #### SPRAWDZAM CZY ZYJE PO KAZDYM UDERZENIU

            if hit.effect.name == "slow":
                #print("EFFECT SLOW z GRUPY LAVAS")
                self.active_effects_lib.add_effect(hit.effect)
                self.update_stats()
                ## NIE UZYWAM UPDATE STATS CELEM NIE OBCIAZANIA PAMIECI. ZMIENIAM TYLKO SZYBKOSC!
        self.check_live()
        ### KOLIZJE Z MUREM ###################
        self.hit_rect.centerx = self.pos.x
        collide_wall(self,self.game.act_lvl.walls,'x')
        collide_hr_obstacle(self,self.game.act_lvl.hr_obstacles,'x')
        self.hit_rect.centery = self.pos.y
        collide_wall(self,self.game.act_lvl.walls,'y')
        collide_hr_obstacle(self, self.game.act_lvl.hr_obstacles, 'y')
        self.rect.center = self.hit_rect.center
        ### UPDATE POZYCJI BRONI tej malej NA MAPIE z graczem
        for slot in self.active_slots:
            if slot.item:
                if isinstance(slot.item, Armor) or isinstance(slot.item,Weapon):
                    slot.item.update()
        ### UPDATE PASKA LADOWANIA BRONI
        self.update_weapon_load_bar()
        ### UPDATE DAMAGED BLINK EFFECT
        if self.damaged:
            try:
                self.image.fill((255, 0, 0, next(self.damage_alpha)),special_flags=pygame.BLEND_RGBA_MULT)
            except:
                self.damaged = False
        ### UPDATE INVISIBLE EFFECT
        if self.invisible:
            self.image.fill((180,180,180,100),special_flags=pygame.BLEND_RGBA_MULT)
        ### UPDATE SLOW EFFECT



class Npc(pygame.sprite.Sprite):
    def __init__(self, game, name, start_x, start_y, image):
        self._layer = MOB_LAYER
        self.groups = game.act_lvl.all_sprites, game.act_lvl.npcs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = name
        self.image = image
        self.start_x = start_x
        self.start_y = start_y
        self.visible = True
        self.encountered = False
        self.quests = []
        self.rect = self.image.get_rect()
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.hit_rect = pygame.Rect(0, 0, TILE_SIZE - 5, TILE_SIZE - 5)
        self.hit_rect.center = self.rect.center
        self.dialog_data = Dialog(self.game, self)
        self.sound = False

    def put_quest(self, quest):
        self.quests.append(quest)

    def encounter(self):
        self.game.events_manager.emit(Event(id=f'{self.name} has been encountered.'))
        self.encountered = True

    def put_sound(self, sound):
        self.sound = sound


class Mob(pygame.sprite.Sprite):
    ### KLASA PRZECIWNIKA, STOI W SPAWNLOC,
    ### Movement1:
    ### OD MOMENTU PRZEKROCZENIA PRZEZ GRACZA SLEEP RADIUS
    ### ZMIERZA W KIERUNKU GRACZA ZA POMOCĄ WEKTORA
    ### WRACA NA MIEJSCE GDY GRACz SIE ODDALI
    ### UDERZA WRECZ ZA POMICA COLLIDESPRITE

    def __init__(self, game, name, start_x , start_y, image, s_pos,
                 ranged_parameters, max_speed, min_speed, stun_time,
                 hp, damage, sleep_radius, xp, item):
        self._layer = MOB_LAYER
        self.groups = game.act_lvl.all_sprites, game.act_lvl.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = name
        self.speed = max_speed
        self.min_speed = min_speed
        self.max_hp = hp
        self.hp = hp
        self.xp = xp
        self.damage = damage
        self.item = item
        if not image:
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.HWSURFACE | pygame.SRCALPHA)
        else:
            self.image = image
        self.base_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.hit_rect = pygame.Rect(0, 0, TILE_SIZE - 5,TILE_SIZE -5)
        self.hit_rect.center = self.rect.center
        self.bullet_type = False
        self.bullet_image = False
        self.bullet_damage = False
        self.bullet_speed = False
        self.bullet_hitrate = False
        self.ranged_parameters = ranged_parameters
        if ranged_parameters:
            self.bullet_type = ranged_parameters[0]
            if self.bullet_type == "magic":
                self.bullet_image = bullet_magic_image
            elif self.bullet_type == "fire":
                self.bullet_image = bullet_firebolt_image
            elif self.bullet_type == "arrow":
                self.bullet_image = arrow_img
            elif self.bullet_type == "rock":
                self.bullet_image = bullet_rock_image
            elif self.bullet_type == "dart":
                self.bullet_image = bullet_dart_image
            elif self.bullet_type == "virus":
                self.bullet_image = bullet_virus_image
            else:
                self.bullet_image = bullet_magic_image
            self.bullet_damage = ranged_parameters[1]
            self.bullet_speed = ranged_parameters[2]
            self.bullet_hitrate = ranged_parameters[3]
        self.start_x = start_x
        self.start_y = start_y
        self.pos = vec(start_x,start_y)
        self.s_pos = s_pos
        if s_pos:
            self.second_pos = vec(s_pos)
        else:
            self.second_pos = vec(start_x,start_y)
        self.spawn_position = vec(start_x,start_y)
        self.destination_position = self.second_pos
        self.rect.center = self.pos
        self.hit_rect.centerx = self.pos.x
        self.hit_rect.centery = self.pos.y
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.rot = 0
        self.last_hit_moment = 0
        self.last_damage = 0
        self.last_bullet = 0
        self.hit_stun_time = stun_time * 1000
        self.fire_immune_time = 500
        self.avoid_radius = 50
        self.sleep_radius = sleep_radius
        self.updated_sleep_radius = sleep_radius
        self.frozen = False
        self.freeze_moment = 0
        self.freeze_alpha_counter = 0
        self.attention = 0
        ### DO WYSWIETLENIA EFEKTU GRAFICZNEGO
        self.damaged = False



    def load_image_from_tileset(self, tileset, x, y):
        self.image.blit(tileset, (0, 0), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    def deefreeze(self):
        ## FUNKCJA POWOLNEGO ODMRAZANIA
        ## ZMIenna Frozen niesie za sobą czas do zamrozenia.
        print (self.name + "zamrozony przez " + str(self.freeze_moment) + " s")
        self.freeze_alpha_counter += 1
        if self.freeze_alpha_counter > 150:
            self.freeze_alpha_counter = 0
        self.image.fill((self.freeze_alpha_counter, self.freeze_alpha_counter, 250),
                        special_flags=pygame.BLEND_RGB_MAX)
        self.freeze_moment += self.game.dt
        #### CZAS ZAMROZENIA = CZAR + 2*INT GRACZA
        if self.freeze_moment > (self.frozen + self.game.player.intellect):
            self.frozen = False
            self.freeze_moment = 0

    def avoid_mobs(self):
        for mob in self.game.act_lvl.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length_squared() < self.avoid_radius**2:
                    self.acc += dist.normalize()

    def mob_movement_test(self):
        distance_to_player = (self.game.player.pos - self.pos).length()
        if distance_to_player < self.sleep_radius:
            self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
            self.acc = vec(1,0).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            if self.vel.length()>self.speed:
                self.vel.scale_to_length(self.speed)
            elif self.vel.length()<self.min_speed:
                self.vel.scale_to_length(self.min_speed)
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            print(self.vel)
            print("SPEED: " + str(int(self.vel.length())))
            print("ACC: " + str(int(self.acc.length())))

    def mob_movement_s(self):
        #### TYP RUCHU POSTACI S (w linii)
        if self.game.dt > 0.1:
            self.game.dt = 0.1
        distance_to_player = (self.game.player.pos - self.pos).length_squared()
        awake_distance = max(48,self.updated_sleep_radius)
        if self.game.player.invisible:
            awake_distance = 32
        #print ("distance to player: " + str(distance_to_player))
        #print ("awake distance: " + str(awake_distance))
        #### JEZELI DOSTRZEGL GRACZA
        if distance_to_player < awake_distance ** 2:
            self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
            # jezeli ma rotowac sie w kierunku gracza...
            # self.image = pygame.trasform.rotate(self.non_rotated_image, self.rot)
            ### RUCH
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * - 1
            self.vel += self.acc * self.game.dt
            now = (int(self.game.player.score_time_played * 1000))
            #### JEZELI NIE JEST UDERZONY, WLACZAM  MINIMALNA PREDKOSC!
            if now - self.last_hit_moment > self.hit_stun_time:
                #print ("APPLY MIN SPEED")
                if self.vel.length_squared() <= self.min_speed ** 2:
                    if self.speed:
                        self.vel.scale_to_length(self.min_speed)
            else:
                pass
                #print ("POZWALAM NA ZMINEJSZENIE PREDKOSCI PONIZEJ MINIMALNEJ")
                # print ("SPEED: " + str(self.vel.length()))
                # print ("ACC: " + str(self.acc.length()))
        #### JEZELI NIE WIDZI GRACZA WRACA NA SWOJA POZYCJE
        else:
            #### JEZELI GRACz O 60 od SLEEP RADIUS
            if distance_to_player < (awake_distance + 60)**2:
                self.image.blit(attent_image,(0,0))
            self.rot = (self.destination_position - self.pos).angle_to(vec(1, 0))
            self.acc = vec(1, 0).rotate(-self.rot)
            self.acc.scale_to_length(self.speed / 2)
            self.acc += self.vel * - 2
            self.vel += self.acc * self.game.dt
            ## JEZELI JEST BLISKO SECOND POSITION - IDZIE W KIERUNKU PIERWSZEJ POS
            if (self.pos - self.second_pos).length_squared() < 5**2:
                self.destination_position = self.spawn_position
            elif (self.pos - self.spawn_position).length_squared() < 5**2:
                self.destination_position = self.second_pos
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2

    def mob_movement_ranged(self):
        if self.game.dt > 0.1:
            self.game.dt = 0.1
        distance_to_player = (self.game.player.pos - self.pos).length_squared()
        awake_distance = max(48, self.updated_sleep_radius)
        if self.game.player.invisible:
            awake_distance = 32
        # print ("distance to player: " + str(distance_to_player))
        #### JEZELI DOSTRZEGL GRACZA
        if distance_to_player < awake_distance**2:
            self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
            # jezeli ma rotowac sie w kierunku gracza...
            # self.image = pygame.trasform.rotate(self.non_rotated_image, self.rot)
            ### RUCH
            #print ("Jednostka strzelajaca sie rusza w kierunku przeciwnym do gracza (vec -1")
            self.acc = vec(-1, 0).rotate(self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * - 1
            self.vel += self.acc * self.game.dt
            now = (int(self.game.player.score_time_played * 1000))
            #### JEZELI NIE JEST UDERZONY, WLACZAM  MINIMALNA PREDKOSC!
            if now - self.last_hit_moment > self.hit_stun_time:
                # print ("APPLY MIN SPEED")
                if self.vel.length_squared() <= self.min_speed**2:
                    if self.speed:
                        self.vel.scale_to_length(self.min_speed)
            else:
                pass
                # print ("POZWALAM NA ZMINEJSZENIE PREDKOSCI PONIZEJ MINIMALNEJ")
                # print ("SPEED: " + str(self.vel.length()))
                # print ("ACC: " + str(self.acc.length()))
        #### JEZELI NIE WIDZI GRACZA WRACA NA SWOJA POZYCJE
        else:
            #### JEZELI GRACz O 60 od SLEEP RADIUS
            if distance_to_player < (awake_distance + 60)**2:
                self.image.blit(attent_image,(0,0))
            self.rot = (self.spawn_position - self.pos).angle_to(vec(1, 0))
            self.acc = vec(1, 0).rotate(-self.rot)
            self.acc.scale_to_length(self.speed / 2)
            self.acc += self.vel * - 2
            self.vel += self.acc * self.game.dt
            ## JEZELI JEST BLISKO SPAWN LOC - ZATRZYMUJE SIE
            if (self.pos - self.spawn_position).length_squared() < 5**2:
                self.acc = vec(0, 0)
                self.vel = vec(0, 0)
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2

    def mob_movement1(self):
        if self.game.dt > 0.1:
            self.game.dt = 0.1
        distance_to_player = (self.game.player.pos - self.pos).length_squared()
        awake_distance = max(48, self.updated_sleep_radius)
        if self.game.player.invisible:
            awake_distance = 32
        # print ("distance to player: " + str(distance_to_player))
        #### JEZELI DOSTRZEGL GRACZA
        if distance_to_player < awake_distance**2:
            self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
            # jezeli ma rotowac sie w kierunku gracza...
            # self.image = pygame.trasform.rotate(self.non_rotated_image, self.rot)
            ### RUCH
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * - 1
            self.vel += self.acc * self.game.dt
            now = (int(self.game.player.score_time_played * 1000))
            #### JEZELI NIE JEST UDERZONY, WLACZAM  MINIMALNA PREDKOSC!
            if now - self.last_hit_moment > self.hit_stun_time:
                # print ("APPLY MIN SPEED")
                if self.vel.length_squared() <= self.min_speed**2:
                    if self.speed:
                        self.vel.scale_to_length(self.min_speed)
            else:
                pass
                # print ("POZWALAM NA ZMINEJSZENIE PREDKOSCI PONIZEJ MINIMALNEJ")
                # print ("SPEED: " + str(self.vel.length()))
                # print ("ACC: " + str(self.acc.length()))
        #### JEZELI NIE WIDZI GRACZA WRACA NA SWOJA POZYCJE
        else:
            #### JEZELI GRACz O 60 od SLEEP RADIUS
            if distance_to_player < (awake_distance + 60)**2:
                self.image.blit(attent_image,(0,0))
            self.rot = (self.spawn_position - self.pos).angle_to(vec(1, 0))
            self.acc = vec(1, 0).rotate(-self.rot)
            self.acc.scale_to_length(self.speed / 2)
            self.acc += self.vel * - 2
            self.vel += self.acc * self.game.dt
            ## JEZELI JEST BLISKO SPAWN LOC - ZATRZYMUJE SIE
            if (self.pos - self.spawn_position).length_squared() < 5**2:
                self.acc = vec(0, 0)
                self.vel = vec(0, 0)
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2

    def mob_ranged_attack(self):
        distance_to_player = (self.game.player.pos - self.pos).length_squared()
        ### ZAWSZE BEDZIE AKTYWNY jezeli podejdziesz blizej niz 48)
        awake_distance = max(48, self.updated_sleep_radius)
        ### GDY NIEWIDZIALNY AWAKE DISTANCE = 32 (wielkosc tile).. moze zwieszyc?
        if self.game.player.invisible:
            awake_distance = 32
        if distance_to_player < awake_distance**2:
            mob_rotation_vec = (self.game.player.pos - self.pos)
            dir = vec.normalize(mob_rotation_vec)
            ### STRZAL
            now = (int(self.game.player.score_time_played * 1000))
            if now - self.last_bullet > self.bullet_hitrate:
                #print ("MOB RANGED ATTACK!")
                #print ("ROT:")
                #print (dir)
                #print ("POS:")
                #print (self.pos)
                MobArrow(self.game,self,self.pos,dir,self.bullet_damage,self.bullet_speed,self.bullet_image)
                self.last_bullet = now

    def die(self):
        self.game.player.xp += self.xp
        ### TWORZE obiekt Flesh
        if self.name == "Mad Bull":
            other_image = pygame.Surface((32,32), pygame.HWSURFACE | pygame.SRCALPHA)
            other_image.blit(full_tileset_image,(0,0),(37*TILE_SIZE, 94*TILE_SIZE,TILE_SIZE,TILE_SIZE))
            Flesh(self.game, self.pos, other_image)
        else:
            Flesh(self.game, self.pos, False)
        ### METODY DO KOLEKCJI INFORMACJI, jedna MOJA, druga COPALCO
        self.game.player.score_killed_enemies.append((self.name, self.max_hp))
        self.game.events_manager.emit(Event(id=f'{self.name} has been killed'))
        ### GDY WYPADA PRZEDMIOT Z MOBA
        if self.item:
            if self.item == "gold":
                print("ENEMY IS DEDAD, GENERATINING GOLD")
                Gold_to_take(self.game,self.pos.x,self.pos.y,
                             self.damage)
            elif self.item == "random":
                print("ENEMY IS DEDAD, GENERATINING RANDOM ITEM")
                #### ITEM o MAX COST od 3xHP (min 29)... np. moze HP*DAMAGE?
                Item_to_take(self.game,self.pos.x, self.pos.y,
                             self.game.levelgen.gen.generate_random_item("all",max(29,self.max_hp*3)))
            else:
                print ("ENEMY IS DEDAD, GENERATINING ITEM by NAME")
                Item_to_take(self.game,self.pos.x,self.pos.y,
                             self.game.levelgen.gen.generate_item_by_name(self.item))
        ### USUWAM SPRITE
        self.kill()
        ### DZWIEK
        pygame.mixer.Sound.play(win_snd)
        ### SPRAWDZAM NEXT LEVEL
        if self.game.player.check_next_level():
            self.game.paused = True
        ### TODO AUTO SPRAWDZEIE QUESTOW Z mobs_to_kill

    def update(self):
        self.image = self.base_image.copy()
        #### ADJUSTING SLEEP RADIUS
        self.updated_sleep_radius = self.sleep_radius - (self.game.player.stealth * 3) + self.attention
        #### ZMNIEJSZANIE ATTENTION
        if self.attention > 0:
            self.attention -= 5 * self.game.unpaused_dt
            #print (f'attention: {self.attention}')
            #print (f'sleep radius: {self.sleep_radius}')
            #print (f'up sl radius: {self.updated_sleep_radius}')
        #### ODMRAZANIE (jesli zamrozony)
        if self.frozen:
            self.deefreeze()
        #### RUCH
        if not self.frozen:
            ### JEZELI POSIADA ZMIENNA S_POS - chodzi w linii
            if self.s_pos:
                self.mob_movement_s()
            ### JEZELI NIE CZEKA W MIEJSCU LUB GONI WROGA (MOVEMENT)
            else:
                if not self.ranged_parameters:
                    self.mob_movement1()
                else:
                    self.mob_movement_ranged()
        else:
            print (self.name + " FROZEN!")
        ##### STRZELANIE :
        if self.bullet_type:
            self.mob_ranged_attack()
        #### OBRAZENIA OD FIRE i EFFECT SLOW -- zobaczymy LAVY:
        hits = pygame.sprite.spritecollide(self, self.game.act_lvl.lavas, False)
        for hit in hits:
            if hit.effect.name == "damage":
                ## uderzenie fizyczne .str na 0.2s
                now = (int(self.game.player.score_time_played * 1000))
                if now - self.last_damage >= self.fire_immune_time:
                    self.hp -= hit.effect.strength
                    print(f'Obrażenia od obiektu typ lava, efekt damage: {hit.effect.strength}')
                    self.damage_alpha = chain(DAMAGE_ALPHA_LIST * 2)
                    self.last_damage = now
                    self.damaged = True
            if hit.effect.name == "fire":
                ## uderzenie od ognia .str na 0.2s
                now = (int(self.game.player.score_time_played * 1000))
                if now - self.last_damage >= self.fire_immune_time:
                    self.hp -= hit.effect.strength
                    print (f'Obrażenia od obiektu typ lava, efekt fire: {hit.effect.strength}')
                    self.damage_alpha = chain(DAMAGE_ALPHA_LIST * 2)
                    self.last_damage = now
                    self.damaged = True
                    if isinstance(hit, Blow_Spell):
                        self.game.put_txt(f'Spell explosion inflicted {hit.effect.strength} damage')
                        #print ("TO BYL WYBUCH CZARU!")
                #if self.hp <= 0:
                #    self.kill()
        ### OBRAZENIA OD STRZAL INNYCH POTWOROW:
        hits = pygame.sprite.spritecollide(self,self.game.act_lvl.mob_arrows, False)
        for hit in hits:
            if not hit.owner == self:
                # NIE ZADAJE OBRAZEN SOBIE!
                self.hp -= hit.str
                print("Obrażenia od obiektu mob arrow: " + str(hit.str))
                self.damage_alpha = chain(DAMAGE_ALPHA_LIST * 2)
                self.damaged = True
                hit.kill()
                #if self.hp <= 0:
                #    self.kill()
        ### KOLIZJE Z MUREM
        self.hit_rect.centerx = self.pos.x
        collide_wall(self,self.game.act_lvl.walls,"x")
        collide_hr_obstacle(self, self.game.act_lvl.hr_obstacles, 'x')
        self.hit_rect.centery = self.pos.y
        collide_wall(self, self.game.act_lvl.walls, "y")
        collide_hr_obstacle(self, self.game.act_lvl.hr_obstacles, 'y')
        self.rect.center = self.hit_rect.center
        ### SPRAWDZAM HP i ZABIJAM MOBA, dodaje XP dla gracza
        if self.hp <=0:
            self.die()
        ### JEZELI RANNY - ANIMACJA PULSUJACA CZERWIEN
        if self.damaged:
            try:
                self.image.fill((255, 0, 0, next(self.damage_alpha)),special_flags=pygame.BLEND_RGBA_MULT)
            except:
                self.damaged = False

    def draw_health(self):
        if self.hp > 60*self.max_hp/100:
            col = (0,255,0)
        elif self.hp > 30*self.max_hp/100:
            col = (255,255,0)
        else:
            col = (255,0,0)
        width = int(self.rect.width * (self.hp/self.max_hp))
        self.hp_bar = pygame.Rect(0,0,width,2)
        pygame.draw.rect(self.image,col,self.hp_bar)


class Hit_Splash(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = HIT_GRAPHICS_LAYER
        self.groups = game.act_lvl.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        pygame.mixer.Sound.play(ouch_snd)
        self.game = game
        self.image = hit_image
        size = random.randint(28,38)
        self.image = pygame.transform.scale(self.image,(size,size))
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = (int(self.game.player.score_time_played * 1000))

    def update(self):
        now = (int(self.game.player.score_time_played * 1000))
        if now - self.spawn_time > 60:
            self.kill()


class Mob_Hit_Splash(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = HIT_GRAPHICS_LAYER
        self.groups = game.act_lvl.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = hit_image
        size = random.randint(28,38)
        self.image = pygame.transform.scale(self.image,(size,size))
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = (int(self.game.player.score_time_played * 1000))

    def update(self):
        now = (int(self.game.player.score_time_played * 1000))
        if now - self.spawn_time > 60:
            self.kill()


class Flesh(pygame.sprite.Sprite):
    def __init__(self, game, pos, other_image):
        self._layer = FLOOR_LAYER
        self.groups = game.act_lvl.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        #pygame.mixer.Sound.play(win_snd)
        self.game = game
        if other_image:
            self.image = other_image
        else:
            self.image = flesh_image
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = (int(self.game.player.score_time_played * 1000))

    def update(self):
        pass
        ## JEZELI MA WYSYCHAC i ZNIKAC PO Pewnym czasie ...
        #if pygame.time.get_ticks() - self.spawn_time > 50000:
        #    self.kill()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h, water):
        self.groups = game.act_lvl.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.water = water
        self.removable = False


class RemObstacle(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h, water, remove_event):
        self.groups = game.act_lvl.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.water = water
        self.removable = True
        self.remove_condition = remove_event
        self.game.rem_objects.append(self)

    def remove(self):
        if self.removable:
            self.kill()

    def check_remove_condition(self):
        print ("Check removable walls")
        if self.game.events_manager.search_event(self.remove_condition):
            return True
        else:
            print ("No remove condition in events")
            return False


class Teleport(pygame.sprite.Sprite):
    def __init__(self, game, name, destination, pos_x, pos_y, x, y, w, h):
        self.groups = game.act_lvl.teleports
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = name
        self.destination = destination
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    def activate_teleport(self):
        self.game.player.go_to_level(self.destination, self.pos_x, self.pos_y)
        self.game.events_manager.emit(Event(id=f'{self.name} has been visited'))
        self.game.put_txt(f'Travel to {self.name}')
        self.game.update_game_enviroment()


class ShopDoor(pygame.sprite.Sprite):
    def __init__(self, game, shop, pos_x, pos_y, x, y, w, h):
        self.groups = game.act_lvl.shops
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.shop = self.game.levelgen.shop_gen.generate_shop_by_name(shop)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


class Lava(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h, effect):
        self.groups = game.act_lvl.lavas
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.effect = effect
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.hit_rect = self.rect


class EffectObject(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image, effect):
        self.groups = game.act_lvl.all_sprites, game.act_lvl.lavas
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos = (x, y)
        self.effect = effect
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hit_rect = self.rect


class DartTrap(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image, direction, speed, lifetime, freq, strength, bull_img = bullet_dart_image):
        self._layer = EFFECTS_LAYER
        self.groups = game.act_lvl.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if image:
            self.image = image
        else:
            self.image = pygame.Surface((TILE_SIZE,TILE_SIZE),pygame.HWSURFACE | pygame.SRCALPHA)
        self.bull_img = bull_img
        self.strength = strength
        self.direction = direction
        self.angle = self.direction.angle_to(vec(0,-1))
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.speed = speed
        self.lifetime = lifetime
        self.freq = freq
        self.pos = (x, y)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hit_rect = self.rect
        #self.arrow_vel = vec(1,0) * self.direction
        self.last_dart = 0

    def update(self):
        now = (int(self.game.player.score_time_played * 1000))
        #print (str(now))
        if now - self.last_dart > self.freq:
            #print ("DART DIR")
            #print (self.direction)
            Dart(self.game,self.pos,self.direction, self.speed, self.lifetime, self.strength, self.bull_img)
            self.last_dart = now


class MobArrow(pygame.sprite.Sprite):
    def __init__(self, game, owner, pos, dir, str, speed, image):
        self._layer = HIT_GRAPHICS_LAYER
        self.groups = game.act_lvl.all_sprites, game.act_lvl.mob_arrows
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.speed = speed
        self.lifetime = 2500
        self.game = game
        self.owner = owner
        self.str = str
        self.pos = vec(pos)
        self.vel = dir * self.speed
        self.image = image
        self.image = pygame.transform.rotate(self.image,dir.angle_to(vec(1,0)))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.hit_rect = self.rect
        self.spawn_time = (int(self.game.player.score_time_played * 1000))

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        now = (int(self.game.player.score_time_played * 1000))
        if now - self.spawn_time > 100:
            ## KOLIZJA Z MUREM (nie wodą!)
            hits = pygame.sprite.spritecollide(self, self.game.act_lvl.walls, False)
            for hit in hits:
                if not hit.water:
                    self.kill()
        if now - self.spawn_time > self.lifetime:
            self.kill()
        if collide_double_hit_rect(self,self.game.player):
            self.lifetime = 10
        mob_hits = pygame.sprite.spritecollide(self,self.game.act_lvl.mobs,False,collide_double_hit_rect)
        for mob in mob_hits:
            if not mob == self.owner:
                self.lifetime = 100


class Dart(pygame.sprite.Sprite):
    def __init__(self, game, pos, dir, speed, lifetime, strength, image = bullet_dart_image):
        self._layer = HIT_GRAPHICS_LAYER
        self.groups = game.act_lvl.all_sprites, game.act_lvl.lavas
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.speed = speed
        self.lifetime = lifetime
        self.game = game
        self.strength = strength
        self.effect = ActiveEffect("damage",e_fire_ico,strength,1)
        self.pos = vec(pos)
        self.vel = dir * self.speed
        self.image = image
        self.image = pygame.transform.rotate(self.image,dir.angle_to(vec(1,0)))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.hit_rect = self.rect
        self.spawn_time = (int(self.game.player.score_time_played * 1000))

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        now = (int(self.game.player.score_time_played * 1000))
        if now - self.spawn_time > 250:
            ## Kolizja z murem (nie wodą!)
            hits = pygame.sprite.spritecollide(self, self.game.act_lvl.walls, False)
            for hit in hits:
                if not hit.water:
                    self.kill()
        if now - self.spawn_time > self.lifetime:
            self.kill()
        if collide_double_hit_rect(self,self.game.player):
            self.lifetime = 100
        if pygame.sprite.spritecollide(self,self.game.act_lvl.mobs,False,collide_double_hit_rect):
            self.lifetime = 100


class PinTrap(pygame.sprite.Sprite):
    def __init__(self, game, x, y, img_hidden, img_open, strength):
        self._layer = EFFECTS_LAYER
        self.groups = game.act_lvl.all_sprites #, game.act_lvl.lavas
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.strength = strength
        self.effect = ActiveEffect("damage", e_fire_ico, strength, 1)
        self.image_h = img_hidden
        self.image_o = img_open
        self.image = self.image_h
        self.pos = (x, y)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hit_rect = pygame.Rect(self.rect.left + 5, self.rect.top + 8 ,18,18)
        self.active = True
        self.open = False

    def pin_up(self):
        if self.active:
            if not self.open:
                pygame.mixer.Sound.play(pintrap_o_snd)
                self.open = True
                self.image = self.image_o
                self.game.act_lvl.lavas.add(self)

    def pin_down(self):
        if self.open:
            self.image = self.image_h
            self.game.act_lvl.lavas.remove(self)
            self.open = False

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def update(self):
        if self.active:
            if collide_double_hit_rect(self,self.game.player):
                self.pin_up()
            if pygame.sprite.spritecollide(self, self.game.act_lvl.mobs,False,collide_double_hit_rect):
                self.pin_up()


class Trap(pygame.sprite.Sprite):
    def __init__(self, game, x, y, img, direction, strength):
        self._layer = EFFECTS_LAYER
        self.groups = game.act_lvl.all_sprites, game.act_lvl.lavas
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pins_img = img
        self.image = pygame.Surface((22,12),pygame.HWSURFACE|pygame.SRCALPHA)
        self.effect = ActiveEffect("damage", e_fire_ico, strength, 1)
        self.range = 12
        self.speed = 0.2
        self.tween = pytw.easeInExpo
        self.step = 0
        self.dir_sign = 1
        if direction == "S":
            self.dir = vec(0,1)
            self.rect = self.image.get_rect()
            self.surf_pos = (x, y)
            self.rect.bottomleft = self.surf_pos
            self.pins_img = pygame.transform.rotate(self.pins_img, 180)
            self.dir_sign = -1
            self.pin_rect = self.pins_img.get_rect()
            self.pins_pos = (0, 0)
            self.hit_rect = pygame.Rect(self.surf_pos[0] + self.pins_pos[0], self.surf_pos[1] + self.pins_pos[1], 22, 12)
        elif direction == "E":
            self.pins_img = pygame.transform.rotate(self.pins_img,90)
            self.image = pygame.transform.rotate(self.image,90)
            self.dir = vec(1,0)
            self.rect = self.image.get_rect()
            self.surf_pos = (x, y)
            self.rect.topleft = self.surf_pos
            self.pin_rect = self.pins_img.get_rect()
            self.pins_pos = (0, 0)
            self.hit_rect = pygame.Rect(self.surf_pos[0] + self.pins_pos[0], self.surf_pos[1] + self.pins_pos[1], 12, 22)
        elif direction == "N":
            #self.pins_img = pygame.transform.rotate(self.pins_img,180)
            self.dir = vec(0,-1)
            self.rect = self.image.get_rect()
            self.surf_pos = (x, y)
            self.rect.topleft = self.surf_pos
            self.pin_rect = self.pins_img.get_rect()
            self.pins_pos = (0, 0)
            self.hit_rect = pygame.Rect(self.surf_pos[0] + self.pins_pos[0], self.surf_pos[1] + self.pins_pos[1], 22, 12)
        elif direction == "W":
            self.pins_img = pygame.transform.rotate(self.pins_img, 270)
            self.image = pygame.transform.rotate(self.image, 270)
            self.dir = vec(-1, 0)
            self.rect = self.image.get_rect()
            self.surf_pos = (x, y)
            self.rect.topright = self.surf_pos
            self.dir_sign = -1
            self.pin_rect = self.pins_img.get_rect()
            self.pins_pos = (0, 0)
            self.hit_rect = pygame.Rect(self.surf_pos[0] + self.pins_pos[0], self.surf_pos[1] + self.pins_pos[1], 12, 22)
        else:
            print("ERROR TRAP DIRECTION!")


    def update(self):
        if self.dir.x == 1:
            offset = self.range * (self.tween(self.step / self.range) - 0.5)
            self.pin_rect.centerx = offset * self.dir_sign
            self.hit_rect.centerx = self.surf_pos[0] + self.pin_rect.centerx
            self.step += self.speed
            self.image.fill((255,255,255,0))
            self.image.blit(self.pins_img,(self.pin_rect.topleft))
            if self.step > self.range:
                self.step = 0
                self.dir_sign *= -1
        if self.dir.x == -1:
            offset = self.range * (self.tween(self.step / self.range) - 0.5)
            self.pin_rect.centerx = offset * self.dir_sign
            self.hit_rect.centerx = self.surf_pos[0] + self.pin_rect.centerx
            self.step += self.speed
            self.image.fill((255, 255, 255, 0))
            self.image.blit(self.pins_img, (self.pin_rect.topright))
            if self.step > self.range:
                self.step = 0
                self.dir_sign *= -1
        if self.dir.y == 1:
            offset = self.range * (self.tween(self.step / self.range) - 0.5)
            self.pin_rect.centery = offset * self.dir_sign
            self.hit_rect.centery = self.surf_pos[1] + self.pin_rect.centery
            self.step += self.speed
            self.image.fill((255, 255, 255, 0))
            self.image.blit(self.pins_img, (self.pin_rect.bottomleft))
            if self.step > self.range:
                self.step = 0
                self.dir_sign *= -1
        if self.dir.y == -1:
            offset = self.range * (self.tween(self.step / self.range) - 0.5)
            self.pin_rect.centery = offset * self.dir_sign
            self.hit_rect.centery = self.surf_pos[1] + self.pin_rect.centery
            self.step += self.speed
            self.image.fill((255, 255, 255, 0))
            self.image.blit(self.pins_img, (self.pin_rect.topleft))
            if self.step > self.range:
                self.step = 0
                self.dir_sign *= -1


class Torch(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = DECORATION_OVER_LAYER
        self.groups = game.act_lvl.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.images = torch_animation_images
        self.image = pygame.Surface((TILE_SIZE,TILE_SIZE),pygame.HWSURFACE | pygame.SRCALPHA)
        self.image.blit(torch1_img,(0,0))
        self.pos = (x, y)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hit_rect = self.rect
        self.animation_time = 0
        self.last_animation_time = 0

    def update(self):
        self.animation_time += self.game.dt
        rand_time = random.randint(2,8)
        rand_time *= 0.01
        #print (str(self.game.dt))
        #print (str(self.animation_time))
        if self.animation_time - self.last_animation_time - rand_time > 0.1:
            #print ("Change animation frame)")
            anim_img = random.choice(self.images)
            self.image.fill((0,0,0,0))
            self.image.blit(anim_img,(0,0))
            self.last_animation_time = self.animation_time


class Animated_Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, x, y, name):
        self._layer = DECORATION_OVER_LAYER
        self.groups = game.act_lvl.all_sprites, game.act_lvl.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.HWSURFACE | pygame.SRCALPHA)
        if name == "fountain":
            self.images = fountain_animation_images
            self.image.blit(fountain1_img,(0,0))
        self.pos = (x, y)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hit_rect = self.rect
        self.animation_time = 0
        self.last_animation_time = 0
        self.water = False

    def update(self):
        self.animation_time += self.game.dt
        rand_time = random.randint(2,8)
        rand_time *= 0.01
        #print (str(self.game.dt))
        #print (str(self.animation_time))
        if self.animation_time - self.last_animation_time - rand_time > 0.1:
            #print ("Change animation frame)")
            anim_img = random.choice(self.images)
            self.image.fill((0,0,0,0))
            self.image.blit(anim_img,(0,0))
            self.last_animation_time = self.animation_time




