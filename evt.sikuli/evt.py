from sikuli import *
import lib
import org.sikuli.natives.Vision as Vision;

import evt_img as ix
reload(ix)

gQuestFavOn=False
game=5
state='no train'
usePot=True
potUse=0
potMax=1
bossFight=lib.Ref('bossFight',0)
user='unknown'
stopAT71=True
vartest=True

flower = 5
allimg=ix

def findPanelPage():
    findPage(ix.imgPanelEventPage, -1)

def findColoPage():    
    findPage(ix.imgColoEventPage, -1)

def findEventTrainPage():
    findPage(ix.imgTrainEvenPage, -1)


def maidenStart():
    lib.log('----------------------- Start Training ')
    # lib.log('maidenStart')
    # if lib.logExists(game, ix.imgMaidenBoss):
    #     lib.myClick(game, ix.imgMaidenBoss)
    #     fightMaidenBoss()
    if lib.logExists(game, ix.imgMaidenTraining):
        lib.myClick(game, ix.imgMaidenTraining, 3)

#    if lib.logExists(game, ix.imgMaidenTraining):
 #       lib.myClick(game, ix.imgMaidenTraining)

def Start(firstStage=False):
    global state, stopAT71
    #if game.exists(ix.imgStartTrain):
    if lib.logExists(game, ix.imgStartTrain):
        lib.log('----------------------- start training')
        #if game.exists(ix.imgSevenOne):
        lib.log("stopAT71=" + str(stopAT71))
        if lib.logExists(game, lib.ixact(ix.imgSevenOne)) and stopAT71:
            state='done'
            lib.log('------------ at 7-1 training DONE !')
        else:
            # lib.myClickImg(imgLast(ix.imgStartTrain))
            if firstStage:
                lib.log("firstStage")
                scrollTraining()
                scrollTraining()
                lib.myClickIdx(game, ix.imgStartTrain, 0)
            else:
                lib.myClickIdx(game, ix.imgStartTrain, 0, isLast=True)
            #lib.myClickImg(ix.imgByOrder(ix.imgStartTrain, 0))
        return True
    return

def maidenBackToEvent():
    lib.myClick(game, ix.imgMypage)
    while lib.logExists(game, ix.imgTrainEventEnter, 2):
        lib.myClick(game, ix.imgTrainEventEnter)

def fightMaidenBoss():
    lib.log('----------------------- fightMaidenBoss')
    #clickMaidenMessage()
    if log.exists(game, ix.imgFight):
        fightTrainBoss()
   # while not lib.logExists(game, ix.imgMaidenTraining): 
   #     clickMaidenMessage()

def fightChallenge():
    lib.myClick(game, ix.imgChallenge)
    sleep(10)
    fightTrainBoss()

def fightTrainBoss():
    allyCnt=0
    lib.log('fight begin !')
    while(game.exists(ix.imgFight)):
        lib.log('in fight')
        if (lib.logExists(game, ix.imgSummonAlly) and allyCnt < 3):
            lib.log('call ally')
            lib.myClick(game, ix.imgSummonAlly)
            allyCnt=allyCnt+1
        else:
            lib.myClick(game, ix.imgFight) 
        sleep(2)

def Boss():
    #if game.exists(ix.imgFlee):
    if lib.logExists(game, lib.ixact(ix.imgFlee)):
        lib.screenShot(game, "boss-")
        lib.log('Boss')
        lib.myClick(game, ix.imgFlee)

def Heal():
    global state, potUse, usePot
    if lib.logExists(game, ix.imgHeal):
        lib.log('heal')
        if lib.logExists(game, ix.imgPotLowExact):
            game.hover(ix.imgPotLow)
            lib.log('potion level too low!')
            state='wait'
            return False
        if potUse >= potMax:
            lib.log('Used too much potion=' + str(potUse))
            state='done'
            return False
        if not usePot:
            lib.log('Dont use Pot')
            state='done'
            return False
        lib.myClick(game, ix.imgHeal)
        lib.myClick(game, ix.imgYes)
        # lib.myClick(ix.imgMyPage)
        potUse=potUse+1
        state=='train'
        return True
        #state='no train'
    return True       

