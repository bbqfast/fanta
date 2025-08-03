    # BS resolution
# 1280 x 720
# "WindowWidth"=dword:00000680
# "WindowHeight"=dword:000003a8

from sikuli.Sikuli import *
import sys
import org.sikuli.natives.Vision as Vision;
import datetime
import shutil
import traceback
import time
import os
from cStringIO import StringIO

import lib
reload(lib)
import evt
reload(evt)
import accts
reload(accts)
import pc_img as ix
reload(ix)


Vision.setParameter("MinTargetSize", 10) # A small value such as 6 makes the matching 


#v1
state='no train'
loopStart_t=time()
delay=1100
delayStart=60*60*1.5
potUse=0
usePot=True
multiAcct=True
stopAT71=False
gChkDailyInTraining=True
game=None

gAssistAlly=False
hasDailyAds=False
gDeclineAlly=True
gQuestFavOn=True
Settings.WaitScanRate=3.0
# ------ more popular option
#c1
gJoinPanel=False
gTrainFirst=False
gLoopStart=1
gLastTime=time.time()
gIndex=0

# global settings
loop=2

def heartbeat():
    # lib.log("heartbeat()")
    global gLastTime
    dur=time.time()-gLastTime
    lib.log("heartbeat() Duration: " + lib.dur(dur))
    if (dur > (60 * 30)):
        lib.sendMailTItle("HEARTBEAT-" + str(gIndex) + "-" + evt.user + "-")
        gLastTime=time.time()

def waitHour(hr, min):
    lib.log('waitHour()');
    while True:
        now = datetime.datetime.now()
        if (now.hour == hr and now.minute > min):
            break
        lib.sleeplogx(60)
    #print now.year, now.month, now.day, now.hour, now.minute, now.second

def skipFour():
    now = datetime.datetime.now()
    # if (now.hour == 3 and now.minute > 45):
    # if (now.hour == 3 and now.minute > 55):
    if (now.hour == 2 and now.minute > 53):
        lib.log('skipFour()');
        waitHour(3, 0)
        return True
    return False

def initGame():
    lib.log('initGame')
    global bsicon, game, bottomBarDrag, bottomBarDrop, heroBarDrag, heroBarDrop
    bottomBarDrag = lib.Pts(263, 645)
    bottomBarDrop = lib.Pts(163, 645)
    heroBarDrag = lib.Pts(346, 598)
    heroBarDrop = lib.Pts(5, 598)
    #bsicon=find(ix.imgBsBack)
    #bsicon.setY(bsicon.y - 730)
    #bsicon.setX(bsicon.x - 10)
    #bsicon.setW(1280)
    #bsicon.setH(780)
    #bsicon=find(ix.imgBsIcon)
    #bsicon.setW(1280)
    #bsicon.setH(780)
    bsicon=initBsIcon()
    game = find(ix.imgMobaIcon)
    game.setX(game.x - 20)
    game.setW(460)
    game.setH(780)
    game.highlight(1)
    evt.game=game
    lib.game=game
    setTrainBox()

def initBsWide():
    ub = find(ix.imgBsIconMain)
    ub.setX(ub.x - 20)
    ub.setW(1380+80)
    ub.setH(776+80)
    ub.highlight(1)
    return ub

def initBsIcon():
    bsicon = find(ix.imgBsIcon)
    bsicon.setX(bsicon.x - 20)
    bsicon.setW(450)
    bsicon.setH(750)
    bsicon.highlight(1)
    return bsicon

def findTrainPage():
    findPage(ix.imgTrainPage)

def findGuildPage():
    findPage(ix.imgGuildPage)

def findPage(pic, dir = 1):
    rightcnt=5
    while(not game.exists(pic)):
        lib.scrollPos(bottomBarDrag, bottomBarDrop, 1, dir)
        rightcnt=rightcnt-1
        if rightcnt==0:
           dir = dir * -1
           rightcnt=5
    lib.myClickTillGone(game, pic, True)    

def IntoTrain():
    lib.log('IntoTrain')
    global state
    findTrainPage()
    state='train'

def Brave():
    if lib.logExists(trainBox, ix.imgBrave):
        lib.log('brave')
        lib.myClick(trainBox, ix.imgBrave)
        return True
    else:
        return False
def Adv():
    if lib.logExists(trainBox, ix.imgAdv):
        lib.log('advance')
        lib.myClick(trainBox, ix.imgAdv)
        lib.sleeplogx(.7)
        return True
    else:
        return False

def Cont():
    if lib.logExists(trainBox, ix.imgCont):
        lib.log('continue')
        lib.myClick(trainBox, ix.imgCont)
        lib.sleeplogx(.7)
        return True
    else:
        return False

def imgLast(pic):
    lib.log('ix.imgLast')
    tt = findAll(pic)
    tts  = sorted(tt, key=by_y)
    #lib.log(str(len(tts)))
    button=tts[len(tts)-1]
    hover(button)    
    return button

def Start():
    global state
    #if game.exists(ix.imgStartTrain):
    if lib.logExists(game, ix.imgStartTrain):
        lib.log('----------------------- start training')
        #if game.exists(ix.img71):
        if lib.exactExists(game, ix.img71) and stopAT71:
            state='done'
            lib.log('------------ at 7-1 training DONE !')
        else:
            lib.myClickImg(ix.imgLast(ix.imgStartTrain))
            #lib.myClickImg(ix.imgByOrder(ix.imgStartTrain, 0))

#------------------------------------- Daily
#d1
def bingo2():
    if game.exists():
        lib.myClickTillGone(game, ix.imgMyPage, waitForImgAppear=60)
    lib.sleeplogx(5)

def daily():
    lib.myClick(game, ix.imgDailyStart)
    #lib.myWait(area ,pic):
    lib.myClick(game, ix.imgDailyStop)
    lib.myClick(game, ix.imgDailyAds)
    lib.myClick(game, ix.imgBack, after=1)

#------------------------------------- ~Daily
def loginLoop(acctList):
    global loopStart_t
    lib.log('loginLoop')
    # start with training current acct
    if gTrainFirst:
        trainMainLoop() # comment this out for quick cycling of accts
    n = len(acctList)
    i = gLoopStart
    #for x in acctList:
    while True:
        lib.log('loginLoop i=' + str(i))
        loopStart_t=time.time()
        if 'assist' in acctList[i]:
            i=i+1
            continue
        # logOutAndIn(acctList[i]['user'], acctList[i]['passw'], True)
        if 'assist' in acctList[i] and ix.imgAssistAlly:
            assistAlly()
        if not 'login' in acctList[i]:
            trainMainLoop(acctList[i]['user'])
        else:
            if gJoinPanel:
                joinPanel()
            #assistAlly()
        i=i+1
        if i > n-1:
            i=0
        dur=time.time() - loopStart_t
        lib.log('Cycle duration=' + str(dur))
    
def trainMainLoop(user='unknown'):
    global loop, delay, state
    #for o in range(1,loop):
    while (not state=='done'):
        lib.log('outer train loop')
        if gAssistAlly:
            assistAlly()
        if gJoinPanel:
            joinPanel()
        if gChkDailyInTraining:            
            chkDaily()
        IntoTrain()
        #state='train'
        challenge()
        Start()
        lib.log('state=' + state)      
        while state=='train':
                if Adv():
                    continue
                if Brave():
                    continue
                if Cont():
                    continue
                Boss()
                if not Heal(): ##
                    break
                challenge()
                Start()
                sleep(.1)
        lib.myClickTillGone(game, ix.imgMyPage, waitForImgAppear=30)
        # during multi acct mode, we dont wait for regen, we move on to next account
        if multiAcct:
            state='no train'
            break
        lib.sleeplogx(delay)
        if gChkDailyInTraining:            
            chkDaily()
        #state=='train'
    lib.log('main loop EXIT')      
    saveStatsShot(user)

#if isRotaryHour():
#    chkDaily()


def setTrainBox():
    global trainBox
    trainBox = find(ix.imgMobaIcon)
    trainBox.setX(trainBox.x - 10)
    trainBox.setY(trainBox.y + 620)
    trainBox.setW(400)
    trainBox.setH(90)
    
def cleanLoginBox():
    mouseMove(Location(bsicon.getX() + 126, bsicon.getY() + 138))
    clickHere(1)   
    lib.slowTypeChar(Key.BACKSPACE)
    mouseMove(Location(bsicon.getX() + 126, bsicon.getY() + 188))
    clickHere(1)   
    lib.slowTypeChar(Key.BACKSPACE)
    
def loginFanta(user, passw):
    lib.log('loginFanta(' + user + ', ' + passw + ')')
    lib.myWait(SCREEN, ix.imgTermsYes, 5)
    while lib.logExists(SCREEN, ix.imgTermsYes, 1):
        lib.myClick(SCREEN, ix.imgTermsYes, waitForImgAppear=1, after=1)        

    if lib.myWait(SCREEN ,ix.imgLogin, 10):
        bsicon=initBsIcon()
#        lib.myClickTillGone(SCREEN, ix.imgLogin, waitForImgAppear=5)
        while (lib.logExists(SCREEN, ix.imgSignup)): 
            lib.myClick(SCREEN, ix.imgLogin, waitForImgAppear=0, after=1.5)
        #lib.clicklog(ix.imgLogin)    
        sleep(3)
        loginEnter(user, passw)
        # if lib.logExists(SCREEN, ix.imgLoginErrorOk):
        #     lib.log('Login error')
        #     lib.clicklog(ix.imgLoginErrorOk)    
        #     lib.clicklog(ix.imgLogin)
    #lib.myClick(SCREEN,ix.imgStartGame, waitForImgAppear=30)
    #lib.myWait(SCREEN, ix.imgStartGame, 30)
    afterLogin()
    #cancelMoba() 
    #cancelSound()
    sleep(1)
    #lib.myClick(SCREEN,ix.imgStartGame)


def afterLogin():
    lib.log('afterLogin()')
    # lib.myWaitFor3(SCREEN, ix.imgStartGame, ix.imgTermsYes, ix.imgLogin, 5)
    # while lib.logExists(SCREEN, ix.imgTermsYes):
    #     lib.myClick(SCREEN, ix.imgTermsYes)
    # cmax=180
    cmax=120
    c=0
    while not lib.logExists(SCREEN, ix.imgStartGame) and c<=cmax:
        lib.mysleep(1)
        lib.log("Waiting start game =" + str(c))
        if lib.logExists(SCREEN, ix.imgNetworkErrorTxt):
            lib.log("network error")
            raise lib.LoginFail("network error")
        c=c+1

    if c > cmax:
        lib.log("Fanta crashed")
        raise lib.LoginFail("Fanta crashed")

    lib.myClickTillGone(SCREEN, ix.imgStartGame, waitForImgAppear=1, retryIfNotGone=1)
    # lib.myClick(SCREEN, ix.imgStartGame, waitForImgAppear=240)
    initGame()
    lib.sleeplogx(2) # delay on first display
    # if lib.logExists(game, ix.imgNoFull, 1):
    #     lib.myClick(game, ix.imgNoFull)
    if lib.logExists(game, lib.ixact(ix.imgNo), 1):
        lib.myClick(game, lib.ixact(ix.imgNo), after=4)
    if lib.logExists(game, ix.imgMyPage, 1):
        lib.myClick(game, ix.imgMyPage, waitForImgAppear=1, after=1.5)
    if lib.logExists(game, lib.ixact(ix.imgBack), 1):
        lib.myClickTillGone(game, lib.ixact(ix.imgBack), waitForImgAppear=0, retryIfNotGone=3, waitAfterClick=4)
        # lib.myClick(game, ix.imgBack, after=1)
    if lib.logExists(game, ix.imgMina, 0):
        lib.log("Mina=fresh account")
        raise lib.FreshAcctError("fresh account")
    if lib.logExists(game, ix.imgCloseAnnounce, 2):
        lib.log("CLose announcement")
        lib.myClick(game, ix.imgCloseAnnounce)



def loginEnter(user, passw):
    lib.clicklog(ix.imgLoginBox)
    #lib.myClick(SCREEN, ix.imgLoginBox)
    sleep(3)
    lib.slowType(user)
    lib.sleeplogx(3)
    lib.clicklog(ix.imgPassBox)
#            lib.myClick(SCREEN, ix.imgPassBox)
    lib.slowType(passw)
    lib.sleeplogx(3)
    lib.clicklog(ix.imgLogin)    
    lib.sleeplogx(5)
    if lib.logExists(SCREEN, lib.ixact(ix.imgLoginErrorOk)):
        lib.log('loginEnter() - bad password')
        raise lib.LoginError("wrong password")

def cancelAnnounce():
    if(game.exists(ix.imgAnnounceClose)):
        lib.log('cancelAnnounce')
        lib.myClick(game, ix.imgAnnounceClose)
        sleep(2)

# old version doesnt restart bs

