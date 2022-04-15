import pygame
from pygame.locals import *
from pygame import mixer
import math
import random

# initialize
pygame.init()
win = pygame.display.set_mode((1366, 700))
pygame.display.set_caption("Dino")
icon = pygame.image.load("Idle (1).png")
pygame.display.set_icon(icon) 

#bg music
mixer.music.load("bgm.mp3")
mixer.music.play(-1)

#score
score=0
font=pygame.font.Font('pixeled.ttf',32)
textX=10
textY=8
def score_show(x,y):
	score_dispay = font.render("Score : " + str(score), True,(212, 226, 212))
	win.blit(score_dispay,(x,y))

# clocks
clock = pygame.time.Clock()
clock2 = pygame.time.Clock()

# game over
ovmusic=mixer.Sound("gov.mp3")
over_font=pygame.font.Font('pixeled.ttf',64)
start_font=pygame.font.Font('pixeled.ttf',50)
def game_over(x,y):
	over_text = over_font.render("GAME OVER", True, (212, 226, 212))
	start_text = start_font.render("PRESS ENTER TO START AGAIN", True, (212, 226, 212))
	win.blit(over_text,(x,y))
	win.blit(start_text,(x - 260,y + 100))
	
#image loading

# DINO RUN
player_img = [pygame.image.load("Run (1).png"),pygame.image.load("Run (2).png"),pygame.image.load("Run (3).png"),pygame.image.load("Run (4).png"),pygame.image.load("Run (5).png")]
value = 0 # iteration of run index

# DEAD DINO
img = pygame.image.load("Dead (5).png")
img = pygame.transform.scale(img, (210, 180))

# DINO JUMP
jplayer_img = [pygame.image.load("Jump (1).png"),pygame.image.load("Jump (2).png"),pygame.image.load("Jump (3).png"),pygame.image.load("Jump (4).png"),pygame.image.load("Jump (5).png"),pygame.image.load("Jump (6).png"),pygame.image.load("Jump (7).png"),pygame.image.load("Jump (8).png"),pygame.image.load("Jump (9).png"),pygame.image.load("Jump (10).png"),pygame.image.load("Jump (11).png"),pygame.image.load("Jump (12).png")]
jy = 400 # initial y of jump
jvalue = 0 # iteration of jump index

# BACKGROUND
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (1365,900))

# PLATFORM
platformimg = pygame.image.load("2dplatform.png")
platformimg = pygame.transform.scale(platformimg, (1566,600))
platformimg2 = pygame.transform.scale(platformimg, (1566,600))
x = -20 # platformimg x
y = 340 # platform y
x2 = 1320 # platformimg2 x

# SINGLE CACTUS
cactus = pygame.image.load("cactus.png")
cactus = pygame.transform.scale(cactus, (120,150))

# DOUBLE CACTUS
cactus2 = pygame.image.load("2cactus.png")
cactus2 = pygame.transform.scale(cactus2, (210,180))

# TRIPLE CACTUS
cactus3 = pygame.image.load("3cactus.png")
cactus3 = pygame.transform.scale(cactus3, (210,180))

# LIST OF CACTUS
enemyimg = [cactus,cactus2,cactus3]
en1x = 1160 # enemy1 x
en1y = 410 # enemy y
en2x = 1740 # enemy2 x

# controller
run=True

# velocity
velocity = 20

#collision detector
def is_collision(enemyy,bxp,byp,en2x):
	distance=math.sqrt(math.pow(-10 - bxp,2)+math.pow(enemyy- byp,2))
	distance2=math.sqrt(math.pow(-10 - en2x,2)+math.pow(enemyy- byp,2))
	if distance<110 or distance2 < 110:
		return True
	else:
		return False

# Flags for jump, enemy and jump limit
d = False
c = False
jump = False
a = True
running = True

#game loop
while run:
	# clock for dino
	clock.tick(10)

	# temp windows fill color
	win.fill((0,0,0))

	#background here
	win.blit(background,(0,0))

	# key events
	for event in pygame.event.get():
		# quit pygame
		if event.type==pygame.QUIT:
			run = False

		if running == True:
			# jump
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					jump = True
				if event.key == pygame.K_SPACE:
					jump = True
		
	if running == True:
		# dino run
		if jump == False:
			player = player_img[value]
			player = pygame.transform.scale(player, (210, 180))
			win.blit(player,(-10,jy))
			value += 1
			if value == 4:
				value = 0
		# dino jump
		else:
			if jy < 220:
				a = False
			if a == False:
				jy += 15
			else:
				jy -= 15
			jplayer = jplayer_img[jvalue]
			jplayer = pygame.transform.scale(jplayer, (210, 180))
			win.blit(jplayer,(-10,jy))
			jvalue += 1
			if jvalue == 12:
				jvalue = 0
			if jy == 400:
				jump = False
				a = True

		# collision detecton
		collide = is_collision(jy,en1x,en1y,en2x)
		if collide:
			explode=mixer.Sound("Explosion+1.wav")
			explode.play()
			running = False

		# cactus blit
		en1x -= velocity
		en2x -= velocity
		if c == False:
			enemy = random.choice(enemyimg)
			win.blit(enemy,(en1x,en1y))
			c = True
		else:
			win.blit(enemy,(en1x,en1y))
			if en1x < -100:
				score += 1
				en1x = random.randint(1200,1300)
				c = False
		if d == False:
			enemy2 = random.choice(enemyimg)
			win.blit(enemy2,(en2x,en1y))
			d = True
		else:
			win.blit(enemy2,(en2x,en1y))
			if en2x < -100:
				score += 1
				en2x = random.randint(1250,1300)
				d = False
		# moving platform
		x -= velocity
		x2 -= velocity
		if x < -1350:
			x = 1320
		if x2 < -1350:
			x2 = 1320
		win.blit(platformimg, (x,y))
		win.blit(platformimg2, (x2,y))

		# showing score
		score_show(10,0)
	else:
		game_over(350,150)
		win.blit(img,(-10,400))
		win.blit(platformimg, (x,y))
		win.blit(platformimg2, (x2,y))
		score_show(10,0)
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				d = False
				c = False
				jump = False
				a = True
				en1x = 1160 # enemy1 x
				en1y = 410 # enemy y
				en2x = 1740 # enemy2 x
				value = 0 # iteration of run index
				jy = 400 # initial y of jump
				jvalue = 0 # iteration of jump index
				x = -20 # platformimg x
				y = 340 # platform y
				x2 = 1320 # platformimg2 x
				velocity = 20
				running = True
				score = 0
		# Update Display
	pygame.display.update()