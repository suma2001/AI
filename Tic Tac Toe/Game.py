import pygame as pg
import itertools

class Game():  
    
    def __init__(self):
        self.gridsize=3
        global player
        global computer
        global algo
        player='x'
        computer='o'

        self.windowsize=600
        self.screen=pg.display.set_mode((self.windowsize+10,self.windowsize+10),0,32)

        self.border=5
        self.box_size=self.windowsize//self.gridsize
        self.box_width=self.box_size-(2*self.border)
        self.box_height=self.box_size-(2*self.border)
        global board
        board=[['_' for i in range(3)]for j in range(3)]


    def __str__(self):
        s=''
        for i in range(3):
            for j in range(3):
                s+=board[i][j]+" "
        return s

    def createboard(self):
        pg.display.set_caption("Tic-Tac-Toe")
        self.screen.fill((0,0,0))

    def displaytext(self,string,pos,color,flag):
        font=pg.font.SysFont(None,self.windowsize//18)
        string=string+str(flag)
        text=font.render(string,True,color)
        self.screen.blit(text,pos)

    def displaystr(self,string,pos,color):
        font=pg.font.SysFont(None,self.windowsize//18)
        text=font.render(string,True,color)
        self.screen.blit(text,pos)

    def lines(self):
        for i in range(1,4):
            start_position = ((self.box_size * i) + (5 * (i - 1))) + self.border
            width = self.screen.get_width() - (2 * self.border)
            pg.draw.rect(self.screen,((255,255,255)), (start_position,self.border,6, width))
            pg.draw.rect(self.screen,((255,255,255)), (self.border, start_position, width, 6))


    def center_coordinates(self,x,y):
        xcoord=y*self.box_size+(self.box_width)/2 - self.windowsize/20
        ycoord=x*self.box_size+(self.box_height)/2 - self.windowsize/20
        return (xcoord,ycoord)

    def mark_x(self,x,y):
        board[x][y]='x'
        print(board)
        font=pg.font.SysFont(None,self.windowsize//5)
        text=font.render("X",True,(21,244,238))
        self.screen.blit(text,self.center_coordinates(x,y))

    def mark_o(self,x,y):
        board[x][y]='o'
        print(board)
        font=pg.font.SysFont(None,self.windowsize//5)
        text=font.render("O",True,(255,20,147))
        self.screen.blit(text,self.center_coordinates(x,y))

    def human(self,x,y):
        for i in range(3):
            for j in range(3):
                tile=pg.Rect(j*self.box_size,i*self.box_size,self.box_width,self.box_height)
                if tile.collidepoint((x,y))==1 and board[i][j]=='_' :
                    self.mark_x(i,j)
                    return True
        else:
            return False

    def movesleft(self):
        for i in range(3):
            for j in range(3):
                if board[i][j]=='_':
                    return True
        return False

    def lineheuristic(self, row1, col1, row2, col2, row3, col3):
        b=board
        # b=[['_', '_', '_'], ['_', 'x', '_'], ['o', '_', '_']]
        score=0
        if b[row1][col1]==player:
            score = 1 
        elif b[row1][col1]==computer:
            score = -1

        if b[row2][col2]==player:
            if score==1:
                score=10
            elif score==-1:
                return 0
            else:
                score=1
        elif b[row2][col2]==computer:
            if score==-1:
                score=-10
            elif score==1:
                return 0
            else:
                score=-1

        if b[row3][col3]==player:
            if score>0:
                score=score*10
            elif score<0:
                return 0
            else:
                score=1
        elif b[row3][col3]==computer:
            if score<0:
                score*=10
            elif score>1:
                return 0
            else:
                score=-1
        return score

    def heuristic(self):
        score=0
        # print(self.lineheuristic(0, 0, 0, 1, 0, 2))
        # print(self.lineheuristic(1, 0, 1, 1, 1, 2))
        # print(self.lineheuristic(2, 0, 2, 1, 2, 2))
        # print(self.lineheuristic(0, 0, 1, 0, 2, 0))
        # print(self.lineheuristic(0, 1, 1, 1, 2, 1))
        # print(self.lineheuristic(0, 2, 1, 2, 2, 2))
        # print(self.lineheuristic(0, 0, 1, 1, 2, 2))
        # print(self.lineheuristic(0, 2, 1, 1, 2, 0))

        score+=self.lineheuristic(0, 0, 0, 1, 0, 2)
        score+=self.lineheuristic(1, 0, 1, 1, 1, 2)
        score+=self.lineheuristic(2, 0, 2, 1, 2, 2)
        score+=self.lineheuristic(0, 0, 1, 0, 2, 0)
        score+=self.lineheuristic(0, 1, 1, 1, 2, 1)
        score+=self.lineheuristic(0, 2, 1, 2, 2, 2)
        score+=self.lineheuristic(0, 0, 1, 1, 2, 2)
        score+=self.lineheuristic(0, 2, 1, 1, 2, 0)
        return score

    def eval(self):
        b=board
        for i in range(3):
            if (b[i][0]==b[i][1] and b[i][1]==b[i][2]):
                if(b[i][0]==player):
                    return 10
                elif (b[i][0]==computer):
                    return -10
        for i in range(3):
            if (b[0][i]==b[1][i] and b[1][i]==b[2][i]):
                if(b[0][i]==player):
                    return 10
                elif (b[0][i]==computer):
                    return -10

        if (b[0][0]==b[1][1] and b[1][1]==b[2][2]):
            if (b[0][0]==player):
                return 10
            elif (b[0][0]==computer):
                return -10

        if (b[0][2]==b[1][1] and b[1][1]==b[2][0]):
            if(b[0][2]==player):
                return 10
            elif(b[0][2]==computer):
                return -10
        if(not self.movesleft()):
            return 0
        return -1

    def miniMax(self, Max):

        score=self.eval()

        if score!=-1:
            return score

        if Max:
            best=-1000000
            for i in range(3):
                for j in range(3):
                    if (board[i][j]=='_'):
                        board[i][j]=player
                        val=self.miniMax(not Max)
                        best=max(best,val)
                        board[i][j]='_'
            return best
        else:
            best=1000000
            for i in range(3):
                for j in range(3):
                    if (board[i][j]=='_'):
                        board[i][j]=computer
                        val=self.miniMax(not Max)
                        best=min(best,val)
                        board[i][j]='_'
            return best


    def depthLimit(self, Max, depth):
        # score, choice = GetScore()
        # if depth == 0 or score == WIN or score == LOSE:
        #     return score, game
        utility=self.eval()
        score = self.heuristic()
        # print("Heuristic is :", score)
        # if(not self.movesleft()):
        #     return 0
        if depth==0 or utility!=-1:
            return score
        # if score!=-1:
        #     return score

        if Max:
            best=-1000000
            for i in range(3):
                for j in range(3):
                    if (board[i][j]=='_'):
                        board[i][j]=player
                        val=self.depthLimit(not Max,depth-1)
                        best=max(best,val)
                        board[i][j]='_'
            return best
        else:
            best=1000000
            for i in range(3):
                for j in range(3):
                    if (board[i][j]=='_'):
                        board[i][j]=computer
                        val=self.depthLimit(not Max,depth-1)
                        best=min(best,val)
                        board[i][j]='_'
            return best

    def AlphaBeta(self,Max,alpha,beta):
        score=self.eval()
        if score!=-1:
            return score

        if(Max):
            best=-1000000
            for i in range(3):
                for j in range(3):
                    if (board[i][j]=='_'):
                        board[i][j]=player
                        val=self.AlphaBeta(not Max,alpha,beta)
                        board[i][j]='_'
                        best=max(best,val)
                        alpha=max(best,alpha)

                        if beta<=alpha:
                            return alpha
            return alpha
        else:
            best=1000000
            for i in range(3):
                for j in range(3):
                    if (board[i][j]=='_'):
                        board[i][j]=computer
                        val=self.AlphaBeta(not Max,alpha,beta)
                        board[i][j]='_'
                        best=min(best,val)
                        beta=min(best,beta)

                        if beta<=alpha:
                            return beta
            return beta

    def AlphaBeta_with_depthLimited(self,Max,depth,alpha,beta):
        utility=self.eval()
        score = self.heuristic()
        if depth==4 or utility!=-1:
            return score

        if(Max):
            best=-1000000
            for i in range(3):
                for j in range(3):
                    if (board[i][j]=='_'):
                        board[i][j]=player
                        val=self.AlphaBeta_with_depthLimited(not Max,depth+1,alpha,beta)
                        board[i][j]='_'
                        best=max(best,val)
                        alpha=max(best,alpha)

                        if beta<=alpha:
                            return alpha-depth
            return alpha-depth
        else:
            best=1000000
            for i in range(3):
                for j in range(3):
                    if (board[i][j]=='_'):
                        board[i][j]=computer
                        val=self.AlphaBeta_with_depthLimited(not Max,depth+1,alpha,beta)
                        board[i][j]='_'
                        best=min(best,val)
                        beta=min(best,beta)

                        if beta<=alpha:
                            return beta+depth
            return beta+depth

    def findnext(self):
        bestnow=1000000
        bestmove=[-1,-1]
        for i in range(3):
            for j in range(3):
                if(board[i][j]=='_'):
                    board[i][j]=computer
                    # moveval=self.miniMax(True,1)
                    depth=10
                    if self.algo==1:
                        # print("minimax")
                        moveval=self.miniMax(True)
                    elif self.algo==2:
                        # print("depth limited")
                        moveval=self.depthLimit(True,4)
                    elif self.algo==3:
                        # print("alpha beta")
                        moveval=self.AlphaBeta(True,-1000000,1000000)
                    elif self.algo==4:
                        moveval=self.AlphaBeta_with_depthLimited(True,1,-1000000,1000000)
                    board[i][j]='_'
                    if(moveval<bestnow):
                        bestnow=moveval
                        # print("Best value is: ", bestnow)
                        print()
                        bestmove=[i,j]
        return bestmove

    def AI(self):
        coordx,coordy=self.findnext()
        # print("Done till here")
        self.mark_o(coordx,coordy)

#g=Game()
#board=[['x','_','_'],['_','_','_'],['_','_','_']]
#print g.eval()
#print g.miniMax(False,-1000000,1000000)
#print g.findnext()
