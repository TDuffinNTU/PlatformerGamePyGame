from Scenes.StateMachine import *
from Code.MenuObjects import *
from Code.Settings import *

class ControlMenu(GameState):
    def __init__(self):
        super(ControlMenu, self).__init__()

        self.sprite_group.empty()
        self.return_button = Button((WIDTH / 2, 500), (150, 40), "RETURN", pg.Color("dodgerblue"), self.sprite_group, "MAINMENU")

        self.title_label = Text((WIDTH/2,60), "CONTROLS", 60, pg.Color("grey"), self.sprite_group)

        self.controls_label_1 = Text ((WIDTH/2,100), "WASD TO MOVE, SPACE TO JUMP/DOUBLE JUMP", 40, pg.Color("grey"), self.sprite_group)
        self.controls_label_2 = Text ((WIDTH/2,150), "GET TO THE GOAL ASAP!", 40, pg.Color("grey"), self.sprite_group)


    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        #handle mouse events for selecting buttons
        elif event.type == pg.MOUSEBUTTONDOWN:
            if self.return_button.if_hovered():
                self.next_state = self.return_button.clicked()
                self.done = True

    def update(self, dt):
        self.sprite_group.update()

    def draw(self, surface):
        surface.fill(pg.Color("grey"))
        self.sprite_group.draw(surface)