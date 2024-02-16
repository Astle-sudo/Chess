import copy
from piece import Piece
from utilities import swap_attrs
from utilities import copy_attrs

# Directions for Queen, Rook, Bishop and King along with the Knight
directions = [(1, 0), (0, 1), (-1, 0), (0, -1),(1, 1), (-1, 1), (-1, -1), (1, -1)]
kdirections = [(2, 1), (2, -1), (-2, 1), (-2, -1),(-1, 2), (1, 2), (-1, -2), (1, -2)]

class vector :

    def __init__(self, l) :
        self.data = l
    
    def __add__ (self, other) :
        new = []
        for i in range(len(self.data)) :
            new.append(self.data[i] + other[i])
        return vector(new)
    
    def __getitem__(self, item) :
        return self.data[item]
    
    def square (self) :
        return self.data[0] * 8 + self.data[1]
    
def generateMoves (startPosition, Map, directions) :
    all = []
    startPosition = vector(startPosition)
    for  i in directions :
        all += moves(startPosition, i, Map, [], startPosition)
    return sorted(all)

def moves (start, direction, Map, pos, og) :
    start += direction

    # Check if the moves are beyond the board's boundary
    if start.data[0] >= 8 or start.data[1] >= 8 or start.data[0] < 0 or start.data[1] < 0 :
        return pos
    
    # Make sure there is a piece in that square, and of opposite color before adding it to
    # legal moves.
    if Map[start.data[0]*8+start.data[1]].points > 0 :
        if Map[start.data[0]*8+start.data[1]].color != Map[og.data[0]*8+og.data[1]].color :
            pos.append(start.data[0] * 8 + start.data[1])
        return pos
    pos.append(start.data[0] * 8 + start.data[1])

    # If it's a king or a knight, terminate the loop after one iteration
    if Map[og.data[0]*8+og.data[1]].points == 1e10 or Map[og.data[0]*8+og.data[1]].points == 4 :
        return pos
    return moves(start, direction, Map, pos, og)

def pawn_moves (startPosition, Map, pdirections) :
    pos = []
    startPosition = vector(startPosition)
    diagonals = pdirections[:2]

    # Look in the diagonal positions for a piece of opposite color, if present, add
    # the move to the legal moves.
    for direction in diagonals :
        move = startPosition + vector(direction)
        if 0 <= move.data[0] < 8 and 0 <= move.data[1] < 8 and Map[move.square()].color != None:
            if Map[move.square()].color != Map[startPosition.square()].color :
                pos.append(move.square())
        if 0 <= move.data[0] < 8 and 0 <= move.data[1] < 8 and Map[move.square()].color == None:
            if Map[startPosition.square()].color == 0 :
                if Map[(move+vector([-1, 0])).square()].points == 1 :
                    if Map[(move+vector([-1, 0])).square()].enPassant :
                        pos.append(move.square())
            if Map[startPosition.square()].color == 1 :
                if Map[(move+vector([1, 0])).square()].points == 1 :
                    if Map[(move+vector([1, 0])).square()].enPassant :
                        pos.append(move.square())

    # Check the usual conditions for the move.
    move = startPosition + vector(pdirections[2])
    if Map[move.square()].points == 0 and (0 <= move.data[0] < 8 and 0 <= move.data[1] < 8) :
        pos.append(move.square())

    # Special case of the first pawn move for white and black
    if startPosition.data[0] == 1 and Map[startPosition.square()].color == 0 :
        if Map[move.square()].points == 0 and Map[(startPosition+vector(pdirections[3])).square()].points == 0 :
            pos.append((startPosition+vector(pdirections[3])).square())

    if startPosition.data[0] == 6 and Map[startPosition.square()].color == 1 :
        if Map[move.square()].points == 0 and Map[(startPosition+vector(pdirections[3])).square()].points == 0 :
            pos.append((startPosition+vector(pdirections[3])).square())
    
    return pos