def challenge():
    lib.log('find challenge')
    #if game.exists(ix.imgChallenge):
    if lib.logExists(game, ix.imgChallenge):
        lib.log('----------------------- challenge')
        fightChallenge()
        return True
    return False


def setPositionsMaiden():
    global center, pos1, pos2, pos3, pos4, pos5, pos6
    ydelta = 0
    
    center = Pts(135, 248 + ydelta) #278
    pos3 = Pts(151, 223 + ydelta) #278
    pos2 = Pts(202, 223 + ydelta)
    pos1 = Pts(270, 223 + ydelta) #429
    pos6 = Pts(151, 375 + ydelta)    
    pos5 = Pts(227, 375 + ydelta)    
    pos4 = Pts(278, 375 + ydelta)    

#x2
def TrainEventBoss(skip=False):
    lib.log('TrainEventBoss()')
    global bossFight
    #if game.exists(ix.imgFlee):
    if lib.logExists(game, ix.imgFightExact):
        if skip:
            lib.myClick(game, ix.imgFlee, 1)
            return
        lib.screenShot(game, user + "-boss-")
        if lib.logExists(game, ix.imgBossHard):
            lib.log('Hard Boss, skipping')
            lib.myClick(game, ix.imgFlee, 1)
            return
        if not lib.logExists(game, ix.imgBossLevel1):
            lib.log('Big Boss, skipping')
            lib.myClick(game, ix.imgFlee, 1)
            return
        bossFight.set(bossFight.get()+1)
        #lib.screenShot(game, "boss-")
        lib.log('Easy Boss')
        lib.myClick(game, ix.imgFight)
        pl = initTrainDeployPos()
        placeUnit(pl)
        # lib.myWait(game ,ix.imgBackToEvent, 60)
        trainBossHandleResult()
        return True
        # lib.myWaitFor2(game, ix.imgBackToEvent, ix.imgEvtTrain, 60)
        # if lib.logExists(game, ix.imgBackToEvent):
        #     lib.myClick(game, ix.imgBackToEvent)
    return False

def TrainEventBossCont():
    lib.log('TrainEventBossCont()')
    global bossFight, state
    fought=False
    win = False
    #if game.exists(ix.imgFlee):
    # while not win:
    if lib.logExists(game, ix.imgFightBossCont):
        # lib.myClick(game, ix.imgFightBossCont)
        lib.clickTillNext(game, ix.imgFightBossCont, ix.imgTrainSelectBoss)
        if lib.logExists(game, ix.imgFightBossCont2):
            fought=True
            lib.myClick(game, ix.imgFightBossCont2)
            if lib.logExists(game, ix.imgYes, 1):
                lib.myClick(game, ix.imgYes)
            #bossFight=bossFight+1
            #lib.screenShot(game, "boss-")
            lib.log('Boss Cont')
            #lib.myClick(game, ix.imgFight)
            pl = initTrainDeployPos()
            placeUnit(pl)
            # lib.myWait(game, ix.imgBackToEvent, 40)
            trainBossHandleResult()
        else:
            lib.myClick(game, ix.imgBackToEvent2)
            bossFight.set(0)
            # break
    return fought

def trainBossHandleResult():
    global state, bossFight
    lib.myWaitFor3(SCREEN, ix.imgBackToEvent, ix.imgEvtTrain, ix.imgQuestFailed, 40)
    if lib.logExists(game, ix.imgFightWon):
        lib.log('Boss Won!!!')
        win = True
        state='done'
        bossFight.set(0)
    if lib.logExists(game, ix.imgQuestFailed):
        lib.log('trainBossHandleResult() - FAILED')
        state='outer'
        lib.myClick(game, ix.imgQuestFailed)    
    if lib.logExists(game, ix.imgBackToEvent):    
        lib.myClick(game, ix.imgBackToEvent)    

