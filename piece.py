class Position :

    def __init__(self, x, y) :
        self.x = x
        self.y = y

class Piece :

    def __init__(self, color, points, image=None, asc=None, x=0, y=0, square=0, hasMoved=False, enPassant=False) :
        self.position = Position(x, y)
        self.color = color
        self.points = points
        self.image = image
        self.asc = asc
        self.square = square
        self.hasMoved = hasMoved
        self.enPassant = enPassant

PieceMap = {
    "p": Piece(color=0, points=1, asc="♙", image="static/bp.svg"),
    "b": Piece(color=0, points=3, asc="♗", image="static/bb.svg"),
    "n": Piece(color=0, points=4, asc="♘", image="static/bn.svg"),
    "r": Piece(color=0, points=5, asc="♖", image="static/br.svg"),
    "q": Piece(color=0, points=9, asc="♕", image="static/bq.svg"),
    "k": Piece(color=0, points=1e10, asc="♔", image="static/bk.svg"),
    "P": Piece(color=1, points=1, asc="♟", image="static/wp.svg"),
    "B": Piece(color=1, points=3, asc="♝", image="static/wb.svg"),
    "N": Piece(color=1, points=4, asc="♞", image="static/wn.svg"),
    "R": Piece(color=1, points=5, asc="♜", image="static/wr.svg"),
    "Q": Piece(color=1, points=9, asc="♛", image="static/wq.svg"),
    "K": Piece(color=1, points=1e10, asc="♚", image="static/wk.svg")
}


