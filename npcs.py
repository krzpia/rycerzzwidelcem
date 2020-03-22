import sprites
import ui
from events.event import Event


class NpcGenerator:
    def __init__(self, game,tileset1, tileset2):
        self.game = game
        self.tileset = tileset1
        self.f_set = tileset2

    def generate(self, name, x, y, image):
        if name == "Gold Crusader":
            gold_crusader = sprites.Npc(self.game,name,x,y,image)
            q_holy_grail = ui.Quest(self.game,image,"Holy Grail","Find and bring a Holy Grail",1,[],["Holy Grail"],[],[],10,50)
            gold_crusader.dialog_data.load_text(True,"welcome",0, 0,
                                                "Hello, " + self.game.player.name,
                                                False,False,False,False,False, False,False)
            gold_crusader.dialog_data.load_text(False,"welcome",0, 1,
                                                "Hello, " + name,
                                                False,False,False,False,False,False,False)
            gold_crusader.dialog_data.load_text(True, "welcome", 1, 0,
                                                "Hello again, " + self.game.player.name,
                                                False, False, False, False, False,False,False)
            gold_crusader.dialog_data.load_text(False, "welcome", 1, 1,
                                                "Hello again, " + name,
                                                False, False, False, False, False,False,False)
            gold_crusader.dialog_data.load_text(True, "quest Holy Grail", 0, 0,
                                                "I have a task for you. I`m looking for a Holy Grail. Will you help me?",
                                                ["Yes",q_holy_grail,(0,1)], ["No",False,(0,2)],
                                                False, False, False,False,False)
            gold_crusader.dialog_data.load_text(True, "quest Holy Grail", 0, 1,
                                                "Thank`s, Look for and bring it to me, I`ll be grateful!",
                                                False, False, False, False,True, False,False)
            gold_crusader.dialog_data.load_text(True, "quest Holy Grail", 0, 2,
                                                "Thats a pitty!",
                                                False, False, False, False,True, False,False)
            gold_crusader.dialog_data.load_text(True, "quest Holy Grail", 1, 0,
                                                "Are you still searching?",
                                                False, False, False, False, True, False, False)
            gold_crusader.dialog_data.load_text(True, "quest Holy Grail", 2, 0,
                                                "Wonderful you have made it! Congratulations",
                                                False, False, False, False, False, False, "quest Holy Grail has been completed")
            gold_crusader.dialog_data.load_text(True, "quest Holy Grail", 2, 1,
                                                "I have a reward for you!",
                                                False, False, False, False, False, False, False)
            gold_crusader.dialog_data.load_text(False, "quest Holy Grail", 2, 2,
                                                "Thanks!",
                                                False, False, False, False, True, False, "quest Holy Grail has been rewarded")
            gold_crusader.dialog_data.load_text(True, "quest Holy Grail", 3, 0,
                                                "Thanks for your help. Now I can rest!",
                                                False, False, False, False, True, False, False)
            gold_crusader.dialog_data.load_text(True, "bye",0 , 0, "Goodbye, " + self.game.player.name,
                                                False,False,False,False,False,False,False)
            gold_crusader.dialog_data.load_text(False,"bye",0, 1, "Goodbye, " + name,
                                                False,False,False,False,False,False,False)
            return gold_crusader
            #gold_crusader.dialog_data.load_text(True, 90,0,"So, you have killed a Rat? Impressive",
            #                                    compl_event='Rat has been killed.',
            #                                    block_event=False,block_event2=False,ask= False, goto=False)