def checkBossAndStart():
    TrainEventBossCont()
    lib.myWait(game, ix.imgMaidenTraining, 5)
    maidenStart()

# state
# training -> boss -> failed -> FailedScreen (quick) -> Train main page
# training -> stage clear -> choose level

def trainLoop(user='unknown'):
    global loop, delay, state, bossFight, potUse
    lib.log('trainLoop=' + state)      
    potUse=0
    cnt=0
    state='train'
    if lib.logExists(game, ix.imgTrainEventEnter):
        lib.clickTillNext(game, ix.imgTrainEventEnter, ix.imgMaidenTraining)
    while (not state=='done'):
        lib.log('outer train loop bossFight=' + bossFight.s())
        #IntoTrain()
        if TrainEventBossCont():
            continue
        lib.sleeplogx(5)
        # checkBossAndStart()
        maidenStart()
        #if bossFight > 0:
        Start()
        state='train'
        lib.log('state=' + state)      
        while state=='train':
            lib.log('Loop:' + str(cnt) + ' bossFight='+ bossFight.s() + " potUse="+str(potUse) + ' state=' + state)
            if Adv():
                continue
            if Brave():
                continue
            if Cont():
                continue
            if not Heal(): ##
                break
            if lib.logExists(game, ix.imgMaidenYes):
                lib.myClick(game, ix.imgMaidenYes)
                # doQuest()
            # if bossFight.get() > 0:
            #     lib.log("Boss fought, back to main")
            #     break
            #challenge()
            # maidenStart() # can see start after event boss
            Start() # could pop back to train screen if level done
            TrainEventBoss()
            sleep(1)
            cnt+=1
        # during multi acct mode, we dont wait for regen, we move on to next account
        #saveRanks()
        lib.sleeplogx(1)
        #state=='train'
    lib.log('maiden loop EXIT')      
    trainRank()
    lib.myClickTillGone(game, ix.imgMyPage, waitForImgAppear=30)

def scrollTraining():
    p2 = lib.Pts(74, 552)
    p1 = lib.Pts(74, 250)
#    p2 = lib.Pts(74, 195)
    #lib.scrollPos(locBsIcon(), p1,p2,1,1)
    lib.scrollPos(game, p1,p2,1,1)

#ep1
def episode1():
    if lib.logExists(game, lib.ixact(ix.imgTrainSelectEpisode), 2):
        lib.myClick(game, ix.imgTrainSelectEpisode, waitForImgAppear=1, after=1)
        scrollTraining()
        # pic=lib.imgByOrder(ix.imgTrainSelect, 0)
        # lib.myWait(game ,evt.ix.imgTrainSelect, totalWaits=10, takeshot=True)
        # lib.myClickImg(pic)
        lib.myClickIdx(game, ix.imgTrainSelect, 0)

