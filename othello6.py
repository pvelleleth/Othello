import sys; args = sys.argv[1:]

board = ''
global player, oddOrEven, finBoard,depth
depth=11
player = ''
finBoard = ''
global cache, movesCache, findMovesCache,moves, alphaBetaCache
alphaBetaCache = {}
movesCache = {}
findMovesCache = {}
cache = {}
moves = []
global cornerDict, cornToEdge, edgeToCorn # , dangerZone
cornerDict = {(0, 1): (0, 0), (1, 0): (0, 0), (1, 1): (0, 0), (0, 6): (0, 7), (1, 7): (0, 7), (1, 6): (0, 7),
              (6, 0): (7, 0), (7, 1): (7, 0), (6, 1): (7, 0), (7, 6): (7, 7), (6, 6): (7, 7), (6, 7): (7, 7)}
# dangerZone = {(2,1),(3,1),(4,1),(5,1),(1,2),(1,3),(1,4),(1,5),(2,6),(3,6),(4,6),(5,6),(6,2),(6,3),(6,4),(6,5)}
cornToEdge = {(0, 7): {(r, c) for r in range(1) for c in range(7)} | {(r, c) for r in range(1, 8) for c in range(7, 8)},
              (7, 0): {(r, c) for r in range(7) for c in [0]},
              (7, 7): {(r, c) for r in range(7) for c in range(7, 8)} | {(r, c) for r in [7] for c in range(7)}}
edgeToCorn = {i: j for j in cornToEdge for i in cornToEdge[j]}
oddOrEven = True

alpha = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
movePaths = {k: [] for k in range(64)}

for arg in args:
  if len(arg) == 64 and (not any(chr.isdigit() for chr in arg)):
    board = arg
  elif arg[:2]=="HL": depth=int(arg[2:])
  elif len(arg) == 1 and arg in 'XxOo':
    player = arg.upper()
    if (board.count('X') + board.count('O')) % 2 == 0:
      if player == 'X':
        oddOrEven = True
      else:
        oddOrEven = False
  elif len(arg) == 1 or len(arg) == 2:
    try:
      #depth=int(arg)
      if int(arg) >= 0:
        moves.append(arg)
    except Exception:
      moves.append(str((alpha.index(arg[0]) % 26) + 8 * (int(arg[1]) - 1)))
  else:
    for i in range(0, len(arg), 2):
      if '_' in arg[i:i + 2]:
        moves.append(arg[i:i + 2][1])
      else:
        if int(arg[i:i + 2]) > -1:
          moves.append(arg[i:i + 2])
#if depth>11: exit()
if len(board) == 0:
  board = '.' * 27 + "OX......XO" + '.' * 27
  #board= ""
  #tkn=1
else:
  board = board.upper()
if len(player) == 0:
  player = 'X' if (board.count('X') + board.count('O')) % 2 == 0 else 'O'
# board = '..................x.o.....ooxx...ooxxx.....ox.......o...........'.upper()
global boardArr
boardArr = [['' for i in range(8)] for k in range(8)]
boIter = iter(board)
for i in range(8):
  for j in range(8):
    boardArr[i][j] = next(boIter)


# print(boardArr)
def printBoard(board, cond='ff'):
  # for i in range(0, 64, 8):
  # print(''.join(board[i:i + 8]))
  toRet = ''
  if cond != 'ff':
    for i in board:
      toRet += ''.join(i)
  else:
    for i in board:
      toRet += ''.join(i) + '\n'
  return toRet


# print(moves)


def checkPath(boardd, row, col, drow, dcol, player):
  opponent = 'O' if player == 'X' else 'X'
  key = col + 8 * row
  row += drow
  col += dcol
  if row < 0 or row >= 8 or col < 0 or col >= 8 or boardd[row][col] == '.' or boardd[row][col] == '*':
    return False
  if boardd[row][col] != opponent:
    return False
  toAdd = []
  toAdd.append(col + 8 * row)
  while True:
    row += drow
    col += dcol
    if row < 0 or row >= 8 or col < 0 or col >= 8 or boardd[row][col] == '.' or boardd[row][col] == '*':
      toAdd = []
      return False
    if boardd[row][col] == player:
      movePaths[key] += toAdd
      return True
    if boardd[row][col] == opponent:
      toAdd.append(col + 8 * row)
      continue


