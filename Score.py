from Settings import *

#Class which tracks the score for every level.
class Score:
    def __init__(self):
        #initial score set at 5000
        self.score = 5000

    #updates score by integer passed to it
    def update_score(self, integer):
        self.score += integer



