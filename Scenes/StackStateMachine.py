import pygame as pg
import Code.Settings as settings

# Fully implemented stack-based FSM

#TODO implement pygame features
# State class handles menus, gameplay, other user-interaction
class State:
    # Final version will have game data passed between states via initializer
    def __init__(self, game_data):
        self.suspend_me = False
        self.suspend_params = []
        self.game_data = game_data


    # The user can interact directly with the application's state "stack" from within a state instance
    def exit_state(self, keyword = None, next_state = None):
        # Sets the suspend_me flag to true so that the statemachine knows its time to flip
        if str(keyword).upper() in ["PUSH", "POP", "SWAP"]:
            self.suspend_params = [keyword, next_state]
            self.suspend_me = True
        else:
            print("Failed to transition between states with params: {0}".format([keyword, next_state]))

    # initilising code outside of init()
    def startup(self):
        pass

    # handles user input
    def get_event(self, event):
        pass

    # update sprites, other data
    def update(self, dt):
        pass

    # draw the updated data to the screen
    def draw(self, screen):
        pass

# Statemachine controls which state machine gets control at any one time
class StateMachine:
    def __init__(self, initial_state):
        # Initialise pygame
        pg.init()

        # pygame variables
        self.screen = pg.display.set_mode((settings.WIDTH, settings.HEIGHT))
        self.clock = pg.time.Clock()
        self.frame_rate = 60
        self.delta_time = 0
        self.game_data = {}
        self.running = True

        # Using a list as a stack allows for stack-based design pattern for UI management
        self.stack = []
        self.stack.append(initial_state)

        # Underlying functions for executing state methods should remain unchanged.
        self.current_state: State = self.stack[-1](self.game_data)
        self.current_state.startup()

    # give program control to a new state
    def flip_state(self):
        # Get the arguments from the state
        args = self.current_state.suspend_params
        self.game_data = self.current_state.game_data

        # process arguments to get new running state
        if args[0] == "PUSH":
            self.stack.append(args[1])
        elif args[0] == "POP" and len(self.stack):
            self.stack.pop()
        elif args[0] == "SWAP":
            if len(self.stack):
                self.stack.pop()
            self.stack.append(args[1])

        # New running state is initialised
        self.current_state = self.stack[-1](self.game_data)

    # will handle pygame events
    def event_loop(self):
        for event in pg.event.get():
            self.current_state.get_event(event)
            if event.type == pg.QUIT:
                self.running = False

    # check that state isn't suspended yet, otherwise update
    def update(self, dt):
        if self.current_state.suspend_me:
            self.flip_state()
        self.current_state.update(dt)

    def draw(self):
        self.current_state.draw(self.screen)

    # run all the other functions until stopped
    def run(self):
        while self.running:
            dt = self.clock.tick(self.frame_rate)
            self.event_loop()
            self.update(dt)
            self.draw()
            pg.display.update()