#if(game.exists(ix.imgBack)):
        #lib.log('ix.imgBack -- free card promo')
        #lib.myClick(game, ix.imgBack, after=1)
        #sleep(2)
    # chkDaily()  # no daily for now replaced by bingo

def deferAlly():
    lib.log('deferAlly()')
    #if game.exists(ix.imgAllyWaiting):
    if lib.logExists(game, ix.imgAllyWaiting, 2):
        declineAlly()
        lib.log('declineAlly')
        lib.myClickTillGone(game, ix.imgBack, waitForImgAppear=5)
        #lib.myClick(game, ix.imgBack, after=1)
        sleep(3)


def singleTrain():
    global multiAcct, usePot
    multiAcct=False
    usePot=False
    trainMainLoop()

def saveStatsShot(name):
    #pic = find(gImgScore) 
    pic = find(ix.imgMobaIcon)
    pic.setW(400)
    pic.setH(600)
    pic.hover()
    file=capture(pic)
    #shutil.move(file, name + "=" + timestamp() + ".png")
    shutil.move(file, name + ".png")
    pic = None # clean up


def lookatInventory(name):
    findPage(ix.imgProfilePage)
    lib.myClick(game, ix.imgInventory)
    lib.myWait(game, ix.imgInventoryView, 3)
    lib.screenShot(game, name)
    lib.myClick(game, ix.imgBack, after=1)

def assistAlly():
    lib.log('assistAlly()')
    findEventTrainPage()
    lib.myClickTillGone(game, ix.imgAssists, waitForImgAppear=5)
    lib.sleeplogx(3)
    while exists(ix.imgAssistAlly):
        lib.myClick(game, ix.imgAssistAlly)
        lib.sleeplogx(3)
    lib.myClickTillGone(game, ix.imgEvent, waitForImgAppear=5)
    lib.myClickTillGone(game, ix.imgMyPage, waitForImgAppear=5)

#jp
def joinPanelold():
    lib.log('joinPanel()')
    findPanelPage()
    lib.sleeplogx(3)
    if game.exists(ix.imgPanelEventButton):
        lib.myClickTillGone(game, ix.imgPanelEventButton, waitForImgAppear=5)
    lib.myClickTillGone(game, ix.imgBack, waitForImgAppear=5)

def declineAlly():
    while game.exists(ix.imgDeclineAlly):
        lib.myClick(game, ix.imgDeclineAlly)
        lib.sleeplogx(3)

def postMsg(msg):
    Env.setClipboard(msg)
    hover(ix.imgMsgBox)
    game.mouseDown(Button.LEFT)
    lib.sleeplogx(3)
    game.mouseUp(Button.LEFT)
    lib.myClick(game, ix.imgPaste)
    lib.myClick(game, ix.imgSend)

def findProfile():
    lib.myClick(game, ix.imgProfile)
    #lib.myClick(game, ix.imgProfileExact)

def loopAds(msg, times):
    for n in range(1, times):
        if not game.exists(ix.imgMyname):
            postMsg(msg)
            lib.sleeplogx(7)
        dragDrop(ix.imgProfile, ix.imgSend)
        findProfile()

def clickHere(hold = .5):
    mouseDown(Button.LEFT)
    sleep(hold)
    mouseUp(Button.LEFT)
    sleep(.5)

def place(pos):
    lib.log('place() x=' + str(pos.x) + 'y=' + str(pos.y))
    mouseMove(Location(game.getX() + pos.x, game.getY() + pos.y))
#myDrag(Location(game.getX() + pos1.x, game.getY() + pos1.y))            
    clickHere()   

def repeatClicks():
    for n in range(1, 50):
        place(center)

def bossMessage():
    bossMsg = Pts(209, 553)
    place(bossMsg)

def clickMaidenMessage():
    while game.exists(ix.imgMaidenMsgArea):
        lib.myClick(game, ix.imgMaidenMsgArea)
        lib.sleeplogx(1)

def placeUnit():
    lib.log('placeUnit()');
    l = [pos1, pos2, pos3]
    loopUnits(l)

def placeAlly():
    lib.log('placeAlly()');
    l = [pos4, pos5, pos6]
    loopAlly(l)

def loopAlly(posList):
    loopDeploy(ix.imgCallAllyExact, posList)

def loopUnits(posList):
    loopDeploy(ix.imgDeployStartExact, posList, True)

def loopDeploy(imgButton, posList, fav=False):
    #lib.myClick(game, imgButton) #first Ally click can be missed
    ## potential infinite loop if there are timing issue where Deploy button just disappear right before doing my click
    ## consider using a special version of myClick where we dont wait for the button
    lib.myClickTillGone(game, imgButton, waitForImgAppear=5)   
    c=1
    if gQuestFavOn and game.exists(ix.imgFavOff):
        lib.myClick(game, ix.imgFavOff)
    for x in posList:
        if not deploy(imgButton, x, c):
            return
        lib.log('placed ' + str(c))
        c=c+1

def deploy(imgButton, pos, idx):
    #ix.imgCallAllyZeroExact
    #comp=Image2(ix.imgDeployStartZeroExact, ix.imgCallAllyZeroExact)
    #if lib.logExists(game, ix.imgDeployStartZeroExact):
    #if comp.existsOr(game):
        #lib.log('No more ally or unit left to deploy')
        #return False
    if lib.logExists(game, ix.imgDefenseFailed):
        lib.log('DEFENSE FAILED')
        return False
    if not idx==1:
        if not lib.logExists(game, imgButton):
            lib.log('No more deploy for ' + strimg(imgButton))
            return False
        lib.myClick(game, imgButton) 
    if not lib.logExists(game, ix.imgDeployExact):
        lib.log('No Unit to deploy')
        lib.myClick(game, ix.imgBack, after=1)
        return False
    # ix.imgFirstDeploy=ix.imgByOrder(ix.imgDeployExact, 0)
    ix.imgFirstDeploy=ix.findByOrder(game, ix.imgDeployExact, 0)
    lib.myWait(game ,ix.imgDeployConfirm, totalWaits=10, takeshot=True)
    lib.myClickImg(ix.imgFirstDeploy)
    if not lib.logExists(game, ix.imgDeployConfirm):
        lib.myClick(game, ix.imgBack, after=1)
        return False
    #place(pos)
    #lib.myClick(game, ix.imgDeployConfirm)
    #while not lib.myWait(SCREEN ,ix.imgMyProfileFrom, 6):
    while lib.logExists(game, ix.imgDeployConfirm):
        lib.log('Confirm place')
        place(pos)
        lib.myClick(game, ix.imgDeployConfirm)
        lib.sleeplogx(1)
    return True

def doQuest():
    global questEndime
    placeUnit()
    placeAlly()
    while(not game.exists(ix.imgEventPageSmall)): # wait for event end
        sleep(5)
    maidenBackToEvent()        
    questEndime=time.time()

def saveRanks():
    lib.myClick(game, ix.imgRankings)
    lib.myWait(game ,ix.imgBack, 10)
    lib.screenShot(game, "Ranking-")
    lib.myClick(game, ix.imgBack, after=1)


def showList(list):
    for i, val in enumerate(list):
        lib.log( str(i) + ' ' + val['user'])

def showList(list):
    out = StringIO()
    # return out.getvalue()    
    for i, val in enumerate(list):
        print >>out, str(i) + ' ' + val['user']    # 'out' behaves like a file
        # lib.log( str(i) + ' ' + val['user'])

    lib.log(out.getvalue())        

def loopAlly():
    while makeAlly():
        lib.log("loopAlly")

def clearAlly():
    lib.log('clearAlly()')
    #if game.exists(ix.imgAllyWaiting):
    if lib.myWait(game, ix.imgAllyWaiting, 3):
        loopAlly()
        lib.myClickTillGone(game, ix.imgBack, waitForImgAppear=5)
        #lib.myClick(game, ix.imgBack, after=1)
        sleep(3)

def makeAlly(idx=0):
    #pic=game.find(ix.imgDeclineAlly)
    if not lib.logExists(game, ix.imgDeclineAlly ):
        lib.log("No more pending Ally")
        return False
    # pic = ix.imgByOrder(ix.imgDeclineAlly, idx)
    pic = ix.findByOrder(game, ix.imgDeclineAlly, idx)
    #game.hover(pic)
    pic.setX(pic.x - 300)
    pic.setY(pic.y - 130)
    pic.setW(400)
    pic.setH(170)
    #lib.hoverBox(pic)
    if lib.logExists(pic, ix.imgKppExact):
        lib.log("approve")
        pic.hover(ix.imgApproveAlly)
        lib.myClick(pic,ix.imgApproveAlly)
    else:
        lib.log("decline")
        pic.hover(ix.imgDeclineAlly)
        lib.myClick(pic,ix.imgDeclineAlly)
    return True

def bingo3(): 
    if lib.logExists(game, ix.imgMyPage):
        lib.myClick(game, ix.imgMyPage)            
    if lib.logExists(game, ix.imgBingo):
        while not lib.logExists(game, ix.imgBingoRemainingExact): 
            if lib.logExists(game, ix.imgSquare):
                lib.myClick(game, ix.imgSquare)
                lib.sleeplogx(2)
            while lib.logExists(game, ix.imgReceive):
                lib.myClick(game, ix.imgReceive)    
                lib.sleeplogx(5)
        lib.myClick(game, ix.imgMyPage)            
    #hover(ix.imgMyPage)
    #hover(ix.imgMyPageExact)

def launchPlayStore():
    lib.clickTillNext(SCREEN, ix.imgBsIcon, ix.imgBSSystemApp)
    lib.clickTillNext(SCREEN, ix.imgBSSystemApp, ix.imgBSPlayStore)
    lib.clickTillNext(SCREEN, ix.imgBSPlayStore, ix.imgBSPlayTextBox)
    playStoreFindFanta()

def launchFileManager():
    lib.clickTillNext(SCREEN, ix.imgBsIcon, ix.imgBSSystemApp)
    lib.clickTillNext(SCREEN, ix.imgBSFileManager, ix.imgFileManager2)

def locBsIcon():
    return find(ix.imgBsIcon)

#ri1
def reinstall():
    # lib.clickTillNext(SCREEN, ix.imgPlayStore, ix.imgPlayUninstall)
    lib.clickTillNext(SCREEN, ix.imgPlayStore, ix.imgBSPlayHighlighted, after=1.3)
    # lib.myClick(SCREEN, ix.imgPlayStore)
    # lib.myClick(SCREEN, ix.imgPlayUninstall)
    playStoreFindFanta()
    lib.clickTillNext(SCREEN, ix.imgPlayUninstall, ix.imgPlayOk)
    lib.clickTillNext(SCREEN, ix.imgPlayOk, ix.imgPlayInstall)
    # lib.myClick(SCREEN, ix.imgPlayOk)
    # lib.myClick(SCREEN, ix.imgPlayInstall)
    lib.clickTillNext(SCREEN, ix.imgPlayInstall, ix.imgPlayAccept, after=1.5)
    lib.myClick(SCREEN, ix.imgPlayAccept)      

    # lib.clickTillNext(SCREEN, ix.imgPlayAccept, ix.imgPlayUninstall)
    # lib.myWait(SCREEN ,ix.imgPlayUninstall, 30)

def startFanta():
    lib.myClick(SCREEN, ix.imgPlayStore)
    playStoreFindFanta()
    # lib.myClick(SCREEN, ix.imgPlayOpen)
    # lib.clickTillGone(SCREEN, ix.imgPlayOpen)
    # lib.clickTillGone(SCREEN, ix.imgPlayOpen)
    if not lib.clickTillNext(SCREEN, ix.imgPlayOpen, lib.ixact(ix.imgFantaIconTop, .85), retryIfNotGone=20):
        raise lib.InfiniteLoop('startFanta()')

def renameBox(ub):
     setBox(ub, -30, -80, w=450, h=330)
     return ub


def renameBack():
    # lib.sleeplogx(1) handle rename faile
    tt=find(ix.imgFolderRenameTitle)
    box=renameBox(tt)
    cnt=10
    # while lib.logExists(box, lib.ixact(ix.imgFolderEdited)) and cnt > 0:
    while not lib.logExists(box, lib.ixact(ix.imgFolderNotEdited, .85)) and cnt > 0:
        lib.slowTypeChar(Key.RIGHT)
        lib.slowTypeChar(Key.BACKSPACE)
        lib.sleeplogx(.5)
        cnt-=1
    if cnt <= 0:
        lib.slowTypeChar(Key.ESC)
        # lib.myClick(SCREEN, ix.imgFolderRenameCancel)
        return False
        # raise lib.InfiniteLoop('Infinite loop')
    lib.myClick(SCREEN, ix.imgFolderRenameOK)
    return True
    
def rename():
    tt=find(ix.imgFolderRenameTitle)
    box=renameBox(tt)
    cnt=10
    while not lib.logExists(box, lib.ixact(ix.imgFolderEdited, .85)) and cnt > 0:
        lib.slowTypeChar('5')
        # keyUp()
        lib.sleeplogx(.5)
        cnt-=1
    if cnt <= 0:
        lib.slowTypeChar(Key.ESC)
        # lib.myClick(SCREEN, ix.imgFolderRenameCancel)
        return False
    lib.myClick(SCREEN, ix.imgFolderRenameOK)
    return True

