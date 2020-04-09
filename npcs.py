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
        self.q_killer_bees = ui.Quest(self.game,"Killer Bees","Kill 3 giant bees             from the John`s filed",1,["Killer Bee", "Killer Bee", "Killer Bee"],[],False,[],[],15,10)
        self.q_killer_bees.put_image_from_tileset(5,65,full_tileset_image)
        self.q_mieszko_ring = ui.Quest(self.game, "Mieszko Family Signet", "Find Mieszko`s father family signet", 1, [],["Mieszko Family Signet"], True, [], [], 12, 120)
        self.q_mieszko_ring.put_image_from_tileset(17, 43, full_tileset_image)
        self.q_mad_cow = ui.Quest(self.game,"Mad Cow","Try to cure the Mad Cow",1,["Mad Bull"],[],False,[],[],10,0,"Wilfredo`s Lasso")
        self.q_mad_cow.put_image_from_tileset(15,63,full_tileset_image)
        self.q_miraflorida = ui.Quest(self.game,"Miraflorida","Find castle of Miraflorida",1,[],[],False,[],["George the Guard"],6,0)
        self.q_miraflorida.set_to_autochecking()
        self.q_miraflorida.put_image_from_tileset(0,60,full_tileset_image)
        self.q_open_the_gates = ui.Quest(self.game,"Open the Gates","Find and bring: Sunset Flower,Mad Bat Wing, Gremlin Tooth",1,[],["Sunset Flower","Mad Bat Wing", "Gremlin Tooth"],False,[],[],20,0,"Miraflorida Magic Key")
        self.q_open_the_gates.put_image_from_tileset(32,94,full_tileset_image)
        self.q_karol_the_alchemist = ui.Quest(self.game,"Karol the Alchemist","Find Karol and bring          him the ingriedients",1,[],["Sunset Flower","Mad Bat Wing", "Gremlin Tooth"],True,[],[],25,0,"Elixir Arechinix")
        self.q_karol_the_alchemist.put_image_from_tileset(1, 59, full_tileset_image)
        self.q_speak_with_the_king = ui.Quest(self.game,"Speak with the King","Find King Sancho and bring    the Arechinix elixir",1,[],["Elixir Arechinix"],True,[],[],25,50,False)
        self.q_speak_with_the_king.put_image_from_tileset(23, 76, full_tileset_image)
        self.q_golden_mask = ui.Quest(self.game,"Golden Mask","Find Golden Mask",1,[],["Golden Mask"],False,[],[],45,100)
        self.q_golden_mask.put_image_from_tileset(36,94,full_tileset_image)

        ### SPECIAL FACTORS - auto next quest
        self.q_open_the_gates.put_auto_next_quest(self.q_karol_the_alchemist)
        self.q_karol_the_alchemist.put_auto_next_quest(self.q_speak_with_the_king)

        ### END........
        ### ALL QUESTS IN LIST
        self.quests = [self.q_holy_grail, self.q_killer_bees, self.q_mieszko_ring, self.q_mad_cow, self.q_miraflorida,
                       self.q_open_the_gates, self.q_karol_the_alchemist, self.q_speak_with_the_king, self.q_golden_mask]

    def return_quest_by_name(self, name):
        for quest in self.quests:
            if quest.name == name:
                return quest

    def return_quest_list_by_name_list(self, name_list):
        print ("QUEST GENERATOR RE-GAINING QUESTS:")
        quest_list = []
        print ("QUEST LIST")
        print (name_list)
        for quest_name in name_list:
            for quest in self.quests:
                if quest_name == quest.name:
                    quest_list.append(quest)
        print (quest_list)
        return quest_list

