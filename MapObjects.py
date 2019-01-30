from Settings import *
from Textures import *
from Score import *


# all objects on the map apart from player inherit from this class
class Obstacle(pg.sprite.Sprite):
    def __init__(self,x,y,image):
        # intialise obstacle sprite
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = image
        self.image = pg.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x,self.y)

    def collisionSide(self,player,axis):
        # if collision occurs after updating xAxis movement, assume the collision occurs on the Xaxis
        if axis == 0:
            # approaching from right
            if player.rect.right - player.xVel > self.rect.right:
                return "right"
            # approaching from left
            elif player.rect.left - player.xVel < self.rect.left:
                return "left"
        # otherwise we assume the collision occurs on the y axis
        elif axis == 1:
            # We subtract the yVelocity to catch instances where the object moves so fast it passes THROUGH the self
            if player.rect.top - player.yVel < self.rect.top:
                return "top"
            if player.rect.bottom - player.yVel > self.rect.bottom:
                return "bottom"


# objects below inherit from Obstacle
# platform object
class Platform(Obstacle):
    texture = pg.image.load(imgPLATFORM)

    # inherits from obstacle class
    def __init__(self,x,y):
        Obstacle.__init__(self,x,y,self.texture)

    def collisionBehaviour(self,player,axis,fallThrough):
        sideCollided = Obstacle.collisionSide(self, player, axis)

        #Allow player to pass through any side apart from above, unless "Fall" key is held, in which case allow this too
        if sideCollided == "top" and fallThrough == False and player.yVel > 0:
            player.rect.bottom = self.rect.top
            player.yVel = 0
            player.jumpsLeft = MAXJUMPS


# block object
class Block(Obstacle):
    texture = pg.image.load(imgBLOCK)

    # inherits from obstacle class
    def __init__(self,x,y):
        Obstacle.__init__(self,x,y,self.texture)

    def collisionBehaviour(self,player,axis,fallThrough):
        sideCollided = Obstacle.collisionSide(self,player,axis)
        # No matter what side the player collides on, stop the player's movement.
        if sideCollided == "top":
            player.rect.bottom = self.rect.top
            player.yVel = 0
            player.jumpsLeft = MAXJUMPS
        elif sideCollided == "bottom":
            player.rect.top = self.rect.bottom
            player.yVel = 0
        elif sideCollided == "left":
            player.rect.right = self.rect.left
        elif sideCollided == "right":
            player.rect.left = self.rect.right


class Coin(Obstacle):
    texture = pg.image.load(imgCOIN)

    def __init__(self,x,y):
        Obstacle.__init__(self,x,y,self.texture)

    def collisionBehaviour(self,player,axis,fallThrough):
        # ignore WHERE it collided, just run collision code
        pg.sprite.Sprite.kill(self)
        GLOBALS["coin_collected"] = True


class Start(Obstacle):
    texture = pg.image.load(imgSTART)

    # inherits from obstacle class
    def __init__(self, x, y):
        Obstacle.__init__(self, x, y, self.texture)

    def collisionBehaviour(self, player, axis, fallthrough):
        pg.sprite.Sprite.kill(self)


class Goal(Obstacle):
    texture = pg.image.load(imgFLAG)
    
    # inherits from obstacle class
    def __init__(self, x, y):
        Obstacle.__init__(self, x, y, self.texture)
    
    # When collided, set level complete flag to true
    def collisionBehaviour(self, player, axis, fallThrough):
        # ignore WHERE it collided, just run collision code
        pg.sprite.Sprite.kill(self)
        GLOBALS["level_complete"] = True


# Dictionary storing obstacles and their representative RGB value for the map generator
obstacle_pixels = {
    RED: Platform,
    BLUE: Block,
    MAGENTA: Coin,
    GREEN: Start,
    YELLOW: Goal,
}


