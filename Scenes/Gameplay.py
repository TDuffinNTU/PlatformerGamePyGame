class Gameplay(GameState):
    def __init__(self):
        super(Gameplay, self).__init__()

    def startup(self, persistent):
        GLOBALS["level_complete"] = False
        self.persist = persistent
        color = self.persist["screen_colour"]
        self.screen_colour = pg.Color(color)
        self.player = self.persist["player"]
        self.obstacle_group = self.persist["obstacle_group"]
        self.sprite_group = self.persist["sprite_group"]
        self.overlay_group = pg.sprite.Group()
        self.next_state = "LEVELLOAD"

        # SCORE
        self.level_score = Score()

        # HUD/UI Elements
        self.score_label = Text((WIDTH / 2, 35), "SCORE: #####", 30, pg.Color("white"), self.overlay_group)

    def get_event(self, event):
        # print(event)
        if event.type == pg.QUIT:
            self.quit = True
        if event.type == pg.KEYDOWN:
            if event.key in CONTROLS:
                # send player control to player object
                self.player.control(CONTROLS[event.key], 1)
            elif event.key == pg.K_ESCAPE:
                self.next_state = "LEVELPAUSE"
                if self.player.xVel > 0:
                    self.persist["ignore_keyup"].append(pg.K_a)
                elif self.player.xVel < 0:
                    self.persist["ignore_keyup"].append(pg.K_d)
                self.done = True

        # Check if we need to ignore the keyup, otherwise send it to player control
        if event.type == pg.KEYUP:
            if event.key in CONTROLS:
                if event.key in self.persist["ignore_keyup"]:
                    self.persist["ignore_keyup"].remove(event.key)
                else:
                    self.player.control(CONTROLS[event.key], -1)

    def update(self, dt):
        # Restart level if the player fails
        if self.level_score.score <= 0 or self.player.rect.top > HEIGHT:
            self.restart_level()

        # Level_complete will equate to False as long as the player has not collected the "goal" object (flag)
        if not GLOBALS["level_complete"]:
            # if player is near the edges of the screen, move all sprites to create scrolling effect
            if (self.player.rect.left > WIDTH * 0.6 and self.player.xVel > 0) or (
                    self.player.rect.right < WIDTH * 0.4 and self.player.xVel < 0):
                for sprite in self.sprite_group:
                    sprite.rect.left -= int(self.player.xVel)

            # if a coin is collected, increase score by 500
            if GLOBALS["coin_collected"]:
                GLOBALS["coin_collected"] = False
                self.level_score.update_score(500)
            # reduce score using dt
            self.level_score.update_score(int(-dt / 3))

            # update the score label with the current score
            self.score_label.update_text("SCORE: {}".format(str(self.level_score.score)))

            # update sprite groups
            self.overlay_group.update()
            self.obstacle_group.update()

            # update player sprite, pass obstacle group for collision checking
            self.player.update(self.obstacle_group)

        # Level is complete, show end level screen
        else:
            GLOBALS["final_score"] += self.level_score.score
            GLOBALS["level_scores"].append(self.level_score.score)
            print(GLOBALS["final_score"])
            self.next_state = "ENDLEVEL"
            self.done = True

    def draw(self, surface):
        surface.fill(self.screen_colour)
        # draw the game sprites
        self.sprite_group.draw(surface)
        # draw the overlay
        self.overlay_group.draw(surface)

    # Restarts the level
    def restart_level(self):
        self.persist["next_level"] = self.persist["current_level"]
        self.done = True