import sprites
import ui
from os import path
import csv
import data
from events.event import Event
game_folder = path.dirname(__file__)
dialog_folder = path.join(game_folder, 'dialog')

class QuestGenerator:
    def __init__(self,game):
        self.game = game
        self.q_holy_grail = ui.Quest(self.game,
                                     "Holy Grail", "Find and bring a Holy Grail",
                                     1, [], ["Holy Grail"], [], [], 10, 50)
        self.quests = [self.q_holy_grail]

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
        #############

    def generate(self, name, x, y, image):
        if name == "Gold Crusader":
            gold_crusader = sprites.Npc(self.game,name,x,y,image)
            gold_crusader.dialog_data.load_from_dict(self.gold_crusader_csv,self.quest_gen)
            return gold_crusader