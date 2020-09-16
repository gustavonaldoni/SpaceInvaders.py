import pygame
import random
import math

# Import the sound module of pygame
from pygame import mixer

# Initialize pygame
pygame.init()

WIDTH = 800 #px
HEIGHT = 600 #px

# Colors
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)

# Initialize mixer module of pygame
pygame.mixer.init()

# Creating the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Title and Icon
icon = pygame.image.load('./images/icon.png')
pygame.display.set_caption('Space Invaders')
pygame.display.set_icon(icon)

# Background image
background = pygame.image.load('./images/bg.png')

# Background music
mixer.music.load('./sounds/music.wav')
mixer.music.play(-1) # "-1" keeps the music in loop

# Player information
playerImg = pygame.image.load('./images/player.png')
playerImgSize = 64
playerSpeed = 3

playerX = (WIDTH/2) - (playerImgSize/2)
playerY = 480

playerX_change = 0
playerY_change = 0

# Red enemies information
enemyImg = []
enemyImgSize = []
enemySpeed = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

enemyNumber = 6
newEnemySpeed = 0

for i in range(enemyNumber):
    enemyImg.append(pygame.image.load('./images/enemy.png'))
    enemyImgSize.append(64)
    enemySpeed.append(1.8)
    enemyX.append(random.randint(0, WIDTH-64))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1.8)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('./images/bullet.png')
bulletImgSize = 32
bulletSpeed = 5

bulletX = 0
bulletY = playerY

bulletY_change = bulletSpeed
bullet_state = "ready" # Ready --> You can't see the bullet / Fired --> Bullet is moving

# Score

scoreValue = 0
font = pygame.font.Font('./fonts/space_invaders.ttf', 32)

textX = 10*2
textY = 10*2

# Game Over font
gameOver_font = pygame.font.Font('./fonts/space_invaders.ttf', 64)

# Useful functions
def player(x,y):
    screen.blit(playerImg, (x, y))

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x, y))

def fireBullet(x,y):
    global bullet_state
    bullet_state = "fired"

    screen.blit(bulletImg, (x + playerImgSize/4, y + 10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)+(math.pow(enemyY-bulletY,2))))
    if distance < 20:
        return True
    else:
        return False

def showScore(x,y):
    score = font.render(f'Score : {scoreValue}', True, WHITE)
    screen.blit(score, (x,y))

def gameOverText():
    gameOver_text = gameOver_font.render('GAME OVER', True, WHITE)
    screen.fill(BLACK)
    screen.blit(gameOver_text, (200,250))
    

# Main Loop
running = True
while running:

    # Change screen color
    screen.fill(BLACK)

    # Background image
    screen.blit(background,(0,0))

    # Events 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        # If the user presses the left or right arrow keys or the spacebar
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -playerSpeed
            if event.key == pygame.K_RIGHT:
                playerX_change = playerSpeed
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    # Add the laser sound and play it
                    bulletSound = pygame.mixer.Sound('./sounds/laser.ogg')
                    bulletSound.set_volume(0.5)
                    bulletSound.play()

                    bulletX = playerX # Save the current playerX value on bulletX
                    fireBullet(bulletX, bulletY)

        # If the key is not pressed anymore
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerX_change = 0


    # Checking boudaries to the player
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= WIDTH - playerImgSize:
        playerX = WIDTH - playerImgSize

    # Bullet movement
    if bulletY <= 0:
        bulletY = playerY
        bullet_state = "ready"

    if bullet_state == "fired":
        fireBullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Enemy movement 
    for i in range(enemyNumber):

        # Game Over
        if enemyY[i] >= playerY-20:
            # Move all the enemies and player out the screen and show "GAME OVER"
            for j in range(enemyNumber):
                enemyY[j] = 2000
            playerY = 2000
            pygame.mixer.music.stop() # Stop background music
            gameOverText()

            bullet_state = "fired"

            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            if scoreValue%5 ==0 and scoreValue != 0:
                enemySpeed[i] += newEnemySpeed
            enemyX_change[i] = enemySpeed[i]
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= WIDTH - enemyImgSize[i]:
            if scoreValue%5 == 0 and scoreValue != 0:
                enemySpeed[i] += newEnemySpeed
            enemyX_change[i] = -enemySpeed[i]
            enemyY[i] += enemyY_change[i]
    
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            # Add the explosion sound and play it
            explosionSound = pygame.mixer.Sound('./sounds/explosion.ogg')
            explosionSound.set_volume(0.5)
            explosionSound.play()

            bulletY = playerY
            bullet_state = 'ready'
            scoreValue += 1

            enemyX[i] = random.randint(0, WIDTH-64)
            enemyY[i] = random.randint(50, 150)
        
        enemy(enemyX[i], enemyY[i], i)

    if scoreValue%5 == 0 and scoreValue != 0:
        newEnemySpeed += 0.0002

    player(playerX, playerY)  

    # Show the score on top left corner
    showScore(textX, textY)

    # Update the screen
    pygame.display.update()