def findMoves(boarda, player):
  global findMovesCache
  player = player.upper()
  if type(boarda)==str: boarda = boarda.upper()
  possible_moves = set()
  if (str(boarda), player) in findMovesCache: return findMovesCache[(boarda, player)]
  if type(boarda) == str:
    boardAr = [['' for i in range(8)] for k in range(8)]
    boIte = iter(boarda)
    for i in range(8):
      for j in range(8):
        boardAr[i][j] = next(boIte)
    # check all cells of the board
    for row in range(8):
      for col in range(8):
        # if the cell is empty, check if it is a possible move
        if boardAr[row][col] in '.*':
          # check the eight directions around the cell
          for drow, dcol in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            
            if checkPath(boardAr, row, col, drow, dcol, player):
              possible_moves.add((row, col))
  else:
    # check all cells of the board
    for row in range(8):
      for col in range(8):
        # if the cell is empty, check if it is a possible move
        if boarda[row][col] in '.*':
          # check the eight directions around the cell
          for drow, dcol in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            
            if checkPath(boarda, row, col, drow, dcol, player):
              possible_moves.add((row, col))

            # break
  findMovesCache[(str(boarda), player)] = possible_moves
  return possible_moves


def display(board):
  for i in range(8):
    print(board[i * 8:(i + 1) * 8])


def stats(board, token, i):
  print("Player " + token + " moves to " + str(i))
  oppT = 'O' if token == 'X' else 'X'
  locs = findMoves(board, oppT)
  for loc in locs:
    board = board[:loc[0] * 8 + loc[1]] + '*' + board[loc[0] * 8 + loc[1] + 1:]
  display(board)
  print('')
  for loc in locs:
    board = board[:loc[0] * 8 + loc[1]] + '.' + board[loc[0] * 8 + loc[1] + 1:]
  xc = board.count('X')
  oc = board.count('O')
  
  print(board, str(xc) + '/' + str(oc))
  if locs:
    print('Possible moves for', oppT + ':', str(loc[0] * 8 + loc[1])[1:-1])
  else:
    print('Possible moves for', oppT + ': No moves possible')


def makeMove(board, token, i):
  global movesCache
  i = int(i)
  board = board.replace("*", ".")
  token = token.upper()
  board = board.upper()
  if (board, token, i) in movesCache: return movesCache[(board, token, i)]
  opponent = 'O' if token == 'X' else 'X'
  if i % 8 > 0:
    temp = 1
    while (i - temp) % 8 > 0 and board[i - temp] == opponent:
      temp += 1
    if temp > 1 and board[i - temp] == token:
      for j in range(temp):
        board = board[:i - j] + token + board[i - j + 1:]
  if i % 8 < 8 - 1:
    temp = 1
    while (i + temp) % 8 != 8 - 1 and board[i + temp] == opponent:
      temp += 1
    if temp > 1 and board[i + temp] == token:
      for j in range(temp):
        board = board[:i + j] + token + board[i + j + 1:]
  if i // 8 > 0:
    temp = 1
    while i - temp * 8 >= 8 and board[i - temp * 8] == opponent:
      temp += 1
    if temp > 1 and board[i - temp * 8] == token:
      for j in range(temp):
        board = board[:i - j * 8] + token + board[i - j * 8 + 1:]
  if i // 8 < 8 - 1:
    temp = 1
    while i + temp * 8 < (8 - 1) * 8 and board[i + temp * 8] == opponent:
      temp += 1
    if temp > 1 and board[i + temp * 8] == token:
      for j in range(temp):
        board = board[:i + j * 8] + token + board[i + j * 8 + 1:]
  if i % 8 > 0 and i // 8 > 0:
    temp = 1
    while i % 8 - temp > 0 and i - temp * 8 >= 8 and board[
      i - temp * 8 - temp] == opponent:
      temp += 1
    if temp > 1 and board[i - temp * 8 - temp] == token:
      for j in range(temp):
        board = board[:i - j * 8 - j] + token + board[i - j * 8 - j + 1:]
  if i % 8 < 8 - 1 and i // 8 < 8 - 1:
    temp = 1
    while (i + temp) % 8 < 8 - 1 and i + temp * 8 < (8 - 1) * 8 and \
      board[i + temp * 8 + temp] == opponent:
      temp += 1
    if temp > 1 and board[i + temp * 8 + temp] == token:
      for j in range(temp):
        board = board[:i + j * 8 + j] + token + board[i + j * 8 + j + 1:]
  if i % 8 > 0 and i // 8 < 8 - 1:
    temp = 1
    while i % 8 - temp > 0 and i + temp * 8 < (8 - 1) * 8 and board[
      i + temp * 8 - temp] == opponent:
      temp += 1
    if temp > 1 and board[i + temp * 8 - temp] == token:
      for j in range(temp):
        board = board[:i + j * 8 - j] + token + board[i + j * 8 - j + 1:]
  if i % 8 < 8 - 1 and i // 8 > 0:
    temp = 1
    while (i + temp) % 8 < 8 - 1 and i - temp * 8 >= 8 and board[
      i - temp * 8 + temp] == opponent:
      temp += 1
    if temp > 1 and board[i - temp * 8 + temp] == token:
      for j in range(temp):
        board = board[:i - j * 8 + j] + token + board[i - j * 8 + j + 1:]
  # stats(board,token,i)
  board = list(board)
  for c in range(len(board)):
    if c==i:
      board[c]=board[c].lower()
  board = ''.join(board)
  movesCache[(board, token, i)] = board
  return board


