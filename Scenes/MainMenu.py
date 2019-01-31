class MainMenu(GameState):
    def __init__(self):
        super(MainMenu, self).__init__()

        # Empty and initialise sprite groups
        self.sprite_group.empty()
        self.button_group = pg.sprite.Group()

        # Buttons/UI elements
        self.new_button = Button((WIDTH/2, 200), (150, 40), "NEW", pg.Color("dodgerblue"), self.sprite_group, "LEVELLOAD")
        self.load_button = Button((WIDTH/2, 300), (150, 40), "LOAD", pg.Color("dodgerblue"), self.sprite_group, "LOADGAME")
        self.scores_button = Button((WIDTH/2, 400), (150, 40), "HISCORES", pg.Color("dodgerblue"), self.sprite_group, "HISCORES")
        self.exit_button = Button((WIDTH/2, 500), (150, 40), "EXIT", pg.Color("red"), self.sprite_group, "EXIT")
        self.controls_button = Button((85, 30), (150, 40), "HOW TO PLAY", pg.Color("red"), self.sprite_group, "CONTROLS")

        # add buttons to the button group
        for sprite in self.sprite_group:
            self.button_group.add(sprite)

        self.title_label = Text((WIDTH/2,60),"Platformer ver: " + VERSION,50,pg.Color("grey"),self.sprite_group)
        # Setting attribs from persistent dict.
        self.persist["screen_colour"] = "grey"

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        #handle mouse events for selecting buttons
        elif event.type == pg.MOUSEBUTTONDOWN:
            for sprite in self.button_group:
                if sprite.if_hovered():
                    self.next_state = sprite.clicked()
                    #if player selects to start new game, set scores/level to default values
                    if self.next_state == "LEVELLOAD":
                        self.persist["next_level"] = 1
                        GLOBALS["final_score"] = 0
                        GLOBALS["level_scores"][:] = []

                    self.persist["screen_colour"] = "grey"
                    self.done = True

    # update sprites
    def update(self,dt):
        self.sprite_group.update()

    #draw screen
    def draw(self, surface):
        surface.fill(pg.Color("grey"))
        self.sprite_group.draw(surface)