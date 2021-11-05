import pygame as pg
import sys
from Game import *

def beginscreen():
	global game,g
	global turn
	turn={'Player':0,'Computer':0}
	game=Game()
	# g=Game()
	game.createboard()
	game.displaystr("1.) TIC TAC TOE",(game.windowsize//2-game.box_size*1.25,game.windowsize//2-game.windowsize//5),(255, 191, 0))
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
				# If the user enters the key 'y'.
				if event.key==pg.K_1:
					pg.display.update()
					tictactoe()

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


def tictactoe():
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
			# 	break

		pg.display.update()
		if status!=-1:
			break
		# if status<=-100 or status==0:
		# 	break
	# print("You are here")
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