class NpcGenerator:
    def __init__(self, game,tileset1, tileset2):
        print ("initializing NPC GENERATOR")
        self.game = game
        self.tileset = tileset1
        self.f_set = tileset2
        self.quest_gen = QuestGenerator(self.game)
        ##### DIALOGS
        self.gold_crusader_csv = csv.DictReader(open(path.join(dialog_folder, 'gold_crusader_dialog.csv')),delimiter=';')
        self.blue_gnom_csv = csv.DictReader(open(path.join(dialog_folder,'blue_gnom_dialog.csv')),delimiter=';')
        self.john_the_farmer_csv = csv.DictReader(open(path.join(dialog_folder, 'john_the_farmer_dialog.csv')), delimiter=';')
        self.mieszko_the_knight_csv = csv.DictReader(open(path.join(dialog_folder,'mieszko_the_knight_dialog.csv')), delimiter=';')
        self.george_the_guard_csv = csv.DictReader(open(path.join(dialog_folder,'george_the_guard_dialog.csv')),delimiter=';')
        self.eveandro_the_druid_csv = csv.DictReader(open(path.join(dialog_folder,'eveandro_the_druid_dialog.csv')),delimiter=';')
        self.king_sancho_csv = csv.DictReader(open(path.join(dialog_folder,'king_sancho_dialog.csv')),delimiter=';')
        self.karol_the_alchemist_csv = csv.DictReader(open(path.join(dialog_folder, 'karol_the_alchemist_dialog.csv')), delimiter=';')
        self.ivan_the_physician_csv = csv.DictReader(open(path.join(dialog_folder, 'ivan_the_physician_dialog.csv')), delimiter=';')
        self.dori_the_smith_csv = csv.DictReader(open(path.join(dialog_folder,'dori_the_smith_dialog.csv')), delimiter=';')
        self.wilfredo_the_cowboy_csv = csv.DictReader(open(path.join(dialog_folder,'wilfredo_the_cowboy_dialog.csv')), delimiter=';')
        #############

    def generate(self, name, x, y, image):
        if name == "Gold Crusader":
            gold_crusader = sprites.Npc(self.game,name,x,y,image)
            gold_crusader.dialog_data.load_from_dict(self.gold_crusader_csv,self.quest_gen)
            print ("Gold Crusader generated at:")

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

        if name == "Mieszko the Knight":
            mieszko_the_knight = sprites.Npc(self.game,name,x,y,image)
            mieszko_the_knight.dialog_data.load_from_dict(self.mieszko_the_knight_csv, self.quest_gen)
            return mieszko_the_knight

        if name == "Piggy":
            piggy = sprites.Npc(self.game,name,x,y,image)
            piggy.dialog_data.load_text(True,"welcome",0,0,"Oink, oink",False,False,False,False,False,False,False)
            piggy.put_sound(oink_snd)
            return piggy

        if name == "Young Knight":
            young_kinght = sprites.Npc(self.game, name, x, y, image)
            young_kinght.dialog_data.load_text(True, "welcome", 0, 0, "Hello, adventurer",
                                        False, False, False, False, False, False,False)
            return young_kinght

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
            print("Eveandro generated at:")
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

        if name == "Ivan the Physician":
            ivan_the_physician = sprites.Npc(self.game,name,x,y,image)
            ivan_the_physician.dialog_data.load_from_dict(self.ivan_the_physician_csv, self.quest_gen)
            ivan_the_physician.dialog_data.thread_unblock_with_event("quest Golden Mask",['quest Speak with the King has been completed'])
            ivan_the_physician.dialog_data.thread_block_with_event("ill",['quest Speak with the King has been completed'])
            return ivan_the_physician

        if name == "Dori the Smith":
            dori_the_smith = sprites.Npc(self.game,name,x,y,image)
            dori_the_smith.dialog_data.load_from_dict(self.dori_the_smith_csv, self.quest_gen)
            dori_the_smith.dialog_data.thread_unblock_with_event("quest Golden Mask",['got quest Golden Mask'])
            dori_the_smith.dialog_data.thread_block_with_event("ill",['got quest Golden Mask'])
            return dori_the_smith

        if name == "Wilfredo the Cowboy":
            wilfredo_the_cowboy = sprites.Npc(self.game,name,x,y,image)
            wilfredo_the_cowboy.dialog_data.load_from_dict(self.wilfredo_the_cowboy_csv, self.quest_gen)
            return wilfredo_the_cowboy