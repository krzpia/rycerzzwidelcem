import sprites
import ui
import sys
from os import path
import csv
from data import *
from events.event import Event

if getattr(sys, 'frozen', False): # PyInstaller adds this attribute
    # Running in a bundle
    CurrentPath = sys._MEIPASS
else:
    # Running in normal Python environment
    CurrentPath = path.dirname(__file__)

game_folder = CurrentPath
dialog_folder = path.join(game_folder, 'dialog')

class QuestGenerator:
    def __init__(self,game):
        self.game = game
        self.q_holy_grail = ui.Quest(self.game,"Holy Grail", "Find and bring a Holy Grail",
                                     1, [], ["Holy Grail"],True, [], [], 10, 50)
        self.q_holy_grail.put_image_from_tileset(23,94,full_tileset_image)
        self.q_killer_bees = ui.Quest(self.game,"Killer Bees","Kill 3 giant bees from the John`s filed",
                                      1,["Killer Bee", "Killer Bee", "Killer Bee"],[],False,[],[],15,10)
        self.q_killer_bees.put_image_from_tileset(5,65,full_tileset_image)
        self.q_miraflorida = ui.Quest(self.game,"Miraflorida","Find castle of Miraflorida",1,[],[],False,[],["George the Guard"],6,0)
        self.q_miraflorida.set_to_autochecking()
        self.q_miraflorida.put_image_from_tileset(0,60,full_tileset_image)
        self.q_open_the_gates = ui.Quest(self.game,"Open the Gates","Help the druid and find ingriedients",1,[],["Sunset Flower","Mad Bat Wing", "Gremlin Tooth"],False,[],[],20,0,"Miraflorida Magic Key")
        self.q_open_the_gates.put_image_from_tileset(32,94,full_tileset_image)
        self.q_karol_the_alchemist = ui.Quest(self.game,"Karol the Alchemist","Find Karol and bring ingriedients",1,[],["Sunset Flower","Mad Bat Wing", "Gremlin Tooth"],True,[],[],25,0,"Elixir Arechinix")
        self.q_karol_the_alchemist.put_image_from_tileset(1, 59, full_tileset_image)
        self.q_speak_with_the_king = ui.Quest(self.game,"Speak with the King","Find King Sancho and bring the elixir",1,[],["Elixir Arechinix"],True,[],[],25,50,False)
        self.q_speak_with_the_king.put_image_from_tileset(23, 76, full_tileset_image)

        ### SPECIAL FACTORS - auto next quest
        self.q_open_the_gates.put_auto_next_quest(self.q_karol_the_alchemist)
        self.q_karol_the_alchemist.put_auto_next_quest(self.q_speak_with_the_king)

        ### END........
        ### ALL QUESTS IN LIST
        self.quests = [self.q_holy_grail, self.q_killer_bees, self.q_miraflorida,
                       self.q_open_the_gates, self.q_karol_the_alchemist, self.q_speak_with_the_king]

    def return_quest_by_name(self, name):
        for quest in self.quests:
            if quest.name == name:
                return quest

