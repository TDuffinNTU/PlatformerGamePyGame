from Scenes.StateMachine import *
from Code.Settings import *

# saves the game at the end of every level
class SaveGame(GameState):
    # inherit from gamestate
    def __init__(self):
        super(SaveGame, self).__init__()

    # run save routine, then load next level
    def startup(self, persistent):
        self.persist = persistent
        self.save_game()

        # When saved, load the next level
        self.next_state = "LEVELLOAD"
        self.done = True

    # save routine saves the current playthrough data every level
    def save_game(self):
        data = []
        data.append(str(self.persist["current_level"])+"\n")
        data.append(str(GLOBALS["final_score"])+"\n")

        for score in GLOBALS["level_scores"]:
            data.append(str(score) + "\n")

        with open(SAVEFILE, 'w') as f:
            f.writelines(data)