#tln1
def trainLoopNormal(user='unknown', isDaily=False, skip=False, firstStage=False):
    global loop, delay, state, bossFight, potUse
    lib.log('trainLoop normal=' + state)      
    potUse=0
    cnt=0
    state='train'
    if not isDaily:
        lib.myClick(game, ix.imgTrainPage, 1)
        if firstStage:
            episode1()
    while (not state=='done'):
        lib.log('outer normal loop bossFight=' + bossFight.s())
        #IntoTrain()3
        # lib.sleeplogx(5)
        # checkBossAndStart()
        # maidenStart()
        #if bossFight > 0:
        if not isDaily:
            challenge()
        Start(firstStage)
        state='train'
        lib.log('state=' + state)
        iadv=0
        while state=='train':
            lib.log('Loop:' + str(cnt) + ' bossFight='+ bossFight.s() + " potUse="+str(potUse) + ' state=' + state)
            sleep(1)
            if Adv():
                iadv=iadv+1
                if isDaily:
                    state='done'
                    lib.canSkip(skip, "trainLoopNormal")
                    lib.sleeplogx(6)
                    Boss()
                    break
                sleep(1)
                continue
            if Brave():
                continue
            if Cont():
                continue
            if not Heal(): ## 
                break
            # if lib.logExists(game, ix.imgMaidenYes):
            #     lib.myClick(game, ix.imgMaidenYes)
                # doQuest()
            if TrainEventBoss(True):
                continue
            # if isDaily or challenge():
            if challenge():
                continue
            # maidenStart() # can see start after event boss
            if Start(firstStage): # could pop back to train screen if level done
                cnt=0
                continue
            cnt+=1
            #x1
            if cnt > 20:
                lib.log(user + " Infinite trainLoopNormal")
                raise ValueError(user + " Infinite trainLoopNormal")
        # during multi acct mode, we dont wait for regen, we move on to next account
        #saveRanks()
        lib.sleeplogx(1)
        #state=='train'
    lib.log('normal loop EXIT')      
    if lib.logExists(game, ix.imgBack):
        lib.myClick(game, ix.imgBack, waitForImgAppear=1, after=1)
    elif lib.logExists(game, ix.imgMyPage):
        lib.myClickTillGone(game, ix.imgMyPage)
    else:
        lib.myClick(game, ix.imgBack, waitForImgAppear=1, after=1)
        if lib.logExists(game, ix.imgMyPage, 2):
            lib.myClickTillGone(game, ix.imgMyPage)

def trainRank():
    if lib.logExists(game, ix.imgTrainRanking):
        lib.myClick(game, ix.imgTrainRanking, 1)
        lib.screenShot(game, "Rank-" + user + "-shot-")
        lib.myClick(game, ix.imgBack, 1)

def fightColo(minBeforeStart = 0):
    global multiAcct, usePot
    global loop, delay, state
    sleepMinute(minBeforeStart)
    while True:
        delay = 0
        multiAcct=True
        usePot=False
        mainLoop()
        findColoPage()
        lib.myClick(game, ix.imgColoEnter, waitForImgAppear=10)
        fightArea()
        lib.myClick(game, ix.imgBack, waitForImgAppear=10)
        sleep(1)
        lib.myClick(game, ix.imgBack, waitForImgAppear=10)
        sleepMinute(10)

def fightArea():
    #image = lib.ix.imgByOrder(ix.imgColoFight, 0)
    image = lib.ix.imgLast(ix.imgColoFight)
    lib.myClickImg(image)
    lib.sleeplogx(3)
    if lib.logExists(game, ix.imgColoBossNear):
        lib.myClick(game, ix.imgYes)
    #lib.myWait(game, ix.imgSkip,10)
    lib.myClick(game, ix.imgSkip, waitForImgAppear=30)
    lib.myClick(game, ix.imgBack, waitForImgAppear=30)        

def guildDeployTeam():
    lib.myClick(game, ix.imgGuildManage)
    lib.myClick(game, ix.imgGuildDeploy)
    lib.myClick(game, ix.imgGuildDeploySpot)
    lib.myClick(game, ix.imgYes)    

def buildCannon():
    while True:
        if Adv():
            continue
        if Brave():
            continue
        if Cont():
            continue
        if game.exists(ix.imgGuildFire):
            break
    lib.sleeplogx(3) 
    lib.myClick(game, ix.imgGuildFire)
    lib.clicklog(ix.imgBsBack)
    lib.myClick(game, ix.imgGuildToBattle)

def initTrainDeployPos():
    pl = []
    pl.append(lib.Pts(146, 281))
    pl.append(lib.Pts(146, 334)) 
    pl.append(lib.Pts(199, 387)) 
    pl.append(lib.Pts(253, 387)) 
    pl.append(lib.Pts(306, 387)) 
    pl.append(lib.Pts(359, 334)) 
    pl.append(lib.Pts(359, 281)) 
    return pl

