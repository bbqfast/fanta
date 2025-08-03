from sikuli import *
from sikuli.Sikuli import *

#import skyblock_img

#from skyblock_img import *

import lib
reload(lib)

#import skyblock_img
import skyblock_img as ix
#reload(ix)
#from org.sikuli.script.natives import Vision
#import org.sikuli.script.natives.Vision
#import org.sikuli.natives.Vision as Vision;
# import datetime
# import shutil
#Vision.setParameter("MinTargetSize", 10) # A small value such as 6 makes the matching 

#1763 ,1026

#,,code

#,,init,,ig
def initGame():
    lib.log('initGame')
    global game, bottombar, gameTop, gameLeft, gameTreeTop
    game = find(ix.imgGameIcon)
    ## 1763 ,1026
    gameHeight=1050
    gameWidth=1763
    game.setW(gameWidth)
    game.setH(gameHeight)
    
    bottomBarHeight=150
    bottombar = find(ix.imgGameIcon) 
    bottombar.setW(gameWidth)
    bottombar.setH(bottomBarHeight)
    bar_y = bottombar.getY()
    bottombar.setY(bar_y + gameHeight - bottomBarHeight)
    #bottombar.setY(626)x

    gameTop = find(ix.imgGameIcon) 
    gameTop.setW(gameWidth)
    gameTop.setH(gameHeight - bottomBarHeight)

    gameTreeTop = find(ix.imgGameIcon) 
    gameTreeTop.setW(gameWidth)
    gameTreeTop.setH(gameHeight / 2)


    gameLeft = find(ix.imgGameIcon) 
    gameLeft.setW(gameWidth / 2)
    gameLeft.setH(gameHeight - bottomBarHeight)
    

def clearIron():
    while lib.logExists(SCREEN, ix.imgIron, 1):
        lib.myClick(SCREEN,ix.imgIron)


#lib.myClick(SCREEN,ix.imgIron)
#lib.myClickTillGone(SCREEN,ix.imgIron, 1)

#,,tr,,gt
def getTrees():
    rocks=[ix.imgTree1,ix.imgTree2,ix.imgTree3,ix.imgTree4,ix.imgTree5,ix.imgTree6,ix.imgTree7,ix.imgTree8,ix.imgTree9]
    rocks=[ix.imgTree1,ix.imgTree2,ix.imgTree3,ix.imgTree4,ix.imgTree5,ix.imgTree6,ix.imgTree7]
    getAnyTrees(rocks)

def getBirchTrees():
    rocks=[ix.imgBirchTree1,ix.imgBirchTree2,ix.imgBirchTree3,ix.imgBirchTree4,ix.imgBirchTree5,ix.imgBirchTree6,ix.imgBirchTree7]
    getAnyTrees(rocks)

def getAnyTrees(treelist):
    cnt=1
    notfoundcnt=0
    while True:
        notfound=True
        for r in treelist:
            r=r.similar(ix.treeSimilar)
            lib.log("----------------- " + str(cnt))
            if lib.logExists(gameTreeTop, r):
                notfound=False
                cnt=cnt+1
                lib.myClick(gameTreeTop, r, holdDur=3.5)
        if notfound:
            notfoundcnt = notfoundcnt + 1
        if notfoundcnt > 2:
            break



def getIronRocks():
    cnt=1
    rocks=[ix.imgIronRock1,ix.imgIronRock2,ix.imgIronRock3,ix.imgIronRock4,ix.imgIronRock5,ix.imgIronRock6,ix.imgIronRock7,ix.imgIronRock8,ix.imgIronRock9]
    stoneAxeDuration = 4
    glidedSteelPickAxe = 2
    while True:
        for r in rocks:
            if lib.logExists(gameTop, r):
                lib.log("----------------- " + str(cnt))
                cnt=cnt+1
                lib.myClick(gameTop, r, holdDur = glidedSteelPickAxe)

