import pgzrun
import random
import pygame
import time
import sys

#setting the variables

#Heart Power Ups
heartPowerUpCounterStart = time.perf_counter()
heartPowerUpCounterEnd = 0
heartPowerUpCounter = random.randint(40,80)
health = 5

#Enemy Timing
enemyTimingStart = time.perf_counter()
enemyTimingEnd = 0

#Bulllet Power Up
bulletTimerStart = time.perf_counter()
bulletTimerStartEnd = 0
bulletPowerUpSpawnStart = time.perf_counter()
bulletPowerUpSpawnEnd = 0
bulletPowerUpTimePassedStart = time.perf_counter()
bulletPowerUpTimePassedEnd = 0
bulletPowerUpFlag = False

#Game Variables
maxEnemies = 30
highscore = 0
score = 0
WIDTH = 725
HEIGHT = 350
xspeed = 0
yspeed = 0
enemySpeed = 2.5
playerBulletSpeed = -5
enemyBulletSpeed = 5


#Creating the player and bullet powerup actors

player = Actor('player', center=(WIDTH / 2, 300),anchor=('center', 'bottom') )
bulletPowerUp = Actor('bullet_powerup', center=( -5, player.y - 10))


#using an empty list to control all the hearts

heartList = []
heartPowerUpList = []

#using an empty list to control all the bullets

playerBullets = []
enemyBullets = []
enemyTiming = []

#using an empty list to control all the enemys

enemies = []
enemyHealth = []


def resetHeart(numberOfHearts):
    global heartList
    heartList = []
    for i in range(0, numberOfHearts):
        heart = Actor('heart', center=(10 + i * 20, 15),anchor=('center', 'bottom') )
        heartList.append(heart)

resetHeart(health)



def spawnEnemies():  
    global enemies, enemyTiming
    enemies = []
    enemyTiming = []

    for j in range(0,3):
        for i in range(0,10):
            randomEnemyGenorator = random.randint(1,12)
            if randomEnemyGenorator <= 8:
                enemy = Actor('enemy1', center=((WIDTH / 10 ) + (i *(WIDTH/20)), 100 - 25 * j),anchor=('center','bottom'))
            elif randomEnemyGenorator <= 11:
                enemy = Actor('enemy2', center=((WIDTH / 10 ) + (i *(WIDTH/20)), 100 - 25 * j),anchor=('center','bottom'))
            else:
                enemy = Actor('enemy3', center=((WIDTH / 10 ) + (i *(WIDTH/20)), 100 - 25 * j),anchor=('center','bottom'))
        
            enemies.append(enemy)


    for e in enemies:
        if e.image == 'enemy1':
            timing = random.randint(0,10)
        elif e.image == 'enemy2':
            timing = random.randint(0,5)
        else:
            timing = random.randint(0,3)
        enemyTiming.append(timing)

spawnEnemies()

def playAgain():
    global enemySpeed, score, enemyTiming, enemyTimingStart, enemyTimingEnd, heartPowerUpCounterStart, heartPowerUpCounterEnd
    enemyTimingStart = time.perf_counter()
    enemyTimingEnd = enemyTimingStart 
    heartPowerUpCounterStart = time.perf_counter()
    heartPowerUpCounterEnd = heartPowerUpCounterStart
    enemySpeed = 2.5
    score = 0
    resetHeart(health)
    spawnEnemies()

def gameOver():
    global enemySpeed, enemyBullets, highscore, heartPowerUpList
    enemyBullets = []
    heartPowerUpList = []
    enemySpeed = 0
    if score > highscore:
        highscore = score
    screen.draw.text('Game 0ver! \n\nPress y to play again, n to quit\nScore: ' + str(score) +'\nHighscore: ' + str(highscore), (WIDTH / 2 - 50, HEIGHT/ 2))


def on_key_down(key):
    #setting all the keybinds when they are pressed
    global yspeed, xspeed, bulletTimerStart, bulletTimerStartEnd
    bulletTimerStartEnd = time.perf_counter()
    if key == keys.D:
        xspeed = 3
    if key == keys.A:
        xspeed = -3
    if key == keys.SPACE and ((bulletTimerStartEnd - bulletTimerStart) >= 0.5 or bulletPowerUpFlag == True):
        if bulletPowerUpFlag == False:
            bulletTimerStart = time.perf_counter()
        bullet = Actor('bullet', center=(player.x, player.y))
        playerBullets.append(bullet)
    if len(heartList) == 0:
        if key == keys.Y:
            playAgain()

        elif key == keys.N:
            sys.exit()

    

        


def on_key_up(key):
    #setting the keybind when they stopped getting pressed
    global yspeed
    global xspeed
    if key == keys.D:
        xspeed = 0
    # if key == keys.W:
    #     yspeed = 0
    if key == keys.A:
        xspeed = 0
    # if key == keys.S:
    #     yspeed = 0
    # clock.schedule(enemys, 1.0)