def placeUnit2():
    lib.log('placeUnit()');
    l = [pos1, pos2, pos3]
    loopUnits(l)

def placeUnit(l):
    lib.log('placeUnit()');
    #l = [pos1, pos2, pos3]
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
    lib.myClickTillGone(game, imgButton, waitForImgAppear=20)
    c=1
    if gQuestFavOn and game.exists(ix.imgFavOff):
        lib.myClick(game, ix.imgFavOff)
    for x in posList:
        if not deploy(imgButton, x, c):
            return
        lib.log('placed ' + str(c))
        c=c+1


def place(pos):
    lib.log('place() x=' + str(pos.x) + 'y=' + str(pos.y))
    mouseMove(Location(game.getX() + pos.x, game.getY() + pos.y))
#myDrag(Location(game.getX() + pos1.x, game.getY() + pos1.y))            
    lib.clickHere()  
    
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
            lib.log('No more deploy for ' + lib.strimg(imgButton))
            return False
        lib.myClick(game, imgButton) 
    if not lib.logExists(game, ix.imgDeployExact):
        lib.log('No Unit to deploy')
        if lib.logExists(game, ix.imgBack):
            lib.myClick(game, ix.imgBack)
        return False
    ix.imgFirstDeploy=lib.ix.imgByOrder(ix.imgDeployExact, 0)
    #lib.myWait(game ,ix.imgDeployConfirm, totalWaits=10, takeshot=True)
    lib.myClickImg(ix.imgFirstDeploy)
#    if not lib.logExists(game, ix.imgDeployConfirm):
#        lib.myClick(game, ix.imgBack)
#        return False
    #place(pos)
    #lib.myClick(game, ix.imgDeployConfirm)
    #while not lib.myWait(SCREEN ,ix.imgMyProfileFrom, 6):
    #while lib.logExists(game, ix.imgDeployConfirm):
    lib.log('Confirm place')
    place(pos)
    lib.myClick(game, ix.imgDeployConfirm)
    lib.sleeplogx(1)
    return True


def Brave():
    if lib.logExists(game, ix.imgBrave):
        lib.log('brave')
        lib.myClick(game, ix.imgBrave)
        return True
    else:
        return False
def Adv():
    global bossFight
    if lib.logExists(game, ix.imgAdv):
        lib.log('advance bossFight=' + bossFight.s() + ' potUse=' + str(potUse))
        lib.myClick(game, ix.imgAdv)
        lib.sleeplogx(.7)
        return True
    else:
        return False

def imgLast(image):
    lib.log('ix.imgLast')
    tt = findAll(image)
    tts  = sorted(tt, key=lib.by_y)
    #lib.log(str(len(tts)))
    button=tts[len(tts)-1]
    hover(button)    
    return button

def Cont():
    if lib.logExists(game, ix.imgCont):
        lib.log('continue')
        lib.myClick(game, ix.imgCont)
        lib.sleeplogx(.7)
        return True
    else:
        return False

def rookBox(image, hover=True): # unused
    ub=find(image)
    ub.setX(ub.x - 5)
    ub.setY(ub.y - 50)
    ub.setW(450)
    ub.setH(90)  
    if hover:
        lib.hoverBox(ub)
    return ub


def joinClash():
    lib.myClick(game, ix.imgClashMain, after=1)
    if lib.logExists(game, ix.imgNo, 2):
        lib.myClick(game, ix.imgNo, after=2)
    lib.myClick(game, ix.imgMyPage) 