#,,cook,,ck
def cookStuff(impRaw, impCooked, useCoal=True):
    cnt=1
    while True:
        lib.log("----------------- " + str(cnt))
        if useCoal:
            lib.myClick(bottombar, ix.imgCoal, after=.5, times=1, moveAway=True)
        lib.sleeplogx(1)
        lib.myClick(bottombar, impRaw, after=.5, times=3, moveAway=True)
        lib.sleeplogx(1)
        lib.myClickTillGone(gameLeft, impCooked, waitForImgAppear=1, waitAfterClick=.5, skipIfNotExist=1, moveAway=True)
        cnt=cnt+1

def cookBread(useCoal=True):
    cookStuff(ix.imgDough, ix.imgBread, useCoal)

def cookIron():
    cnt=1
    while True:
        lib.log("----------------- " + str(cnt))
        lib.myClick(bottombar, ix.imgCoal, after=.5, times=1, moveAway=True)
        lib.sleeplogx(1)
        lib.myClick(bottombar, ix.imgIronOre, after=.5, times=3, moveAway=True)
        lib.sleeplogx(1)
        lib.myClickTillGone(SCREEN,ix.imgIron, waitForImgAppear=1, waitAfterClick=.5, skipIfNotExist=1, moveAway=True)
        cnt=cnt+1

def getPlank():
    cnt=1
    while True:
        lib.log("----------------- " + str(cnt))
        lib.myClick(game, ix.imgCoal, after=.5)
        lib.myClick(game, ix.imgWood, after=.5, times=3)
        lib.myClickTillGone(game,ix.imgPlank, waitForImgAppear=1, retryIfNotGone=2, waitAfterClick=.5)
        cnt=cnt+1

def bobApple():
    cnt=1
    while True:
        lib.log("----------------- " + str(cnt))
#        lib.slowTypeChar(Key.SPACE)
        #lib.myClick(game, ix.imgApple, after=.5)
        if lib.logExists(game, ix.imgApple):
            lib.myClickNoerror(game, ix.imgApple, after=.5, holdDur=0.3, times=2, moveAway=True)
        if lib.logExists(SCREEN, ix.imgBubble1):
            lib.myClickNoerror(SCREEN, ix.imgBubble1, after=.5, holdDur=0.2, times=2, moveAway=True)
        if lib.logExists(SCREEN, ix.imgBubble2):
            lib.myClickNoerror(SCREEN, ix.imgBubble2, after=.5, holdDur=0.2, times=2, moveAway=True)
        if lib.logExists(SCREEN, ix.imgBubble3):
            lib.myClickNoerror(SCREEN, ix.imgBubble3, after=.5, holdDur=0.2, times=2, moveAway=True)
        if lib.logExists(SCREEN, ix.imgBubble4):
            lib.myClickNoerror(SCREEN, ix.imgBubble4, after=.5, holdDur=0.2, times=2, moveAway=True)
        if lib.logExists(SCREEN, ix.imgProfile):
            lib.myClickNoerror(SCREEN, ix.imgProfile, after=.5, holdDur=0.2, times=2, moveAway=True)
            
        if lib.logExists(game, ix.imgStar):
            lib.myClickNoerror(game, ix.imgStar, after=.5, holdDur=0.2, times=2)
        #lib.myClickTillGone(game,ix.imgApple, waitForImgAppear=1, waitAfterClick=.5, skipIfNotExist=1, moveAway=True)
        #lib.myClickTillGone(game,ix.imgBubble, waitForImgAppear=1, waitAfterClick=.5, skipIfNotExist=1, moveAway=True)        
        if cnt % 3 == 0:
            lib.slowTypeChar(Key.SPACE)
        lib.sleeplogx(2)        
        cnt=cnt+1    

def debug():
    i=find(testix.img)
    lib.printImgSize(i)
    lib.screenSize()
    
#,,main
initGame()
SCREEN.hover()
lib.log("============================================================") 
bobApple()
#lib.hoverBox(bottombar)
#getPlank()
#getIronRocks()

# lib.sleeplogx(120)
# getTrees()C
# getBirchTrees()z    5755

#cookIron()
    #cookBread(useCoal=True)
    #clearIron()z\\zzzCzXw