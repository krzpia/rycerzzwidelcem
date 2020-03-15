import sprites
from events.event import Event


class NpcGenerator:
    def __init__(self, game,tileset1, tileset2):
        self.game = game
        self.tileset = tileset1
        self.f_set = tileset2

    def generate(self, name, x, y, image):
        if name == "Gold Crusader":
            gold_crusader = sprites.Npc(self.game,name,x,y,image)
            gold_crusader.dialog_data.load_text(True, 0,0,"Hello, " + self.game.player.name,
                                                compl_event=False, goto=False)
            gold_crusader.dialog_data.load_text(False, 0, 1, "Hello, " + name,
                                                compl_event=False,goto=False)
            gold_crusader.dialog_data.load_text(True, 5, 0, "What do you seek?",
                                                compl_event=False, goto=False)
            gold_crusader.dialog_data.load_text(False, 5, 1, "I`m seek for a holy grail!",
                                                compl_event=False, goto=False)
            gold_crusader.dialog_data.load_text(True, 5, 2, "Ahhh It will be difficult to find..",
                                                compl_event=False, goto=False)
            gold_crusader.dialog_data.load_text(False, 5, 3, "I`m know...",
                                                compl_event=False, goto=False)
            gold_crusader.dialog_data.load_text(True, 10,0,"So, you have killed a Rat? Impressive",
                                                'Rat has been killed', False)
            gold_crusader.dialog_data.load_text(True, 99, 0, "Goodbye, " + self.game.player.name,
                                                compl_event=False,goto=False)
            gold_crusader.dialog_data.load_text(False, 99, 1, "Goodbye, " + name,
                                                compl_event=False,goto=False)
            return gold_crusader