def clash():
    lib.log('Clash()')
    lib.myClick(game, ix.imgClashMain)
    if lib.logExists(game, ix.imgNo, 2):
        lib.myClick(game, ix.imgNo)
    lib.myClick(game, ix.imgClashBattleLg, 1)
    #lib.myClick(game, ix.imgClashFight)
    box=rookBox(ix.imgClashRook)
    lib.myClick(box, ix.imgClashFight, 1)
    win=False
    clashpot=0
    lib.myClick(game, ix.imgClashBattleStart, 1)
    lib.myClick(game, ix.imgYes)
    while not win:
        lib.myClick(game, ix.imgClashSkip)
        lib.myWaitFor2(game, ix.imgClashBattle, ix.imgYes, 20)
        if lib.logExists(game, ix.imgYes):
            lib.myClick(game, ix.imgYes)        
            lib.myClick(game, ix.imgYes, 1) # for potion
            clashpot+=1
        else:
            win=True
            break
    #  finish battle
    lib.myClick(game, ix.imgClashBattle,1)
    # lib.myClick(game, ix.imgClashBack)
    lib.clickTillGone(game, ix.imgClashBack)   
    lib.log('Clash() pot=' + str(clashpot))
    if lib.logExists(game, ix.imgMyPage, 2): 
        lib.myClick(game, ix.imgMyPage) 

def joinTacticsOnly():
    lib.myClick(game, ix.imgTacticsMain)
    lib.sleeplogx(3)
    if lib.logExists(game, ix.imgYes):
       lib.myClick(game, ix.imgYes, after=1.5)
    # lib.sleeplogx(1)
    lib.myClick(game, ix.imgTacticsMain2, 1)

#pt1
def playTactics():
    lib.myClick(game, ix.imgTacticsMain)
    lib.sleeplogx(3)
    if lib.logExists(game, ix.imgYes):
        lib.myClick(game, ix.imgYes)
        lib.sleeplogx(3)
    if lib.logExists(game, ix.imgTacticsFormTeam):
        lib.myClick(game, ix.imgTacticsFormTeam)
    cnt=3
    while cnt > 0:
        lib.myWaitFor2(game ,ix.imgTacticsBattle, ix.imgTacticsBoss, 63)
        if lib.logExists(game, ix.imgTacticsBoss):
            lib.myClick(game, ix.imgTacticsBoss)
        else:
            lib.myClick(game, ix.imgTacticsBattle)
            lib.myClick(game, ix.imgTacticsCP6)
        #lib.myClickTillGone(game, ixact(ix.imgTacticsBattle), waitForImgAppear=63)
        lib.sleeplogx(7)
        #lib.myClick(game, ix.imgTacticsAutoOff)
        lib.myClickTillGone(game, ixact(ix.imgTacticsAutoOff), waitForImgAppear=1)
        lib.myClick(game, ix.imgTacticsFF)
    #lib.myClick(game, ix.imgTacticsNext)
        lib.myWaitFor2(game ,ix.imgTacticsNext, ix.imgTacticsGiveup, 30)
        if lib.logExists(game, ix.imgTacticsNext):
            lib.log('playTactics() - Win')
            break
        else:
            lib.log('playTactics() - Give up')
            lib.myClick(game, ix.imgTacticsGiveup)               
            lib.myClick(game, ix.imgYes)               
        cnt=cnt-1
    lib.myClick(game, ix.imgTacticsNext, waitForImgAppear=30)
    lib.myClick(game, ix.imgTacticsTop)
    lib.sleeplogx(3)
    lib.myClick(game, ix.imgTacticsMenu)
    lib.myClick(game, ix.imgTacticsRankings)
    # lib.screenShot(game, user + "-tactics-ranking-")    
    lib.myClick(game, ix.imgBack)
    lib.myClick(game, ix.imgTacticsMain2)        

def diceEvent():
    diceEnter()
    diceRoll()
    
def diceEnter():
    lib.myClick(game, ix.imgDiceMain, after=1.5)
    lib.myClick(game, ix.imgDiceEventPage, after=1.5)
    if lib.logExists(game, ix.imgNo, 2):
        lib.myClick(game, ix.imgNo, waitForImgAppear=1, after=2)
    # lib.myClick(game, ix.imgBack, waitForImgAppear=3, after=1)
    # lib.myClickTillGone(game, lib.ixact(ix.imgBack), waitForImgAppear=2, waitAfterClick=1.5)
    lib.myClickTillNext(game, lib.ixact(ix.imgBack, .85), ix.imgMenu)