def clickAndRename(renamer):
    # if lib.logExists(SCREEN, ix.imgFolderFanta):
    try:
        res=False
        retry=0
        while not res:
            lib.myClickHold(SCREEN, lib.ixact(ix.imgFolderFanta))
            lib.clicklog(ix.imgFolderRename)
            res=renamer()
            lib.sleeplogx(2)
            lib.logx("rename retry=" + str(retry))
            retry+=1
            if retry > 20:
                lib.logx("rename retry exceeded")
                raise lib.InfiniteLoop('Infinite clickAndRename')
    except:
        lib.log("clickAndRename exception")
        lib.log(traceback.format_exc())       
        raise lib.InfiniteLoop('Infinite loop 3')

def gotoFanta():
    global bswide
    # lib.myClick(SCREEN, ix.imgFileManager)
    lib.clickTillNext(SCREEN, ix.imgFileManager, ix.imgFileManager2, after=1.5)
    bswide=initBsWide()
    bswide.highlight(1)
    if lib.logExists(bswide, lib.ixact(ix.imgPathRoot)):
        lib.clickTillNext(bswide, ix.imgFolderSdcard, lib.ixact(ix.imgPathSD))
    if lib.logExists(bswide, lib.ixact(ix.imgPathSD)):
        lib.clickTillNext(bswide, ix.imgFolderAndroid, lib.ixact(ix.imgPathAndroid))
    if lib.logExists(bswide, lib.ixact(ix.imgPathAndroid)):
        lib.clickTillNext(bswide, ix.imgFolderData, lib.ixact(ix.imgPathData))
    if lib.logExists(bswide, lib.ixact(ix.imgPathData)):
        while(not exists(ix.imgFolderFanta)):
            p1 = lib.Pts(566, 679)
            p2 = lib.Pts(572, 346)
            lib.scrollPos(locBsIcon(), p1,p2,1,1)    

def playStoreFindFanta():
    lib.log("playStoreFindFanta()")
    if lib.logExists(SCREEN, ix.imgBSPlayTextBox):
        #lib.clickTillNext(SCREEN, ix.imgBSPlayStore, ix.imgBSPlayTextBox)
        lib.clicklog(ix.imgBSPlayTextBox)
        #lib.clicklog(ix.imgBSPlayTextBox)
        lib.slowType('fantasica')
        lib.slowTypeChar(Key.ENTER)
        lib.clicklog(ix.imgBSFantaApp)


def logOff():
    gotoFanta()
    clickAndRename(rename)
    reinstall()
    gotoFanta()
    clickAndRename(renameBack)    
    #lib.clickTillNext(SCREEN, ix.imgPlayAccept, ix.imgPlayUninstall)
    startFanta()

def bingo():
    lib.log("bingo() new")
    if lib.logExists(game, ix.imgMyPage, 1):
        lib.myClick(game, ix.imgMyPage)
        lib.sleeplogx(3)
        # lib.myWaitFor2(game ,ix.imgBack, ix.imgNextPage, 5)
        if lib.logExists(game, ix.imgBack, 2):
            lib.myClick(game, ix.imgBack, after=1)        
        if lib.logExists(game, ix.imgNextPage, 2):
            lib.myClick(game, ix.imgNextPage)
        # bingo removed in 2018
        # if lib.logExists(game, ix.imgBingo):
        #     while(not exists(lib.ixact(ix.imgBingoRemain, .92))):
        #         lib.myClick(game, ix.imgBingoFlip)
        #         while(game.exists(ix.imgBingoReceive)):
        #             lib.myClick(game, ix.imgBingoReceive)
        #             lib.sleeplogx(5)
        #     if lib.logExists(game, ix.imgMyPage):
        #         lib.log("Finish Bingo")
        #         lib.myClickTillGone(game, ix.imgMyPage, waitForImgAppear=60)
        if lib.logExists(game, ix.imgCloseAnnounce, 2):
            lib.log("CLose announcement")
            lib.myClick(game, ix.imgCloseAnnounce)

#rg1 re1
def receiveGift():
    lib.log("receiveGift()")
    # lib.myClick(game, ix.imgMenu)
    lib.myClickTillNext(game, ix.imgMenu, ix.imgMenuPressed)
    lib.myClick(game, ix.imgPastEvent, after=1.5)
    lib.myClick(game, ix.imgFinalRanking, after=1.5)
    lib.screenShot(game, "old-rank-" + evt.user + "-shot-")
    lib.myClick(game, ix.imgReceive, after=1)
    lib.myClick(game, ix.imgBack, waitForImgAppear=1, after=1)
    lib.myClick(game, ix.imgBack, waitForImgAppear=1.5, after=1)
    # lib.myClick(game, ix.imgMyPage, waitForImgAppear=1, after=1)
    # lib.myClick(game, ix.imgMainPage, waitForImgAppear=1, after=1)
    # lib.myClick(game, ix.imgBackToMyPage, 1)
    #ib.myClick(game, ix.imgBackMain, 1)
    lib.myClick(game, ix.imgMenuPressed)


def topBarBox(ub):
     setBox(ub, -7, -7, w=450, h=40)
     return ub

def closeFantaApp():
    lib.log('closeFantaApp()')
    ii=find(ix.imgBsIcon)
    bx=topBarBox(ii)
    try:
        lib.myClick(bx, ix.imgFantaClose, waitForImgAppear=0, after=1)
        clickHere(1)
    except:
        lib.log('closeFantaApp() except OK')
        pass   

def restartFanta():
    lib.log('restartFanta')
    closeFantaApp()
    #lib.clickTillNext(SCREEN, ix.imgPlayStore, ix.imgBSPlayHighlighted)
    startFanta()
    loginFanta(user, passw)    

#,loi
def logOutAndIn(user, passw, reset=False):
    lib.log('logOutAndIn(' + user + ', ' + passw + ',' + str(reset) + ')')
    if reset:
        closeFantaApp()
        #lib.clickTillNext(SCREEN, ix.imgPlayStore, ix.imgBSPlayHighlighted)
        # startFanta()
        quickLaunch()
        afterLogin()
        # loginFanta(user, passw)    
    elif lib.logExists(bsicon, ix.imgLogin): 
        if lib.logExists(SCREEN, ix.imgSignup): # on sign up page
            lib.myClick(SCREEN, ix.imgLogin)
        loginEnter(user, passw)
        afterLogin()
    else:
        # logOff()
        quickLogOff()
        # lib.sleeplogx(5)
        loginFanta(user, passw)
    evt.user=user

def joinClash():
    lib.log("joinClash()")
    lib.myClick(game, ix.imgClash)
    if game.exists(ix.imgClashSearch):
        lib.myClick(game, ix.imgClashSearch, waitForImgAppear=1)
        lib.myClick(game, ix.imgClahsRandom, waitForImgAppear=1)
        lib.myClick(game, ix.imgYes, waitForImgAppear=1)
        lib.clicklog(ix.imgClashMina)
    lib.myClick(game, ix.imgMyPage)

def joinGift():
    lib.log("joinGift()")
    lib.myClick(game, evt.imgGiftMain)    
    lib.myClick(game, evt.imgGiftGift)
    lib.myClick(game, evt.imgGiftRandom, 1)
    lib.sleeplogx(1)
    #lib.locateg(game, lib.ixact(evt.imgGiftGift2))
    while not lib.logExists(game, lib.ixact(evt.imgGiftGift2)):
        lib.clicklog(evt.imgGiftPlusOne)
    lib.myClick(game, evt.imgGiftGift2)
    lib.myClick(game, evt.imgYes)
    lib.myClick(game, evt.imgBack)
    lib.myClick(game, evt.imgGiftBack, 1)


# doesnt go back to main menu
# jf1
def joinFrontlines():
    lib.myClick(game, evt.imgFrontlinesMain)
    lib.myWait(game, evt.imgMyPage, 3) # get the pause
    while lib.logExists(game, evt.imgFrontlinesIntro, 1):
        lib.quickClick(game, evt.imgFrontlinesIntro)
    # lib.clickTillGone(game, evt.imgFrontlinesIntro)
    lib.myClick(game, evt.imgMyPage, waitForImgAppear=2, after=1)


def InboxAndRegister():
    lib.myClick(game,ix.imgMenu,1)
    lib.myClick(game,ix.imgInboxMain, waitForImgAppear=1, after=1.5)
    if lib.logExists(game, ix.imgRegister, 1):
        lib.myClick(game,ix.imgRegister,1)
        lib.myClick(game,ix.imgRegisterMore,1)
        lib.myClick(game,ix.imgBack,1)
        lib.myClick(game,ix.imgRegisterDevice,1)
        lib.myClick(game,ix.imgMyPage,1)
    else:
        lib.myClick(game,ix.imgBack,1)
    lib.myClick(game,ix.imgMenuPressed,1)

def unitBox2(pic):
    try:
        ub=find(pic)
        ub.setX(unitBox.x - 10)
        ub.setY(unitBox.y - 80)
        ub.setW(450)
        ub.setH(100)  
        lib.hoverBox(ub)
        return ub
    except:
       return None
    return None

def unitBox(ub):
    lib.log('unitBox()')
    # ub=find(pic)
    ub.setX(ub.x - 10)
    ub.setY(ub.y - 80)
    ub.setW(450)
    ub.setH(100)  
    ub.highlight(1)
#    lib.hoverBox(ub)
    return ub


def selectUnit(pic):
    lib.log('selectUnit()')
    while True:
        # ub=unitBox(ix.imgOneStarExact)
        ub=unitBox(pic)
        if not ub:
            lib.log('No unit found')
            return
    if lib.logExists(ub, ix.imgUnselected):
        # lib.log('advance')
        lib.myClick(ub, ix.imgUnselected)


def selectUnits(total, unit1, unit2):
    lib.log("selectUnits()" + str(total))
    if total==0:
        return 0
    cnt=0
    try:
        # io=lib.tryImgsByOrder(lib.ixact(ix.imgOneStar))
        io=lib.tryImgsByOrder(lib.ixact(unit1))
        # if len(io)==0:
        #     lib.log("selectUnits- no units, try monster")
        io=io + lib.tryImgsByOrder(lib.ixact(unit2))
        for x in io:
            hover(x)
            ub=unitBox(x)
            if lib.logExists(ub, lib.ixact(ix.imgUnselected)):
                # lib.log('advance')
                lib.myClick(ub, ix.imgUnselected)
                cnt+=1
                if (cnt >= total):
                    return cnt
    except:
        lib.log('selectUnits() no units found')
        raise
        # return 0
    return cnt

def scrollUnits():
    p1 = lib.Pts(74, 552)
    p2 = lib.Pts(74, 250)
#    p2 = lib.Pts(74, 195)
    #lib.scrollPos(locBsIcon(), p1,p2,1,1)
    lib.scrollPos(game, p1,p2,1,1)

def scrollAndSelect(num, pic1, pic2):
    lib.log("scrollAndSelect()" + str(num))
    cnt=0
    page=0
    while True:
        page+=1
        inc=selectUnits(num-cnt, pic1, pic2)
        # if inc==0:
        #     break
        cnt=cnt+inc
        lib.log("cnt="+str(cnt))
        if cnt>=num:
            break;
        if page>5:
            break;
        scrollUnits()
    return cnt

#su1
def sellUnits():
    lib.myClick(game, ix.imgMenu)
    lib.myClick(game, ix.imgSellMain)
    doSell()

def doSell(num=12):
    cnt=scrollAndSelect(num, ix.imgOneStar, ix.imgOneStarMon)
    if not cnt==0:
        lib.myClick(game, ix.imgSell)
        lib.myClick(game, ix.imgSell2)
    lib.myClick(game, ix.imgBack, after=1)
    lib.myClick(game, ix.imgMenuPressed)    

def inbox8star():
    inboxGetUnit(ix.imgInbox7to8, ix.img7StarInbox, unitBoxFromStars)

def inboxQCunit():
    inboxGetUnit(ix.imgInbox5to6, ix.imgQCUnit)


def inboxGetUnit(unitlevel, unit, boxFunc, cnt=1):
    lib.myClick(game, ix.imgMenu)
    lib.myClick(game, ix.imgInboxMain, 1)

    lib.myClick(game, ix.imgInboxAll, 1)
    lib.myClick(game, ix.imgInboxUnits, 1)
    lib.myClick(game, ix.imgInbox1to4, 1)
    lib.myClick(game, unitlevel, 1)
   
    while(cnt > 0):
        i=0   
        while not lib.logExists(game, unit):
            i=i+1
            if (i>4):
                lib.myClick(game, ix.imgBack, waitForImgAppear=1, after=1)
                lib.myClick(game, ix.imgMenuPressed, 1)
                return
            scrollUnits()
                
        ub=boxFunc(unit)
        lib.myClick(ub, ix.imgReceive, 1)
        cnt=cnt-1
    lib.myClick(game, ix.imgBack, waitForImgAppear=1, after=1)
    lib.myClick(game, ix.imgMenuPressed, 1)

    
