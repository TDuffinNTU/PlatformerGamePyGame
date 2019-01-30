from PIL import Image

#game textures
imgPLAYER   = "Player.png"
imgPLATFORM = "platform.png"
imgBLOCK    = "block.png"
imgFLAG     = "flag.png"
imgCOIN     = "coin.png"
imgSTART    = "start.png"

#load mapfiles with PIL
imgMAP = Image.open("map1.png", 'r')
imgMAP2 = Image.open("map2.png", 'r')
imgMAP3 = Image.open("map3.png", 'r')

#dict with all levels in game
LEVELS = {
    1: imgMAP,
    2: imgMAP2,
    3: imgMAP3,
    4: imgMAP3,
}