def diceRoll():
    c=4
    lib.sleeplogx(1)    
    while c>0 and lib.logExists(game, ixact(ix.imgDiceBTzero, 0.95)):
        #lib.myClick(game, ix.imgDiceRoll)
        if lib.logExists(game, ixact(ix.imgDiceRoll, .95)):
            lib.myClickTillGone(game, ixact(ix.imgDiceRoll, .95), waitForImgAppear=0, retryIfNotGone=30, waitAfterClick=1)
            #lib.clickTillNext(game, ixact(ix.imgDiceRoll, .95), ix.imgDiceStop)
            lib.myClick(game, ix.imgDiceStop)
            lib.sleeplogx(5)
        if lib.logExists(game, ix.imgDiceFight):
            lib.log('diceRoll() - fight')
            lib.myClick(game, ix.imgDiceFight)
            diceFightBoss()
            break;
        if lib.logExists(game, ix.imgDiceOpenChest):
            lib.log('diceRoll() - chest')
            lib.myClick(game, ix.imgDiceRetreat)
            lib.myClick(game, ix.imgYes)
            #break;
        c=c-1
    
def diceFightBoss():
    lib.log('diceFightBoss()')
    lib.clickTillNext(game, ix.imgDiceRoll, ix.imgDiceStop)
    lib.myClick(game, ix.imgDiceStop)
    lib.sleeplogx(7)
    #lib.myWaitFor2(game ,ix.imgDiceToBoard, ix.imgTrainPage, 5)    
    if not lib.logExists(game, ix.imgDiceToBoard):
        lib.log('diceFightBoss() - not winning')        
        lib.clickTillNext(game, ix.imgDiceRetreat, ix.imgYes)
        lib.myClick(game, ix.imgYes)
        lib.sleeplogx(5)
    lib.myClick(game, ix.imgDiceToBoard)    
    if lib.logExists(game, ix.imgYes):
        lib.myClick(game, ix.imgYes)    
    lib.myClick(game, ix.imgBack)    
    lib.sleeplogx(1)
    lib.myClick(game, ix.imgBack)     
    

def joinEvo():
    lib.log("joinEvo() 5")
    lib.myClick(game, ix.imgEvoMain, after=1)
    # lib.sleeplogx(5)
    lib.myWait(game, ix.imgBack, 5)
    if lib.logExists(game, ix.imgEvoEventPage):
        lib.myClick(game, ix.imgEvoEventPage, after=1)
    while lib.logExists(game, ix.imgEvoMina):
        lib.quickClick(game, ix.imgEvoMina)
    lib.myClick(game, ix.imgBack, waitForImgAppear=1, after=1)

def joinGift():
    lib.log("joinGift()")
    lib.myClick(game, ix.imgGiftMain, after=.5)    
    lib.myClick(game, ix.imgGiftBack, waitForImgAppear=1, after=1)

def joinTrain():
    lib.log("joinTrain()")
    if lib.logExists(game, ix.imgTrainEvent, 2):
        lib.myClick(game, ix.imgTrainEvent)        
    if lib.logExists(game, ix.imgTrainEvent2, 2):
        lib.myClick(game, ix.imgTrainEvent2)    
    lib.myClickTillGone(game, ix.imgMyPage, 0, 2, 2)    

def joinPanel():
    lib.log("joinPanel()")
    lib.myClick(game, ix.imgPanelEventPage)
    lib.sleeplogx(1)
    if game.exists(ix.imgPanelEventPage2):
        lib.myClick(game, ix.imgPanelEventPage2)
    lib.myClick(game, ix.imgBack, after=1)
