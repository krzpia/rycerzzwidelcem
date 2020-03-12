import sprites

class NpcGenerator:
    def __init__(self, game,tileset1, tileset2):
        self.game = game
        self.tileset = tileset1
        self.f_set = tileset2

    def generate(self, name, x, y, image):
        if name == "Gold Crusader":
            gold_crusader = sprites.Npc(self.game,name,x,y,image)
            gold_crusader.dialogs.add_line("w", "n", True, False, False, ("Welcome " + self.game.player.name))
            gold_crusader.dialogs.add_line("w", "p", True, False, False, "Welcome!")
            gold_crusader.dialogs.add_line("b", "n", True, False, False, ("Farewell " + self.game.player.name))
            gold_crusader.dialogs.print_lines()
            #gold_crusader.dialogs.add_n_txt('welcome', "Welcome " + self.game.player.name)
            #gold_crusader.dialogs.add_n_txt('goodbye', "Farewell " + self.game.player.name)
            #gold_crusader.dialogs.initial_construct()
            # Thread welcome:
            # NPC: <Witaj Kris>
            # PL: <Witaj>
            # NEXT Thread:
            # if thread.type == "question"
            # if thread.avaible and if not thread.closed:
            # NPC: print question <Jak mogę Ci pomóc
            # PL: print answers <1/ Tak, 2/Smak, 3/Owak
            # NPC: print comment on answer(answer)
            # NEXT THREAD:
            #
            #
            #
            return gold_crusader
