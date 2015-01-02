#!/usr/local/bin/python3

import random

# Board generator
def generator(side):
    board = {}
    for x in range (side):
        for y in range (side):
            board[(x,y)] = 0
    board[(side//2, side//2)] = 2
    board[(side//2-1, side//2-1)] = 2
    board[(side//2, side//2-1)] = 1
    board[(side//2-1, side//2)] = 1
    return board

# Reads a file to import a board
def readFile(symbol):
    try:
        board = {}
        f = open('board.txt')
        lines = f.readline()
        x = 0
        y = len(lines.strip('\n').split(','))-1
        length = len(lines)
        while row != '':
            if len(lines) != length:
                raise ('Rows are not the same length')
            for column in lines.strip('\n').split(','):
                if column == symbol[0]:
                    board[(x, y)] = 0
                elif column == symbol[1]:
                    board[(x, y)] = 1
                elif column == symbol[2]:
                    board[(x, y)] = 2
                x += 1
            lines = f.readline()
            y -= 1
            x = 0
        f.close()
        return board, length//2
    except:
        print('Error encountered while importing file, generating new board')
        f.clos5e()
        raise

# Shows the board
def show(board, symbol, side):
    print(' '*4, end='')
    for x in range(side):
        print(x, end=' '*3)
    print()
    for y in range (side):
        print(' '*2+'-'*(side*4+1))
        print('{0} | '.format(y), end='')
        for x in range(side):
            print(symbol[board[(x,y)]], end=' | ')
        print()
    print(' '*2+'-'*(side*4+1))
   
    

# Checks a position for a status, returns false if position does not
# exist
def safe_check(board, coord, status):
    try:
        return board[coord] == status
    except KeyError:
        return False

# Checks if there are enemies around a given position
# and returns in which direction they are
# returns (Bool, [direction, ...])
def enemy_check(coord, enemy, board, side):
    directions= []
    for x in range (-1, 2):         #generate -1,0,1 and create (x,y) 
        for y in range (-1, 2):
            if (x, y) != (0, 0) and (0 < coord[0]+x < side and
                                     0 < coord[1]+y < side):
                if safe_check(board, (coord[0]+x, coord[1]+y), enemy):
                    directions.append((x,y))          # check if in the x,y is in the board
    if len(directions) == 0:
        return (False,)
    return (True, directions)

# Checks if there are allies in a certain direction
# returns (Bool, coord)
def ally_check(coord, direction, ally, board, side):
    x = coord[0] + direction[0]
    y = coord[1] + direction[1]
    while -1<x<side and -1<y<side and not safe_check(board, (x, y), 0):
        if safe_check(board, (x, y), ally):
            return (True, (x,y))
        x += direction[0]
        y += direction[1]
    return (False,)

# Finds out valid moves for a player
# moves = [[(move), (direction), (next_ally)], ...]
# moves_short = [(move), ...]
def valid(player, enemy, board, side):
    moves = []
    for move in board:
        if board[move] == 0:
            e_check = enemy_check(move, enemy, board, side)
            if e_check[0]:
                for direction in e_check[1]:
                    a_check = ally_check(move, direction, player, board, side)
                    if a_check[0]:
                        moves.append([move, direction, a_check[1]])
    moves_short = []
    for e in moves:
        if e[0] not in moves_short:
            moves_short.append(e[0])
    return moves, moves_short

# Shows a set of moves on the board as valid
def show_valid(board, moves_short, symbol, side):
    for move in board:
        if move in moves_short:
            board[move] = 3
    show(board, symbol, side)
    for move in board:
        if board[move] == 3:
            board[move] = 0

# Asks player for move
def ask_player(moves_short, board, symbol, side):
        move = ()
        while move not in moves_short:
            print('Move must be valid')
            move = input('Place your disc (x, y): ')
            move = move.split(',')
            try:
                for i in range (len(move)):
                    move[i] = int(move[i])
                move = tuple(move)
            except ValueError:
                move = ()
        return move

# Executes a move
def execute(moves, move, player, board):
    effects = []
    for e in moves:
        if e[0] == move:
            effects.append((e[1], e[2]))
    for effect in effects:
        x = move[0]
        y = move[1]
        while (x, y) != effect[1]:
            board[(x, y)] = player
            x += effect[0][0]
            y += effect[0][1]

# Handles a single turn
def turn(player, enemy, board, skip, turnCounter, symbol, side):
    print('Turn number {0}, player {1}: {2}'.format(turnCounter, player,
                                                    symbol[player]))
    moves, moves_short = valid(player, enemy, board, side)
    if len(moves_short) == 0:
        print('No valid moves for player {0}, turn skipped'.format(player))
        skip += 1
        turnCounter += 1
        return skip, turnCounter
    show_valid(board, moves_short, symbol, side)
    move = ask_player(moves_short, board, symbol, side)
    execute(moves, move, player, board)
    turnCounter += 1
    skip = 0
    return skip, turnCounter

# Figures out who won
def winner(board):
    p1 = 0
    p2 = 0
    for coord in board:
        if board[coord] == 1:
            p1 += 1
        if board[coord] == 2:
            p2 += 1
    if p1 > p2:
        return 1, p1, p2
    elif p2 > p1:
        return 2, p2, p1
    else:
        return False

# Checks if the board is full
def fullboard(board):
    for e in board:
        if board[e] == 0:
            return False
    return True

# Handles the whole game
def play():
    symbol = {0: ' ', 1: '*', 2: 'o', 3: '+'}
    try:
        board, side = readFile(symbol)
    except:
        side = 8
        board = generator(side)
    skip = 0
    turnCounter = 0
    player = 1
    enemy = 2
    while skip < 2 and not fullboard(board):
        skip, turnCounter = turn(player, enemy, board, skip,
                                 turnCounter, symbol, side)
        player, enemy = enemy, player
    show(board, symbol, side)
    win = winner(board)
    if not win:
        print('Tie')
    else:
        print('Player {0} wins, {1} to {2}.'.format(win[0], win[1], win[2]))
    print('The game has ended\nPress any key to exit')
    input()

play()