class NpcGenerator:
    def __init__(self, game,tileset1, tileset2):
        self.game = game
        self.tileset = tileset1
        self.f_set = tileset2
        self.quest_gen = QuestGenerator(self.game)
        ##### DIALOGS
        self.gold_crusader_csv = csv.DictReader(open(path.join(dialog_folder, 'gold_crusader_dialog.csv')),delimiter=';')
        self.blue_gnom_csv = csv.DictReader(open(path.join(dialog_folder,'blue_gnom_dialog.csv')),delimiter=';')
        self.john_the_farmer_csv = csv.DictReader(open(path.join(dialog_folder, 'john_the_farmer_dialog.csv')), delimiter=';')
        self.george_the_guard_csv = csv.DictReader(open(path.join(dialog_folder,'george_the_guard_dialog.csv')),delimiter=';')
        self.eveandro_the_druid_csv = csv.DictReader(open(path.join(dialog_folder,'eveandro_the_druid_dialog.csv')),delimiter=';')
        self.king_sancho_csv = csv.DictReader(open(path.join(dialog_folder,'king_sancho_dialog.csv')),delimiter=';')
        self.karol_the_alchemist_csv = csv.DictReader(open(path.join(dialog_folder, 'karol_the_alchemist_dialog.csv')), delimiter=';')
        #############

    def generate(self, name, x, y, image):
        if name == "Gold Crusader":
            gold_crusader = sprites.Npc(self.game,name,x,y,image)
            gold_crusader.dialog_data.load_from_dict(self.gold_crusader_csv,self.quest_gen)
            return gold_crusader

        if name == "Blue Gnom":
            blue_gnom = sprites.Npc(self.game,name,x,y,image)
            blue_gnom.dialog_data.load_from_dict(self.blue_gnom_csv, self.quest_gen)
            blue_gnom.dialog_data.thread_block_with_event("intro blue gnom",['thread intro blue gnom has been read'])
            return blue_gnom

        if name == "John the Farmer":
            john_the_farmer = sprites.Npc(self.game,name,x,y,image)
            john_the_farmer.dialog_data.load_from_dict(self.john_the_farmer_csv, self.quest_gen)
            return john_the_farmer

        if name == "Piggy":
            piggy = sprites.Npc(self.game,name,x,y,image)
            piggy.dialog_data.load_text(True,"welcome",0,0,"Oink, oink",False,False,False,False,False,False,False)
            piggy.put_sound(oink_snd)
            return piggy

        if name == "George the Guard":
            george_the_guard = sprites.Npc(self.game,name,x,y,image)
            george_the_guard.dialog_data.load_from_dict(self.george_the_guard_csv,self.quest_gen)
            george_the_guard.dialog_data.thread_unblock_with_event("pass",['King Sancho has been encountered'])
            george_the_guard.dialog_data.thread_block_with_event("quest Miraflorida",['King Sancho has been encountered'])
            return george_the_guard

        if name == "Eveandro the Druid":
            eveandro_the_druid = sprites.Npc(self.game,name,x,y,image)
            eveandro_the_druid.dialog_data.load_from_dict(self.eveandro_the_druid_csv,self.quest_gen)
            eveandro_the_druid.dialog_data.thread_unblock_with_event("quest Open the Gates", ['quest Miraflorida has been completed'])
            eveandro_the_druid.dialog_data.thread_block_with_event("intro void",['quest Miraflorida has been completed'])
            eveandro_the_druid.dialog_data.thread_unblock_with_event("intro eveandro",['quest Miraflorida has been completed'])
            eveandro_the_druid.dialog_data.thread_block_with_event("bye",['got quest Open the Gates'])
            eveandro_the_druid.dialog_data.thread_block_with_event("intro eveandro",['got quest Open the Gates'])
            eveandro_the_druid.dialog_data.thread_block_with_event("quest Open the Gates", ['quest Speak with the King has been completed'])
            eveandro_the_druid.dialog_data.thread_unblock_with_event("cure",['quest Speak with the King has been completed'])
            return eveandro_the_druid

        if name == "King Sancho":
            king_sancho = sprites.Npc(self.game,name,x,y,image)
            king_sancho.dialog_data.load_from_dict(self.king_sancho_csv,self.quest_gen)
            king_sancho.dialog_data.thread_unblock_with_event("quest Speak with the King",['got quest Speak with the King'])
            king_sancho.dialog_data.thread_block_with_event("ill",['quest Karol the Alchemist has been completed'])
            return king_sancho

        if name == "King`s Guard":
            kings_guard = sprites.Npc(self.game,name,x,y,image)
            kings_guard.dialog_data.load_text(True,"welcome",0,0,"Step off, adventurer!",False,False,False,False,False,False,False)
            return kings_guard

        if name == "Karol the Alchemist":
            karol_the_alchemist = sprites.Npc(self.game,name,x,y,image)
            karol_the_alchemist.dialog_data.load_from_dict(self.karol_the_alchemist_csv,self.quest_gen)
            karol_the_alchemist.dialog_data.thread_unblock_with_event("quest Karol the Alchemist",['got quest Karol the Alchemist'])
            karol_the_alchemist.dialog_data.thread_block_with_event("intro void",['got quest Karol the Alchemist'])
            return karol_the_alchemist