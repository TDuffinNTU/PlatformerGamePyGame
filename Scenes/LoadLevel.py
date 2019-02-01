from Scenes.StateMachine import *
from Code.Settings import *
from Code.Textures import *

# Loads the next level of the game
class LevelLoad(GameState):
    # inherit from gamestate
    def __init__(self):
        super(LevelLoad,self).__init__()

    # Load the level, or hiscores screen if player completed all levels
    def startup(self,persistent):
        self.persist = persistent

        # If the next_level counter exceeds the number of levels, show hiscores.
        if not LEVELS.get(self.persist["next_level"], False):
            # If player selected "load game" from main menu, set scores to 0 to avoid inputting hiscores again
            if self.persist.get("load_game", False):
                self.persist["load_game"] = False
                GLOBALS["final_score"] = 0

            # load hiscores state
            self.next_state = "HISCORES"
            self.done = True

        else:
            # Load the level
            self.load_level()

    # Loads the level
    def load_level(self):
        # The level to be loaded is stored under "next level" and fetched from the LEVELS dictionary
        level = LEVELS[self.persist["next_level"]]

        # create the obstacle group, add it to the persistent dict.
        self.obstacle_group = pg.sprite.Group()
        self.persist["obstacle_group"] = self.obstacle_group

        # Empty the sprite group to overwrite with new objects
        self.sprite_group.empty()

        # Set the w/h using the .size attribute of the image
        lvl_width, lvl_height = level.size

        # load list called pixels with RGB data from image file
        pixels = list(level.getdata())

        # Check each pixel on the map image
        # If the pixel's colour matches a colour in the dictionary of object/pixel pairs
        for i in range(0, lvl_width * lvl_height - 1):
            i += 1
            if pixels[i] in obstacle_pixels:
                y, x = divmod(i, lvl_width)
                new_obstacle = obstacle_pixels[pixels[i]](x * 20, y * 20)
                self.obstacle_group.add(new_obstacle)
                self.sprite_group.add(new_obstacle)

                if pixels[i] == GREEN:
                    startPos = (x * 20, y * 20)

        # If a player object already exists, set its position to StartPos
        # Otherwise, we create a new player object at StartPos
        if self.persist.get("player", False):
            player = self.persist["player"]
            player.rect.topleft = startPos
            player.xVel = 0
        else:
            player = Player(startPos)

        # Add the player object to the sprite group
        self.sprite_group.add(player)

        # Load sprite groups to the persist dictionary so that they're overwritten
        self.persist["player"] = player
        self.persist["sprite_group"]=self.sprite_group

        # After loading the level, load the level intro screen, increment the next level, and close the state.
        self.persist["current_level"] = self.persist["next_level"]
        self.persist["next_level"] += 1
        self.next_state = "LEVELINTRO"
        self.done = True