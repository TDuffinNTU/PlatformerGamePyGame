from Code.Settings import *
from Code.Textures import *


# Player Class
class Player(pg.sprite.Sprite):
    jumpsLeft = MAXJUMPS # Number of jumps
    yVel = 0
    xVel = 0
    maxYVel = MAXFALLSPEED
    fallThrough = False

    # intialise player sprite
    def __init__(self,startPos):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(imgPLAYER)
        self.image = pg.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        # set player to intial position
        self.rect.topleft = startPos

    def update(self,obstacles):
        # stop player accelerating due to gravity if they reach 'terminal' velocity
        if self.yVel < self.maxYVel:
            # otherwise increase fallspeed by gravity
            self.yVel += GRAVITY
        #run collision checks after updating X and Y axis movement independently
        self.rect.x += self.xVel
        self.collisionCheck(obstacles,0,False)
        self.rect.y += self.yVel
        self.collisionCheck(obstacles,1,self.fallThrough)

    def control(self, control, modifier):
        #set fallthru flag to false
        self.fallThrough = False

        #NB: modifier = 1 on KEYDOWN, -1 on KEYUP
        #if player has more jumps left and the key is KEYDOWN
        if control == "JUMP" and self.jumpsLeft > 0 and modifier == 1:
            self.yVel = -JUMPHEIGHT
            self.jumpsLeft -= 1
        #Add x velocities together to create final x velocity
        elif control == "RIGHT":
            self.xVel += RUNSPEED * modifier
        elif control == "LEFT":
            self.xVel -= RUNSPEED * modifier
        #set fallthru flag to true if fall key is pressed
        elif control == "FALL" and modifier == 1:
            self.fallThrough = True


    # 0 for x axis col.check, 1 for y axis col.check
    def collisionCheck(self,group,axis,fallThrough):
        collisions = pg.sprite.spritecollide(self,group,False)
        # if collision with sprite(s), run their collision behaviours
        for objects in collisions:
            objects.collisionBehaviour(self,axis,fallThrough)



        
        
