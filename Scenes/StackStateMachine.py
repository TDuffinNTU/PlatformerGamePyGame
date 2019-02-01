import pygame as pg

# TODO Change FSM to stack-based system to avoid circular references, make code cleaner/faster
# Stack class for the stack-based FSM
class Stack:
    def init(self):
        self.items = []
        self.top = None

    def push(self, item):
        self.items.append(item)
        self.top = item

    def pop(self):
        if len(self.items):
            self.items.pop()
            self.top = self.items[-1]

    def swap(self, item):
        self.items.pop()
        self.push(item)

    def peek(self):
        return self.top

    def count(self):
        return len(self.items)

    def stack(self):
        return self.items

# The modified state machine for use with stacks
class StackMachine:
    def __init__(self, screen, initial_state):
        # pygame data
        self.screen = screen
        self.clock = pg.time.Clock()
        self.frame_rate = 60
        # stack/state data
        self.states = Stack()
        self.states.push(initial_state)
        self.current_state = self.states.peek()()

        self.quit = False

    #TODO implement these as interfaces to stack class
    def push_state(self):
        pass

    def pop_state(self):
        pass

    def swap_state(self):
        pass

    def event_loop(self):
        for event in pg.event.get():
            self.current_state.get_event(event)

    def update(self, dt):
        self.current_state.update(dt)

    def draw(self):
        self.current_state.draw(self.screen)

    def run(self):
        while not self.quit:
            dt = self.clock.tick(self.frame_rate)
            self.event_loop()
            self.update(dt)
            self.draw()
            pg.display.update()

class State:
    def __init__(self, data):
        pass
