class LevelPause(GameState):
    def __init__(self):
        super(LevelPause, self).__init__()

    def startup(self, persistent):
        self.persist = persistent
        self.button_group = pg.sprite.Group()
        self.label_group = pg.sprite.Group()
        self.sprite_group = self.persist["sprite_group"]
        self.ignore_keyup = self.persist["ignore_keyup"]

        self.paused_label = Text((WIDTH/2, 100),"*PAUSED*",70,pg.Color("grey"),self.label_group)
        self.resume_button = Button((WIDTH/2, 200), (150, 40), "RESUME", pg.Color("dodgerblue"), self.button_group, "GAMEPLAY")
        self.exit_button = Button((WIDTH/2, 300), (150, 40), "EXIT", pg.Color("dodgerblue"), self.button_group, "EXIT")
        self.restart_button = Button((WIDTH/2, 250), (150, 40), "RESTART", pg.Color("dodgerblue"), self.button_group, "RESTART")
        self.menu_button = Button((WIDTH / 2, 350), (150, 40), "MENU", pg.Color("dodgerblue"), self.button_group, "MAINMENU")

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            for button in self.button_group:
                #if player clicked button
                if button.if_hovered():
                    # run button clicked code
                    if button.clicked() in states:
                        self.next_state = button.clicked()
                        self.done = True
                    else:
                        # restart level if restasrt clicked
                        if button.clicked() == "RESTART":
                            self.persist["next_level"] = self.persist["current_level"]
                            self.next_state = "LEVELLOAD"
                            self.done = True
        # if player presses key
        elif event.type == pg.KEYDOWN:
            # go back to gamelay if ESC is pressed again
            if event.key == pg.K_ESCAPE:
                self.next_state = "GAMEPLAY"
                self.done = True
        #ignore controls pressed while paused
            if event.key in CONTROLS:
                self.ignore_keyup.append(event.key)
        if event.type == pg.KEYUP:
            if event.key in CONTROLS:
                if event.key in self.persist["ignore_keyup"]:
                    self.ignore_keyup.remove(event.key)
        self.persist["ignore_keyup"] = self.ignore_keyup

    def update(self, dt):
        #update sprites
        self.button_group.update()
        self.label_group.update()

    def draw(self, surface):
        # draw the game sprites
        self.sprite_group.draw(surface)
        self.button_group.draw(surface)
        self.label_group.draw(surface)
