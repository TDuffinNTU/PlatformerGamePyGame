class EndLevel(GameState):
    def __init__(self):
        super(EndLevel,self).__init__()

    def startup(self, persistent):
        # import persistent dict, initialise sprite groups
        self.persist = persistent
        self.overlay_group = pg.sprite.Group()
        self.button_group = pg.sprite.Group()

        # Screen colour, labels
        self.screen_colour = pg.Color("dodgerblue")
        self.level_label = Text((WIDTH/2, 100), "LEVEL" + str(self.persist["current_level"]), 60, self.screen_colour, self.overlay_group)
        self.score_level = Text((WIDTH/2, 400), "LEVEL SCORE: " + str(GLOBALS["level_scores"][-1]), 40, self.screen_colour, self.overlay_group)
        self.score_total = Text((WIDTH/2, 450), "TOTAL SCORE: " + str(GLOBALS["final_score"]), 40, self.screen_colour, self.overlay_group)

        # Menu buttons
        self.restart_button = Button((WIDTH/2, 170), (200, 40), "RESTART LEVEL", pg.Color("white"), self.button_group, "RESTART")
        self.next_button =    Button((WIDTH/2, 220), (200, 40), "NEXT LEVEL", pg.Color("white"), self.button_group, "SAVEGAME")
        self.exit_button =    Button((WIDTH/2, 270), (200, 40), "EXIT", pg.Color("white"), self.button_group, "EXIT")
        self.menu_button =    Button((WIDTH/2, 320), (200, 40), "MAIN MENU", pg.Color("white"), self.button_group, "MAINMENU")

    def get_event(self, event):
        #Handle mouse events
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            for button in self.button_group:
                if button.if_hovered():
                    if button.clicked() in states:
                        self.next_state = button.clicked()
                        self.done = True
                    else:
                        # If restart is clicked set next level to start of prev level, restart level
                        if button.clicked() == "RESTART":
                            GLOBALS["final_score"] -= GLOBALS["level_scores"][-1]
                            GLOBALS["level_scores"][-1] = 0
                            self.persist["next_level"] = self.persist["current_level"]
                            self.next_state = "LEVELLOAD"
                            self.done = True

    def update(self, dt):
        # Update the button groups
        self.button_group.update()
        self.overlay_group.update()

    def draw(self, surface):
        surface.fill(self.screen_colour)
        self.button_group.draw(surface)
        self.overlay_group.draw(surface)