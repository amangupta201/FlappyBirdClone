import random  # For generating random numbers
import sys  # We will use sys.exit to exit the program
import pygame
from pygame.locals import *  # Basic pygame imports

# Global Variables for the game
FPS = 32
WidthofScreen = 289
HeightofScreen = 600
Screen = pygame.display.set_mode((WidthofScreen, HeightofScreen))
Ground = HeightofScreen* 0.8
SpritesofGame = {}
SoundsofGame = {}
FlappyBird = r'C:\Users\theam\Downloads\flappy\gallery\sprites\capbird.png'
Background = r'C:\Users\theam\Downloads\flappy\gallery\sprites\flappy bird background.png'
Mountain = r'C:\Users\theam\Downloads\flappy\gallery\sprites\unimo.png'


def welcomeScreen():


    playerx = int(WidthofScreen / 5)
    playery = int((HeightofScreen - SpritesofGame['player'].get_height()) / 2)
    messagex = int((WidthofScreen - SpritesofGame['message'].get_width()) / 2)
    messagey = int(HeightofScreen * 0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                Screen.blit(SpritesofGame['background'], (0, 0))
                Screen.blit(SpritesofGame['player'], (playerx, playery))
                Screen.blit(SpritesofGame['message'], (messagex, messagey))
                Screen.blit(SpritesofGame['base'], (basex, Ground))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    score = 0
    playerx = int(WidthofScreen / 5)
    playery = int(WidthofScreen / 2)
    basex = 0

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # my List of upper pipes
    upperPipes = [
        {'x': WidthofScreen + 300, 'y': newPipe1[0]['y']},
        {'x': WidthofScreen + 300 + (WidthofScreen / 2), 'y': newPipe2[0]['y']},
    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': WidthofScreen + 300, 'y': newPipe1[1]['y']},
        {'x': WidthofScreen + 300 + (WidthofScreen / 2), 'y': newPipe2[1]['y']},
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8  # velocity while flapping
    playerFlapped = False  # It is true only when the bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    SoundsofGame['wing'].play()

        crashTest = isCollide(playerx, playery, upperPipes,
                              lowerPipes)  # This function will return true if the player is crashed
        if crashTest:
            return

            # check for score
        playerMidPos = playerx + SpritesofGame['player'].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + SpritesofGame['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Your score is {score}")
                SoundsofGame['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = SpritesofGame['player'].get_height()
        playery = playery + min(playerVelY, Ground - playery - playerHeight)

        # move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -SpritesofGame['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # Lets blit our sprites now
        Screen.blit(SpritesofGame['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            Screen.blit(SpritesofGame['pipe'][0], (upperPipe['x'], upperPipe['y']))
            Screen.blit(SpritesofGame['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        Screen.blit(SpritesofGame['base'], (basex, Ground))
        Screen.blit(SpritesofGame['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += SpritesofGame['numbers'][digit].get_width()
        Xoffset = (WidthofScreen - width) / 2

        for digit in myDigits:
            Screen.blit(SpritesofGame['numbers'][digit], (Xoffset, HeightofScreen * 0.12))
            Xoffset += SpritesofGame['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > Ground - 25 or playery < 0:
        SoundsofGame['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = SpritesofGame['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < SpritesofGame['pipe'][0].get_width()):
            SoundsofGame['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + SpritesofGame['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < \
                SpritesofGame['pipe'][0].get_width():
            SoundsofGame['hit'].play()
            return True

    return False


def getRandomPipe():

    pipeHeight = SpritesofGame['pipe'][0].get_height()
    offset = HeightofScreen / 3
    y2 = offset + random.randrange(0, int(HeightofScreen - SpritesofGame['base'].get_height() - 1.2 * offset))
    pipeX = WidthofScreen + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},  # upper Pipe
        {'x': pipeX, 'y': y2}  # lower Pipe
    ]
    return pipe


if __name__ == "__main__":
    # This will be the main point from where our game will start
    pygame.init()  # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by Aman')
    SpritesofGame['numbers'] = (
        pygame.image.load(r'C:\Users\theam\Downloads\flappy\gallery\sprites\0.png').convert_alpha(),
        pygame.image.load(r'C:\Users\theam\Downloads\flappy\gallery\sprites\1.png').convert_alpha(),
        pygame.image.load(r'C:\Users\theam\Downloads\flappy\gallery\sprites\2.png').convert_alpha(),
        pygame.image.load(r'C:\Users\theam\Downloads\flappy\gallery\sprites\3.png').convert_alpha(),
        pygame.image.load(r'C:\Users\theam\Downloads\flappy\gallery\sprites\4.png').convert_alpha(),
        pygame.image.load(r'C:\Users\theam\Downloads\flappy\gallery\sprites\5.png').convert_alpha(),
        pygame.image.load(r'C:\Users\theam\Downloads\flappy\gallery\sprites\6.png').convert_alpha(),
        pygame.image.load(r'C:\Users\theam\Downloads\flappy\gallery\sprites\7.png').convert_alpha(),
        pygame.image.load(r'C:\Users\theam\Downloads\flappy\gallery\sprites\8.png').convert_alpha(),
        pygame.image.load(r'C:\Users\theam\Downloads\flappy\gallery\sprites\9.png').convert_alpha(),
    )

    SpritesofGame['message'] = pygame.image.load(r'C:\Users\theam\Downloads\flappy\gallery\sprites\redog.png').convert_alpha()
    SpritesofGame['base'] = pygame.image.load(r'C:\Users\theam\Downloads\flappy\gallery\sprites\base.png').convert_alpha()
    SpritesofGame['pipe'] = (pygame.transform.rotate(pygame.image.load(Mountain).convert_alpha(), 180),
                            pygame.image.load(Mountain).convert_alpha()
                            )

    # Game sounds
    SoundsofGame['die'] = pygame.mixer.Sound(r'C:\Users\theam\Downloads\flappy\gallery\audio\die.wav')
    SoundsofGame['hit'] = pygame.mixer.Sound(r'C:\Users\theam\Downloads\flappy\gallery\audio\hit.wav')
    SoundsofGame['point'] = pygame.mixer.Sound(r'C:\Users\theam\Downloads\flappy\gallery\audio\point.wav')
    SoundsofGame['swoosh'] = pygame.mixer.Sound(r'C:\Users\theam\Downloads\flappy\gallery\audio\swoosh.wav')
    SoundsofGame['wing'] = pygame.mixer.Sound(r'C:\Users\theam\Downloads\flappy\gallery\audio\wing.wav')

    SpritesofGame['background'] = pygame.image.load(Background).convert()
    SpritesofGame['player'] = pygame.image.load(FlappyBird).convert_alpha()

    while True:
        welcomeScreen()  # Shows welcome screen to the user until he presses a button
        mainGame()  # This is the main game function
