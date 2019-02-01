from Scenes.StateMachine import *
from Code.Settings import *

# Quits the game
class Exit(GameState):
    def __init__(self):
        super(Exit, self).__init__()
        self.quit = True