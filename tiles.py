import pygame
from sprite import SpriteSheet, AnimatedCoin, AnimatedFlag

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile, x, y, spriteSheet="grassTiles.png"):
        super().__init__()
        self.ss = SpriteSheet(spriteSheet)
        self.image = self.ss.get_image(tile[0], tile[1], 16, 16)
        self.rect = pygame.Rect(x, y, 16, 11)
        #self.rect = self.image.get_rect(topleft=(x, y))
            

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, spriteSheet="coin.png"):
        super().__init__()
        self.animPlayer = AnimatedCoin(spriteSheet)
        self.image = self.animPlayer.image
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, dt):
        self.animPlayer.update(dt)
        self.image = self.animPlayer.image

class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y, spriteSheet="flag.png"):
        super().__init__()
        self.animPlayer = AnimatedFlag(spriteSheet)
        self.image = self.animPlayer.image
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, dt):
        self.animPlayer.update(dt)
        self.image = self.animPlayer.image

class LevelGen:
    def __init__(self, text):
        self.text = text
        self.lines = []
        self.longest = 0
        self.tiles = []
        self.playerPos = (0, 0)
        self.coins = []
        self.flag = None

        # storing level
        with open(self.text, "r", encoding="utf-8") as file:
            for line in file:
                self.lines.append(line.strip())
        

        # storing the length of the longest line of characters
        for line in self.lines:
            if len(line) > self.longest:
                self.longest = len(line)
        
        # adding tiles
        for y in range(len(self.lines)):
            for x in range(len(self.lines[y])):

                # establish tile position
                posX = x * 16
                posY = y * 16

                # if the symbyl is a space
                if " " in self.lines[y][x]:
                    continue
                elif "p" in self.lines[y][x]:
                    self.playerPos = (posX, posY)
                    continue
                elif "c" in self.lines[y][x]:
                    coin = Coin(posX+3, posY-2)
                    self.coins.append(coin)
                    continue
                elif "f" in self.lines[y][x]:
                    self.flag = Flag(posX, posY+1)
                    continue

                

                # look at the adjecent tiles
                try:
                    circ = {"northwest": self.look(self.look(self.lines, y, -1), x, -1) if self.look(self.lines, y, -1) != None else None,
                            "north": self.look(self.look(self.lines, y, -1), x, 0) if self.look(self.lines, y, -1) != None else None,
                            "northeast": self.look(self.look(self.lines, y, -1), x, 1) if self.look(self.lines, y, -1) != None else None,
                            "west": self.look(self.look(self.lines, y, 0), x, -1) if self.look(self.lines, y, 0) != None else None,
                            "center": self.lines[y][x],
                            "east": self.look(self.look(self.lines, y, 0), x, 1) if self.look(self.lines, y, 0) != None else None,
                            "southwest": self.look(self.look(self.lines, y, 1), x, -1) if self.look(self.lines, y, 1) != None else None,
                            "south": self.look(self.look(self.lines, y, 1), x, 0) if self.look(self.lines, y, 1) != None else None,
                            "southeast": self.look(self.look(self.lines, y, 1), x, 1) if self.look(self.lines, y, 1) != None else None
                            }
                except:
                    pass


                
                # init a tile
                tile = ""

                
                
                if circ["north"] != "g":
                    if circ["west"] != "g":
                        if circ["east"] != "g":
                            if circ["south"] != "g":
                                # all directions are none
                                tile = Tile((48, 64), posX, posY)       
                            else:
                                # north west east = none, but not south
                                tile = Tile((48, 0), posX, posY)
                        elif circ["south"] != "g":
                            # north west south = none, but not east
                            tile = Tile((0, 48), posX, posY)
                        else:
                            # north west = none, but not east south
                            if circ["southeast"] != "g":
                                # if southeast = none
                                tile = Tile((0, 64), posX, posY)
                            else:
                                # if southeast is filled
                                tile = Tile((0, 0), posX, posY)
                    elif circ["east"] != "g":
                        if circ["south"] != "g":
                            # north east south = none, but not west
                            tile = Tile((32, 48), posX, posY)
                        else:
                            # north east = none, but not west south
                            if circ["southwest"] != "g":
                                # if southwest is none
                                tile = Tile((32, 64), posX, posY)
                            else:
                                # if southwest is filled
                                tile = Tile((32, 0), posX, posY)
                    elif circ["south"] != "g":
                        # north south = none, but not west east
                        tile = Tile((16, 48), posX, posY)
                    else:
                        # north = none, but not west east south
                        if circ["southwest"] != "g":
                            if circ["southeast"] != "g":
                                # southwest and southeast is none
                                tile = Tile((16, 64), posX, posY)
                            else:
                                # southwest is none, but not southeast
                                tile = Tile((32, 80), posX, posY)
                        elif circ["southeast"] != "g":
                            # southeast is none, but not southwest
                            tile = Tile((48, 80), posX, posY)
                        else:
                            # southwest and southeast is filled
                            tile = Tile((16, 0), posX, posY)
                elif circ["west"] != "g":
                    if circ["east"] != "g":
                        if circ["south"] != "g":
                            # west east south = none, but not north
                            tile = Tile((48, 32), posX, posY)
                        else:
                            # west east = none, but not north south
                            tile = Tile((48, 16), posX, posY)
                    elif circ["south"] != "g":
                        # west south = none, but not north east
                        if circ["northeast"] != "g":
                            # northeast is none
                            tile = Tile((64, 32), posX, posY)
                        else:
                            # northeast is filled
                            tile = Tile((0, 32), posX, posY)
                    else:
                        # west = none, but not north east south
                        if circ["southeast"] != "g":
                            if circ["northeast"] != "g":
                                # southeast and northeast is none
                                tile = Tile((16, 80), posX, posY)
                            else:
                                # southeast is none, but not northeast
                                tile = Tile((64, 0), posX, posY)
                        elif circ["northeast"] != "g":
                            # northeast is none, but not southeast
                            tile = Tile((32, 96), posX, posY)
                        else:
                            # southeast and northeast is filled
                            tile = Tile((0, 16), posX, posY)
                elif circ["east"] != "g":   
                    if circ["south"] != "g":
                        # east south = none, but not north west
                        if circ["northwest"] != "g":
                            # northwest is none
                            tile = Tile((96, 32), posX, posY)
                        else:
                            # northwest is filled
                            tile = Tile((32, 32), posX, posY)
                    else:
                        # east = none, but not north west south
                        if circ["northwest"] != "g":
                            if circ["southwest"] != "g":
                                # northwest and southwest is none
                                tile = Tile((0, 80), posX, posY)
                            else:
                                # northwest is none, but not southwest
                                tile = Tile((48, 96), posX, posY)
                        elif circ["southwest"] != "g":
                            # southwest is none, but not northwest
                            tile = Tile((96, 0), posX, posY)
                        else:
                            # northwest and southwest is filled
                            tile = Tile((32, 16), posX, posY)
                elif circ["south"] != "g":
                    # south = none, but not north west east
                    if circ["northwest"] != "g":
                        if circ["northeast"] != "g":
                            # northwest and northeast is none
                            tile = Tile((80, 64), posX, posY)
                        else:
                            # northwest is none, but not northeast
                            tile = Tile((96, 64), posX, posY)
                    elif circ["northeast"] != "g":
                        # northeast is none, but not northwest
                        tile = Tile((64, 64), posX, posY)
                    else:
                        # northwest and northeast is filled
                        tile = Tile((16, 32), posX, posY)
                else:
                    # all directions are filled
                    if circ["northwest"] != "g":
                        if circ["southwest"] != "g":
                            if circ["southeast"] != "g":
                                if circ["northeast"] != "g":
                                    # all corners none
                                    tile = Tile((80, 16), posX, posY)  
                                else:
                                    # all corners none except northeast
                                    tile = Tile((80, 80), posX, posY)
                            elif circ["northeast"] != "g":
                                # all corners none except southeast
                                tile = Tile((64, 96), posX, posY)
                            else:
                                # northwest and southwest is none, northeast and southeast is filled
                                tile = Tile((0, 96), posX, posY)
                        elif circ["southeast"] != "g":
                            if circ["northeast"] != "g":
                                # all corners none except southwest
                                tile = Tile((80, 96), posX, posY)
                            else:
                                # northwest and southeast none, southwest and northeast filled
                                tile = Tile((96, 96), posX, posY)
                        elif circ["northeast"] != "g":
                            # northwest and northeast none, southwest and southeast filled
                            tile = Tile((80, 32), posX, posY)
                        else:
                            # northwest none, rest is filled
                            tile = Tile((0, 112), posX, posY)
                    elif circ["southwest"] != "g":
                        if circ["southeast"] != "g":
                            if circ["northeast"] != "g":
                                # southwest southeast northeast is none, northwest is filled
                                tile = Tile((64, 80), posX, posY)
                            else:
                                # southwest southeast is none, northwest northeast is filled
                                tile = Tile((80, 0), posX, posY)
                        elif circ["northeast"] != "g":
                            # southwest northeast is none, northwest southeast is filled
                            tile = Tile((96, 80), posX, posY)
                        else:
                            # southwest is none, northwest southeast northeast is filled
                            tile = Tile((96, 16), posX, posY)
                    elif circ["southeast"] != "g":
                        if circ["northeast"] != "g":
                            # southeast northeast is none, northwest southwest is filled
                            tile = Tile((16, 96), posX, posY)
                        else:
                            # southeast is none, northwest southwest northeast is filled
                            tile = Tile((64, 16), posX, posY)
                    elif circ["northeast"] != "g":
                        # northeast is none, northwest southwest southeast is filled
                        tile = Tile((16, 112), posX, posY)
                    else:
                        # all corners are filled
                        tile = Tile((16, 16), posX, posY)
                    

                self.tiles.append(tile)

        
    def look(self, list, start, shift):
        target = start + shift
        if 0 <= target < len(list):
            if list[target] == " ":
                return None
            return list[target]
        return None
    
