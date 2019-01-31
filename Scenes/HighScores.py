class HighScores(GameState):
    def __init__(self):
        #Inherit from GameState class
        super(HighScores, self).__init__()

    def startup(self, persistent):
        # Import persistent dict and initialise sprite groups, screen colour
        self.persist = persistent
        self.button_group = pg.sprite.Group()
        self.label_group = pg.sprite.Group()
        self.screen_colour = pg.Color("gold")

        # buttons/labels
        self.exit_button = Button((WIDTH - 100, 500), (100, 40), "EXIT", pg.Color("white"), self.button_group, "EXIT")
        self.menu_button = Button((100, 500), (100, 40), "MAIN", pg.Color("white"), self.button_group, "MAINMENU")
        self.new_button = Button((WIDTH/2, 500), (150, 40), "NEW GAME", pg.Color("green"), self.button_group, "LEVELLOAD")
        self.title_label = Text((WIDTH/2,50), "HIGH SCORES", 80, self.screen_colour, self.label_group)

        # Load scores to the labels
        self.load_scores()

    def get_event(self, event):
        # If the player quits the game, quit
        if event.type == pg.QUIT:
            self.quit = True
            self.done = True

        # Handles button input
        if event.type == pg.MOUSEBUTTONDOWN:
            for button in self.button_group:
                if button.if_hovered():
                    if button.clicked() in states:
                        self.next_state = button.clicked()

                        # if the new-game button is clicked, start from level 1
                        if self.next_state == "LEVELLOAD":
                            self.persist["next_level"] = 1
                            GLOBALS["final_score"] = 0
                            GLOBALS["level_scores"][:] = []
                        self.done = True

    def update(self, dt):
        # Update the button/labels
        self.button_group.update()
        self.label_group.update()

    def draw(self, surface):
        # Draw the elements to the screen
        screen.fill(self.screen_colour)
        self.button_group.draw(surface)
        self.label_group.draw(surface)

    # Loads the scores for the game
    def load_scores(self):
        final_score = GLOBALS["final_score"]

        with open(HISCOREFILE, 'r') as f:
            hiscores = f.read().splitlines()

        # Copy, by value, the hiscores list to a new list
        score_string = hiscores[:]

        # If the score is on the hiscores list, insert it in the correct place on the list
        for i in range(0, len(score_string)):
            if final_score > int(score_string[i]):
                # Append "new" to the score to indicate that it's a new score
                score_string.insert(i, str(final_score) + " *NEW*")
                hiscores.insert(i, final_score)
                # slice the lists back down to size, then break from the loop
                score_string = score_string[:5]
                hiscores = hiscores[:5]
                break

        # All the boxes will have the same text size, so just define it here to save time
        text_size = 40

        # In Descending order, load the hiscore buttons with their respective score data
        self.first = Text((WIDTH / 2, 200), "1. {:6}".format(score_string[0]), text_size, pg.Color("white"), self.label_group)
        self.second = Text((WIDTH / 2, 240), "2. {:6}".format(score_string[1]), text_size, pg.Color("white"), self.label_group)
        self.third = Text((WIDTH / 2, 280), "3. {:6}".format(score_string[2]), text_size, pg.Color("white"), self.label_group)
        self.fourth = Text((WIDTH / 2, 320), "4. {:6}".format(score_string[3]), text_size, pg.Color("white"), self.label_group)
        self.fifth = Text((WIDTH / 2, 360), "5. {:6}".format(score_string[4]), text_size, pg.Color("white"), self.label_group)

        # Write the new hiscores to the hiscores file, with one score on each line
        data = []
        for i in hiscores:
            data.append(str(i) + "\n")

        with open(HISCOREFILE, 'w') as f:
            f.writelines(data)