#
# In development by Jihye Sofia Seo https://www.linkedin.com/in/jihyeseo
# forked from the code of another game Slide Puzzle by Al Sweigart  
# http://inventwithpython.com/pygame/chapter4.html 
# whose books are very helpful for learning Python and PyGame. Many thanks!
#
# The final goal is an autoplay with computer vision, 
# so that one can earn more scores in a mobile game.
#
# Any comments are welcome at jihyeseo@post.harvard.edu 
# upload: May 7 2016 Berlin Germany
#

import pygame, sys, random, math
from pygame.locals import *

# currently, the code runs correctly only with fixed board size. 
BOARDWIDTH = 4  # number of columns in the board
BOARDHEIGHT = 4 # number of rows in the board
TILECOUNT = BOARDHEIGHT * BOARDWIDTH
TILESIZE = 80
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 30
waitingTime = 100
BLANK = None

#                 R    G    B
BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)
BRIGHTBLUE =    (  0,  50, 255)
DARKTURQUOISE = (  3,  54,  73)
GREEN =         (  0, 204,   0)

BGCOLOR = DARKTURQUOISE
 
darkMergeTILECOLOR = (0,0,0)
mergeTILECOLOR = (122,122,122)
randomTILECOLOR = (255,0,0)
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

valueAt = [0]*TILECOUNT  
tileColors = [randomTILECOLOR]*TILECOUNT


def createRandomTile(): 
    randomLoc = random.randint(0,TILECOUNT-1)
    if valueAt[randomLoc] == 0 :
        valueAt[randomLoc] = random.choice([1,2])
        tileColors[randomLoc] = randomTILECOLOR
    else : 
        createRandomTile()
        
        # initionalizeTileColors()
for i in range(2):
    createRandomTile() 
            
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('2048')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
  

    pygame.display.update()
    lastMove = None
     

    
    while True: # main game loop
        slideTo = None # the direction, if any, a tile should slide
    
        drawBoard()
        pygame.display.update()
        pygame.time.wait(waitingTime)
        initionalizeTileColors(True)
        drawBoard()
        pygame.display.update()
        pygame.time.wait(waitingTime)
        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == KEYUP:
                # check if the user pressed a key to slide a tile
                if event.key in (K_LEFT, K_a)  :
                    slideTo = LEFT
                elif event.key in (K_RIGHT, K_d) :
                    slideTo = RIGHT
                elif event.key in (K_UP, K_w) :
                    slideTo = UP
                elif event.key in (K_DOWN, K_s)  :
                    slideTo = DOWN

        if slideTo:
            move = slideTo
            if move == UP: 
                (startMem, nextMember, nextTeam) = (0, 4, 1) 
            elif move == DOWN:
                (startMem, nextMember, nextTeam) =(TILECOUNT-1, -4, -1) 
            elif move == LEFT:
                (startMem, nextMember, nextTeam) = (0, 1, 4) 
            elif move == RIGHT:
                (startMem, nextMember, nextTeam )= (TILECOUNT-1, -1, -4)  
            initionalizeTileColors(True)  
            existChangeI = slideMove(startMem, nextMember, nextTeam, False)
            initionalizeTileColors(False) 
            drawBoard()
            pygame.display.update()
            pygame.time.wait(waitingTime)
            existChangeII = slideMove(startMem, nextMember, nextTeam, True)
            initionalizeTileColors(True) 
            drawBoard()
            pygame.display.update()
            pygame.time.wait(waitingTime) 
            if existChangeI or existChangeII: 
                createRandomTile()
                drawBoard()
                pygame.display.update()
                pygame.time.wait(waitingTime)
        initionalizeTileColors(True)
        drawBoard()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

COLORSCHEMES = [(150, 200, 255),   
                (97, 215, 164)  ,  #lightGr 
                (0, 125, 50) ,#darkGr
                (23, 149, 195) , # light ocean
                (81, 85 , 141), # lightPur
                (147, 3, 167) , # purple
                (241, 109, 149), # jindalle 
                (255, 180, 115), # tangerine
                (166, 147, 0)  # tangerine?   
                ]
     
def initionalizeTileColors(deep):
    for i in range(TILECOUNT):
        if deep :  
            tileColors[i] = COLORSCHEMES[valueAt[i] % len(COLORSCHEMES)]
        elif tileColors[i] != randomTILECOLOR :
            tileColors[i] = COLORSCHEMES[valueAt[i] % len(COLORSCHEMES)]
            

 
    
def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back



             
def slideMove(startMem, nextMember, nextTeam, squeeze):   
    existChange = False  
    # for each team, we slide into right direction.  
    for teamID in range(4): 
    
        tempArray = []
        
        for memberIndex in range(4):             
            tempArray.append(valueAt[startMem + nextTeam * teamID + nextMember * memberIndex]) 

        slideTempArray = []
        for i in range(4):
            tempValue = tempArray[i]
            if tempValue != 0:
                slideTempArray.append(tempValue)
        
        numOfZeros = 4 - len(slideTempArray)
        slideTempArray.extend([0]*numOfZeros)
        
        if not squeeze: 
            for memberIndex in range(4): 
                valueAt[startMem + nextTeam * teamID + nextMember * memberIndex]  = slideTempArray[memberIndex]                
            
            for i in range(4): 
                if tempArray[i] != slideTempArray[i]:
                    existChange = True
                    break 
                    
      
        for i in range(3):
            if (slideTempArray[i] != 0) & (slideTempArray[i] == slideTempArray[i+1]):
                if squeeze:
                    slideTempArray[i] += 1
                    slideTempArray[i+1] = 0
                    existChange = True 
                else : # only change color for those
                    tileColors[startMem + nextTeam * teamID + nextMember * i] = randomTILECOLOR
                    tileColors[startMem + nextTeam * teamID + nextMember * (i+1)] = randomTILECOLOR
                break                    

        if squeeze: 
            newTempArray = []
            for i in range(4):
                tempValue = slideTempArray[i]
                if tempValue != 0:
                    newTempArray.append(tempValue)
            
            numOfZeros = 4 - len(newTempArray)
            newTempArray.extend([0]*numOfZeros)          

            for i in range(4): 
                if tempArray[i] != newTempArray[i]:
                    existChange = True
                    break 
            
            for memberIndex in range(4): 
                valueAt[startMem + nextTeam * teamID + nextMember * memberIndex]  = newTempArray[memberIndex]                
              
    return existChange
     
def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)
  
def drawTile(tilex, tiley, number, tileCOLOR, adjx=0, adjy=0):
    # draw a tile at board coordinates tilex and tiley, optionally a few
    # pixels over (determined by adjx and adjy)
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, tileCOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    textSurf = BASICFONT.render(str(pow(2,number)), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(textSurf, textRect)
 
def drawBoard():
    DISPLAYSURF.fill(BGCOLOR)
     
    for tilex in range(4):
        for tiley in range(4):
            loc = tilex + 4 * tiley
            if valueAt[loc] != 0:
                drawTile(tilex, tiley, valueAt[loc], tileColors[loc])

    left, top = getLeftTopOfTile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)

 

if __name__ == '__main__':
    main()