# ~/Skull/SikuliX.app/Contents/Java/TrainLog.tx

from sikuli.Sikuli import *
import lib
import evt
import accts
import traceback
import datetime
import mac_img as mimg1


reload(mimg1)
reload(lib)
reload(evt)
reload(accts)
import org.sikuli.natives.Vision as Vision;
import datetime
import shutil
Vision.setParameter("MinTargetSize", 10) # A small value such as 6 makes the matching 


def waitHour(hr, min):
    lib.log('waitHour()');
    while True:
        now = datetime.datetime.now()
        if (now.hour == hr and now.minute > min):
            break
        lib.sleeplogx(60)
    #print now.year, now.month, now.day, now.hour, now.minute, now.second


def ixact(img, sim=0.9):
    return lib.XP(img).fx(img.f+"Exact").similar(sim)    

#mc3
def myClick3(area, img, waitForImgAppear=0, after=0.5):
    lib.myClick(area, img, waitForImgAppear=waitForImgAppear, holdDur=0.5, after=after)

def myClick4(area, img, waitForImgAppear=.5, after=0.8):
    lib.myClick(area, img, waitForImgAppear=waitForImgAppear, holdDur=0.5, after=after)

def initGame():
    lib.log('initGame')
    global bsicon, game, bottomBarDrag, bottomBarDrop, heroBarDrag, heroBarDrop
    #bsicon=initBsIcon()
    game = find(mimg1.imgMobaIcon)
    game.setX(game.x - 20)
    game.setW(500)
    game.setH(900)
    evt.game=game
    lib.game=game


def setup(first=True):
    lib.log("setup")
    if lib.logExists(SCREEN, mimg1.imgMobaIcon):
        initGame()
        if first:
            myClick3(game, mimg1.imgMobaIcon)
        game.highlight(1)

def sendLuna():
    lib.log("sendLuna")
    if lib.logExists(game, mimg1.imgSelect):
        myClick3(game, mimg1.imgSelect)
        myClick3(game, mimg1.imgViewItems)
        while lib.logExists(game, ixact(mimg1.imgLunaTotal, .95)):
            myClick3(game, mimg1.imgLuna, holdDur=.4)
        myClick3(game, mimg1.imgTrade)
        myClick3(game, mimg1.imgConfirm)
        myClick3(game, mimg1.imgContinue)
        myClick3(game, mimg1.imgBack)

def goBack():
    if lib.logExists(game, mimg1.imgBack):
        myClick3(game, mimg1.imgBack)
        myClick3(game, mimg1.imgBack)

#tl
def tradeLoop():
    lib.log("tradeLoop")
    while True:
        myClick4(game,  mimg1.imgMenu)
        myClick4(game, mimg1.imgTradeMain)
        lib.sleeplogx(3)
        if lib.logExists(game, mimg1.imgDetails):
            myClick4(game, mimg1.imgDetails)
            lib.sleeplogx(3)
            sendLuna()
            goBack()
        else:
            myClick4(game, mimg1.imgBack) 
        lib.sleeplogx(2)
        myClick4(game,  mimg1.imgMenuPressed)
    

def allyAccept():
    myClick3(game, mimg1.imgAllyMain)
    clearApprove()
    myClick3(game, mimg1.imgBack)
    lib.sleeplogx(3)

def clearApprove():
    lib.log("clearApprove")
    while lib.logExists(game, mimg1.imgAllyApprove):
        myClick3(gambge, mimg1.imgAllyApprove)
        lib.sleeplogx(2)
        myClick3(game, mimg1.imgBack)
        
def allyApprove():
    lib.log("allyApprove")
    #if lib.logExists(game, mimg1.imgAllyWaiting):
    myClick3(game, mimg1.imgAllyWaiting)
    lib.sleeplogx(2)
    myClick3(game, mimg1.imgWaitApproval)    
    while lib.logExists(game, mimg1.imgAllyApprove):
        myClick3(game, mimg1.imgAllyApprove)
        lib.sleeplogx(2)
    #if lib.logExists(game, mimg1.imgBack):
    myClick3(game, mimg1.imgBack)

def allyLoop():
    while True:
        #allyAccept()
        allyApprove()
        lib.sleeplogx(14)

def setBox(ub, dx, dy, w, h):
    ub.setX(ub.x + dx)
    ub.setY(ub.y + dy)
    ub.setW(w)
    ub.setH(h)  
    #lib.hoverBox(ub)
    ub.highlight(1)

