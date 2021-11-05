import pygame as pg
import sys
import itertools

class Game():  
    
    def __init__(self):
        self.gridsize=4
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
        board=[['_' for i in range(self.gridsize)]for j in range(self.gridsize)]


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
        for i in range(1,self.gridsize):
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
        for i in range(self.gridsize):
            for j in range(self.gridsize):
                tile=pg.Rect(j*self.box_size,i*self.box_size,self.box_width,self.box_height)
                if tile.collidepoint((x,y))==1 and board[i][j]=='_' :
                    self.mark_x(i,j)
                    return True
        else:
            return False

    def movesleft(self):
        for i in range(self.gridsize):
            for j in range(self.gridsize):
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

    def eachHeuristic(self, ar):
        score=0
        if ar[0]==player:
            score=1
        elif ar[0]==computer:
            score=-1

        for i in range(1,self.gridsize):
            if ar[i]==player:
                if score>=1:
                    score=score*10
                elif score<=-1:
                    return 0
                else:
                    score=1
            elif ar[i]==computer:
                if score<=-1:
                    score*=10
                elif score>=1:
                    return 0
                else:
                    score=-1
        return score

    def heuristic(self):
        score=0
        # board=self.board(self.gridsize)
        b=board

        # for each row
        for i in range(self.gridsize):
            score+=self.eachHeuristic(b[i])

        # for each column
        for i in range(self.gridsize):
            col=[]
            for j in range(self.gridsize):
                col.append(b[j][i])
            score+=self.eachHeuristic(col)

        # for each diagonal
        diag1=[]
        for i in range(self.gridsize):
            diag1.append(b[i][i])
        score+=self.eachHeuristic(diag1)

        diag2=[]
        for i in range(self.gridsize):
            for j in range(self.gridsize):
                if i+j==self.gridsize-1:
                    diag2.append(b[i][j])
        score+=self.eachHeuristic(diag2)

        return score

    def eval(self):
        # print("TTT Board")
        # print(self.gridsize)
        # board=self.board(gridsize)
        b=board
        check_func = lambda arr: arr[0] != '_' and all(elem == arr[0] for elem in arr)

        for i in range(self.gridsize):
            if check_func(b[i]):
                if b[i][0]==player:
                    return 10
                elif b[i][0]==computer:
                    return -10

        for i in range(self.gridsize):
            col=[]
            for j in range(self.gridsize):
                col.append(b[j][i])
            if check_func(col):
                if col[0]==player:
                    return 10
                elif col[0]==computer:
                    return -10
        diag1=[]
        for i in range(self.gridsize):
            diag1.append(b[i][i])
        if check_func(diag1):
            if diag1[0]==player:
                return 10
            elif diag1[0]==computer:
                return -10

        diag2=[]
        for i in range(self.gridsize):
            for j in range(self.gridsize):
                if i+j==self.gridsize-1:
                    diag2.append(b[i][j])
        if check_func(diag2):
            if diag2[0]==player:
                return 10
            elif diag2[0]==computer:
                return -10
                

        if not self.movesleft():
            return 0


        return -1

    def miniMax(self, Max, depth):
        # board=self.board(gridsize)
        utility=self.eval()
        # score=self.heuristic()
        # print("Utility is: ",utility)

        if utility!=-1:
            return utility

        if Max:
            best=-1000000
            for i in range(self.gridsize):
                for j in range(self.gridsize):
                    if (board[i][j]=='_'):
                        board[i][j]=player
                        val=self.miniMax(not Max,depth+1)
                        best=max(best,val)
                        board[i][j]='_'
            return best
        else:
            best=1000000
            for i in range(self.gridsize):
                for j in range(self.gridsize):
                    if (board[i][j]=='_'):
                        board[i][j]=computer
                        val=self.miniMax(not Max,depth+1)
                        best=min(best,val)
                        board[i][j]='_'
            return best

    def depthLimit(self, Max, depth):
        # board=self.board(gridsize)
        utility=self.eval()
        score = self.heuristic()
        if depth==0 or utility!=-1:
            return score

        if Max:
            best=-1000000
            for i in range(self.gridsize):
                for j in range(self.gridsize):
                    if (board[i][j]=='_'):
                        board[i][j]=player
                        val=self.depthLimit(not Max,depth-1)
                        best=max(best,val)
                        board[i][j]='_'
            return best
        else:
            best=1000000
            for i in range(self.gridsize):
                for j in range(self.gridsize):
                    if (board[i][j]=='_'):
                        board[i][j]=computer
                        val=self.depthLimit(not Max,depth-1)
                        best=min(best,val)
                        board[i][j]='_'
            return best


    def AlphaBeta(self,Max,depth,alpha,beta):
        # board=self.board(gridsize)
        utility=self.eval(gridsize)
        score=self.heuristic(gridsize)
        if(utility!=-1):
            return score

        if(Max):
            best=-1000000
            for i in range(gridsize):
                for j in range(gridsize):
                    if (board[i][j]=='_'):
                        board[i][j]=player
                        val=self.AlphaBeta(not Max,depth+1,alpha,beta)
                        board[i][j]='_'
                        best=max(best,val)
                        alpha=max(best,alpha)

                        if beta<=alpha:
                            return alpha-depth
            return alpha-depth
        else:
            best=1000000
            for i in range(gridsize):
                for j in range(gridsize):
                    if (board[i][j]=='_'):
                        board[i][j]=computer
                        val=self.AlphaBeta(not Max,depth+1,alpha,beta)
                        board[i][j]='_'
                        best=min(best,val)
                        beta=min(best,beta)

                        if beta<=alpha:
                            return beta+depth
            return beta+depth

    def AlphaBeta_with_depthLimited(self,Max,depth,alpha,beta):
        utility=self.eval()
        score = self.heuristic()
        if depth==7 or utility!=-1:
            return score

        if(Max):
            best=-1000000
            for i in range(self.gridsize):
                for j in range(self.gridsize):
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
            for i in range(self.gridsize):
                for j in range(self.gridsize):
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
        # board=self.board(gridsize)
        bestnow=1000000
        bestmove=[-1,-1]
        for i in range(self.gridsize):
            for j in range(self.gridsize):
                if(board[i][j]=='_'):
                    board[i][j]=computer
                    # moveval=self.miniMax(True,1)
                    if self.algo==1:
                        moveval=self.miniMax(True,1)
                    elif self.algo==2:
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
                        bestmove=[i,j]
        return bestmove

    def AI(self):
        coordx,coordy=self.findnext()
        # print("Done till here")
        self.mark_o(coordx,coordy)