def inboxItems_old():
    lib.log('inboxItems()')
    lib.myClick(game, ix.imgMenu)
    lib.myClick(game, ix.imgInboxMain, 1)
    lib.myClick(game, ix.imgInboxAll, 1)
    lib.myClick(game, ix.imgInboxItems, 1)
    while True:
        try:
            lib.myClick(game, ix.imgReceive, waitForImgAppear=2, after=1.5)
        except:
            lib.log('inboxItems() except: no receive')
            break
    lib.myClick(game, ix.imgBack, waitForImgAppear=1, after=1)
    lib.myClick(game, ix.imgMenuPressed, 1)

def inboxItems():
    lib.log('inboxItems()')
    lib.myClick(game, ix.imgMenu)
    lib.myClick(game, ix.imgInboxMain, 1)
    # lib.sleeplogx(2)
    lib.myWait(game ,ix.imgBack, 4)
    if not lib.logExists(game, lib.ixact(ix.imgInboxItemsTabHighLight)):
        lib.myClick(game, ix.imgInboxItemsTab, after=1)
    while lib.logExists(game, lib.ixact(ix.imgInboxSelectAll)):
        lib.myClick(game, ix.imgInboxSelectAll)
        lib.myClick(game, ix.imgInboxConfirm)
        lib.myClick(game, ix.imgInboxReceive)
        lib.myClick(game, ix.imgYes)
        lib.sleeplogx(2)
    lib.myClick(game, ix.imgBack, waitForImgAppear=1, after=1)
    lib.myClick(game, ix.imgMenuPressed, 1)

def unitBox3(pic, hover=True): # unused
    ub=find(pic)
    ub.setX(ub.x - 5)
    ub.setY(ub.y - 10)
    ub.setW(450)
    ub.setH(90)  
    if hover:
        lib.hoverBox(ub)
    return ub

def unitBoxFromStars(pic): # unused
    ub=unitBox3(pic, hover=False)
    ub.setY(ub.y - 50)
    #lib.hoverBox(ub)
    ub.highlight(1)
    return ub

def changeLeader():
    lib.myClick(game, ix.imgMenu)
    lib.myClick(game, ix.umgUnitsMain)
    if lib.logExists(game, ix.imgSortByDefault, 2):
        lib.myClick(game, ix.imgSortByDefault)
    if lib.logExists(game, ix.imgSortByLevelHigh, 2):
        lib.myClick(game, ix.imgSortByLevelHigh)
    #lib.clickTillNext(game, ix.imgSortByRarityHigh, ix.imgSortByRarityHigh)
    #ub=unitBox(find(ix.imgEightStar))    
    #ub=unitBox(find(ix.imgOneStar))    
    #lib.myClick(ub, ix.imgDetails)

    lib.myClickIdx(game, ix.imgDetails, 0)

    lib.myClick(game, ix.imgUnitsLeader)
    lib.myClick(game, ix.imgBack, after=1)
    lib.myClick(game, ix.imgBack, after=1)
    lib.myClick(game, ix.imgMenuPressed)

def OLDpullPack(): 
    lib.myClick(game, ix.imgCardPackMain, 1)
    lib.myClick(game, ix.imgCardPackStandard, 1)
    if lib.logExists(game, ix.imgCardUseTicketExact, 1):
        lib.myClick(game, ix.imgCardUseTicketExact)
        lib.myClick(game, ix.imgBack, after=1)
    lib.myClick(game, ix.imgBack, after=1)

def pullBraveMain():
    lib.myClick(game, ix.imgCardPackMain, 1)
    lib.sleeplogx(1)
    pullBrave()

def pullGSPack():
    lib.myClick(game, ix.imgCardPackMain, 1)
    lib.sleeplogx(1)
    gotoGSPacks()
    while lib.logExists(game, ix.imgCardPackUseTicket, 2):
        lib.myClick(game, ix.imgCardPackUseTicket, waitForImgAppear=1, after=1)
        # lib.myWait(game ,ix.imgBack, 2)
        lib.sleeplogx(1.5)
        lib.screenShot(game, "Pull-" + evt.user)
        if lib.logExists(game, ix.imgBack, 2):
            lib.myClick(game, ix.imgBack, waitForImgAppear=1, after=2)
        else:
            break    

#cl2
def loginAndChk(user, pw):
    lib.log("loginAndChk: " + user + "  " + pw)
    logOutAndIn(user, pw)
    bingo()
    InboxAndRegister()
    inboxItems()
    ssPotion()
    # leaderAndTrain()

def loginAndClaim(user, pw, reset=False, actions=''):
    lib.log("loginAndClaim: " + user + "  " + pw + " actions=" + actions)
    try:
        start_t=time.time()

        # raise lib.InfiniteLoop("test error 1011")
        logOutAndIn(user, pw, reset)
        # getMPtrade()
        # ally()
#cl1
        # getPotion()
        # tradeStuffPure()
        # if 'p' in actions:
        #     getMP()
        # inboxItems()
        # getPotion()
        # InboxAndRegister()
        # if 'e' in actions:
        joinEvent()
        # if 't' in actions:
        # evt.trainLoopNormal(isDaily=False, firstStage=True)
        # evt.trainLoopNormal(isDaily=False)
        # if 'l' in actions:
        # leaderOnly()
        if not 's' in actions:
            missions()
        # changeLeader()
        # lib.screenShot(game, "leader-" + evt.user + "-shot-")
        # sellAndLeader()
        # trainAndAlly()
        # doQuest()
        # changeLeader()
        # leaderAndTrain()
        # inboxItems()
        # sellUnits()
        #fixMP()
        #chkAcct()
  
    finally:
        dur=time.time() - start_t
        lib.log("loginAndClaim() Duration: " + lib.dur(dur))

def joinEvent():
    receiveGift()
    evt.joinPanel()
    # evt.diceEnter()
    # evt.joinClash()
    # evt.joinTrain()
    # evt.joinTacticsOnly()
    # evt.joinGift()
    # evt.joinEvo()
    # joinFrontlines()

def runEvent():
    #setupClash()
    #evt.clash()          
    #playTactics()
    raise ValueError

def leaderOnly():
    # sellUnits()
    InboxAndRegister()
    pullBraveMain()
    inboxGetCard([lib.ixact(ix.imgInboxFilterStar_7), lib.ixact(ix.imgInboxFilterStar_8, .93)])
    changeLeader()
    evt.trainLoopNormal(isDaily=False, firstStage=True)

def inboxAndGsPack():
    InboxAndRegister()
    inboxItems()
    pullGSPack()

def doQuest():
    # receiveGift()
    joinPanel()

def ally():
    InboxAndRegister()
    pullBraveMain()
    # changeLeader()
    evt.trainLoopNormal(isDaily=False)
    removeAllies()
    recruitAlly()

def trainAndAlly():
    # receiveGift()
    InboxAndRegister()
    inboxItems()
    checkInventory()
    removeAllies()
    recruitAlly()
    evt.trainLoopNormal()
    removeAllies()
    lib.screenShotNoTime(game, "mail.png")
    lib.sendMail("Final-" + evt.user + "-")

def frontLineAndChk():
    receiveGift()
    checkInventory()
    joinFrontlines()

#ts1
def tradeStuff():
    InboxAndRegister()
    inboxItems()
    sellUnits()
    inboxGetCard([ix.imgInboxFilterStar_8, ix.imgInboxFilterStar_11])
    # inboxGetCard([ix.imgInboxFilterStar_8, ix.imgInboxFilterStar_9, ix.imgInboxFilterStar_11])    
    trade()

def tradeStuffPure():
    InboxAndRegister()
    inboxItems()
    trade(False)

#gmp1
def getMP():
    InboxAndRegister()
    inboxItems()
    #sellUnits()
    #inboxGetUnit(ix.imgInbox9to10, ix.img9StarInbox, unitBoxFromStars, 2)
    getPotion()
    inboxItems()
    #inboxGetUnit(ix.imgInbox7to8, ix.img7StarInbox, unitBoxFromStars, 2)

def getMPtrade():
    InboxAndRegister()
    inboxItems()
    #sellUnits()
    #inboxGetUnit(ix.imgInbox9to10, ix.img9StarInbox, unitBoxFromStars, 2)
    getPotion()    
    inboxItems()
    trade(hasUnits=False)

def simpleTrain():
    receiveGift()
    checkInventory()
    evt.stopAT71=stopAT71
    evt.trainLoopNormal()
    evt.joinClash()
    # evt.diceEnter()

def leaderAndTrain():
    InboxAndRegister()
    inboxItems()
    # if getPotion() > 0:
    #     inboxItems()   
    sellUnits()
    # inboxGetCard([ix.imgInboxFilterStar_8, ix.imgInboxFilterStar_9, ix.imgInboxFilterStar_11])    
    inboxGetCard([ix.imgInboxFilterStar_8, ix.imgInboxFilterStar_9, ix.imgInboxFilterStar_11])    
    changeLeader()
    lib.sleeplogx(2)
    # joinTrain()
    evt.trainLoopNormal()
    # lib.screenShot(game, "home-" + evt.user + "-shot-")
    # trade()

def menuScroll():
    p1 = lib.Pts(377, 591)
    p2 = lib.Pts(77, 591)
    lib.scrollPos(game, p1,p2,1,1)
    lib.sleeplogx(.5)

def checkInventory():
    lib.log('checkInventory()');
    lib.myClick(game, ix.imgMenu)
    menuScroll()
    lib.myClick(game, ix.imgProfileMain)      
    lib.myClick(game, ix.imgProfileInventory)
    lib.screenShot(game, "Inventory-" + evt.user + "-shot-")
    lib.screenShotNoTime(game, "mail.png")
    lib.sendMail("Inventory-" + evt.user + "-")

    lib.myClick(game, ix.imgBack, after=1)
    lib.myClick(game, ix.imgBack, after=1)
    lib.myClick(game, ix.imgMenuPressed)      

def sellAndLeader():
    sellUnits()
    inboxGetUnit(ix.imgInbox7to8, ix.img7StarInbox, unitBoxFromStars)
    inboxGetUnit(ix.imgInbox7to8, ix.img8StarInbox, unitBoxFromStars)
    #pull6Pack()
    changeLeader()

def chkAcct():   
    inboxItems()
    inboxGetUnit(ix.imgInbox7to8, ix.img7StarInbox, unitBoxFromStars)
    inboxGetUnit(ix.imgInbox7to8, ix.img8StarInbox, unitBoxFromStars)
    inboxGetUnit(ix.imgInbox9to10, ix.img9StarInbox, unitBoxFromStars)
    #lib.screenShot(game, evt.user + "-screen-")
    chkUnits()


def chkUnits():
    lib.myClick(game, ix.imgMenu)    
    lib.myClick(game, ix.imgUnitsMain, 1)
    lib.sleeplogx(3)
    lib.screenShot(game, evt.user + "-screen-")
    lib.myClick(game, ix.imgBack, waitForImgAppear=1, after=1)
    lib.myClick(game, ix.imgMenuPrefed)    

# def joinPanel():
#     lib.log("joinClash()")
#     lib.myClick(game, evt.allimg.imgPanelEventPage)
#     lib.sleeplogx(1)
#     if game.exists(evt.allimg.imgPanelEventPage2):
#         lib.myClick(game, evt.allimg.imgPanelEventPage2)
#     lib.myClick(game, ix.imgBack, after=1)
     
def questLocator():
    lib.locatebr(game, ix.imgLocate)

def testPlace():
    pl = []
    pl.append(lib.Pts(108, 286))
    pl.append(lib.Pts(171, 292))
    ##pl.append(lib.Pts(277, 265))
    pl.append(lib.Pts(330, 239))
    #evt.place(pl[2])
    evt.placeUnit([pl[2]])

def joinQC():
    lib.myClick(game, ix.imgMenu)
    lib.myClick(game, evt.imgQCMain, 1)
    lib.myClick(game, ix.imgBack, waitForImgAppear=1, after=1)
    lib.myClick(game, ix.imgMenuPressed, 1)
    inboxQCunit()    

def joinQC2():
    lib.myClick(game, ix.imgMenu)
    lib.myClick(game, evt.imgQCMain, 1)
    lib.myClick(game, evt.imgQCRook)    
    playQCAll()
    lib.myClick(game, ix.imgMenuPressed, 1)

def playQC1(n, pos):
    pic=lib.imgByOrder(evt.imgStartQuest, n)
    lib.myClickImg(pic)
    evt.placeUnit([pos])

def playQC2(n, pos):
    pic=lib.imgByOrder(evt.imgStartQuestTE, n)
    lib.myClickImg(pic)
    lib.myClick(game, evt.imgYes)
    evt.placeUnit([pos])