def remAsterisks(board):
  for i in range(8):
    for j in range(8):
      if board[i][j] == '*':
        board[i][j] = '.'
  return board


def quickMove(brd, tkn):
  # if type(brd)==str:
  # cornerDict = {(0,1):(0,0),(1,0):(0,0),(1,1):(0,0),(0,6):(0,7),(1,7):(0,7),(1,6):(0,7),(6,0):(7,0),(7,1):(7,0),(6,1):(7,0),(7,6):(7,7),(6,6):(7,7),(6,7):(7,7)}
  #brd = brd.upper()
  #tkn = tkn.upper()
  # if brd.count('.')<4:
  # print("foo")
  # print(f"{brd=}")
  global depth
  bd = ''.join(str(item) for il in brd for item in il)
  if bd =="" or brd=="":
    depth=tkn
    return
  bd = bd.replace("*", ".")
  
  if (bd.count('.')) < depth:
    # print(bd, tkn)
    # print(bd, tkn)
    # print(bd)
    #er = negamax(bd, tkn)
    er = alphabeta(bd, tkn, -64, 64)
    # print(er)
    # print(mvSq)
    return er[-1]
  
  goodMoves = set()
  oTkn = 'O' if tkn == 'X' else 'X'
  
  boardAr = [['' for i in range(8)] for k in range(8)]
  boIte = iter(bd)
  for i in range(8):
    for j in range(8):
      boardAr[i][j] = next(boIte)
  psblMoves = findMoves(brd, tkn)
  
  for k in psblMoves:
    rating = 0
    if k in {(0, 0), (0, 7), (7, 0), (7, 7)}:
      rating += 10
    elif k in edgeToCorn:
      if boardAr[edgeToCorn[k][0]][edgeToCorn[k][1]] == tkn:
        rating += 9
    if k in cornerDict:
      if boardAr[cornerDict[k][0]][cornerDict[k][1]] == tkn:
        rating += 9
      elif boardAr[cornerDict[k][0]][cornerDict[k][1]] == '.':
        rating = -1000
      elif boardAr[cornerDict[k][0]][cornerDict[k][1]] == oTkn:
        rating = -1000
    goodMoves.add((rating, k))
  
  fin = max(goodMoves)[1]
  return fin[1] + 8 * fin[0]


def alphabeta(brd, tkn, lowerBnd, upperBnd):
  
  eTkn = 'O' if tkn == 'X' else 'X'
  brd = brd.replace("*", ".")
  if not findMoves(brd, tkn):
    if not findMoves(brd, eTkn):
      return [brd.count(tkn) - brd.count(eTkn)]
    
    #ab = alphabeta(brd, eTkn, -lowerBnd, -upperBnd)
    ab = alphabeta(brd, eTkn, -65, 65)
    return [-ab[0]] + ab[1:] + [-1]
    # return the right thing
  best = [lowerBnd - 1]
  for mv in findMoves(brd, tkn):
    ab = alphabeta(makeMove(brd, tkn, mv[0] * 8 + mv[1]), eTkn, -upperBnd, -lowerBnd)
    score = -ab[0]
    if score < lowerBnd: continue
    if score > upperBnd: return [score]
    best = [-ab[0]] + ab[1:] + [mv[0] * 8 + mv[1]]
    lowerBnd = score + 1
  return best
  
