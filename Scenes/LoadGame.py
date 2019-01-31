class LoadGame(GameState):
    def __init__(self):
        super(LoadGame, self).__init__()

    def startup(self, persistent):
        self.persist = persistent
        self.persist["load_game"] = True
        #open file
        with open(SAVEFILE, 'r') as f:
            data = f.read().splitlines()
        #load globals and persist with data from file
        self.persist["next_level"] = int(data[0]) + 1
        GLOBALS["final_score"] = int(data[1])

        for i in data[2:]:
            GLOBALS["level_scores"].append(int(i))
        #load next level
        self.next_state = "LEVELLOAD"
        self.done = True