def playQCAll():
    playQC1(0, lib.Pts(108, 286))
    lib.myClick(game, evt.imgChooseQuest, 40)
    lib.myClick(game, evt.imgQCRook)
    playQC2(1, lib.Pts(171, 292))
    lib.myClick(game, evt.imgChooseQuest, 40)
    lib.myClick(game, evt.imgQCRook)
    playQC2(2, lib.Pts(330, 239))
    lib.myClick(game, evt.imgMyPage, 40)

def pull6Pack():
    lib.myClick(game, ix.imgCardPackMain, 1)
    lib.myClick(game, ix.imgCardPackStandard, 1)
    scrollUnits()
    scrollUnits()
    scrollUnits()
    box=card6to8Box(ix.imgCardPack6to8)
    if lib.logExists(box,ix.imgCardUseTicket):
        lib.myClickTillGone(box, ix.imgCardUseTicket, True)    
        lib.sleeplogx(3)
        cnt=5
        while cnt>0:
            lib.myClick(game, ix.imgDrawAgainExact, 1)    
            cnt-=1
        lib.myClick(game, ix.imgBack, after=1)
    lib.myClick(game, ix.imgBack, after=1)


def card6to8Box(pic):
    try:
        ub=find(pic)
        ub.setX(ub.x - 10)
        ub.setY(ub.y - 80)
        ub.setW(300)
        ub.setH(300)  
        lib.hoverBox(ub)
        return ub
    except:
       #return None
       raise
    return None

## ------------------------------- MAIN
def chkdup(list):
    dict = {}
    for i, e in enumerate(list):
        k=e['user']
        if k in dict:
            lib.log(k + ' dup ERROR')
            raise ValueError("dup name in list")
        else:
            dict[k]=1
        #print(i, e)
    print(len(dict))
    
def findidx(list, p):
    i=0
    while i < len(list):
        usr=list[i]
        fidx=-1
        fcnt=0
        if usr['user']==p:
            lib.log("idx=" + str(i))
            return i
        i+=1
    return -1

#ma1
def main(acct='', list=[], loop=False):
    global gIndex
    #initGame()

    if (len(list)==0):
        # continue GP
        #list= accts.train() + accts.Gaau2() + accts.Haau3()
        # list=accts.BluuAll() + accts.Gaau()
        # list=accts.Trial()
        # list=accts.dukk()
        # list=accts.others()
        # list=accts.Haau2()
        # list=accts.others()
        # list=accts.passwd()
        # list=accts.train()
        #list=accts.Gaau() + accts.dukk()
        # list=accts.err() 
        # list=accts.Haau1() + accts.dukk() + accts.Gaau()
        # list=accts.dukk()
        # list=accts.Gaau()
        # list=accts.BluuAll()
        # list=accts.err()
        list=accts.Haau1() + accts.Gaau()

    chkdup(list)

    lib.log('gLoopStart = ' + list[gLoopStart]['user']);
    showList(list)
    #i = gLoopStart
    if (acct==''):
        i = 0
    else:
        i = findidx(list, acct)
        if i==-1:
            raise ValueError(acct + " not found")
    ex = 0
    totalex=0
    reset=False
    loginretry=0
    dailylimit=300  #,dl1

    while i < len(list):
        gIndex=i
        if skipFour():
            i=0
        usr=list[i]
        uname=usr['user']
        #lib.log(list[i]['user'] + list[i]['passw'])
        if 'a' in usr:
            actions=usr['a']
        else:
            actions=''

        # hack ,ma2
        # if i > 276: 
        #     actions='l'
        # if i > 231:
        #     actions=actions+'t'
        # if i < 250:
        #     actions='e'
        # if i > 256:
        #     actions='s'

        try:
            if i > dailylimit:
                lib.log("Dailylimit over: i=" + str(i))
                lib.sleeplogx(180)
                continue
            else:
                heartbeat()
                lib.log("=============== Start! idx:" + str(i) + " ssssss:" + uname)
                if not 'chk' in usr:
                    loginAndClaim(uname, usr['passw'], reset, actions)
                else:
                    loginAndChk(uname, usr['passw'])
                reset=False
                lib.log("=============== Success! idx:" + str(i) + " eeeeee:" + uname)

        except lib.LoginError:
            lib.log('Bad passwd = ' + uname)
            lib.log(traceback.format_exc())            
            #lib.screenShot(bsicon, usr + "-LOGIN-")    
            lib.screenShotNoTime(bsicon, "mail.png")
            lib.sendMail("ERROR-" + uname + "-")
            lib.clicklog(ix.imgLoginErrorOk)
            cleanLoginBox()
            loginretry=loginretry+1
            if loginretry < 2:
                continue
            else:
                loginretry = 0
        except lib.FreshAcctError:
            lib.screenShot(bsicon, uname + "-FRESH-")
            lib.log('fresh account = ' + uname);
        except lib.NoAllyError:
            lib.screenShotNoTime(game, "mail.png")
            lib.sendMail("NoAlly-" + uname + "-")
            lib.log('No Ally = ' + uname);
        except lib.InfiniteLoop as ie:
            # lib.screenShot(bsicon, uname + "-INFINITE-")
            lib.log("err=" + ie.msgstr())
            lib.log('Infinite Looop = ' + uname);
            lib.screenShotNoTime(SCREEN, "mail.png")
            raise ValueError('Infinite Looop')
        except lib.SkipError:
            # lib.screenShot(bsicon, uname + "-FRESH-")
            lib.log('skipping battle = ' + uname);
            lib.log("=============== Success! idx:" + str(i) + " eeeeee:" + uname)
        except lib.LoginFail as lf:
            lib.log(lf.msgstr() + ", Retry=" + str(ex))
            lib.log(traceback.format_exc())
            lib.screenShotNoTime(SCREEN, "mail.png")
            lib.sendMail("Network-" + uname + "-")
            reset=False
            ex=ex+1
            if (ex < 3):
                continue
            else:
                ex=0
        except:
            lib.log("caught fatal, Retry=" + str(ex) + ' Total=' + str(totalex))
            lib.log(traceback.format_exc())       
            if not game==None:
                lib.screenShotNoTime(game, "mail.png")
            else:
                lib.screenShotNoTime(SCREEN, "mail.png")
            lib.sendMail("FATAL-" + str(gIndex) + "-" + uname + "-")
            ex=ex+1
            totalex+=1
            if (ex < 3):
                reset=True
                continue
            else:
                reset=False
                ex=0
            if totalex > 80:
                lib.log('Exceeded exception limit=' + str(totalex))
                raise ValueError('Exceeded exception limit')

            # raise 
        i += 1
        if (i >= len(list) and loop):
            lib.log("REPEAT: loopback")
            i=0


def setBox(ub, dx, dy, w, h):
    ub.setX(ub.x + dx)
    ub.setY(ub.y + dy)
    ub.setW(w)
    ub.setH(h)  
    #lib.hoverBox(ub)
    ub.highlight(1)
    
def allyBox(ub):
     setBox(ub, -320, -80, w=450, h=130)
     return ub

def acceptAlly():
    # tt = lib.imgFirst(game, ix.imgAllyDecline)
    tt = lib.findByOrder(game, ix.imgAllyDecline, idx=0)
    #tt = find(ix.imgAllyDecline)
    #hover(tt)
    abox=allyBox(tt)
    if lib.logExists(abox, lib.ixact(ix.imgAllyStar1)):
        lib.myClick(abox, ix.imgAllyDecline)
    elif lib.logExists(abox, lib.ixact(ix.imgAllyStar2)):
        lib.myClick(abox, ix.imgAllyDecline)
    elif lib.logExists(abox, lib.ixact(ix.imgAllyStar3)):
        lib.myClick(abox, ix.imgAllyDecline)
    elif lib.logExists(abox, lib.ixact(ix.imgAllyStar4)):
        lib.myClick(abox, ix.imgAllyDecline)
    elif lib.logExists(abox, lib.ixact(ix.imgAllyStar5)):
        lib.myClick(abox, ix.imgAllyDecline)
    else:
        lib.myClick(abox, ix.imgAllyApprove)
    
def removeAlly():
    while lib.logExists(game, ix.imgProfile):
        lib.myClick(game, ix.imgProfile)
        lib.myClick(game, ix.imgRemoveAlly)
        lib.myClick(game, ix.imgYes)
        lib.myClick(game, ix.imgBack, after=2)

def acceptAllies():
    while lib.logExists(game, lib.ixact(ix.imgAllyDecline)):
        lib.myClick(game, ix.imgAllyDecline)
        # acceptAlly()
    #lib.myClick(game, ix.imgBack, after=1)

def allyPage():
    lib.myClick(game, ix.imgMenu)
    lib.myClick(game, ix.imgAllyMain)
    lib.sleeplogx(2)
    acceptAllies()
    lib.myClick(game, ix.imgBack, after=1)
    lib.myClick(game, ix.imgBack, after=1)
    lib.myClick(game, ix.imgMenuPressed, 1)    

def removeAllies():
    lib.myClick(game, ix.imgMenu)
    lib.myClick(game, ix.imgAllyMain)
    lib.sleeplogx(2)
    deferAlly()
    acceptAllies()
    removeAlly()
    # lib.myClick(game, ix.imgBack, after=1)
    while lib.logExists(game, ix.imgBack, 1):
        lib.myClick(game, ix.imgBack, after=1)
    lib.myClick(game, ix.imgMenuPressed, 1)        

def recruitAlly():
    findTrade()
    if lib.logExists(game, ix.imgRecruit, 2):
        lib.myClick(game, ix.imgRecruit, after=1)
    lib.myClick(game, ix.imgBack, after=1)
    lib.myClick(game, ix.imgBack, after=1)
    lib.myClick(game, ix.imgMenuPressed)


def cardPackScrollLeft():
    p1 = lib.Pts(309,118)
    p2 = lib.Pts(109,118)
    lib.scrollPos(game, p1,p2,1,1)
    
def gotoStandardPacks():
    gotoPacksTab(ix.imgCardPackStandard)

def gotoGSPacks():
    gotoPacksTab(ix.imgCardPackTicket)

def gotoPacksTab(image3):
    i=0
    while not lib.logExists(game, image3) and i < 3:
        cardPackScrollLeft()
        i=i+1
    lib.myClick(game, image3, waitForImgAppear=1, holdDur=1, after=1)


def pullBrave(skip=False):
    gotoStandardPacks()
    i=0
    while not lib.logExists(game, lib.ixact(ix.imgCardBravePts)) and i < 1:    
        scrollUnits()
        i+=1
    if lib.logExists(game, ix.imgCardBravePts):
        lib.myClick(game, ix.imgCardBravePts, waitForImgAppear=1, after=1)
        lib.canSkip(skip, "pullBrave")
        lib.myClick(game, ix.imgBack, after=1)
    else:
        lib.screenShot(game, "NoBrave-" + evt.user + "-")
    # lib.myClickTillGone(game, ix.imgBack, waitForImgAppear=1, retryIfNotGone=3)
    lib.myClickTillNext(game, lib.ixact(ix.imgBack), lib.ixact(ix.imgMenuPressed))
    # lib.myClick(game, ix.imgBack, after=1)


def missionBox(ub):
    #ub=find(pic)
    setBox(ub, 1, -40, w=410, h=70)
    return ub

# def missionCardPull_old():
#     lib.log('missionCardPull()')
#     if lib.logExists(game, lib.ixact(ix.imgMissionDrawCardPack), 1):
#         tt = lib.imgFirst(game, lib.ixact(ix.imgMissionDrawCardPack))
#         mbox=missionBox(tt)
#         lib.myClick(mbox, ix.imgMissionSelect)
#         pullBrave()
#         lib.myClick(game, ix.imgMenuPressed, 1)
#         return 1
#     return 0

# def missionAllyMsg_old():
#     lib.log('missionAllyMsg()')
#     if lib.logExists(game, lib.ixact(ix.imgMissionMsgToAlly), 1):
#         tt = lib.imgFirst(game, lib.ixact(ix.imgMissionMsgToAlly))
#         mbox=missionBox(tt)
#         lib.myClick(mbox, ix.imgMissionSelect)
#         allyMsg()
#         lib.myClick(game, ix.imgMenuPressed, 1)  
#         return 1
#     return 0

def missionSelect(imgMissionText, nextImg, missionFunc, skip):
    lib.log('missionSelect()')
    if lib.logExists(game, imgMissionText, 0):
        tt = lib.findByOrder(game, imgMissionText, idx=0)
        # tt = lib.imgFirst(game, imgMissionText)
        mbox=missionBox(tt)
        if nextImg:
            lib.myClickTillNext(mbox, lib.ixact(ix.imgMissionSelect), nextImg, nextArea=game)
        else:
            lib.myClick(mbox, ix.imgMissionSelect, waitForImgAppear=1, after=0)
            lib.sleeplogx(2)
        missionFunc(skip)
        lib.sleeplogx(2)
        if lib.logExists(game, ix.imgMenuPressed):
            lib.myClickTillNext(game, ix.imgMenuPressed, ix.imgMenu, after=1)
            # lib.myClick(game, ix.imgMenuPressed, 1)  
        return 1
    return 0