def beginscreen():
    global game,boardsize
    global turn
    turn={'Player':0,'Computer':0}
    game=Game()
    # g=Game()
    game.createboard()
    game.displaystr("1.) Extended TIC TAC TOE",(game.windowsize//2-game.box_size*1.25,game.windowsize//2-game.windowsize//5),(255, 191, 0))
    game.displaystr("Choose the game you want to play (1)",(game.windowsize//2-game.box_size*1.25,game.windowsize//2-game.windowsize//10),(0,255,100))
    # game.displaystr("Do you want to start first?",(game.windowsize//2-game.box_size*1.25,game.windowsize//2-game.windowsize//10),(0,100, 67))
    # game.displaystr("Press 'Y' for Yes.",(game.windowsize//2-game.box_size*1.25,game.windowsize//2),(0,255,100))
    pg.display.update()
    while True:
        for event in pg.event.get():
            if event.type==pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type==pg.KEYDOWN:
                pg.display.update()
                # If the user enters the key '1'.
                if event.key==pg.K_1:
                    pg.display.update()
                    tictactoe()
                # elif event.key==pg.K_2:
                #     extendedtictactoe()


def our_choice(flag):
    game.screen.fill((0,0,0))
    game.displaytext("You choose: ",(game.windowsize//2-game.box_size*1.25,game.windowsize//2-game.windowsize//3),(255, 191, 0), flag)
    pg.display.update()
    while True:
        for event in pg.event.get():

            if event.type==pg.QUIT:
                pg.quit()
                sys.exit()

            if flag==1:
                pg.time.delay(700)
                pg.display.update()
                gameplay(1)
            elif flag==2:
                pg.time.delay(700)
                pg.display.update()
                gameplay(2)
            elif flag==3:
                pg.time.delay(700)
                pg.display.update()
                gameplay(3)
            elif flag==4:
                pg.time.delay(700)
                pg.display.update()
                gameplay(4)


def algorithm():
    game.screen.fill((0,0,0))
    game.displaystr("Choose the algorithm(1/2/3/4)",(game.windowsize//2-game.box_size*1.25,game.windowsize//2-game.windowsize//3),(255, 191, 0))
    game.displaystr("1.) Minimax",(game.windowsize//2-game.box_size*1.25,game.windowsize//2-game.windowsize//4),(0,255, 100))
    game.displaystr("2.) Depth Limited Search",(game.windowsize//2-game.box_size*1.25,game.windowsize//2-game.windowsize//5),(0,255, 100))
    game.displaystr("3.) Alpha-Beta",(game.windowsize//2-game.box_size*1.25,game.windowsize//2-game.windowsize//7),(0,255, 100))
    game.displaystr("4.) Alpha-Beta with depth Limited",(game.windowsize//2-game.box_size*1.25,game.windowsize//2-game.windowsize//12),(0,255, 100))
        
    pg.display.update()
    while True:
        for event in pg.event.get():
            if event.type==pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type==pg.KEYDOWN:
                if event.key==pg.K_1:
                    our_choice(1)
                elif event.key==pg.K_2:
                    our_choice(2)
                elif event.key==pg.K_3:
                    our_choice(3)
                elif event.key==pg.K_4:
                    our_choice(4)

# def extendedtictactoe():
#     game.screen.fill((0,0,0))
#     # length = int(input())
#     game.displaystr("Board size is:  ",(game.windowsize//2-game.box_size*1.25,game.windowsize//2-game.windowsize//10),(255, 191, 0))
#     pg.time.delay(700)
#     pg.display.update()
#     # tictactoe()
#     while(True):
#         for event in pg.event.get():
#             if event.type==pg.QUIT:
#                 pg.quit()
#                 sys.exit()

#             if event.type==pg.KEYDOWN:
#                 pg.display.update()
#                 key_name = pg.key.name(event.key)
#                 print(int(key_name))
#                 grid=int(key_name)
#                 # bo=Board(grid)
#                 # print("The answer I got is ",bo.gridsize)
#                 # game.size(self.gridsize)
#                 tictactoe()


def tictactoe():
    # print("Board size: ",self.gridsize)
    game.screen.fill((0,0,0))
    game.displaystr("Do you want to start first?",(game.windowsize//2-game.box_size*1.25,game.windowsize//2-game.windowsize//10),(255, 191, 0))
    game.displaystr("Press 'Y' for Yes.",(game.windowsize//2-game.box_size*1.25,game.windowsize//2),(0,255,100))
    pg.display.update()
    while True:
        for event in pg.event.get():

            if event.type==pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type==pg.KEYDOWN:
                pg.display.update()
                if event.key==pg.K_y:
                    turn['Player']=1
                    algorithm()
                    return
                else:
                    turn['Computer']=1
                    # print("Heyy")
                    algorithm()
                    return


def gameplay(flag):

    game.screen.fill((0,0,0))
    # print(player)
    # print("Size of board:", self.gridsize)
    game.lines()
    # pg.display.update()
    status=-1
    while True:
        for event in pg.event.get():
            if event.type==pg.QUIT:
                pg.quit()
                sys.exit()

            if(turn['Computer']==1):
                print("System's turn")
                game.algo=flag
                game.AI()
                print("Heuristic after Computer's turn: ", game.heuristic())
                turn['Computer']=0
                turn['Player']=1

            elif event.type==pg.MOUSEBUTTONDOWN:
                if (turn['Player']==1):
                    game.algo=flag
                    x,y=event.pos
                    done=game.human(x,y)
                    print("Heuristic after Player's turn: ", game.heuristic())
                    # pg.display.update()
                    if done:
                        turn['Computer']=1
                        turn['Player']=0

            status=game.eval()
            # print(status)
            if status!=-1:
                break
            # if status<=-100 or status==0:
            #   break

        pg.display.update()
        if status!=-1:
            break
        # if status<=-100 or status==0:
        #   break
    print("You are here")
    status=game.eval()
    pg.time.delay(900)
    game.screen.fill((0,0,0))
    if (status>0):
        game.displaystr("YOU WIN",(game.windowsize/2-game.box_size*1.25,game.windowsize/2-game.windowsize/10),(0,255,100))
    elif (status<0):
        game.displaystr("COMPUTER WINS",(game.windowsize/2-game.box_size*1.25,game.windowsize/2-game.windowsize/10),(0,255,100))
    else:
        game.displaystr("TIE!",(game.windowsize/2-game.box_size*1.25,game.windowsize/2-game.windowsize/10),(0,255,100))
    pg.display.update()
    pg.time.delay(1000)
    gameoverscreen()

def gameoverscreen():

    game.screen.fill((0,0,0))
    game.displaystr("GAME OVER !!",(game.windowsize/2-game.box_size*1.25,game.windowsize/2-game.windowsize/10),(0,255,100))
    game.displaystr("RESTART(R) OR QUIT(Q)",(game.windowsize/2-game.box_size*1.25,game.windowsize/2),(0,255,100))
    pg.display.update()
    while True:
        for event in pg.event.get():
            if event.type==pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type==pg.KEYDOWN :
                if event.key==pg.K_r:
                    game.screen.fill((0,0,0))
                    # pg.display.update()
                    beginscreen()
                    return None
                elif event.key==pg.K_q:
                    pg.quit()
                    quit()
                    return None


pg.init()
beginscreen()