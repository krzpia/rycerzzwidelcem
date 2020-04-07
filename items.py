import pygame
import random
import sprites
import math
import copy


class ItemGenerator:
    def __init__(self, game, tileset1, tileset2):
        self.game = game
        self.tileset = tileset1
        self.f_set = tileset2
        self.weapons = []
        self.armors = []
        self.potions = []
        self.rings = []
        self.arrows = []
        self.books = []
        self.q_items = []

        ######## QUEST ITEMS #######
        self.q_items.append(sprites.Quest_Item(self.game,"Holy Grail",0,23,94))
        self.q_items.append(sprites.Quest_Item(self.game,"Mad Bat Wing",0,33,94))
        self.q_items.append(sprites.Quest_Item(self.game, "Gremlin Tooth", 0, 34, 94))
        self.q_items.append(sprites.Quest_Item(self.game, "Sunset Flower", 0, 35, 94))
        self.q_items.append(sprites.Quest_Item(self.game, "Elixir Arechinix",0,61,41))
        self.q_items.append(sprites.Quest_Item(self.game, "Golden Mask",0,35,95))
        self.q_items.append(sprites.Quest_Item(self.game, "Mieszko Family Signet",100,17,43))
        self.q_items.append(sprites.Weapon(self.game,"Wilfredo`s Lasso","weapon","blunt",5,False,5,550,"big",
                                           0,0,0,0,0,0,50,48,44,35,90))

        ######## WEAPONS ###########
        self.weapons.append(sprites.Weapon(self.game, "Wooden Club", "weapon","blunt",
                                                     10, False, 2, 850, "medium",
                                                     0,0,0,0,0,0,25,55, 44, 35, 87))
        self.weapons.append(sprites.Weapon(self.game, "Small Sword","weapon","sword",
                                           10,False,2,625,"small",
                                           0,0,0,0,0,0,50,4,45,52,89))
        self.weapons.append(sprites.Weapon(self.game, "Short Hammer", "weapon", "blunt",
                                           15, False, 5, 1250, "small",
                                           0, 0, 0, 0, 0, 0,75, 37, 46, 37, 88))
        self.weapons.append(sprites.Weapon(self.game, "Knife", "weapon","dagger",
                                           15, False, 1, 500, "small",
                                           0, 0, 0, 0, 0, 0,40, 2, 45, 42, 87))
        self.weapons.append(sprites.Weapon(self.game, "Spiked Club", "weapon","blunt",
                                           15, False, 4, 850, "medium",
                                           0, 0, 0, 0, 0, 0,25, 58, 45, 14, 88))
        self.weapons.append(sprites.Weapon(self.game,"Wood Staff","weapon","staff",
                                           15,False,2,700,"big",
                                           0,0,0,0,0,0,25,3,47,10,89))
        self.weapons.append(sprites.Weapon(self.game, "Machete", "weapon", "sword",
                                           20, False, 4, 725, "medium",
                                           0, 0, 0, 0, 0, 0,45, 36, 45, 56, 87))
        self.weapons.append(sprites.Weapon(self.game, "Hard Wood Staff", "weapon", "staff",
                                           20, False, 3, 700, "big",
                                           0, 0, 0, 0, 0, 0,35, 2, 47, 10, 89))
        self.weapons.append(sprites.Weapon(self.game, "Iron Mace", "weapon", "blunt",
                                           25, False, 4, 800, "medium",
                                           0, 0, 0, 0, 0, 0,60, 50, 46, 2, 89))
        self.weapons.append(sprites.Weapon(self.game, "Iron Dagger", "weapon","dagger",
                                                     25, False, 2, 500, "small",
                                                     0, 0, 0, 0, 0, 0,50,5,45,42,87))
        self.weapons.append(sprites.Weapon(self.game, "Short Sword", "weapon","sword",
                                                     25, False,3, 625,"small",
                                                     0, 0, 0, 0, 0, 0,55,63,46,52,89))
        self.weapons.append(sprites.Weapon(self.game, "Wooden Spear", "weapon","spear",
                                           30, False, 5, 900, "big",
                                           0, 0, 0, 0, 0, 0,30, 27, 47, 56, 89))
        self.weapons.append(sprites.Weapon(self.game, "Wood Axe", "weapon","axe",
                                           35, False, 6, 750, "medium",
                                           0, 0, 0, 0, 0, 0,45, 52, 47, 32, 90))
        self.weapons.append(sprites.Weapon(self.game,"Short Saber","weapon","sword",
                                           35,False,3,600,"small",
                                           0,0,0,0,0,0,45,5,47,38,89))
        self.weapons.append(sprites.Weapon(self.game, "Trident", "weapon","spear",
                                           35, False, 5, 900, "big",
                                           0, 0, 0, 0, 0, 0,50, 43, 47, 7, 89))
        self.weapons.append(sprites.Weapon(self.game, "Scythe", "weapon","spear",
                                           40, False, 7, 1000, "big",
                                           0, 0, 0, 0, 0, 0,40, 14, 47, 46, 89))
        self.weapons.append(sprites.Weapon(self.game, "Steel Dagger", "weapon","dagger",
                                           45, False, 3, 500, "small",
                                           0, 0, 0, 0, 0, 0, 55,17, 45, 43, 87))
        self.weapons.append(sprites.Weapon(self.game, "Iron Sword", "weapon","sword",
                                           50, False, 4, 625, "small",
                                           0, 0, 0, 0, 0, 0,60, 22, 47, 52, 89))
        self.weapons.append(sprites.Weapon(self.game, "Halaberd", "weapon","spear",
                                           60, False, 7, 950, "big",
                                           0, 0, 0, 0, 0, 0,50, 27, 44, 19, 88))
        self.weapons.append(sprites.Weapon(self.game, "Apprentice Staff", "weapon", "staff",
                                           65, False, 4, 700, "big",
                                           0, 0, 0, 0, 0, 0,40, 0, 47, 11, 89))
        self.weapons.append(sprites.Weapon(self.game, "Wood Bow", "weapon","bow",
                                           75, True, 3, 1250, False,
                                           0, 0, 0, 0, 0, 0,25, 38, 49, 26, 87))
        self.weapons.append(sprites.Weapon(self.game, "Saber", "weapon","sword",
                                           75, False, 4, 625,"small",
                                           0, 0, 0, 0, 0, 0,45,8,47,38,89))
        self.weapons.append(sprites.Weapon(self.game, "Sharp Axe", "weapon", "axe",
                                           80, False, 6, 750, "medium",
                                           0, 0, 0, 0, 0, 0, 50,39,44,23,88))
        self.weapons.append(sprites.Weapon(self.game,"Iron Flail","weapon","blunt",
                                           85,False,8,1000,"big",
                                           0,0,0,0,0,0,65,37,47,1,88))
        self.weapons.append(sprites.Weapon(self.game, "Scimitair", "weapon","sword",
                                           100, False, 5, 550, "small",
                                           0, 0, 0, 0, 0, 0,50,10,47,42,89))
        self.weapons.append(sprites.Weapon(self.game,"Double Axe", "weapon","axe",
                                           120,False,9,725,"medium",
                                           0,0,0,0,0,0,60,31,44,10,87))
        self.weapons.append(sprites.Weapon(self.game, "Hunter`s Bow", "weapon", "bow",
                                           135, True, 4, 1200, False,
                                           0, 0, 0, 0, 0, 0, 45,32,49, 26, 87))
        self.weapons.append(sprites.Weapon(self.game, "Obsidian Spear", "weapon", "spear",
                                           150, False, 10, 900, "big",
                                           0, 0, 0, 0, 0, 0,65, 30,47,57,89))
        self.weapons.append(sprites.Weapon(self.game, "Dwarf Axe", "weapon", "axe",
                                           160, False, 8, 750, "medium",
                                           0, 0, 0, 0, 0, 0,85, 42, 44, 23, 88))
        self.weapons.append(sprites.Weapon(self.game, "Royal Saber", "weapon","sword",
                                          175, False, 7, 625, "small",
                                          0, 0, 0, 0, 0, 0,55, 9, 47, 57, 88))
        self.weapons.append(sprites.Weapon(self.game, "Golden Mace", "weapon", "blunt",
                                           175, False, 10, 800, "medium",
                                           0, 0, 0, 0, 0, 0,95, 53, 46, 1, 89))
        self.weapons.append(sprites.Weapon(self.game, "Broad Sword", "weapon", "sword",
                                           185, False, 8, 700, "medium",
                                           0, 0, 0, 0, 0, 0,80, 30, 46, 28, 88))
        self.weapons.append(sprites.Weapon(self.game, "Royal Scimitair", "weapon","sword",
                                           190, False, 6, 550,"small",
                                           0, 0, 0, 0, 0, 0,60,11,47,41,89))
        self.weapons.append(sprites.Weapon(self.game, "Golden Flail", "weapon", "blunt",
                                           200, False, 10, 1000, "big",
                                           0, 0, 0, 0, 0, 0, 90,39,47, 2, 88))
        self.weapons.append(sprites.Weapon(self.game, "Golden Dwarf Axe", "weapon", "axe",
                                           220, False, 10, 750, "medium",
                                           0, 0, 0, 0, 0, 0,95, 43, 44, 23, 88))
        self.weapons.append(sprites.Weapon(self.game, "Oriental Mace", "weapon", "blunt",
                                           220, False, 7, 875, "medium",
                                           0, 0, 0, 2, 0, 0, 70,49,46,54,87))
        self.weapons.append(sprites.Weapon(self.game, "Sapphire Sword", "weapon", "sword",
                                           250, False, 9, 700, "medium",
                                           0, 1, 0, 0, 0, 0,80, 33,46,17,91))
        self.weapons.append(sprites.Weapon(self.game, "Composite Bow", "weapon", "bow",
                                           275, True, 6, 1180, False,
                                           0, 0, 0, 0, 0, 0,65, 33, 49, 27, 87))
        self.weapons.append(sprites.Weapon(self.game, "Obsidian Dagger", "weapon", "dagger",
                                           300, False, 5, 500, "small",
                                           0, 0, 0, 0, 1, 0,90, 21,47,49,89))
        self.weapons.append(sprites.Weapon(self.game, "Sapphire Spear", "weapon", "spear",
                                           350, False, 12, 900, "big",
                                           0, 1, 0, 0, 0, 0,80, 38,48,52,90))
        self.weapons.append(sprites.Weapon(self.game, "Devil`s Flail", "weapon", "blunt",
                                           380, False, 12, 1000, "big",
                                           1, 0, 0, 0, 0, 0,90, 11, 45, 2, 88))
        self.weapons.append(sprites.Weapon(self.game, "Devil`s Sword", "weapon", "sword",
                                           400, False, 9, 575, "medium",
                                           1, 0, 0, 0, 0, 0,80,  15, 48, 44, 90))
        self.weapons.append(sprites.Weapon(self.game, "Neptun Spear", "weapon", "spear",
                                           420, False, 14, 900, "big",
                                           0, 2, 0, 0, 0, 0,85, 49, 47, 31, 90))
        self.weapons.append(sprites.Weapon(self.game, "Giant`s Hammer", "weapon", "blunt",
                                           450, False, 24, 1175, "medium",
                                           2, 2, 0, 0, 0, 0,99,58,47,36,88))
        self.weapons.append(sprites.Weapon(self.game, "Jade Bow", "weapon", "bow",
                                           475, True, 9, 1175, False,
                                           0, 0, 0, 0, 0, 0,80, 40,49, 29, 87))
        self.weapons.append(sprites.Weapon(self.game, "Alladin`s Falcon", "weapon", "sword",
                                           500, False, 10, 570, "medium",
                                           0, 0, 2, 0, 0, 0,95, 47, 48, 63, 90))

        #### ARMORS ###########
        self.armors.append(sprites.Armor(self.game,"Leather Cloak", "armor","robe",
                                         10,4,1,0,0,0,0,0,0,40,9,36,60,81))
        self.armors.append(sprites.Armor(self.game,"Apprentice Robe", "armor","robe",
                                         12,2,1,0,0,1,0,0,0,55,24,38,12,82))
        self.armors.append(sprites.Armor(self.game, "Leather Armor", "armor","leather",
                                         16, 6, 1, 0, 0, 0, 0, 0, 0,50, 0, 38, 23, 82))
        self.armors.append(sprites.Armor(self.game, "Hard Leather Armor", "armor","leather",
                                         20, 8, 1.025, 0, 0, 0, 0, 0, 0,65, 1, 38, 23, 82))
        self.armors.append(sprites.Armor(self.game,"Light Scale Armor","armor","chain",
                                         25,10,1.1,0,0,0,0,0,0,45,22,38,23,82))
        self.armors.append(sprites.Armor(self.game,"Spiked Leather Armor", "armor","leather",
                                         30,10,1.05,0,0,0,0,0,0,60,45,38,39,82))
        self.armors.append(sprites.Armor(self.game, "Hard Spiked Armor", "armor","leather",
                                         35, 12, 1.1, 0, 0, 0, 0, 0, 0,75, 46, 38, 39, 82))
        self.armors.append(sprites.Armor(self.game, "Scale Armor", "armor","chain",
                                         40, 16, 1.25, 0, 0, 0, 0, 0, 0,60, 7, 38, 27, 83))
        self.armors.append(sprites.Armor(self.game, "Iron Plate Armor", "armor","plate",
                                         50, 20, 1.5, 0, 0, 0, 0, 0, 0,85, 14,38,53,82))
        self.armors.append(sprites.Armor(self.game, "Imperial Leather Armor", "armor","leather",
                                         60, 10, 1, 0, 0, 0, 0, 0, 0,60, 2, 38, 23, 82))
        self.armors.append(sprites.Armor(self.game, "Thief Leather Armor", "armor","leather",
                                         60, 8, 1, 0, 0, 0, 0, 1, 0,50, 8, 38, 24, 82))
        self.armors.append(sprites.Armor(self.game, "Heavy Plate Armor", "armor","plate",
                                         65, 24, 1.6, 0, 0, 0, 0, 0, 0,90, 15, 38, 53, 82))
        self.armors.append(sprites.Armor(self.game,"Dryad`s Armor", "armor","robe",
                                         70,12,1,0,0,2,0,0,0,70,53,38,44,83))
        self.armors.append(sprites.Armor(self.game, "Steel Plate Armor", "armor","plate",
                                         75, 25, 1.4, 0, 0, 0, 0, 0, 0,125, 16, 38, 53, 82))
        self.armors.append(sprites.Armor(self.game, "Spiked Plate Armor", "armor","plate",
                                         85,30,1.66,1,0,0,0,0,0,100,10,38,57,82))
        self.armors.append(sprites.Armor(self.game,"Imperial Scale Armor","armor","chain",
                                         100,20,1.25,0,0,0,0,0,0,75,21,38,28,82))
        self.armors.append(sprites.Armor(self.game,"Mithril Armor", "armor","chain",
                                         150,25,1,0,0,0,0,0,2,50,33,38,27,83))
        self.armors.append(sprites.Armor(self.game,"Royal Armor", "armor","chain",
                                         225,28,1.1,0,0,0,1,0,0,90,35,38,53,81))
        self.armors.append(sprites.Armor(self.game,"Wizard`s Robe", "armor","robe",
                                         275,5,1,0,0,4,4,0,0,35,30,38,0,83))
        self.armors.append(sprites.Armor(self.game,"Dragon Lava Heavy Armor","armor","plate",
                                         500,50,1.66,2,2,0,0,0,0,150,39,38,50,82))



        ### SHIELDS
        self.armors.append(sprites.Armor(self.game, "Wooden Shield", "shield","wood",
                                         10, 4, 1, 0, 0, 0, 0, 0, 0,20, 5,37,38,85))
        self.armors.append(sprites.Armor(self.game, "Iron Round Shield", "shield","iron",
                                         12, 8, 1.05, 0, 0, 0, 0, 0, 0, 60,11, 37, 16, 86))
        self.armors.append(sprites.Armor(self.game, "Round Shield", "shield","wood",
                                         15, 6, 1 ,0,0,0,0,0,0,50,29,37,21,86))
        self.armors.append(sprites.Armor(self.game, "Cavalry Shield","shield","iron",
                                         20, 9,1.05,0,0,0,0,0,0,60,33,37,57,85))
        self.armors.append(sprites.Armor(self.game, "Scull Round Shield", "shield","iron",
                                         55, 10, 1, 0, 0, 0, 0, 0, 0,75, 31,37,26,86))
        self.armors.append(sprites.Armor(self.game, "Tower Shield", "shield","iron",
                                         60, 16, 1.2, 0, 0, 0, 0, 0, 0,85, 17, 37, 53, 85))
        self.armors.append(sprites.Armor(self.game, "Hoplite Shiled", "shield", "iron",
                                         80, 12, 1, 0, 0, 0, 0, 0, 0,65, 7, 37, 46, 85))
        self.armors.append(sprites.Armor(self.game, "Phalanx Shield", "shield", "iron",
                                         90, 20, 1.25, 0, 0, 0, 0, 0, 0,75, 15, 37, 49, 85))
        self.armors.append(sprites.Armor(self.game, "Orc Shiled", "shield", "leather",
                                         100, 10, 1, 1, 0, 0, 0, 0, 0,50, 30,37, 27,86))
        self.armors.append(sprites.Armor(self.game, "Dragon Shiled", "shield", "iron",
                                         150, 20, 1.1, 0, 0, 0, 0, 0, 0,90, 25, 37, 45, 85))
        self.armors.append(sprites.Armor(self.game, "High Moon Shield", "shield", "iron",
                                         200, 24, 1.1, 0, 0, 1, 1, 0, 0,65, 21, 37, 4, 86))
        self.armors.append(sprites.Armor(self.game, "Royal Shield", "shield", "iron",
                                         225, 26, 1.15, 1, 1, 0, 0, 0, 0,80, 19, 37, 47, 85))



        ### BOOTS
        self.armors.append(sprites.Armor(self.game, "Pilgrim Sandals", "boots", "robe",
                                         8, 1, 1, 0, 0, 0, 0, 0, 0,50, 24, 36, 53, 83))
        self.armors.append(sprites.Armor(self.game, "Leather Boots", "boots", "leather",
                                         10, 2, 1, 0, 0, 0, 0, 0, 0,40, 22, 36, 59, 83))
        self.armors.append(sprites.Armor(self.game, "Fur Boots", "boots", "leather",
                                         15, 3, 1, 0, 0, 0, 0, 0, 0,35, 23, 36, 59, 83))
        self.armors.append(sprites.Armor(self.game, "Hard Leather Boots", "boots","leather",
                                         20, 4, 1, 0, 0, 0, 0, 0, 0,60, 21,36,59,83))
        self.armors.append(sprites.Armor(self.game, "Elf Boots", "boots", "leather",
                                         45, 6, 1, 0, 0, 0, 0, 0, 0,50, 26,36,62,83))
        self.armors.append(sprites.Armor(self.game, "Plate Boots", "boots", "plate",
                                         55, 12, 1.2, 0, 0, 0, 0, 0, 0,90, 27,36,0,84))
        self.armors.append(sprites.Armor(self.game, "Chain Boots", "boots", "chain",
                                         75, 10, 1.05, 0, 0, 0, 0, 0, 0,70, 28,36,0,84))


        ### HATS
        self.armors.append(sprites.Armor(self.game, "Leather Hat", "helmet","leather",
                                         8, 2, 1, 0, 0, 0, 0, 0, 0,20, 45,36,17,93))
        self.armors.append(sprites.Armor(self.game, "Fur Cap", "helmet", "leather",
                                         15, 4, 1, 0, 0, 0, 0, 0, 0,20, 40,36,4,92))
        self.armors.append(sprites.Armor(self.game, "Red Hood", "helmet", "leather",
                                         12, 3, 1, 0, 0, 0, 0, 0, 0,35, 41,36,61,92))
        self.armors.append(sprites.Armor(self.game, "Gladiator Helm", "helmet", "plate",
                                         25, 8, 1.15, 0, 0, 0, 0, 0, 0,90, 50,36,59,92))
        self.armors.append(sprites.Armor(self.game, "Mameluk Helm", "helmet", "chain",
                                         45, 6, 1.05, 0, 0, 0, 0, 0, 0,35, 1,37,7,92))
        self.armors.append(sprites.Armor(self.game, "Chain Hood", "helmet", "chain",
                                         60, 8, 1.05, 0, 0, 0, 0, 0, 0,40, 46,36,60,92))
        self.armors.append(sprites.Armor(self.game, "Wizard`s Hat", "helmet", "robe",
                                         70, 2, 1, 0, 0, 1, 1, 0, 0,25, 48, 36, 15, 93))
        self.armors.append(sprites.Armor(self.game, "Knight Helmet", "helmet", "plate",
                                         80, 12, 1.2, 0, 0, 0, 0, 0, 0,90, 58,36,39,92))
        self.armors.append(sprites.Armor(self.game, "Templar Helmet", "helmet", "plate",
                                         125, 14, 1.1, 0, 0, 0, 0, 0, 0,100, 56, 36, 57, 92))
        self.armors.append(sprites.Armor(self.game, "Devil`s Helmet", "helmet", "plate",
                                         205, 20, 1.05, 1, 0, 0, 0, 0, 0, 125,59, 36, 52, 92))

        #### POTIONS ###########
        self.potions.append(sprites.Potion(self.game, "Red Potion", "Cure",15,30,26,42))
        self.potions.append(sprites.Potion(self.game, "Small Red Potion", "Cure",5,15,24,42))
        self.potions.append(sprites.Potion(self.game, "Blue Potion", "Mana",15,30,58,41))
        self.potions.append(sprites.Potion(self.game, "Small Blue Potion", "Mana", 5, 15, 23, 42))

        #### ARROWS
        self.arrows.append(sprites.Arrow_Item(self.game,"Arrows",5,5))
        self.arrows.append(sprites.Arrow_Item(self.game,"Arrows",10,10))
        self.arrows.append(sprites.Arrow_Item(self.game,"Arrows",25,25))

        #### BOOKS ######
        self.books.append(sprites.Book(self.game,"Firebolt",100,2,40,39))
        self.books.append(sprites.Book(self.game, "Fireball", 250,4, 41, 39))
        self.books.append(sprites.Book(self.game, "Icebolt", 160,2, 15,39))
        self.books.append(sprites.Book(self.game, "Tricebolt", 225,3, 3, 39))
        self.books.append(sprites.Book(self.game, "Freeze", 200,5, 0, 39))
        self.books.append(sprites.Book(self.game, "Cure", 175,3, 12, 39))
        self.books.append(sprites.Book(self.game, "Poison Cloud", 290,4, 63, 39))
        self.books.append(sprites.Book(self.game, "Stone Skin", 120,1, 55,38))
        self.books.append(sprites.Book(self.game, "Haste", 100, 3, 49, 39))
        self.books.append(sprites.Book(self.game, "Invisibility", 325, 4, 47,39))
        self.books.append(sprites.Book(self.game, "Iron Skin", 175, 2,7, 39))
        self.books.append(sprites.Book(self.game, "Heroism",125,1,56,39))

        #### RINGS #####
        self.rings.append(sprites.Ring(self.game,"Green Ring",100,0,1,0,0,0,0,0,0,0,1,34,42))
        self.rings.append(sprites.Ring(self.game, "Bronze Ring", 100, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 35, 42))
        self.rings.append(sprites.Ring(self.game, "Dryad`s Ring", 180, 0, 0, 0, 0, 0,1, 0, 0, 2,1, 36, 42))
        self.rings.append(sprites.Ring(self.game,"Jasper Ring",125,0,0,0,0,1,0,0,0,0,1,37,42))
        self.rings.append(sprites.Ring(self.game,"Copper Ring",80,0,0,0,0,0,0,4,0,0,1,38,42))
        self.rings.append(sprites.Ring(self.game, "Red Ring", 130, 0, 0, 1, 0, 0, 0, 0, 0,0, 1, 39, 42))
        self.rings.append(sprites.Ring(self.game, "Quartz Ring", 150, 0, 0, 0, 1,0, 0, 0, 0, 0, 1, 40, 42))
        self.rings.append(sprites.Ring(self.game, "Emerald Ring", 200, 0, 0, 0,2, 0, 0, 0, 0,0, 1, 41, 42))
        self.rings.append(sprites.Ring(self.game, "Azure Ring", 240, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 42, 42))
        self.rings.append(sprites.Ring(self.game, "Gold Ring", 250, 2, 0, 0, 0, 0, 0,0, 2, 0, 1, 43, 42))
        self.rings.append(sprites.Ring(self.game, "Sapphire Ring", 220, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0.93, 44, 42))
        self.rings.append(sprites.Ring(self.game, "Jade Ring", 300, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0.91, 45, 42))
        self.rings.append(sprites.Ring(self.game, "Ruby Ring", 320, 1, 1, 0, 0, 0, 0, 0,3, 0, 1, 46, 42))
        self.rings.append(sprites.Ring(self.game, "Platinium Ring", 175, 0, 0, 0, 0, 1, 0, 0, 2, 2, 1, 47, 42))
        self.rings.append(sprites.Ring(self.game, "Iron Ring", 90, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 48, 42))
        self.rings.append(sprites.Ring(self.game, "Pearl Ring", 160, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 52, 42))
        self.rings.append(sprites.Ring(self.game, "Black Ring", 220, 0, 0, 0, 3, 0, 0, 0, 0, 0, 1, 53, 42))
        self.rings.append(sprites.Ring(self.game, "Black Pearl Ring", 300, 0, 0, 0, 5, 0, 0, 0, 0, 0, 1, 56, 42))
        self.rings.append(sprites.Ring(self.game, "Diamond Ring", 220, 0, 2, 0, 0,0, 0, 10, 0, 0, 1, 60, 42))
        self.rings.append(sprites.Ring(self.game, "Blue Ring", 390, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0.86, 63, 42))
        self.rings.append(sprites.Ring(self.game, "Devil`s Ring", 500, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1,11, 43))
        self.rings.append(sprites.Ring(self.game, "Hunter`s Ring", 375, 2, 0, 0, 0, 2, 2, 0, 0, 2, 0.98, 10, 43))
        self.rings.append(sprites.Ring(self.game, "Royal Ring", 400, 3, 3, 0, 0, 0, 0, 0, 0, 0, 1, 7, 43))
        self.rings.append(sprites.Ring(self.game, "Wizard`s Ring", 400, 0, 0, 3, 3, 0, 0, 0, 0, 0, 1, 12, 43))
        self.rings.append(sprites.Ring(self.game, "Giant`s Ring", 240, 5, 5, 0, 0, 0, 0, 0, 0, 0, 1.2, 17, 43))
        self.rings.append(sprites.Ring(self.game, "Arcmage`s Ring", 500, 0, 0, 6, 6, 0, 0, 0, 0, 0, 1, 13, 43))


        #### NECKLACE
        self.rings.append(sprites.Necklace(self.game, "Troll`s Finger", 125, 4, 0, 0, 0, 0, 0, 1, 0, 0, 1.1, 31, 35))
        self.rings.append(sprites.Necklace(self.game,"Red Necklace",160,1, 0, 0, 0, 0, 0, 1, 0, 0, 1,62,34))
        self.rings.append(sprites.Necklace(self.game, "Blue Necklace", 200, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1, 61, 34))
        self.rings.append(sprites.Necklace(self.game, "Yellow Necklace", 200, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 63, 34))
        self.rings.append(sprites.Necklace(self.game, "Green Necklace", 210, 0, 2, 0, 0, 0, 0, 1, 0, 0, 1, 0, 35))
        self.rings.append(sprites.Necklace(self.game, "Red Necklace", 220, 0, 0, 2, 0, 0, 0, 1, 0, 0, 1, 1, 35))
        self.rings.append(sprites.Necklace(self.game, "Rabbit Foot", 325, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0.96, 3, 35))
        self.rings.append(sprites.Necklace(self.game, "Solar Pedant", 425, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.82, 7, 35))
        self.rings.append(sprites.Necklace(self.game, "Amethyst Bat`s Wings", 225, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0.96, 31, 35))

        #### SMITH ITEMS
        self.smith_items = self.weapons + self.armors
        #### MAGIC ITEMS
        self.magic_items = self.potions + self.books + self.rings
        #### ALL ITEMS
        self.all_items = self.weapons + self.armors + self.potions + self.arrows + self.books + self.rings
        #### ALL ITEMS and QUEST ITEMS (for generate by name only)
        self.all_item_and_quest_items = self.all_items + self.q_items

    #def count(self, id, sd):
    #    #### WYLICZA x,y z tilesetu na podstawie ID z TileMap editora
    #    self.x = id % 64
    #    self.y = math.floor(id / 64)
    #    self.sx = sd % 64
    #    self.sy = math.floor(sd / 64)

    def g_key(self, name, key):
        ####################################
        # generuje klucze z nazwy i klucza #
        ####################################
        if name == "Key":
            return sprites.Key(self.game, "Key", key, 55, 40)
        elif name == "Miraflorida Magic Key":
            return sprites.Key(self.game, "Miraflorida Key", 41, 55, 40)
        else:
            print ("ERROR in KEY CREATING")

    def generate_random_item(self, item_type, max_cost = False):
        if item_type == "weapon":
            item_list = self.weapons
        elif item_type == "armor":
            item_list = self.armors
        elif item_type == "smith":
            item_list = self.smith_items
        elif item_type == "potion":
            item_list = self.potions
        elif item_type == "magic":
            item_list = self.magic_items
        elif item_type == "rings":
            item_list = self.rings
        elif item_type == "book":
            item_list = self.books
        elif item_type == "all":
            item_list = self.all_items
        else:
            print("type o item to generate not recognized, proceeding all_items")
            item_list = self.all_items
        if not max_cost:
            return copy.copy(random.choice(item_list))
        else:
            temp_list = []
            for i in item_list:
                if i.cost <= max_cost:
                    temp_list.append(i)
            if len(temp_list) == 0:
                print ("ERROR - EMPTY TEMP LIST!")
            #else:
            #    print ("LIST of " + str(len(temp_list)) + "objects with max cost: "+ str(max_cost))
            return copy.copy(random.choice(temp_list))

    def generate_item_by_name(self, name):
        for i in self.all_item_and_quest_items:
            if i.name == name:
                return copy.copy(i)
        print ("ERROR - NO ITEM of NAME: "+ name)
        return False

    def generate_weapon_by_name(self, name):
        for i in self.weapons:
            if i.name == name:
                return copy.copy(i)
        print ("ERROR - NO ITEM of NAME: "+ name)
        return False

    def generate_armor_by_name(self, name):
        for i in self.armors:
            if i.name == name:
                return copy.copy(i)
        print ("ERROR - NO ITEM of NAME: "+ name)
        return False

    def generate_potion_by_name(self, name):
        for i in self.potions:
            if i.name == name:
                return copy.copy(i)
        print ("ERROR - NO ITEM of NAME: "+ name)
        return False

    def generate_quest_item_by_name(self, name):
        for i in self.q_items:
            if i.name == name:
                return copy.copy(i)
        print ("e NO ITEM of NAME: " + name)
        return False

    def load_item_by_name(self, name, condition = False):
        if name[:3] == "Key":
            print("found a key")
            new_item = self.g_key(name, condition)
            return new_item
        for i in self.all_item_and_quest_items:
            if i.name == name:
                new_item = copy.copy(i)
                if isinstance(new_item, sprites.Armor) or isinstance(new_item, sprites.Weapon):
                    new_item.set_condition(condition)
        return new_item


