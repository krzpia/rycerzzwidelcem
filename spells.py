import ui
from data import *
import math
import copy
import random

class SpellGenerator:
    def __init__(self):
        self.firebolt = ui.Spell("Firebolt", sb_firebolt_image, bullet_firebolt_image, False,
                              "offensive", "fire", 2,2, 10, 1000, "arrow", 1, 300, 180,
                              False, False, False, False, False, False, False, firebolt_snd)
        self.fireball = ui.Spell("Fireball", sb_fireball_image, bullet_fireball_image, fireball_animation_images,
                              "offensive", "fire", 4, 4, 12, 1000, "arrow", 1, 275, 150,
                              True, 15, 6, False, False, False, False, firebolt_snd)
        self.icebolt = ui.Spell("Icebolt", sb_icebolt_image, bullet_icebolt_image, False,
                             "offensive", "cold", 1, 2, 5, 800, "arrow", 1, 450, 250,
                             False, False, False, False, False, False, False, icebolt_snd)
        self.tricebolt = ui.Spell("Tricebolt", sb_tricebolt_image, bullet_icebolt_image, False,
                               "offensive", "cold", 3, 3, 5, 900, "arrow", 3, 450, 175,
                               False, False, False, False, False, False, False, icebolt_snd)
        self.poisoncloud = ui.Spell("Poison Cloud", sb_poisoncloud_image, bullet_poison_image,
                                 poisoncloud_animation_images,
                                 "offensive", "poison cloud", 8, 4, 0, 2500, "arrow", 1, 75, 100,
                                 True, False, 1, 5, False, False, False, firebolt_snd)
        self.freeze = ui.Spell("Freeze", sb_freeze_image, bullet_icebolt_image, False,
                            "offensive", "cold", 6,4, 5, 2000, "arrow", 1, 375, 175,
                            False, False, False, False, 5, False, False, icebolt_snd)
        self.cure = ui.Spell("Cure", sb_cure_image, False, False, "defensive", "cure", 4, 2, 10, False,
                          False, False, False, False, False, False, False, False,
                          False, False, False, cure_snd)
        self.stoneskin = ui.Spell("Stone Skin", sb_stoneskin_image, False, False, "defensive",
                               "stone skin", 2, 1, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, stoneskin_snd)
        self.haste = ui.Spell("Haste", sb_haste_image, False,False,"defensive",
                              "haste",3,2,False,False,False,False,False,False,False,False,False,
                              False,False,False,False,haste_snd)
        self.invisibility = ui.Spell("Invisibility",sb_invisibility_image,False,False,"defensive",
                                     "invisibility",6,4,False,False,False,False,False,False,False,False,False,
                              False,False,False,False,cure_snd)
        self.ironskin = ui.Spell("Iron Skin", sb_ironskin_image, False, False, "defensive",
                                     "iron skin", 4, 4, False, False, False, False, False, False, False, False,
                                     False,
                                     False, False, False, False, stoneskin_snd)
        self.heroism = ui.Spell("Heroism",sb_heroism_image,False,False,"defensive","heroism",2,1,False,False,False,
                                False,False,False,False,False,False,False,False,False,False,haste_snd)
        self.spells = [self.firebolt, self.fireball,self.icebolt,self.tricebolt,self.poisoncloud,
                       self.freeze,self.cure,self.stoneskin,self.haste, self.invisibility, self.ironskin,
                       self.heroism]

    def get_spell_by_name(self, name):
        for spell in self.spells:
            if spell.name == name:
                return spell

    def get_random_spell(self):
        return random.choice(self.spells)