#mi2
def profileMsg(skip=False):
    lib.myClick(game, lib.ixact(ix.imgProfileMsgBox, .95), waitForImgAppear=1, after=1.5)
    #lib.sleeplogx(1)
    lib.slowType('xx')
    # lib.keydown('h')
    lib.sleeplogx(1)
    lib.myClick(game, lib.ixact(ix.imgSend), waitForImgAppear=0, after=1)
    lib.canSkip(skip, "profileMsg")
    # lib.myClick(game, ix.imgBack, waitForImgAppear=1, after=1)
    lib.myClickTillGone(game, ix.imgBack, waitForImgAppear=1, retryIfNotGone=3)

def doMsg(skip=False):
    # lib.myClick(game, ix.imgAllyProfile) 
    lib.myClickTillNext(game, ix.imgAllyProfile, ix.imgAllyMsg, after=1)
    lib.myClick(game, ix.imgAllyMsg, waitForImgAppear=1, after=1.5) 
    lib.keydown('h')
    lib.myClick(game, ix.imgSend, after=1)  
    lib.canSkip(skip, "allyMsg")
    # lib.myClick(game, ix.imgBack, waitForImgAppear=1, after=1)
    # lib.myClick(game, ix.imgBack, waitForImgAppear=1, after=1)
    lib.myClickTillGone(game, ix.imgBack, waitForImgAppear=1, retryIfNotGone=3)


def allyMsg(skip=False):
    lib.log('missionAllyMsg()')
    lib.myWait(game ,ix.imgAllyTitle , 3)
    while lib.logExists(game, ix.imgMinaAlly):
        # lib.myClick(game, ix.imgMinaQuest)
        lib.quickClick(game, ix.imgMinaAlly)

    if lib.logExists(game, ix.imgAllyProfile):
        doMsg(skip)
    else:
        lib.myClick(game, ix.imgAllyWaitApproval, after=3)
        if lib.logExists(game, ix.imgApproveAlly):        
            lib.myClick(game, ix.imgApproveAlly, waitForImgAppear=1, after=1.5)
            lib.myClick(game, ix.imgBack, waitForImgAppear=1, after=1)
            doMsg(skip)
        else:
            lib.log('no ally')
            lib.screenShot(game, "NoAlly-" + evt.user + "-")
            lib.sendMail("NoAlly-" + evt.user + "-")
            raise lib.NoAllyError("no ally skipping")
            lib.myClick(game, ix.imgBack, waitForImgAppear=1, after=1)
        # lib.myClick(game, ix.imgBack, waitForImgAppear=1, after=1)
    # lib.myClick(game, ix.imgBack, waitForImgAppear=1, after=1)
    # lib.myClickTillGone(game, ix.imgBack, waitForImgAppear=1, retryIfNotGone=3)
    lib.myClickTillNext(game, ix.imgBack, ix.imgMenuPressed)

def doBrave():
    lib.myClick(game, ix.imgBrave)        
    # lib.myClick(game, ix.imgBack, waitForImgAppear=1, after=1)
    # lib.myClickTillNext(game, ix.imgBack, ix.imgMenuPressed)

def braveAlly(skip=False):
    lib.log('braveAlly()')
    # deferAlly()
    lib.myWait(game ,ix.imgAllyTitle , 3)
    if lib.logExists(game, ix.imgBrave):
        doBrave()
    else:
        lib.myClick(game, ix.imgAllyWaitApproval, after=2)
        if lib.logExists(game, ix.imgApproveAlly):        
            lib.myClick(game, ix.imgApproveAlly, waitForImgAppear=1, after=1.5)
            lib.myClick(game, ix.imgBack, waitForImgAppear=1, after=1)
            doBrave()
        else:
            lib.log('no ally')
            # lib.screenShot(game, "NoAlly-" + evt.user + "-")
            lib.screenShotNoTime(game, "mail.png")
            lib.sendMail("NoAlly-" + evt.user + "-")
            raise lib.NoAllyError("no ally skipping")
            lib.myClick(game, ix.imgBack, waitForImgAppear=1, after=1)
            lib.myClick(game, ix.imgBack, waitForImgAppear=1, after=1)
    # lib.myClick(game, ix.imgBack, waitForImgAppear=1.5, after=1)
    lib.log("braveAlly-back-button-problem")
    lib.myClickTillNext(game, ix.imgBack, ix.imgMenuPressed)
    # lib.myClickTillGone(game, ix.imgBack, waitForImgAppear=1, retryIfNotGone=3)


def checkIn():
    # lib.myClick(game, ix.imgInnMain)
    # lib.myClick(game, ix.imgInnCheckIn, waitForImgAppear=1, after=1.5)
    lib.myClickTillNext(game, ix.imgInnCheckIn, ix.imgUnselected)

    if lib.logExists(game, lib.ixact(ix.imgSortByNew)):
        lib.myClick(game, ix.imgSortByNew)
    if lib.logExists(game, lib.ixact(ix.imgSortByLevelLow)):
        lib.myClick(game, ix.imgSortByLevelLow)
    # lib.myWait(game ,ix.imgUnselected, 2)
    # lib.myClickImg(lib.imgFirst(game, ix.imgUnselected))
    lib.myClickIdx(game, ix.imgUnselected, 0)
    #lib.myClick(game, ix.imgBack, after=1)
    lib.myClick(game, ix.imgInnCheckIn2)
    lib.myClick(game, ix.imgTradeConfirm)
    # lib.myClick(game, ix.imgBack, after=1)
    # lib.myClick(game, ix.imgBack, after=1)

def checkOut(skip=False):
    # lib.myClick(game, ix.imgInnMain)
    # lib.myClick(game, ix.imgInnCheckOut, waitForImgAppear=1, after=1)
    lib.myClickTillNext(game, ix.imgInnCheckOut, lib.ixact(ix.imgInnReceive, .8))
    # lib.myWait(game ,ix.imgInnReceive, 2)
    # lib.myClick(game, ix.imgInnReceive)
    lib.myClickTillGone(game, ix.imgInnReceive, retryIfNotGone=5, waitAfterClick=.3)
    lib.canSkip(skip, "checkOut")
    # lib.myClick(game, ix.imgBack, after=1)
    # lib.myClick(game, ix.imgBack, after=1)
    lib.myClickTillGone(game, ix.imgBack, waitForImgAppear=1, retryIfNotGone=3)

def missionInn(skip=False):
    checkIn()
    checkOut(skip)

def missionSell():
    doSell(1)

def sellTop(skip=False):
    lib.log('sellTop()')
    if lib.logExists(game, lib.ixact(ix.imgSortByNew)):
        lib.myClick(game, ix.imgSortByNew)
    if lib.logExists(game, lib.ixact(ix.imgSortByLevelLow)):
        lib.myClick(game, ix.imgSortByLevelLow)
    # lib.myClickImg(lib.imgFirst(game, ix.imgUnselected))    
    lib.myClickIdx(game, ix.imgUnselected, 0)
    lib.myClick(game, ix.imgSell, after=1)
    lib.myClick(game, ix.imgSell2, after=1)
    lib.canSkip(skip, "sellTop")
    # lib.myClick(game, ix.imgBack, waitForImgAppear=1, after=1)
    lib.myClickTillGone(game, ix.imgBack, waitForImgAppear=1, retryIfNotGone=3)

def initBattle():
    pl = []
    pl.append(lib.Pts(164,298))
    #pl.append(lib.Pts(164,331))
    #pl.append(lib.Pts(330,277))
    #pl.append(lib.Pts(330,331))
    return pl

def missionBattle(skip=False):
    lib.sleeplogx(2)
    lib.myClick(game, ix.imgBattleSelect, after=1)
    lib.myClick(game, ix.imgBattleBattle)
    pl=initBattle()
    lib.sleeplogx(1)
    raise lib.SkipError("Skipping battle")
    evt.placeUnit(pl)
    
    if lib.logExists(game, ix.imgBattleSkip):
        lib.myClick(game, ix.imgBattleSkip)
    lib.myClick(SCREEN, ix.imgMyPage, waitForImgAppear=30)

def profileTitle(skip=False):
    if lib.logExists(game, lib.ixact(ix.imgProfileEditTitle)):
        lib.myClick(game, lib.ixact(ix.imgProfileEditTitle), 1)
    lib.myClick(game, ix.imgProfileSetTitle, waitForImgAppear=1, after=1.5)
    lib.canSkip(skip, "profileTitle")
    # lib.myClick(game, ix.imgBack, waitForImgAppear=1, after=1)
    # lib.myClick(game, ix.imgBack, waitForImgAppear=1, after=1)
    # lib.myClickTillGone(game, ix.imgBack, waitForImgAppear=1, retryIfNotGone=3, waitAfterClick=1.5)
    # lib.myClickTillGone(game, ix.imgBack, waitForImgAppear=1, retryIfNotGone=3, waitAfterClick=1.5)
    lib.myClickTillNext(game, ix.imgBack, ix.imgMenuPressed, after=1)


def missionTrain(skip=False):
    evt.stopAT71=False
    evt.trainLoopNormal(isDaily=True, skip=skip)

def missionQuest(skip=False):
    # lib.sleeplogx(2)
    lib.myWait(game ,ix.imgQuestStart, 3)
    # lib.myClickImg(lib.imgFirst(game, ix.imgQuestStart))    
    lib.myClickIdx(game, ix.imgQuestStart, 0)
    pl=[lib.Pts(227,283)]
    evt.placeUnit(pl)
    while not lib.logExists(game, ix.imgMyPage):
        #hover(p1)    
        if lib.logExists(game, ix.imgBattleSkip):
            lib.myClick(game, ix.imgBattleSkip, waitForImgAppear=0, after=1)
        if lib.logExists(game, ix.imgMinaQuest):
            # lib.myClick(game, ix.imgMinaQuest)
            lib.quickClick(game, ix.imgMinaQuest)
            #tt=find(ix.imgMinaQuest)
            #lib.myClickImg(tt)
            # clickHere(hold = 0)
        #lib.myClickImg(lib.imgFirst(game, ix.imgQuestMonsterLeft))
    lib.canSkip(skip, "missionQuest")
    lib.myClick(game, ix.imgMyPage, waitForImgAppear=1, after=1)


def matchImgs(imgs, sim):
    outlist=[]
    for xx in imgs:
        x=xx['pic']
        if lib.logExists(game, lib.ixact(x, sim), 0):
            lib.log('matched' + x.f)
            outlist.append(xx)

    return outlist

#
def matchMissions(sim):
    imgs=[
      {'pic':ix.imgMissionBrave, 'next':ix.imgAllyTitle, 'func':braveAlly }
    , {'pic':ix.imgMissionInnOut, 'next':ix.imgInnCheckIn, 'func':missionInn }
    , {'pic':ix.imgMissionDrawCardPack, 'next':ix.imgCardPackTitle, 'func':pullBrave }
    , {'pic':ix.imgMissionProfileTitle, 'next':ix.imgProfileSetTitle, 'func':profileTitle }
    , {'pic':ix.imgMissionSellUnit, 'next':ix.imgUnselected, 'func':sellTop }
    , {'pic':ix.imgMissionProfile, 'next':ix.imgProfileEditTitle, 'func':profileMsg }
    , {'pic':ix.imgMissionMsgToAlly, 'next':ix.imgAllyTitle, 'func':allyMsg }
    , {'pic':ix.imgMissionTraining, 'next':evt.allimg.imgStartTrain, 'func':missionTrain }
    # , {'pic':ix.imgMissionQuest, 'func':missionQuest }
    , {'pic':ix.imgMissionInnIn, 'next':ix.imgInnCheckIn, 'func':missionInn }
    , {'pic':ix.imgMissionBattle, 'next':ix.imgBattleSelectTitle, 'func':missionBattle }
    ]
    return matchImgs(imgs, sim)

