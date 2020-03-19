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
            q_holy_grail = ui.Quest(self.game,"Holy Grail",1,[],["Holy Grail"],[],[],10,50)
            gold_crusader.dialog_data.load_text(True, 0,0,"Hello, " + self.game.player.name,
                                                compl_event=False,block_event=False,ask= False, goto=False)
            gold_crusader.dialog_data.load_text(False, 0, 1, "Hello, " + name,
                                                compl_event=False,block_event=False,ask= False,goto=False)
            gold_crusader.dialog_data.load_text(True, 1, 0, "Welcome back, " + self.game.player.name,
                                                compl_event=f'{name} has been encountered.',
                                                block_event=False,ask= False,goto=False)
            gold_crusader.dialog_data.load_text(False, 1, 1, "Hello again, " + name,
                                                compl_event=f'{name} has been encountered.',
                                                block_event=False,ask= False,goto=False)
            gold_crusader.dialog_data.load_text(True, 2, 0, "I`m hope you are still seeking..",compl_event='got quest Holy Grail',block_event='quest Holy Grail has been completed',
                                                ask=False,goto=(99,0))
            gold_crusader.dialog_data.load_text(True, 3, 0, "Would you do something for me?",
                                                compl_event=False,block_event='got quest Holy Grail',
                                                ask= [["Yes",q_holy_grail,(4,0)],["No",False,(5,0)]],goto=False)
            gold_crusader.dialog_data.load_text(True, 4, 0, "Great, I`m looking for a Holy Grail,    Find one and bring it to me!", compl_event=False,block_event=False, ask=False, goto=False)
            gold_crusader.dialog_data.load_text(False, 4, 1,"Ok!",
                                                compl_event=False,block_event=False, ask=False, goto=(99,0))
            gold_crusader.dialog_data.load_text(True, 5, 0,"That`s a pitty!",
                                                compl_event=False,block_event=False, ask=False, goto=(99,0))
            gold_crusader.dialog_data.load_text(True, 9, 0, "What do you seek?",
                                                compl_event=False,block_event=False,ask= False, goto=False)
            gold_crusader.dialog_data.load_text(False, 9, 1, "I`m seek for a holy grail!",
                                                compl_event=False,block_event=False,ask= False, goto=False)
            gold_crusader.dialog_data.load_text(True, 9, 2, "Ahhh It will be difficult to find..",
                                                compl_event=False,block_event=False,ask= False, goto=False)
            gold_crusader.dialog_data.load_text(False, 9, 3, "I`m know...",
                                                compl_event=False,block_event=False,ask= False, goto=False)
            gold_crusader.dialog_data.load_text(True, 10,0,"So, you have killed a Rat? Impressive",
                                                'Rat has been killed.',
                                                block_event=False,ask= False, goto=False)
            gold_crusader.dialog_data.load_text(True, 99, 0, "Goodbye, " + self.game.player.name,
                                                compl_event=False,block_event=False,ask= False,goto=False)
            gold_crusader.dialog_data.load_text(False, 99, 1, "Goodbye, " + name,
                                                compl_event=False,block_event=False,ask= False,goto=False)
            return gold_crusader

