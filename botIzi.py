import random


class Play(object):
    def __init__(self, y, x, dy, dx, priority):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.priority = priority


class Bot(object):
    def __init__(self, symbol, mode=0):
        """
        simbol: is the symbol of the bot
        mode: It is the game mode
        """
        self.symbol = symbol
        self.mode = mode
        # print(self.mode)

    def play(self, board):
        if(self.mode == 0):
            return self.randomPlay(board)
        if(self.mode == 1):
            return self.PlayMid(board)

    def PlayMid(self, board):
        """
        board: it is the board game
        """
        self.possiblePlays = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                if(board[i][j] == 0):
                    self.thinkPlay(i, j, board)
        return self.searchPlay(board)

    def thinkPlay(self, r, c, board):
        """
        r: it is the row of the position
        c: it is the column of the position
        board: it is the board game
        """
        # print("Pensando jugada: en ",r,",",c)
        for i in range(r-2, r+3):
            for j in range(c-2, c+3):
                if(i < 0 or i >= len(board)):
                    break
                if(j < 0 or j >= len(board[0])):
                    continue
                # print("Tal vez con ... ",i,",",j)
                if(board[i][j] != 0 and (i != r or j != c)):
                    self.evaluatePlay(i, j, r, c, board)

    def evaluatePlay(self, y, x, r, c, board):
        """
        y: it is the row of the position to be evaluated \n
        x: it is the column of the position to be evaluated \n
        r: it is the row of the position    \n
        c: it is the column of the position \n
        board: it is the board game
        """
        # print("Evaluando Jugada ","con ",y," ",x)
        if((abs(y-r) == 2 and abs(c-x) == 1) or (abs(x-c) == 2 and abs(y-r) == 1)):
            return
        if(y > r):
            dy = 1

        if(y == r):
            dy = 0

        if(y < r):
            dy = -1

        if(x > c):
            dx = +1

        if(x == c):
            dx = 0

        if(x < c):
            dx = -1
        self.evaluatePriority(dx, dy, r, c, y, x, board)

    def evaluatePriority(self, dx, dy, r, c, i, j, board):
        """
        """
        # print("Evaluando Prioridad ","con ","dx: ",dx," dy: ",dy)
        priority = 0
        y = r
        x = c
        if(y+dy >= 0 and y+dy < len(board) and x+dx >= 0 and x+dx < len(board[0]) and board[y+dy][x+dx] == board[i][j]):
            if(y+dy != i and x+dx != j):
                priority = priority+1
            else:
                if(y+dy*2 >= 0 and y+dy*2 < len(board) and x+dx*2 >= 0 and x+dx*2 < len(board[0]) and board[y+dy*2][x+dx*2] == board[i][j]):
                    priority = priority+1
            if(y-dy >= 0 and y-dy < len(board) and x-dx >= 0 and x-dx < len(board[0]) and board[y-dy][x-dx] == board[i][j] and dx >= 0 and dy >= 0):
                priority = priority+1
            if(priority > 0):
                self.addPlay(r, c, dy, dx, priority)

    def addPlay(self, r, c, dy, dx, priority):
        # print("Agregando jugada ",r," ",c)
        find = False
        for p in self.possiblePlays:
            # print(p.priority)
            if(p.x == c and p.y == r):
                if(p.dx != dx or p.dy != dy):
                    p.priority = p.priority+priority
                find = True
        if find is False:
            self.possiblePlays.append(Play(r, c, dy, dx,priority))

    def searchPlay(self, board):
        if(len(self.possiblePlays) == 0):
            return self.randomPlay(board)
        p = int(0)
        for i in range(1, len(self.possiblePlays)):
            if(self.possiblePlays[i].priority > self.possiblePlays[p].priority):
                p = int(i)
        return self.possiblePlays[p].x+self.possiblePlays[p].y*len(board[0])

    def randomPlay(self, board):
        """
        board: it is the board game
        """
        y = 0
        x = 0
        while(board[y][x] != 0):
            y = int(random.random()*len(board))
            x = int(random.random()*len(board[0]))
        return y*len(board[0])+x
