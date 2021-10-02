import pygame
import random
import math
from pygame import mixer  # pygame module for loading and playing sounds

# ----------------------------------------------------------

# initialize pygame
pygame.init()

# create the display surface object
# of specific dimension(X, Y).
screen = pygame.display.set_mode((800, 600))

# Here we set name or title of our pygame window
pygame.display.set_caption("CORONA KILLER")

Icon = pygame.image.load("Images/coronavirus.png")
# We use set_icon to set new icon
pygame.display.set_icon(Icon)

# create a font object.
# 1st parameter is the font file
# which is present in pygame.
# 2nd parameter is size of the font
font = pygame.font.Font("freesansbold.ttf", 32)


def starting_game(x):
    mixer.music.load("Audio/starting.wav")  # Load a music file for playback
    if x:
        # Start the playback of the music stream
        # -1 to repeats music indefinitely times
        mixer.music.play(-1)
    else:
        mixer.music.pause()  # Pausing the music


startX = 350
startY = 270
def start(x, y):
    startImg = pygame.image.load("Images/play-button.png")
    # draw one image onto another
    # at the given coordinate
    screen.blit(startImg, (x, y))


displayX = 180
displayY = 430
def display_starting(x, y):
    line = font.render("'press CAPSLOCK to start GAME'", True, (0, 0, 0))
    screen.blit(line, (x, y))


playerX_change = 0
playerX = 370
playerY = 480
def player(x, y):
    playerImg = pygame.image.load("Images/doctor.png")
    screen.blit(playerImg, (x, y))


def during_game(x):
    mixer.music.load("Audio/background.wav")
    if x:
        mixer.music.play(-1)
    else:
        mixer.music.pause()


num_of_enemies = 8
enemyImg = [0] * num_of_enemies
enemyX = [0] * num_of_enemies
enemyY = [0] * num_of_enemies
enemyX_change = [0] * num_of_enemies
enemyY_change = [0] * num_of_enemies
def create_enemy():
    for i in range(num_of_enemies):
        enemyImg[i] = pygame.image.load("Images/virus.png")
        enemyX[i] = random.randint(0, 735)
        enemyY[i] = random.randint(50, 150)
        enemyX_change[i] = 1
        enemyY_change[i] = 40

create_enemy()


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


bulletX = playerX
bulletY = 480
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"
def fire_bullet(x, y):
    bulletImg = pygame.image.load("Images/bullet.png")
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


lockdown_global = 100
lockX = 470
lockY = 10
lock_change_global = 0
def lockdown_display(x, y, color, lockdown):
    lock = font.render("Lockdown Days: " + str(lockdown), True, color)
    screen.blit(lock, (x, y))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(((enemyX - bulletX) ** 2) + ((enemyY - bulletY) ** 2))
    if distance < 30:
        return True
    else:
        return False


score_value_global = 0
textX = 10
textY = 10
def show_score(x, y, score_value):
    score = font.render("SCORE: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


flag = 0
def game_over_text():
    global flag
    flag = 1
    over_font = pygame.font.Font("freesansbold.ttf", 64)
    # create a text surface object,
    # on which text is drawn on it.
    over_text = over_font.render("GAME OVER", True, (255, 0, 0))
    # copying the text surface object to the display surface object(draw one image onto another)
    # at the given coordinate
    screen.blit(over_text, (200, 250))


def victory(x):
    mixer.music.load("Audio/victory.wav")
    if x:
        mixer.music.play(-1)
    else:
        mixer.music.pause()


def game_survived_text():
    survived_font = pygame.font.Font("freesansbold.ttf", 64)
    survived_text = survived_font.render("SURVIVED!", True, (255, 0, 0))
    screen.blit(survived_text, (240, 250))


def final():
    line = font.render("'press CAPSLOCK to play again'", True, (0, 0, 0))
    screen.blit(line, (180, 430))


def main(score_value, lockdown, lock_change):
    starting_game(True)
    background_music = True
    victory_music = True
    running = True
    playing = False
    game_over = False

    global playerX, playerX_change, bulletY, bullet_state, bulletX

    # create a surface object, image is drawn on it.
    background = pygame.image.load("Images/background.png")
    while running:
        # fill Surface with a solid color
        screen.fill((0, 255, 0))

        screen.blit(background, (0, 0))

        # ------------------------------------------------------------
        # creating a loop to check events that
        # are occuring
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # deactivates the pygame library
                pygame.quit()
                # quit the program.
                quit()

            # checking if keydown event happened or not
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_CAPSLOCK:
                    playing = True
                if event.key == pygame.K_CAPSLOCK and game_over:
                    global flag
                    flag = 0
                    main(score_value_global, lockdown_global, lock_change_global)

                if event.key == pygame.K_LEFT and playing:
                    playerX_change = -5
                # checking if key "	right arrow" was pressed
                if event.key == pygame.K_RIGHT and playing:
                    playerX_change = 5
                if event.key == pygame.K_SPACE and playing:
                    lock_change = -1 / 100
                    if bullet_state == "ready":
                        # for effects if use mixer.sound
                        # Create a new Sound object from a file or buffer object
                        bullet_sound = mixer.Sound("Audio/laser.wav")
                        bullet_sound.play()
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        # ---------------------------------------------------------------
        playerX += playerX_change

        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        player(playerX, playerY)

        # ----------------------------------------------------------------
        for i in range(num_of_enemies):

            if flag == 1:
                create_enemy()
            if enemyY[i] > 430 or flag == 1:
                playing = False
                starting_game(False)
                show_score(textX, textY, score_value)
                game_over_text()
                game_over = True
                final()
                break

            if playing:
                enemyX[i] += enemyX_change[i]
                if enemyX[i] <= 0:
                    enemyX_change[i] = 1
                    enemyY[i] += enemyY_change[i]
                elif enemyX[i] >= 736:
                    enemyX_change[i] = -1
                    enemyY[i] += enemyY_change[i]

                collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
                if collision:
                    collision_sound = mixer.Sound("Audio/explosion.wav")
                    collision_sound.play()
                    bulletY = 480
                    bullet_state = "ready"
                    score_value += 1
                    enemyX[i] = random.randint(0, 735)
                    enemyY[i] = random.randint(50, 150)

                enemy(enemyX[i], enemyY[i], i)

        # ----------------------------------------------------------------
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            bulletY -= bulletY_change
            fire_bullet(bulletX, bulletY)

        # ------------------------------------------------------------------
        if not playing and not game_over:
            start(startX, startY)
            display_starting(displayX, displayY)

        # -------------------------------------------------------------------
        if playing and background_music:
            during_game(True)
            background_music = False

        # --------------------------------------------------------------------
        if playing:
            show_score(textX, textY, score_value)
            lockdown += lock_change

        # ---------------------------------------------------------------------
        if lockdown > 10:
            lockdown_display(lockX, lockY, 'white', lockdown)
        if 10 > lockdown > 0:
            lockdown_display(lockX, lockY, 'red', lockdown)
        if lockdown <= 0:
            lockdown = 0
            playing = False
            game_over = True
            final()
            game_survived_text()
            show_score(textX, textY, score_value)
            lockdown_display(lockX, lockY, (35, 111, 33), lockdown)
        if lockdown == 0 and victory_music:
            victory(True)
            victory_music = False

        # -----------------------------------------------------------------------
        # allows to update a portion of the screen, instead of the entire area of the screen.
        # Passing no arguments, updates the entire display
        # IN SHORT--->Draws the surface object to the screen.
        pygame.display.update()


main(score_value_global, lockdown_global, lock_change_global)