def closeFanta():
    lib.log("closeFanta")
    ex=0
    while ex < 3:
        try:
            ub=find(mimg1.imgFantaTab)
            setBox(ub, -5, -5, w=120, h=30)
            myClick3(ub, mimg1.imgTabClose)    
            break
        except:
            lib.screenShot(game, "closeFanta-")
            lib.log("CloseFanta failed: ex=" + str(ex))
            lib.log(traceback.format_exc())
            ex=ex+1

def launch():
    lib.log("launch()")
    #while lib.logExists(SCREEN,  mimg1.imgFantaIcon):
    myClick3(SCREEN, ixact(mimg1.imgFantaIcon))
    #lib.clicklog(mimg1.imgFantaIcon)
    #lib.locateg(SCREEN, ixact(mimg1.imgFantaIcon))`
    mouseDown(Button.LEFT)
    mouseUp(Button.LEFT)    
    lib.sleeplogx(1)

def relaunch():
    lib.log("relaunch()")
    closeFanta()
    lib.sleeplogx(1)
    try:
        launch()
        lib.myClickTillGone(SCREEN, mimg1.imgStartGame, waitForImgAppear=240)
        setup(False)
    except:
        lib.screenShot(game, "relaunch()-except")
        lib.log(traceback.format_exc())
        return False
    return True

def afterLaunch():
    lib.log("afterLaunch()")
    lib.sleeplogx(2)
    if lib.logExists(game, mimg1.imgClose):
        myClick3(game,  mimg1.imgClose)
    myClick3(game,  mimg1.imgMenu)
    myClick3(game, mimg1.imgAllyMain)
    clearApprove()

def allyLoopCatch():
    lib.log("allyLoopCatch")
    re=False
    while True:
        try:
            if re:
                afterLaunch()
            allyLoop()
        except:
            lib.screenShot(game, "allyLoopCatch-")
            lib.log(traceback.format_exc())
            if not relaunch():
                conitinue
            re=True

def tradeLoopCatch():
    while True:
        try:
            tradeLoop()
        except:
            lib.screenShot(game, "tradeLoopCatch-")
            lib.log(traceback.format_exc())
            relaunch()
            re=True    

def leana():
    while True:
        if lib.logExists(game, mimg1.imgGetLp):
            myClick3(game, mimg1.imgGetLp)
        if lib.logExists(game, mimg1.imgYes):
            myClick3(game, mimg1.imgYes)
            lib.sleeplogx(1)

#waitHour(2, 30)           
def mysleep(sec):
    start_t=time.time()
    while True:
        dur=time.time() - start_t
        if dur > sec:
            lib.log('mysleep() ' + str(dur))
            return
        
def sleeptest():
    start_t=time.time()
    mysleep(0.5)
    dur=time.time() - start_t
    lib.log(str(dur))

#leana()

def pullBrave():
    cnt=0
    while True:
        cnt+=1
        lib.log("--------------- Idle Round =" + str(cnt))
        while lib.logExists(game, lib.ixact(mimg1.imgBraveNext), 1.5):
            cnt=0
            if lib.logExists(game, lib.ixact(mimg1.imgYes)):
                myClick3(game, mimg1.imgYes)
            myClick3(game, mimg1.imgBraveNext)
            #lib.sleeplogx(1.5)
        if lib.logExists(game, lib.ixact(mimg1.imgYes)):
            myClick3(game, mimg1.imgYes)
        if lib.logExists(game, lib.ixact(mimg1.imgBraveAgain)):
            cnt=0
            myClick3(game, mimg1.imgBraveAgain)
        if cnt > 20:
            break
        lib.sleeplogx(1)
    

def mysleep2(sec):
    start_t=datetime.datetime.now()
    while True:
        now_t=datetime.datetime.now()
        dur=(now_t-start_t).total_seconds()
        if dur > sec:
            lib.log('mysleep() ' + str(dur))
            return

def inboxCardLP():
    cnt=0
    while True:
        if lib.logExists(game, mimg1.imgSelectAll):
            cnt=0
            myClick3(game, mimg1.imgSelectAll)
        if lib.logExists(game, mimg1.imgConfirm):
            myClick3(game, mimg1.imgConfirm)
        if lib.logExists(game, mimg1.imgExchangeLP, 3):
            myClick3(game, mimg1.imgExchangeLP)
        if lib.logExists(game, mimg1.imgYes):
            myClick3(game, mimg1.imgYes)
            lib.sleeplogx(3)
        cnt+=1
        if cnt > 3:
            break


def clickIfExists(area, image1, wait=0, after=0):
    if lib.logExists(game, image1, wait):
        myClick3(game, image1)
        lib.sleeplogx(after)

def inboxStack(stack):
    while True:
        clickIfExists(game, mimg1.imgSelectAll)
        clickIfExists(game, mimg1.imgStack)
        clickIfExists(game, stack, after=2)