#mi1
def mission():
    lib.log('mission()')
    lib.myClickTillGone(game, ix.imgMenu, waitForImgAppear=1, retryIfNotGone=3, waitAfterClick=.3)
    # lib.myClick(game, ix.imgMenu, after=0.5)
    # lib.myClick(game, ix.imgAllNotice, after=1)
    # lib.myWait(game ,ix.imgNoticeTitle, 3)
    lib.myClickTillNext(game, ix.imgAllNotice, ix.imgNoticeTitle, after=1)
    # lib.myClickImg(lib.imgFirst(game, ix.imgDetail))
    # lib.myClickIdx(game, ix.imgDetail, 0)
    lib.myClickTillNext(game, ix.imgDetail, ix.imgMissionExchange, after=1, idx=0)
    # lib.sleeplogx(2)
    lib.myWait(game, ix.imgMissionExchange, 2)

    sim=.75
    mm=matchMissions(sim)
    remain=len(mm)
    lib.log('matched missions=' + str(remain))

    skip=False
    if remain > 0:
        if remain == 1:
            skip=True
        if 'next' in mm[0]:
            nextImg=mm[0]['next']
        else:
            nextImg=None
        missionSelect(lib.ixact(mm[0]['pic'], sim), nextImg, missionFunc=mm[0]['func'], skip=skip)
    # numMission += missionSelect(lib.ixact(ix.imgMissionQuest), missionFunc=missionQuest)
    else:
        lib.screenShot(game, "NoMission-" + evt.user + "-")

        # lib.myClick(game, ix.imgBack, after=1)    
        lib.myClickTillNext(game, ix.imgBack, ix.imgMenuPressed)
        lib.myClickTillGone(game, ix.imgMenuPressed, waitForImgAppear=1, retryIfNotGone=3)
        # lib.myClick(game, ix.imgMenuPressed, 1)
    # else:
    #     lib.log("Finish")
    return remain

def mission0():
    lib.log('mission()')
    numMission=0
    lib.myClick(game, ix.imgMenu, after=0.5)
    lib.myClick(game, ix.imgAllNotice, after=1)
    lib.myWait(game ,ix.imgDetail, 3)
    lib.myClickImg(lib.imgFirst(game, ix.imgDetail))
    lib.sleeplogx(2)
    numMission += missionSelect(lib.ixact(ix.imgMissionBrave), missionFunc=braveAlly)
    
    numMission += missionSelect(lib.ixact(ix.imgMissionInnOut), missionFunc=missionInn)
    numMission += missionSelect(lib.ixact(ix.imgMissionMsgToAlly), missionFunc=allyMsg)
    numMission += missionSelect(lib.ixact(ix.imgMissionTraining), missionFunc=missionTrain)
    numMission += missionSelect(lib.ixact(ix.imgMissionDrawCardPack), missionFunc=pullBrave)
    numMission += missionSelect(lib.ixact(ix.imgMissionProfileTitle), missionFunc=profileTitle)
    numMission += missionSelect(lib.ixact(ix.imgMissionInnIn), missionFunc=missionInn)
    numMission += missionSelect(lib.ixact(ix.imgMissionSellUnit), missionFunc=sellTop)

    numMission += missionSelect(lib.ixact(ix.imgMissionProfile), missionFunc=profileMsg)
    # numMission += missionSelect(lib.ixact(ix.imgMissionQuest), missionFunc=missionQuest)
    numMission += missionSelect(lib.ixact(ix.imgMissionBattle), missionFunc=missionBattle)
    if numMission == 0:
        lib.screenShot(game, "NoMission-" + evt.user + "-")
        lib.myClick(game, ix.imgBack, after=1)    
        lib.myClick(game, ix.imgMenuPressed, 1)
    return numMission

def missions0():    
    cnt=0
    while True:
        cnt+=1
        lib.log('missions() cnt=' + str(cnt))
        remain=mission()
        if cnt >= 2 or remain==0:
            break

def missions():    
    cnt=0
    while True:
        # lib.log('missions() cnt=' + str(cnt))
        remain=mission()
        if remain <= 1:
            break

#cg1
def createGuild():
    lib.myClick(game, evt.imgGuildPage)
    lib.sleeplogx(2)
    if lib.logExists(game, evt.imgGuildCreate):
        lib.myClick(game, evt.imgGuildCreate, 2)
        lib.myClick (game, evt.imgGuildCreate2, 1)
        lib.myClick(game, evt.imgYes, 1)
        lib.sleeplogx(2)
    elif lib.logExists(game, lib.ixact(evt.imgGuildToBattle, .95)):
        lib.myClick(game, evt.imgGuildToBattle, 2)
        lib.sleeplogx(2)
        lib.myClick(game, evt.imgGuildAttack, 2)
        lib.myClickTillGone(game, evt.imgGuildSkip, waitForImgAppear=10)
        lib.myClickTillGone(game, evt.imgBack, waitForImgAppear=45)
    if lib.logExists(game, evt.imgBack): 
        lib.myClick(game, evt.imgBack, 2)

#ft1
def findTrade():
    lib.myClick(game, ix.imgMenu, 1)
    lib.myClick(game, ix.imgTradeMain, 1)
    lib.myClick(game, lib.ixact(ix.imgTradeID), 1)
    # lib.slowType('102014420') # bluu123
    lib.slowType('100998882') # bluu100
    #lib.slowType('93152216')
    # lib.slowType('98227954')
    # lib.slowType('84583825')
    # lib.slowType('1000289852')
    # lib.slowType('108395630') #gaau1
    # lib.slowType('109158727') #gaau2
    # lib.slowType('109163713') #gaau3
    # lib.slowType('109341895') #gaau4
    # lib.slowType('109488328') #gaau5
    # lib.slowType('124188303') #gaau7
    # lib.slowType('109542370') #gaau8
    # lib.slowType('109565485') #gaau9
    # lib.slowType('109569392') #gaau10
    # lib.slowType('109581912') #gaau11
    # lib.slowType('109588686') #gaau12
    # lib.slowType('109670219') #gaau13
    # lib.slowType('109675606') #gaau14
    # lib.slowType('109705196') #gaau15
    # lib.slowType('109731502') #gaau16
    lib.myClick(game, ix.imgTradeSearchID, 1)

def tradeStart():
    findTrade()
    lib.myClick(game, ix.imgTradeProfile, 1)

def trade(hasUnits=True):    
    tradeStart()
    tradePure(0)
    tradePure(1)
    if hasUnits:
        tradeUnits()
    cycleTrade()

def tradePure(idx):
    lib.log('tradePure:'+str(idx))
    lib.myClick(game, ix.imgTradeViewItem, 1)
    # ic=lib.imgByOrder(lib.ixact(ix.imgTradePlusOne, 0.90), idx)
    ic=lib.findByOrder(game, lib.ixact(ix.imgTradePlusOne, 0.90), idx)
    if ic is None:
        lib.log('Pure not found = ')
        return
    hover(ic)
    game.mouseDown(Button.LEFT)
    lib.sleeplogx(4)
    game.mouseUp(Button.LEFT)

def cycleTrade():
    # lib.myClick(game, ix.imgTradeProfile, 1)
    if lib.logExists(game, lib.ixact(ix.imgTradeProfile), 1):
        lib.myClickTillNext(game, ix.imgTradeProfile, ix.imgTradeConfirm)
        lib.screenShotNoTime(game, "mail.png")
        lib.sendMail("ChkTrade-" + evt.user + "-")
        # lib.myClick(game, ix.imgTradeConfirm, waitForImgAppear=1, after=1)
        lib.myClickTillNext(game, ix.imgTradeConfirm, ix.imgTradeCont, after=1)
        # lib.myClick(game, ix.imgTradeCont, waitForImgAppear=1, after=1)
        lib.myClickTillNext(game, ix.imgTradeCont, ix.imgTradePending)
        while lib.logExists(game, lib.ixact(ix.imgTradePending)):
            # lib.myClick(game, ix.imgBack, waitForImgAppear=1, after=1)
            lib.myClickTillNext(game, ix.imgBack, ix.imgTradeMain)
            # lib.myClick(game, ix.imgTradeMain, waitForImgAppear=1, after=1)
            lib.myClickTillNext(game, ix.imgTradeMain, ix.imgTradeTitle)
        # lib.myClick(game, ix.imgTradeDetails, waitForImgAppear=1, after=1)
        lib.myClickTillNext(game, ix.imgTradeDetails, ix.imgTradeConfirm, after=1)
        lib.myClick(game, ix.imgTradeConfirm, waitForImgAppear=1, after=1)
    else:
        lib.myClick(game, ix.imgBack, waitForImgAppear=1, after=1)
    lib.myClick(game, ix.imgBack, waitForImgAppear=1, after=1)
    lib.myClick(game, ix.imgMenuPressed)

def tradeUnits():
    lib.myClick(game, ix.imgTradeViewUnits, 1)
    # scrollAndSelect(4, ix.imgUnitStar_9, ix.imgMonStar_9)
    scrollAndSelect(4, ix.imgUnitStar_8, ix.imgMonStar_8)

def ssPotion():
    InboxAndRegister()
    inboxItems()
    lib.myClick(game, ix.imgMenu)
    lib.myClick(game, ix.imgAllNotice)
    # lib.myClickImg(lib.imgFirst(game, ix.imgDetail))
    lib.myClickIdx(game, ix.imgDetail, 0)
    lib.sleeplogx(1.5)
    lib.screenShot(game, "Chk-" + evt.user + "-shot-")

def getPotion():
    lib.log('getPotion')
    cnt=0
    lib.myClick(game, ix.imgMenu, after=0.5)
    lib.myClick(game, ix.imgAllNotice, after=1)
    # lib.myClickImg(lib.imgFirst(game, ix.imgDetail))
    lib.myClickIdx(game, ix.imgDetail, 0)
    lib.myWait(game, ix.imgMissionExchange, 2)
    # lib.myClick(game, ix.imgMissionExchange)
    lib.myClickTillNext(game, ix.imgMissionExchange, ix.imgMissionExchangeTitle, after=1)
    # start loop
    while not lib.logExists(game, ix.imgMissionPotion):
        scrollUnits()
    lib.sleeplogx(.5)
    # lib.screenShot(game, "MP-" + evt.user + "-shot-")
    ub=find(ix.imgMissionPotion)
    setBox(ub, 1, -10, w=450, h=80)
    c=0
    while c<50:
        if lib.logExists(ub, ix.imgMissionExchange2):
            lib.myClick(ub, ix.imgMissionExchange2)
            if not lib.logExists(game, ix.imgYes, 2):
                lib.screenShot(game, "Exchange-" + evt.user + "-")
                break
            cnt=cnt+1
            lib.myClickTillGone(game, ix.imgYes, waitAfterClick=.2)
            # lib.myClick(game, ix.imgYes)
            # lib.sleeplogx(1.5)
            sleep(0.3)
        c+=1
    lib.myClick(game, ix.imgBack, after=1)
    lib.sleeplogx(0.5)
    lib.myClick(game, ix.imgBack, after=1)
    lib.myClick(game, ix.imgMenuPressed)
    return cnt

def inboxScrollStar():
    p1 = lib.Pts(414, 330)
    p2 = lib.Pts(30, 330)
    lib.scrollPos(game, p1,p2,1,1)

#igc1
def inboxGetCard(cardList):
    lib.log('inboxGetCard()')
    lib.myClick(game, ix.imgMenu)
    lib.myClick(game, ix.imgInboxMain, 1)
    lib.myClickTillNext(game, ix.imgInboxMain, ix.imgInboxFilter, after=1) 
    # lib.sleeplogx(2)
    if not lib.logExists(game, lib.ixact(ix.imgInboxUnitsTabHighLight)):
        lib.myClick(game, ix.imgInboxUnitsTab)
    lib.myClick(game, ix.imgInboxFilter)
    lib.myClick(game, ix.imgInboxFilterUnits)
    #lib.myClick(game, ix.imgInboxFilterMonsters)
    for x in cardList:
        if lib.logExists(game, x):
            lib.log("star:" + lib.strimg(x))
            cardList.remove(x)
            lib.myClick(game, x)

    inboxScrollStar()
    #lib.myClick(game, ix.imgInboxFilterStar_9)
    for x in cardList:
        if lib.logExists(game, x):
            lib.log("star:" + lib.strimg(x))
            cardList.remove(x)
            lib.myClick(game, x)
    # lib.myClick(game, ix.imgInboxConfirm)
    lib.myClickTillNext(game, ix.imgInboxConfirm, ix.imgInboxSelectAll, after=1)
    while lib.logExists(game, lib.ixact(ix.imgInboxSelectAll)):
        lib.myClick(game, ix.imgInboxSelectAll)
        lib.myClick(game, ix.imgInboxConfirm)
        lib.myClick(game, ix.imgInboxReceive)
        lib.myClick(game, ix.imgYes)
        lib.sleeplogx(1.5)
    lib.myClick(game, ix.imgBack, waitForImgAppear=1, after=1)
    lib.myClick(game, ix.imgMenuPressed, 1)
    
def pullTicket():
    gotoStandardPacks()

    # ic=lib.imgByOrder(lib.ixact(ix.imgCardUseTicet, 0.80), 1)
    ic=lib.findByOrder(game, lib.ixact(ix.imgCardUseTicet, 0.80), 1)
    if ic is None:
        lib.log('Pure not found = ')
        return
    lib.myClickImg(ic)
    lib.sleeplogx(1)
    lib.screenShot(game, "Pull-" + evt.user + "-")

    while not lib.logExists(game, lib.ixact(ix.imgDrawAgain, 0.9)):
        lib.myClick(game, ix.imgDrawAgain)
        lib.sleeplogx(1)
        lib.screenShot(game, "Pull-" + evt.user + "-")
        lib.sleeplogx(1)

