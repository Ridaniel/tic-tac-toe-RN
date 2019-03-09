import random

class bot(object):
    def __init__(self,simbol,mode=0):
        self.simbolo=simbol
        self.mode=mode
    
    def randomPlay(self,board):
        y=0
        x=0
        while(board[y][x]!=0):
            y=int(random.random()*len(board))
            x=int(random.random()*len(board[0]))
        return y*len(board[0])+x

    def play(self,board):
        if(self.mode==0):
            return self.randomPlay(board)
        if(self.mode==1):
            print("aún no esta implementada esa función")
        


        