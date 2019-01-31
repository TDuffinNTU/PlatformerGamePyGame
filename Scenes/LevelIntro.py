class LevelIntro(GameState):
    def __init__(self):
        super(LevelIntro,self).__init__()

    def startup(self, persistent):
        self.persist = persistent
        self.overlay_group = pg.sprite.Group()
        self.screen_colour = pg.Color("green")
        self.level_label = Text((WIDTH/2, 100), "LEVEL: " + str(self.persist["current_level"]), 60, self.screen_colour, self.overlay_group)
        self.prompt_label = Text((WIDTH/2, 300), "CLICK TO START", 40, self.screen_colour, self.overlay_group)
        self.score_level = Text((WIDTH/2, 400), "CURRENT SCORE: " + str(GLOBALS["final_score"]), 40, self.screen_colour, self.overlay_group)

        self.ignore_keyup = []

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit = True

            # ignore controls pressed while paused
                if event.key in CONTROLS:
                    self.ignore_keyup.append(event.key)
            if event.type == pg.KEYUP:
                if event.key in CONTROLS:
                    if event.key in self.persist["ignore_keyup"]:
                        self.ignore_keyup.remove(event.key)
            else:
                self.persist['ignore_keyup'] = self.ignore_keyup
                self.next_state = "GAMEPLAY"
                self.done = True

    def update(self, dt):
        self.overlay_group.update()

    def draw(self, surface):
        surface.fill(self.screen_colour)
        self.overlay_group.draw(surface)