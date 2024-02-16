from piece import PieceMap
from piece import Piece
from utilities import convert

class Tile :

    def __init__(self, dimension, color, x=0, y=0, ) :
        self.x = x
        self.y = y
        self.dimension = dimension
        self.color = color

class Board :

    def __init__(self, FEN, tile_size) :
        Map = dict()
        tilemap = dict()

        assert len(FEN.split(' ')) == 6
        positions, move, _, _, _, _ = FEN.split(' ') 
        positions = positions.split('/')

        for i in range(8) :
            for j in range(len(convert(positions[i]))) :

                color = "white" if (i+j)%2 == 0 else (220, 150, 220)
                tilemap[i*8+j] = Tile(tile_size, color)

                if convert(positions[i])[j] == 0 :
                    Map[i*8+j] = Piece(None, 0, asc=' ', square=i*8+j)
                else :
                    Map[i*8+j] = Piece(
                        square=i*8+j,
                        color=PieceMap[convert(positions[i])[j]].color, 
                        image=PieceMap[convert(positions[i])[j]].image,
                        asc=PieceMap[convert(positions[i])[j]].asc,
                        points=PieceMap[convert(positions[i])[j]].points
                    )
            
        self.map = Map
        self.tilemap = tilemap
        self.tile_size = tile_size
        self.move = 1 if move == 'w' else 0

    def box (self, piece=' ') :
        return "|" + str(piece) + "|"
    
    def setPosition(self) :
        for i in range(8) : 
            for j in range(8) :
                self.map[i*8+j].position.x = j * self.tile_size
                self.map[i*8+j].position.y = i * self.tile_size
                self.tilemap[i*8+j].x = j * self.tile_size
                self.tilemap[i*8+j].y = i * self.tile_size
        return self
    
    def render(self) :
        print()
        print(" _  _  _  _  _  _  _  _")
        for i in range(8) :
            for j in range(8) :
                if j != 7 :
                    print(self.box(piece=self.map[i*8+j].asc), end="")
                else:
                    print(self.box(piece=self.map[i*8+j].asc))
            print(" -  -  -  -  -  -  -  -", end="")
            print()
        print()