def receiveItems(maxcnt):
    lib.log('receiveItems()')
    if lib.logExists(game, mimg1.imgInboxItemsTabDark):
        myClick3(game,  mimg1.imgInboxItemsTabDark)
        lib.sleeplogx(1)

    idle=0
    cnt=0
    while True:
        if lib.logExists(game, mimg1.imgSelectAll):
            idle=0
            myClick3(game, mimg1.imgSelectAll)
        if lib.logExists(game, mimg1.imgConfirm):
            myClick3(game, mimg1.imgConfirm)
        if lib.logExists(game, mimg1.imgReceive3):
            myClick3(game, mimg1.imgReceive3)
        if lib.logExists(game, mimg1.imgYes):
            myClick3(game, mimg1.imgYes)
            lib.sleeplogx(3)
            # if cnt > maxcnt:
            if not lib.logExists(game, lib.ixact(mimg1.imgInboxHasNextPage), 2):
                break
            continue
        idle+=1
        cnt+=1
        lib.log('receiveItems() No-op COUNT=' + str(idle))
        if idle > 5:
            lib.log('receiveItems() Idle exceeded=' + str(idle))
            break

    lib.sleeplogx(2)

def inboxStack2(typeButton, page=0, maxcnt=2):
    lib.log('inboxStack2()')
    if lib.logExists(game, mimg1.imgInboxLunaTabDark):
        myClick3(game,  mimg1.imgInboxLunaTab)
        lib.sleeplogx(1)

    myClick3(game,  mimg1.imgInboxFilter, after=1)
    clearType()

    myClick3(game,  lib.ixact(typeButton))
    myClick3(game,  mimg1.imgConfirm)

    while (page>0):
        myClick3(game,  mimg1.imgInboxNextPage)
        page-=1

    cnt=0
    while cnt < maxcnt:
        clickIfExists(game, mimg1.imgSelectAll)
        clickIfExists(game, mimg1.imgStack)
        clickIfExists(game, mimg1.imgLuna5M, after=2)
        clickIfExists(game, mimg1.imgBrave100k, after=2)
        cnt+=1
        if not lib.logExists(game, lib.ixact(mimg1.imgLunaNextPage), 2):
            break        
        lib.log("inboxStack2 COUNT=" + str(cnt))

    lib.sleeplogx(1)

def inboxClear():
    if lib.logExists(game, mimg1.imgItemsTab): 
        receiveItems()
    if lib.logExists(game, mimg1.imgLunaTab):
         inboxStack2()
    if lib.logExists(game, mimg1.imgItemsTab):
        receiveItems()

def filterBy():
    myClick3(game, mimg1.imgItemsTab)

def clearType():
    clickIfExists(game, lib.ixact(mimg1.imgTypeLunaPressed))
    clickIfExists(game, lib.ixact(mimg1.imgTypeAllyPtsPressed))
    clickIfExists(game, lib.ixact(mimg1.imgTypeBravePtsPressed))

def claimInbox():
    lib.log('claimInbox()')
    while True:
        receiveItems(10)
        inboxStack2(mimg1.imgTypeAllyPts,2,50)
        inboxStack2(mimg1.imgTypeBravePts,28,50)
        inboxStack2(mimg1.imgTypeLuna,2,50)

def begin():
    # 1000303354
    # 1000295803
    # 93152216
    setup()
    tradeLoopCatch()
    # leana()

    # receiveItems(200)
    # inboxStack(mimg1.imgBrave100k);
    # claimInbox()        

    # pullBrave()
    # inboxCardLP()

    # inboxClear()

    # inboxStack2(mimg1.imgTypeLuna)
    # inboxStack2(mimg1.imgTypeBravePts,1,100)
    # inboxStack2(mimg1.imgTypeAllyPts,1,100)
    # inboxStack2(mimg1.imgTypeLuna,1,100)
    #m1

    lib.log("------------------ FINISHED")
    # inboxStack(mimg1.imgAlly50k)
    # inboxStack(mimg1.imgLuna5M)
    # inboxStack2()
    # inboxStack(mimg1.imgBrave100k)
    # inboxLunaStack()

    #myClick3(game, mimg1.imgBraveAgain)

            
    #lib.log('x')
    #mysleep2(1.5)
    #lib.log('y')

    #relaunch()
    #launch()
    #[
    #allyLoopCatch()
    #allyLoop()
    #myClick3(game, mimg1.imgStartGame)
    #myClick3(game,  mimg1.imgMenu)
    #myClick3(game, mimg1.imgAllyMain)
    #clearApprove()
    #allyLoop()
        
    #allyApprove()
    