#loginAndClaim('bluu125gk', 'pppppppp')
def lunit():
    im=lib.X("1525966476795.png")
    #game = find(ix.imgMobaIcon)
    
    lib.locateg(game, im)
    #p1=lib.Pts(227,264)
    p1=lib.Pts(227,283)
    #p1=lib.Pts(0,0)
    evt.game=game
    evt.place(p1)

# alt-f3 to rename vars
def pyRefreshRetry():
    c=3
    while True:
        if c < 0:
            break
        try:
            pyRefresh()
            break
        except lib.ClickExcept:
            lib.log("pyRefreshRetry")
            launchPython()
            c=c-1

def pyRefresh():
    lib.log("pyRefresh()")
    sim=0.8
    renbutton=ix.imgPyRename
    lib.clickTillNext(SCREEN, ix.imgPyTop, lib.ixact(ix.imgPyIcon,sim), throw=True)
    bswide=initBsWide()
    # bswide.highlight(1)
    lib.clickTillNext(bswide, lib.ixact(ix.imgPyIcon, sim), ix.imgPyRunScript, throw=True)
    lib.clickTillNext(bswide, ix.imgPyRunScript, ix.imgPyRename, throw=True)
    lib.clickTillGone(bswide, ix.imgPyRefresh, throw=True)
    lib.sleeplogx(3)

def quickLaunch():
    lib.clickTillNext(SCREEN, ix.imgBsIcon, ix.imgSystemApp)
    bswide=initBsWide()
    sim=0.8
    # lib.clickTillNext(bswide, ix.imgHomeFanta, ix.imgSystemSettings)
    lib.clickTillNext(bswide, ix.imgHomeFanta, lib.ixact(ix.imgFantaIconTop, .85))
    # lib.clickTillNext(bswide, ix.imgSystemAppsMgr, ix.imgFantasica)
    # lib.clickTillNext(bswide, ix.imgFantasica, ix.imgSystemUninstall)
    # lib.clickTillNext(bswide, ix.imgSystemUninstall, ix.imgSystemUninstallOk)
    # lib.clickTillGone(bswide, lib.ixact(ix.imgSystemUninstallOk, sim))    

def launchPython():
    lib.clickTillNext(SCREEN, ix.imgBsIcon, ix.imgSystemApp)
    bswide=initBsWide()
    sim=0.8
    # lib.clickTillNext(bswide, ix.imgHomeFanta, ix.imgSystemSettings)
    lib.clickTillNext(bswide, ix.imgHomePython, lib.ixact(ix.imgPythonIconTop, .85))

#,x1
def quickLogOff():
    pyRefreshRetry()
    quickLaunch()

def pyRename(isBack=False):
    sim=0.8
    renbutton=ix.imgPyRename
    if isBack:
        renbutton=ix.imgPyRenameBack
    lib.clickTillNext(SCREEN, ix.imgPyTop, lib.ixact(ix.imgPyIcon,sim))
    bswide=initBsWide()
    bswide.highlight(1)
    lib.clickTillNext(bswide, lib.ixact(ix.imgPyIcon, sim), ix.imgPyRunScript)
    lib.clickTillNext(bswide, ix.imgPyRunScript, ix.imgPyRename)
    lib.clickTillGone(bswide, renbutton)

def quickInstall():
    lib.clickTillNext(SCREEN, ix.imgFileManager, ix.imgFileManager2, after=1.5)
    bswide=initBsWide()
    bswide.highlight(1)
    sim=0.8
    if lib.logExists(bswide, lib.ixact(ix.imgPathSD)):
        lib.clickTillNext(bswide, ix.imgFolderAndroid, lib.ixact(ix.imgPathAndroid))

    lib.clickTillNext(bswide, ix.imgFileManagerApk, lib.ixact(ix.imgQuickNext, sim))
    lib.clickTillNext(bswide, lib.ixact(ix.imgQuickNext, sim), lib.ixact(ix.imgQuickInstall, sim))
    lib.clickTillNext(bswide, lib.ixact(ix.imgQuickInstall, sim), ix.imgQuickInstallOpen)
    lib.clickTillGone(bswide, lib.ixact(ix.imgQuickInstallOpen, sim))

def quickUninstall():
    lib.clickTillNext(SCREEN, ix.imgBsIcon, ix.imgSystemApp)
    bswide=initBsWide()
    sim=0.8
    lib.clickTillNext(bswide, ix.imgSystemApp, ix.imgSystemSettings)
    lib.clickTillNext(bswide, ix.imgSystemSettings, ix.imgSystemAppsMgr)
    lib.clickTillNext(bswide, ix.imgSystemAppsMgr, ix.imgFantasica)
    lib.clickTillNext(bswide, ix.imgFantasica, ix.imgSystemUninstall)
    lib.clickTillNext(bswide, ix.imgSystemUninstall, ix.imgSystemUninstallOk)
    lib.clickTillGone(bswide, lib.ixact(ix.imgSystemUninstallOk, sim))    

def installFantaFast():
    global bswide
    # lib.myClick(SCREEN, ix.imgFileManager)
    lib.clickTillNext(SCREEN, ix.imgFileManager, ix.imgFileManager2, after=1.5)
    bswide=initBsWide()
    bswide.highlight(1)
    if lib.logExists(bswide, lib.ixact(ix.imgPathRoot)):
        lib.clickTillNext(bswide, ix.imgFolderSdcard, lib.ixact(ix.imgPathSD))
    if lib.logExists(bswide, lib.ixact(ix.imgPathSD)):
        lib.clickTillNext(bswide, ix.imgFolderAndroid, lib.ixact(ix.imgPathAndroid))

    # if lib.logExists(bswide, lib.ixact(ix.imgPathAndroid)):
    #     lib.clickTillNext(bswide, ix.imgFolderData, lib.ixact(ix.imgPathData))
    # if lib.logExists(bswide, lib.ixact(ix.imgPathData)):
    #     while(not exists(ix.imgFolderFanta)):
    #         p1 = lib.Pts(566, 679)
    #         p2 = lib.Pts(572, 346)
    #         lib.scrollPos(locBsIcon(), p1,p2,1,1)    



#m4
def locateStuff():
    #lib.hoverBox(game)
    #lib.locateg(game, evt.imgDeployExact)
    #lib.locateg(game,ix.imgLocate)
    #scrollAndSelect(6)

    #ie=xact(ix.imgOneStarMon)
    #ie=xact(ix.imgSell, 1)
    #ie=lib.ixact(ix.imgUnselected)
    #lib.log(ie.f)
    hover(lib.ixact(ix.imgUnselected))

#m3
def event1():
    #evt.clash()
    #setupClash()
    #receiveGift()
    evt.joinPanel()
    #evt.trainLoop()
    #joinQC()
    #joinQC2()
    #playQCAll()

def login1():
    #loginAndClaim('skyfall55', 'moonfalling')    
    #loginAndClaim('womgk345', 'moonfalling')    
    #logOutAndIn('skyfall55', 'moonfalling', True) #21000 LP#!
    loginAndClaim('almondlegend', 'moonfalling')    
    #loginAndClaim('triangel2', 'moonfalling')    
    # main(acct='haau61', list=accts.err())
    #InboxAndRegister()
    #receiveGift()
    #sellUnits()
    #inboxItems()
    #inboxGetUnit(ix.imgInbox7to8, ix.img8StarInbox, unitBoxFromStars)
    #inboxGetUnit(ix.imgInbox7to8, ix.img7StarInbox, unitBoxFromStars)
    #changeLeader()
    #chkAcct()
    #chkUnits()
    # pull6Pack()
    #selectUnit()

def pcSettings():
    lib.log("pcSettings")
    pc=os.environ['COMPUTERNAME'] 
    if (pc=='COREI7'):
        lib.DefaultTypeSleep=.4
    lib.log("DefaultTypeSleep=" + str(lib.DefaultTypeSleep))


def rev(list):
    list.reverse()
    return list

# ########################### init1
def begin():
    try:
        initGame()
    except:
        lib.log('x')

    pcSettings()
    tester()
    misc()
    event()
    # loginAndClaim('skyfall55', 'moonfalling')    
    # loginAndClaim('haau157', 'pppppppp', False)
    # main(acct='xcb100', list=accts.passwd()) # fix leader
    # waitHour(2, 10)
    # main('gaau56') # Trade pure

    # Pc2
    # main(acct='haau203', list=accts.Haau1() + accts.Gaau()) # gaau100
    # Pc1
    main(acct='bluu133f', list=accts.BluuAll() + rev(accts.Gaau())) # gaau100
    # main(acct='gaau561', list=accts.BluuAll() + rev(accts.Gaau()))

    # catch up
    # main(acct='haau149', list=rev(accts.Haau1()))
    # ERROR
    # main(acct='', list=accts.err())
    #,m1
    lib.log("------------------ FINISHED")

def misc():
    lib.log("misc actions")
    #trade(False)
    #ally()

    # pullGSPack()
    # inboxAndGsPack()
    # lib.myClick(game, lib.ixact(ix.imgTradeProfile))
    # trade(False)
    # clickAndRename(rename)
    # changeLeader()
    # deferAlly()
    # ally()
    # recruitAlly()
    # pullBraveMain()
    # clickAndRename(rename)
    # clickAndRename(renameBack)    
    # pullTicket()
    
    # lib.myClickIdx(game, ix.imgDetail, 0)
    # acceptAlly()
    # leaderOnly()
    # getPotion()
    # inboxItems()
    # findTrade()
    # InboxAndRegister()
    # trade(hasUnits=False)
    # getMPtrade()

    # lib.clickTillNext(bswide, ix.imgFileManagerApk, ix.imgPyRename)

    # lib.clickTillNext(SCREEN, ix.imgBsIcon, ix.imgSystemApp)

    # pyRename()
    # pyRename(True)
    # quickInstall()
    # quickUninstall()

    # pyRefresh()
    # quickLaunch()
    # inboxGetCard([ix.imgInboxFilterStar_7, ix.imgInboxFilterStar_8, ix.imgInboxFilterStar_9, ix.imgInboxFilterStar_11])

    # inboxGetCard([lib.ixact(ix.imgInboxFilterStar_7), lib.ixact(ix.imgInboxFilterStar_8, .93)])
    # changeLeader()
    # lib.sendMail("testcode-" + evt.user + "-")
    # lib.sendMailTItle("HEARTBEAT-" + evt.user + "-")
    # lib.sendMailTItle("HEARTBEAT-" + str(gIndex) + "-" + evt.user + "-")
    # pad=''.ljust(10)
    # lib.log(pad + "foo")
    # evt.trainLoopNormal(isDaily=False, firstStage=True)
    # launchPython()
    # pyRefreshRetry()
    # missions()
    # raise ValueError
    #,m2

def event():
    lib.log("event")
    # evt.joinPanel()
    # evt.joinClash()
    # evt.joinTrain()
    # evt.joinEvo()
    # evt.diceEnter()
    # evt.joinGift()
    # evt.joinPanel()
    # evt.joinTacticsOnly()
    # evt.diceEnter()
    # receiveGift()
    joinEvent()
    raise ValueError
    #,m3

def harvest():
    lib.log("harvest") 
    # InboxAndRegister()
    # inboxItems()
    # getPotion()ep
    # getMP()
    # tradeStuffPure()
    # raise ValueError
    #,m4

def tester():
    lib.log("tester")
    # lib.myClick(game, ix.imgMyPage)
    #lib.locateg(game, xx)
    # changeLeader()
    #lib.locateg(bsicon, lib.ixact(evt.imgHeal))
    # lib.myClickTillNext(game, ix.imgBack, ix.imgMenuPressed)
    # lib.screenShot(game, "boss-")
    # imgs=[
    #   {'pic':5, 'func':6 },
    #   {'pic':7, 'func':7 },
    # ] 
    # im=imgs[0]['pic']
    # # ir='hehe'
    # if 'pic2' in imgs[0]:
    #     ir=imgs[0]['pic2']
    # else:
    #     ir=None
    # # lib.log(str(im))
    # if ir:
    #     lib.log(ir)
    # raise ValueError



def testMissions():
    missionTrain()
    missionQuest()
    allyMsg()
    profileTitle()
    sellTop()
    missionBattle()

def testScroll():
    p1 = lib.Pts(74, 552)
    p2 = lib.Pts(74, 195)
    #bsicon=find(ix.imgBsIcon)
    while(not exists(ix.imgFolderFanta)):
        lib.scrollPos(locBsIcon(), p1,p2,1,1)

def ads():
    loopAds('B> pot 7:8', 30)
    lib.myClick(game, ix.imgProfile)
    postMsg('B> Nox 270')

## --------------------------------- test codes
def testWaitOr():
    lib.myWaitFor3(game , ix.imgSend, ix.imgDailyStart, ix.imgLoginBonusStart, 5)
    #lib.myWaitFor2(game ,ix.imgChallenge, fPage, 5)
    #existsTest(Pattern(ix.imgStartGame).similar(0.99), 'start')
