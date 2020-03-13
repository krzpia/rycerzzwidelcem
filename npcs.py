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
            self.game.events_manager.subscribe(gold_crusader.dialog.handle)
            gold_crusader.dialog.add_npc_line(
                f"Welcome {self.game.player.name}! I'm the Gold Crusader!",
            )
            gold_crusader.dialog.add_player_line(
                f'Welcome o Gold Crusader!',
            )
            gold_crusader.dialog.add_npc_line(
                f"What do you seek {self.game.player.name}?",
            )
            gold_crusader.dialog.add_player_line(f'I seek a Holy Grail!')
            gold_crusader.dialog.add_npc_line(
                f"You are too weak {self.game.player.name}!"
                "Come back to me when you kill a rat.",
            )
            gold_crusader.dialog.set_next_stage(
                fired_by=Event('Rat has been killed.')
            )
            gold_crusader.dialog.add_npc_line(
                f"So you have killed a Rat - {self.game.player.name}."
                " I'm impressed!",
            )
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
            return gold_crusader
