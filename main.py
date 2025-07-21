import pygame
from pygame import Vector2 as v2

pygame.init()

scr = (width, height) = (0, 0)
screen = pygame.display.set_mode((width, height))
width = pygame.display.Info().current_w
height = pygame.display.Info().current_h
#init clock for fps manipulation
clock = pygame.time.Clock()
#feel free to edit the fps of your game
fps = 60
game = True

OFFSET = v2(0, height//2 - (width//2))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SIZE = width//8

PAWN = 1
BISHOP = 2
KNIGHT = 3
ROOK = 4
QUEEN = 5
KING = 6

UP = -8
DOWN = 8
LEFT = -1
RIGHT = 1
UP_RIGHT = UP + RIGHT
UP_LEFT = UP + LEFT
DOWN_RIGHT = DOWN + RIGHT
DOWN_LEFT = DOWN + LEFT

PIECES_BITS = 7
COLOR_BITS = 8


def is_in_bounds(pos):
    return pos < 64 and pos >= 0

def piece_rank(index):
    return index // 8
def piece_file(index):
    return index % 8

def piece_type(piece):
    return piece & PIECES_BITS

def is_white(piece):
    return (piece & COLOR_BITS) != COLOR_BITS

def is_legal(piece, pos, dest):
    return dest in legal_moves(piece, pos)
    
def legal_moves(piece, pos):
    legals = []
    p_type = piece_type(piece)
    if p_type == PAWN:
        dir = -1
        if is_white(piece):
            dir = 1
        legals.append(pos + UP * dir)
        if piece_rank(pos) == 1 and is_white(piece):
            legals.append(pos + UP * 2)
        if piece_rank(pos) == 6 and not is_white(piece):
            legals.append(pos + DOWN * 2)
    if p_type == ROOK or p_type == QUEEN:
        i = 0
        while is_in_bounds(pos + UP * i):
            legals.append(pos + UP * i)
            i += 1
        i = 0
        while is_in_bounds(pos + DOWN * i):
            legals.append(pos + DOWN * i)
            i += 1
        i = 0
        while piece_rank(pos + RIGHT * i) == piece_rank(pos):
            legals.append(pos + RIGHT * i
            i += 1
        i = 0
        while piece_rank(pos + LEFT * i) == piece_rank(pos):
            legals.append(pos + LEFT * i)
            i += 1
    
    return legals

def render_piece(surface, piece, pos, size):
    if piece != 0:
        pygame.draw.circle(surface, (100, 100, 100), pos, size + 5)
        color = WHITE if is_white(piece) else BLACK
        pygame.draw.circle(surface, color, pos, size)

def render_board(pieces, surface, size):
    for i in range(64):
        pos = v2((i % 8) * size, (i//8) * size)
        square = pygame.Rect(pos + OFFSET, v2(size, size))
        color = BLACK if i % 2 + (i//8) % 2== 1 else WHITE
        pygame.draw.rect(surface, color, square)
        render_piece(surface, pieces[i], pos + OFFSET + v2(size) * 0.5, 25)


def translate(symbol):
    pieces = [p for p in "pbnrqk"]
    num = 0 if symbol.isupper() else 8
    return pieces.index(symbol.lower()) + 1 + num

def load_fen(fen):
    i = 0
    board = [0 for _ in range(64)]
    for symbol in fen:
        try:
            i += int(symbol)
        except:
            if symbol != '/':
                board[i] = translate(symbol)
                i += 1
    return board

board = load_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")

print(board)

turn_white = True
hand = 0
original_spot = 64

take = False
put = False
prev_click = False

while True:
    clock.tick(fps)
    
    cursor_pos = v2(pygame.mouse.get_pos())
    
    take = False
    put = False
    
    if not prev_click and pygame.mouse.get_pressed(3)[0]:
        take = True
    if prev_click and not pygame.mouse.get_pressed(3)[0]:
        put = True
    prev_click = pygame.mouse.get_pressed(3)[0]
    
    board_pos = (cursor_pos - OFFSET) // SIZE
    board_index = int(board_pos.x + board_pos.y * 8)
    
    
    if take:
        if hand == 0 and is_in_bounds(board_index):
            hand = board[board_index]
            original_spot = board_index
            board[board_index] = 0
    if put:
        if hand != 0 and is_in_bounds(board_index) and is_legal(hand, original_spot, board_index):
            board[board_index] = hand
            hand = 0
            original_spot = 64
        else:
            board[original_spot] = hand
            hand = 0
            original_spot = 64
    
    
    render_board(board, screen, width//8)
    if prev_click:
        render_piece(screen, hand, cursor_pos, 25)
    
    
    pygame.draw.circle(screen, "red", (board_pos * SIZE) + OFFSET + v2(SIZE, SIZE) * 0.5, 5)
    
    pygame.display.flip()