def drawBulletPowerUp():
    global bulletPowerUpSpawnStart, bulletPowerUpSpawnEnd, bulletPowerUp, bulletPowerUpFlag, bulletPowerUpTimePassedStart, bulletPowerUpTimePassedEnd
    bulletPowerUpSpawnEnd = time.perf_counter()
    bulletPowerUpTimePassedEnd = time.perf_counter()
    if bulletPowerUpSpawnEnd - bulletPowerUpSpawnStart >= 10 and bulletPowerUpFlag == True:
        bulletPowerUpFlag = False

    if bulletPowerUpSpawnEnd - bulletPowerUpSpawnStart >= 60 and bulletPowerUp.x < 0:
        bulletPowerUp.x = random.randint(20, WIDTH - 20)
        bulletPowerUpSpawnStart = time.perf_counter()
    if bulletPowerUp.x > 0:
        bulletPowerUp.draw()
    if abs(bulletPowerUp.x - player.x) < 5:
        bulletPowerUpTimePassedStart = time.perf_counter()
        bulletPowerUp.x = -20
        bulletPowerUpSpawnStart = time.perf_counter()
        bulletPowerUpFlag = True






#Bullet
def drawPlayerBullets():
    global enemies, playerBullets, score, enemyTiming
    for p in playerBullets:
        #creating infinite bullets
        p.y += playerBulletSpeed
        #setting their speed
        for e in enemies: 
            if abs(p.x - e.x) < 10 and p.y == e.y:
                if e.image == 'enemy1':
                    score += 10
                    print("+10")
                elif e.image == 'enemy2':
                    score += 25
                    print("+25")
                else:
                    score += 50
                    print("+50")
                playerBullets.remove(p)
                enemyTiming.pop(enemies.index(e))
                enemies.remove(e)

        if p.y <= 0:
            #making sure they delete when they leave the screen
            playerBullets.remove(p)
        
        else:
            p.draw()

def heartPowerUp():
    global heartList
    if len(heartList) < 5:
        resetHeart(len(heartList) + 1)

def drawEnemyBullets():
    global heartList
    for e in enemyBullets:
        #creating infinite bullets
        e.y += enemyBulletSpeed
        #setting their speed
        if e.y >= HEIGHT:
            #making sure they delete when they leave the screen
            enemyBullets.remove(e)
        elif abs(player.x - e.x) < 5 and player.y == e.y:
            heartList.pop()
        else:
            e.draw()
        



def drawEnemies():
    global enemySpeed
    for e in enemies:
        if e.x >= WIDTH or e.x <= 0:
            enemySpeed *= -1
        
    for e in enemies:
        e.x += enemySpeed
        e.draw()

def drawHearts():
    for h in heartList:
        h.draw()

def drawheartPowerUpList():
    global heartPowerUpList, heartPowerUpCounter, heartPowerUpCounterEnd,heartPowerUpCounterStart
    heartPowerUpCounterEnd = time.perf_counter()

    if heartPowerUpCounterEnd - heartPowerUpCounterStart >= heartPowerUpCounter and len(heartList) != 0 and len(heartPowerUpList) < 3:
        heartPowerUpCounterStart = time.perf_counter()
        spinningHeart = Actor('heart', center=(random.randint(20, WIDTH - 20), player.y - 10))
        heartPowerUpList.append(spinningHeart)
        heartPowerUpCounter = random.randint(40,80)

    for h in heartPowerUpList:

        if abs(player.x - h.x) <= 5:

            if len(heartPowerUpList) == 3:

                heartPowerUpCounterStart = time.perf_counter()
            heartPowerUpList.remove(h)
            heartPowerUp()

        else:    
            h.draw()



def draw():
    global enemySpeed
    screen.clear()

    if len(heartList) > 0:
        player.draw()
        drawPlayerBullets()
        drawEnemyBullets()
        screen.draw.text('Score: ' + str(score), (WIDTH - 150,10),color = (255 ,255 ,255))
    else:
        gameOver()

    drawEnemies()
    drawheartPowerUpList()
    drawHearts()
    drawBulletPowerUp()


def update():
    global yspeed, xspeed, player
    if player.x <= -70:
        player.left = 724

    if player.x > WIDTH:
        player.right = 2

    player.x += xspeed
    player.y += yspeed
    autoBullet()

    if len(enemies) == 0:
        spawnEnemies()



    
def autoBullet():
    global enemyTiming, enemyBullets, enemyTimingStart, enemyTimingEnd
    enemyTimingEnd = time.perf_counter()
    timingFlag = False

    for i in enemyTiming:

        if i <= enemyTimingEnd - enemyTimingStart:
            index = enemyTiming.index(i)
            bullet = Actor('bullet', center=(enemies[index].x, enemies[index].y))
            enemyBullets.append(bullet)
            enemyTiming[index] = 100
    for i in enemyTiming:

        if i != 100:
            timingFlag = True
    if not timingFlag:

        enemyTiming = []
        for e in enemies:

            if e.image == 'enemy1':
                timing = random.randint(0,10)
            elif e.image == 'enemy2':
                timing = random.randint(0,5)
            else:
                timing = random.randint(0,3)
            enemyTiming.append(timing)
        enemyTimingStart = time.perf_counter()








pgzrun.go()

    
        

