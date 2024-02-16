# Starting Position in FEN
# rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1

import pygame
from utilities import swap_attrs
from utilities import copy_attrs
from board import Board
from piece import Piece
from movegenerator import check_for_check
from movegenerator import canCastle

def renderImage (x, y, src) :
    if src == None :
        pass
    else:
        img = pygame.image.load(src)
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        screen.blit(img, (x, y))

def renderTile(x, y, dim, color) :
    pygame.draw.rect(screen, color, pygame.Rect(x, y, dim, dim))

TILE_SIZE = 100
SCREEN_WIDTH = SCREEN_HEIGHT = TILE_SIZE * 8

running, moves, selectedSquare, selected, castling = True, [], None, False, True
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", TILE_SIZE).setPosition()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN :
            if event.button == 1 :
                mouseX, mouseY = pygame.mouse.get_pos()
                i = mouseY // TILE_SIZE
                j = mouseX // TILE_SIZE
                if not selected :
                    if board.map[i*8+j].points > 0 and board.map[i*8+j].color == board.move:
                        selected = True
                        selectedSquare = i*8+j
                        piece_position_to_swap = [i, j]
                        moves = check_for_check(board, selectedSquare)
                        if board.map[i*8+j].points == 1e10 and board.map[i*8+j].hasMoved == False:
                            if canCastle(board)[0][0] :
                                moves.append(canCastle(board)[0][1])
                                castling = True
                            if canCastle(board)[1][0] :
                                moves.append(canCastle(board)[1][1])
                                castling = True
                            
                else :
                    x, y = piece_position_to_swap[0], piece_position_to_swap[1]
                    if i*8+j in moves :
                        board.map[x*8+y].hasMoved = True
                        if board.map[i*8+j].points == 0 :
                            if x != i and y != j :
                                if board.map[x*8+y].points == 1 and board.map[x*8+y].color == 0 :
                                    copy_attrs(Piece(None, 0, asc=" "), board.map[(i-1)*8+j], ["color", "points", "image", "asc"])
                                if board.map[x*8+y].points == 1 and board.map[x*8+y].color == 1 :
                                    copy_attrs(Piece(None, 0, asc=" "), board.map[(i+1)*8+j], ["color", "points", "image", "asc"])
                            swap_attrs(board.map[i*8+j], board.map[x*8+y], ["color", "points", "image", "asc"])
                            if i*8+j == 2 and castling :
                                swap_attrs(board.map[0], board.map[3], ["color", "points", "image", "asc"])
                                castling = False
                            if i*8+j == 6 and castling :
                                swap_attrs(board.map[5], board.map[7], ["color", "points", "image", "asc"])
                                castling = False
                            if i*8+j == 58 and castling :
                                swap_attrs(board.map[56], board.map[59], ["color", "points", "image", "asc"])
                                castling = False
                            if i*8+j == 62 and castling :
                                swap_attrs(board.map[61], board.map[63], ["color", "points", "image", "asc"])
                                castling = False
                            if board.map[i*8+j].points == 1 :
                                if x == 1 and i == 3 and board.map[i*8+j].color == 0 :
                                    board.map[i*8+j].enPassant = True
                                if x == 6 and i == 4 and board.map[i*8+j].color == 1 :
                                    board.map[i*8+j].enPassant = True
                            selected = False
                        else :
                            copy_attrs(board.map[x*8+y], board.map[i*8+j], ["color", "points", "image", "asc"])
                            if (x, y) != (i, j) :
                                copy_attrs(Piece(None, 0, asc=" "), board.map[x*8+y], ["color", "points", "image", "asc"])
                        for i in range(64) :
                            if board.move == 0 and board.map[i].points == 1 and board.map[i].color == 1 :
                                board.map[i].enPassant = False
                            if board.move == 1 and board.map[i].points == 1 and board.map[i].color == 0 :
                                board.map[i].enPassant = False
                        board.move = 0 if board.move == 1 else 1   
                    selected = False

    for i in range(64) :
        tile = board.tilemap[i]
        piece = board.map[i]
        if selected :
            if i in moves :
                tile.color = (250, 250, 0) if ((i // 8)+(i % 8))%2 == 0 else (150, 150, 0)
            elif i == selectedSquare :
                tile.color = 'grey'
        if selected == False :
            tile.color = "white" if ((i // 8)+(i % 8))%2== 0 else (220, 150, 220)
        renderTile(tile.x, tile.y, tile.dimension, tile.color)
        renderImage(piece.position.x, piece.position.y, piece.image)
        
        # font = pygame.font.SysFont(None, 24)
        # img = font.render(f'{i}', True, 'black')
        # img = font.render(f'{(i // 8),(i % 8)}', True, 'black')
        # screen.blit(img, (tile.x, tile.y))

    
    pygame.display.flip()
    clock.tick(60) 

pygame.quit()