def negamax(brd, tkn):
  global cache
  eTkn = 'O' if tkn == 'X' else 'X'
  brd = brd.replace("*", ".")
  if brd.count('.') == 0: return [brd.count(tkn) - brd.count(eTkn)]
  if (brd, tkn) in cache:
    return cache[(brd, tkn)]
  if not findMoves(brd, tkn):
    if findMoves(brd, eTkn):
      nmO = negamax(brd, eTkn)
      bestSoFar = [-nmO[0]] + nmO[1:] + [-1]
    else:
      return [brd.count(tkn) - brd.count(eTkn)]
  else:
    bestSoFar = [-65]
    for mv in findMoves(brd, tkn):
      newBrd = makeMove(brd, tkn, mv[0] * 8 + mv[1])
      # print(newBrd)
      nm = negamax(newBrd, eTkn)
      if -nm[0] > bestSoFar[0]:
        bestSoFar = [-nm[0]] + nm[1:] + [mv[0] * 8 + mv[1]]
  cache[(brd, tkn)] = bestSoFar
  return bestSoFar


def main():
  #checkShow=True
  global player, oddOrEven,boardArr
  possMoves = findMoves(boardArr, player)
  if len(possMoves) == 0:
    player = 'O' if player == 'X' else 'X'
    # oddOrEven = False if oddOrEven else True
    possMoves = findMoves(boardArr, player)
  pMoves = []
  tempPrint = boardArr.copy()
  for p in possMoves:
    boardArr[p[0]][p[1]] = '*'
  
  for p in possMoves:
    pMoves.append(p[1] + 8 * p[0])
  
  print(printBoard(boardArr))
  # print()
  temp = printBoard(tempPrint, 'flat')
  print(temp.replace('*', '.'), end='')
  
  print(" " + str(sum(x.count('X') for x in boardArr)) + '/' + str(sum(x.count('O') for x in boardArr)))
  
  if pMoves:
    print("Possible moves for " + player + ': ' + ', '.join(list(map(str, pMoves))))
  else:
    print('No moves possible')
  print()
  #print(moves)
  for m in moves:
    # player,pMoves = makeMove(m,pMoves,boardArr)
    print(player+" plays to "+m)
    booard = makeMove(''.join(str(item) for il in boardArr for item in il), player, int(m))
    #print(booard)
    player = 'O' if player == 'X' else 'X'
    booard2 = booard.upper()
    if not findMoves(booard2, player): player = 'O' if player == 'X' else 'X'
    movesPossibO = findMoves(booard2, player)
    pMoves = []
    for p in movesPossibO:
      pMoves.append(p[1] + 8 * p[0])
    booard = list(booard)
    for p in pMoves:
      booard[p]='*'
    booard = ''.join(booard)
    display(booard)
    booard = booard.upper()
    print(booard.replace("*","."),end='')
    print(" " + str(booard.count('X')) + '/' + str(booard.count('O')))
    
    if pMoves:
      print("Possible moves for " + player + ': ' + ', '.join(list(map(str, pMoves))))
    else:
      #checkShow = False
      #print('No moves possible')
      pass
    print()
    boardArr = [['' for i in range(8)] for k in range(8)]
    boIter = iter(booard)
    for i in range(8):
      for j in range(8):
        boardArr[i][j] = next(boIter)
  # print(movePaths)
  '''
  if pMoves:
    print(set(pMoves))
  else:
    print('No moves possible') '''

  # possy = findMoves(boardArr,player)
  if pMoves:
    # print(''.join(str(item) for il in boardArr for item in il))
    
    mv = quickMove(boardArr, player)
    # stats(''.join(str(item) for il in boardArr for item in il),player,mv)
    print(f'My preferred move is: {mv}')
    # exit()
  boad = ''.join(str(item) for il in boardArr for item in il)
  boad = boad.replace("*", ".")
  if boad.count('.') < depth:
    #nm = negamax(boad, player)
    nm = alphabeta(boad,player,-64,64)
    print(f"Min score: {nm[0]}; move sequence: {nm[1:]}")
    


if __name__ == '__main__':
  main()
  # print(findMoves("...........................ox......xo...........................",'X'))
  # print(negamax("xxxxooooxxoxooooxxxooxooxxxxxxx..xxoooxxooxxoxxxoooxxxxxx.oxxxxx".upper(),"O"))


