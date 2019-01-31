class Game(object):
    # The game, states, and events are handled through this class.
    # The game class is a Finite-State Machine, adapted from this github example:
    # https://gist.github.com/iminurnamez/8d51f5b40032f106a847
    def __init__(self, screen, states, start_state):
        # Initialise game variables.
        # screen is the screen surface, states is a dictionary of all stastes, start_state is the initial state
        # that runs
        self.done = False
        self.screen = screen
        self.clock = pg.time.Clock()
        self.fps = 60
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]()

    def event_loop(self):
        # Events are passed to the state's get_event method to be handled individually
        for event in pg.event.get():
            self.state.get_event(event)

    def flip_state(self):
        # Switch to the next game state if the "done" pointer is true
        current_state = self.state_name
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state

        # persistent dictionary is pulled from previous state to pass to next state
        persistent = self.state.persist

        # Run the startup functions of the next state
        self.state = self.states[self.state_name]()
        self.state.startup(persistent)

    def update(self, dt):
        # Check to see if user quits, or that state is "done".
        if self.state.quit:
            self.done = True

        elif self.state.done:
            self.flip_state()

        self.state.update(dt)

    def draw(self):
        # draw the sprites and other elements to the surface before displaying it
        self.state.draw(self.screen)

    def run(self):
        # loops through the game class methods until the player quits
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.draw()
            # displays the elements drawn to the screen surface in the previous method
            pg.display.update()


# The GameState class defines states within the Finite-State Machine, adapted from this github example:
# https://gist.github.com/iminurnamez/8d51f5b40032f106a847
class GameState(object):
    # Parent class of all GameStates
    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pg.display.get_surface().get_rect()
        self.screen_surf = pg.display.get_surface()
        self.persist = {}
        self.font = pg.font.Font(None, 24)

        # Create a sprite group, add to the persistent dict
        self.sprite_group = pg.sprite.Group()
        self.persist["sprite_group"] = self.sprite_group

    def startup(self, persistent):
        # Called when a state resumes being active.
        # Allows information to be passed between states.
        # persistent: a dictionary passed from state to state
        self.persist = persistent

    def get_event(self, event):
        # Handle a single event passed by the Game object.
        pass

    def update(self, dt):
        # Update the state. Called by the Game object once per frame.
        # dt: time since last frame
        pass

    def draw(self, surface):
        # Draw everything to the screen.
        pass
