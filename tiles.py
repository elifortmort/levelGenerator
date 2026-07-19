import pygame
from sprite import SpriteSheet

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile, x, y):
        super().__init__()
        ss = SpriteSheet("grassTiles.png")
        self.image = ss.get_image(tile[0], tile[1], 16, 16)

        self.rect = self.image.get_rect(topleft=(x, y))

class LevelGen:
    def __init__(self, text):
        self.text = text
        self.lines = []
        self.longest = 0
        self.tiles = []

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
                posX = x * 16
                posY = y * 16

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

                # if the symbyl is a space
                if " " in self.lines[y][x]:
                    continue
                
                
                if circ["north"] == None:
                    if circ["west"] == None:
                        if circ["east"] == None:
                            if circ["south"] == None:
                                # all directions are none
                                tile = Tile((48, 64), posX, posY)       
                            else:
                                # north west east = none, but not south
                                tile = Tile((48, 0), posX, posY)
                        elif circ["south"] == None:
                            # north west south = none, but not east
                            tile = Tile((0, 48), posX, posY)
                        else:
                            # north west = none, but not east south
                            if circ["southeast"] == None:
                                # if southeast = none
                                tile = Tile((0, 64), posX, posY)
                            else:
                                # if southeast is filled
                                tile = Tile((0, 0), posX, posY)
                    elif circ["east"] == None:
                        if circ["south"] == None:
                            # north east south = none, but not west
                            tile = Tile((32, 48), posX, posY)
                        else:
                            # north east = none, but not west south
                            if circ["southwest"] == None:
                                # if southwest is none
                                tile = Tile((32, 64), posX, posY)
                            else:
                                # if southwest is filled
                                tile = Tile((32, 0), posX, posY)
                    elif circ["south"] == None:
                        # north south = none, but not west east
                        tile = Tile((16, 48), posX, posY)
                    else:
                        # north = none, but not west east south
                        if circ["southwest"] == None:
                            if circ["southeast"] == None:
                                # southwest and southeast is none
                                tile = Tile((16, 64), posX, posY)
                            else:
                                # southwest is none, but not southeast
                                tile = Tile((32, 80), posX, posY)
                        elif circ["southeast"] == None:
                            # southeast is none, but not southwest
                            tile = Tile((48, 80), posX, posY)
                        else:
                            # southwest and southeast is filled
                            tile = Tile((16, 0), posX, posY)
                elif circ["west"] == None:
                    if circ["east"] == None:
                        if circ["south"] == None:
                            # west east south = none, but not north
                            tile = Tile((48, 32), posX, posY)
                        else:
                            # west east = none, but not north south
                            tile = Tile((48, 16), posX, posY)
                    elif circ["south"] == None:
                        # west south = none, but not north east
                        if circ["northeast"] == None:
                            # northeast is none
                            tile = Tile((64, 32), posX, posY)
                        else:
                            # northeast is filled
                            tile = Tile((0, 32), posX, posY)
                    else:
                        # west = none, but not north east south
                        if circ["southeast"] == None:
                            if circ["northeast"] == None:
                                # southeast and northeast is none
                                tile = Tile((16, 80), posX, posY)
                            else:
                                # southeast is none, but not northeast
                                tile = Tile((64, 0), posX, posY)
                        elif circ["northeast"] == None:
                            # northeast is none, but not southeast
                            tile = Tile((32, 96), posX, posY)
                        else:
                            # southeast and northeast is filled
                            tile = Tile((0, 16), posX, posY)
                elif circ["east"] == None:   
                    if circ["south"] == None:
                        # east south = none, but not north west
                        if circ["northwest"] == None:
                            # northwest is none
                            tile = Tile((96, 32), posX, posY)
                        else:
                            # northwest is filled
                            tile = Tile((32, 32), posX, posY)
                    else:
                        # east = none, but not north west south
                        if circ["northwest"] == None:
                            if circ["southwest"] == None:
                                # northwest and southwest is none
                                tile = Tile((0, 80), posX, posY)
                            else:
                                # northwest is none, but not southwest
                                tile = Tile((48, 96), posX, posY)
                        elif circ["southwest"] == None:
                            # southwest is none, but not northwest
                            tile = Tile((96, 0), posX, posY)
                        else:
                            # northwest and southwest is filled
                            tile = Tile((32, 16), posX, posY)
                elif circ["south"] == None:
                    # south = none, but not north west east
                    if circ["northwest"] == None:
                        if circ["northeast"] == None:
                            # northwest and northeast is none
                            tile = Tile((80, 64), posX, posY)
                        else:
                            # northwest is none, but not northeast
                            tile = Tile((96, 64), posX, posY)
                    elif circ["northeast"] == None:
                        # northeast is none, but not northwest
                        tile = Tile((64, 64), posX, posY)
                    else:
                        # northwest and northeast is filled
                        tile = Tile((16, 32), posX, posY)
                else:
                    # all directions are filled
                    if circ["northwest"] == None:
                        if circ["southwest"] == None:
                            if circ["southeast"] == None:
                                if circ["northeast"] == None:
                                    # all corners none
                                    tile = Tile((80, 16), posX, posY)  
                                else:
                                    # all corners none except northeast
                                    tile = Tile((80, 80), posX, posY)
                            elif circ["northeast"] == None:
                                # all corners none except southeast
                                tile = Tile((64, 96), posX, posY)
                            else:
                                # northwest and southwest is none, northeast and southeast is filled
                                tile = Tile((0, 96), posX, posY)
                        elif circ["southeast"] == None:
                            if circ["northeast"] == None:
                                # all corners none except southwest
                                tile = Tile((80, 96), posX, posY)
                            else:
                                # northwest and southeast none, southwest and northeast filled
                                tile = Tile((96, 96), posX, posY)
                        elif circ["northeast"] == None:
                            # northwest and northeast none, southwest and southeast filled
                            tile = Tile((80, 32), posX, posY)
                        else:
                            # northwest none, rest is filled
                            tile = Tile((0, 112), posX, posY)
                    elif circ["southwest"] == None:
                        if circ["southeast"] == None:
                            if circ["northeast"] == None:
                                # southwest southeast northeast is none, northwest is filled
                                tile = Tile((64, 80), posX, posY)
                            else:
                                # southwest southeast is none, northwest northeast is filled
                                tile = Tile((80, 0), posX, posY)
                        elif circ["northeast"] == None:
                            # southwest northeast is none, northwest southeast is filled
                            tile = Tile((96, 80), posX, posY)
                        else:
                            # southwest is none, northwest southeast northeast is filled
                            tile = Tile((96, 16), posX, posY)
                    elif circ["southeast"] == None:
                        if circ["northeast"] == None:
                            # southeast northeast is none, northwest southwest is filled
                            tile = Tile((16, 96), posX, posY)
                        else:
                            # southeast is none, northwest southwest northeast is filled
                            tile = Tile((64, 16), posX, posY)
                    else:
                        tile = Tile((16, 16), posX, posY)
                    # check northwest southwest southeast northeast respectively

                self.tiles.append(tile)

        
    def look(self, list, start, shift):
        target = start + shift
        if 0 <= target < len(list):
            if list[target] == " ":
                return None
            return list[target]
        return None
    