def legalMoves (piece, board) :

    # Generate moves according to each piece given below.
    startPosition = (piece.square // 8 , piece.square % 8)
    if piece.points == 1e10 :
        legalMoves = generateMoves(startPosition, board.map, directions)
    if piece.points == 9 :
        legalMoves = generateMoves(startPosition, board.map, directions)
    if piece.points == 5 :
        legalMoves = generateMoves(startPosition, board.map, directions[0:4])
    if piece.points == 3 :
        legalMoves = generateMoves(startPosition, board.map, directions[4:8])
    if piece.points == 4 :
        legalMoves = generateMoves(startPosition, board.map, kdirections)
    if piece.points == 1 and piece.color == 0:
        legalMoves = pawn_moves(startPosition, board.map, [(1, -1), (1, 1),(1, 0), (2, 0)])
    if piece.points == 1 and piece.color == 1:
        legalMoves = pawn_moves(startPosition, board.map, [(-1, 1), (-1, -1),(-1, 0), (-2, 0)])
    return legalMoves

def makeMove (board, pieceSquare, move) :

    # To make a move, first check if the other square is empty or not. If empty, simply swap the 
    # pieces, them being a piece and an empty Piece object. If it is occupied by another piece, copy
    # the piece to the other square and create an empty Piece object in it's stead.
    temp = copy.deepcopy(board)
    if temp.map[move].points == 0 :
        swap_attrs(temp.map[move], temp.map[pieceSquare], ["color", "points", "image", "asc"])
    else :
        copy_attrs(temp.map[pieceSquare], temp.map[move], ["color", "points", "image", "asc"])
        if (pieceSquare) != (move) :
            copy_attrs(Piece(None, 0, asc=" "), temp.map[pieceSquare], ["color", "points", "image", "asc"])
    return temp


def check_for_check (board, square) :

    # Get all the legal moves of the piece
    legalmoves = legalMoves(board.map[square], board)
    lm = copy.deepcopy(legalmoves)
    for move in legalmoves :

        opponentMoves = []

        # Create a Board instance with the move being made already.
        newBoard = makeMove(board, board.map[square].square, move)

        # Loop over the new board.
        for i in range(64) :

            # Get our King's position.
            if newBoard.map[i].points == 1e10 and newBoard.map[i].color == board.map[square].color :
                king = newBoard.map[i]
            
            # Get all the legal moves of the opposition.
            if newBoard.map[i].points > 0 and newBoard.map[i].color != board.map[square].color :
                opponentMoves += legalMoves(newBoard.map[i], newBoard)
                
        # Check if opposition has any attack on the king, after this move. If yes, remove this
        # move from legal moves.
        for oppoMove in opponentMoves :
            if oppoMove == king.square :
                lm.remove(move)
                break
    return lm

def checkSquares (board, squares) :
    for i in squares :
        if board.map[i].points != 0 :
            return False
    return True

def opponentStrike (board, squares) :
    opponentMoves = []
    for i in range(64) :
        if board.map[i].points > 0 and board.map[i].color != board.move :
            opponentMoves += legalMoves(board.map[i], board)
    return set(squares).intersection(set(opponentMoves))

def canCastle (board) :
    blackLong = [1, 2, 3]
    blackShort = [5, 6]
    whiteLong = [57, 58, 59]
    whiteShort = [61, 62]
    if board.move == 1 :
        s, l = [], []
        if checkSquares(board, whiteShort) and board.map[63].hasMoved == False and not opponentStrike(board, whiteShort + [60]):
            s += [True, 62]
        else :
            s.append(False)
        if checkSquares(board, whiteLong) and board.map[56].hasMoved == False and not opponentStrike(board, whiteLong + [60]):
            l += [True, 58]
        else :
            l.append(False)
        return [s, l]
    
    if board.move == 0 :
        s, l = [], []
        if checkSquares(board, blackShort) and board.map[7].hasMoved == False and not opponentStrike(board, blackShort + [4]):
            s += [True, 6]
        else :
            s.append(False)
        if checkSquares(board, blackLong) and board.map[0].hasMoved == False and not opponentStrike(board, blackLong + [4]):
            l += [True, 2]
        else :
            l.append(False)
        return [s, l]