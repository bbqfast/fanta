imgMenu=lib.X("1384927648657.png").fx("imgMenu")
imgLaunchFanta=lib.X("1384962722131.png").fx("imgLaunchFanta")
imgBsSetting=lib.X("1384962796125.png").fx("imgBsSetting")
imgBsBack=lib.X("1384962825250.png").fx("imgBsBack")

#------------------Moba coins

imgMobaOffer=lib.X("1385239767014.png").fx("imgMobaOffer")
imgMobaCancel=lib.X("1385239779197.png").fx("imgMobaCancel")
imgMobaLater=lib.X("1386043000480.png").fx("imgMobaLater")


imgSetting=lib.X("1384961374436.png").fx("imgSetting")
imgSettingFrom=lib.X("1384961474242.png").fx("imgSettingFrom")
imgSettingTo=lib.X("1384961485466.png").fx("imgSettingTo")
imgLogout=lib.X("1384961535394.png").fx("imgLogout")

#-------------- daily img
#imgMyPage=lib.X("1380266124485.png").fx("imgMyPage")
imgDailyStart=lib.X("1382186126149.png").fx("imgDailyStart")
imgDailyStop=lib.X("1382268772148.png").fx("imgDailyStop")
imgDailyAds=lib.X("1382616189506.png").fx("imgDailyAds")
imgSkip=lib.X("1386080679425.png").fx("imgSkip")


imgMyProfileTo=lib.X("1384966556211.png").fx("imgMyProfileTo")

imgMyApps=lib.X("1384969512104.png").fx("imgMyApps")

imgLoginBonusStart=lib.X("1384970164355.png").fx("imgLoginBonusStart")
imgWelcomeBack=lib.X("1402197661205.png").fx("imgWelcomeBack")

imgFree6=lib.X("1402200366320.png").fx("imgFree6")
imgDailyRoulette=lib.X("1398307771076.png").fx("imgDailyRoulette")

 
def logOut():
    click(imgMenu)
    #lib.myClickExact(SCREEN, imgMenu) 
    lib.myClickExact(SCREEN, imgSetting)
    lib.myWait(SCREEN ,imgSettingFrom, 30)   # save guard drag drop 
    dragDrop(imgSettingFrom, imgSettingTo)
    lib.myClick(SCREEN, imgLogout)
    lib.myClickExact(SCREEN, imgLogoutYes)

def logOut2(stopbs=False):
    lib.myClick(SCREEN, imgMobaIcon)
    lib.sleeplogx(1)
    lib.myClick(SCREEN, imgMobaIconGreyExact, waitForImgAppear=30)
    lib.sleeplogx(5)
    # save guard drag drop 
    while not lib.myWait(SCREEN ,imgMyProfileFrom, 6):
        lib.log('grey moba icon might still here, reclicking')
        lib.myClick(SCREEN, imgMobaIconGreyExact, waitForImgAppear=30)
        lib.sleeplogx(5)
    oldDelay=Settings.MoveMouseDelay
    Settings.MoveMouseDelay = 2
    hover(imgMyProfileFrom)
    dragDrop(imgMyProfileFrom, imgMyProfileTo)
    dragDrop(imgMyProfileFrom2, imgMyProfileTo)
    #dragDrop(imgMyProfileFrom, imgMyProfileTo) # seem not needed
    Settings.MoveMouseDelay=oldDelay
    lib.myClick(SCREEN, imgLogout)
    lib.myClick(SCREEN, imgLogoutYes, True)
    if stopbs:
        quitBS()

def runFanta():
    lib.log('runFanta')
    lib.myWait(SCREEN ,imgMyApps, 30)
    while exists(imgMyApps):
        lib.clicklog(imgMyApps)
        lib.clicklog(imgLaunchFanta)
        lib.sleeplogx(4)
    #sleep(2)
    #log('App Icon gone, now adjest Fanta dimension')
    #lib.clicklog(imgBsSetting)
    #lib.clicklog(imgBsBack)  

def cancelMoba():
    if(game.exists(imgMobaCancel)):
        lib.log('cancelMoba')
        lib.myClick(game, imgMobaCancel)
        sleep(2)
    if(game.exists(imgMobaLater)):
        lib.log('laterMoba')
        lib.myClick(game, imgMobaLater)
        sleep(2)    

## new daily
def daily():
    lib.log('daily()')
    #lib.myClick(game, imgDailyStart)
    lib.myClickTillGone(game, imgDailyStart, waitForImgAppear=60)
    sleep(3) ## hope fix the bug stuck at ads screen
    lib.myClick(game, imgDailyStop, waitForImgAppear=30)
    #lib.myClickTillGone(game, imgDailyAds, True, 60)
    if hasDailyAds:
        lib.myClick(game, imgDailyAds, waitForImgAppear=60)
    #comp=Image2(imgSend, imgAllyWaiting)
    comp=Image3(imgSend, imgAllyWaiting, imgAnnounceClose)
    #while game.exists(imgBack):
    while not comp.existsOr(game):
        lib.log('comp.existsOr cond')
        lib.myClick(game, imgBack, waitForImgAppear=30)
        lib.sleeplogx(5) # fix bug a delay of main screen loading

def chkDaily():
    lib.log('chkDaily()')
    if game.exists(imgMyPage):
        lib.myClick(game, imgMyPage)    
        sleep(5)
    if game.exists(imgDailyStart):
        daily()

def dailyAfterStart():
    lib.log('dailyAfterStart')
    # imgDailyStart
    #lib.myWaitFor2(SCREEN ,imgLoginBonusStart, imgDailyStart, 5)
    #lib.myWaitFor3(game, imgAllyWaiting, imgDailyStart, imgLoginBonusStart, 5)
    #lib.myWaitFor4(game, imgWelcomeBack, imgAllyWaiting, imgDailyStart, imgLoginBonusStart, 5)
    lib.myWaitFor3(game, imgAllyWaiting, imgDailyStart, imgBingo, 5)
    #if lib.myWait(game, imgLoginBonusStart, 5):
    if lib.logExists(game, imgWelcomeBack):
        lib.myClick(game, imgMyPage)
    if lib.logExists(game, imgLoginBonusStart):
        lib.myClick(game, imgMyPage)
        lib.sleeplogx(5)
    lib.sleeplogx(2)        
    if lib.logExists(game, imgFree6):
        lib.sleeplogx(2)        
        lib.myClick(game, imgBack)
        lib.sleeplogx(5)
    if lib.logExists(game, imgBingoIntro):
        lib.myClick(game, imgNextPage)
        lib.sleeplogx(3)
    bingo()
    lib.log('dailyAfterStart EXIT')

def logOutAndIn1(user, passw):
    lib.log('logOutAndIn(' + user + ', ' + passw + ')')
    logOut2()
    logIn(user, passw)

def logOutAndIn(user, passw, stopbs=False):
    lib.log('logOutAndIn(' + user + ', ' + passw + ')')
    logOut2(stopbs)
    logIn(user, passw, stopbs)  # if we stop we start also!

def logIn(user, passw, runbs=False):
    lib.log('logIn(' + user + ', ' + passw + ')')
    if runbs:
        runBS()
    runFanta()
    loginFanta(user, passw)
    lib.sleeplogx(6)
    lib.log('logged in(' + user + ', ' + passw + '), game starting')
    #if not (game.exists(imgSend)):
    if not lib.logExists(game, imgSend):
        dailyAfterStart() 
        #deferAlly()
        clearAlly()
        cancelAnnounce()
        sleep(3)
    saveStatsShot(user)

def cancelMoba():
    if(game.exists(imgMobaCancel)):
        lib.log('cancelMoba')
        lib.myClick(game, imgMobaCancel)
        sleep(2)
    if(game.exists(imgMobaLater)):
        lib.log('laterMoba')
        lib.myClick(game, imgMobaLater)
        sleep(2)

def cancelSound():
    if(game.exists(imgSound)):
        lib.log('cancelSound')
        lib.myClick(game, imgNo)
        sleep(2)

def runBS():
    cmd = 'C:\Program Files (x86)\BlueStacks\HD-StartLauncher.exe' 
    lib.log('Start BlueStacks')
    #os.popen(cmd); wait(3)   
    openApp(cmd)
    wait(5)

def quitBS():
    cmd = 'C:\Program Files (x86)\BlueStacks\HD-Quit.exe'
    lib.log('Quit BlueStacks')
    openApp(cmd)
    wait(3)

def isRotaryHour():
    curTime = datetime.datetime.now().time()
    hh = curTime.hour
    mm = curTime.minute
    if (hh == 4):
        return True
    else:
        return False    

def runDaily():
    if (isRotaryHour()):
        chkDaily()

def chkDaily():
    roulette()
    if game.exists(imgMyPage):
        lib.myClickTillGone(game, imgMyPage, waitForImgAppear=60)
    lib.sleeplogx(5)
    if game.exists(imgDailyStart):
        daily()

def runFanta():
    lib.log('runFanta')
    lib.myWait(SCREEN ,imgMyApps, 30)
    while exists(imgMyApps):
        lib.clicklog(imgMyApps)
        lib.clicklog(imgLaunchFanta)
        lib.sleeplogx(4)
    #sleep(2)
    #log('App Icon gone, now adjest Fanta dimension')
    #lib.clicklog(imgBsSetting)
    #lib.clicklog(imgBsBack)    


def roulette():
    if game.exists(imgDailyRoulette=X):
        lib.myClickTillGone(game, imgNextPage=X, waitForImgAppear=3)        

def smartStart(user, passw):
    if lib.logExists(SCREEN, imgMyApps):
        runFanta()
    if lib.logExists(SCREEN, imgLogin):
        loginFanta(user, passw)


def old():
    try:
        lib.log('try ... catch Begins')
        #lib.sleeplogx(delayStart)
        logOutAndIn('kpp111', 'pppppppp', True) #21000 LP#!
        #fightColo(minBeforeStart = 0) #m2
        #hover(imgMyPageExact)
        #loginLoop(list)
        #hover(imgBingoRemainingExact)
        #singleTrain()
        #saveRanks()
        #maidenLoop()
    except:
        #screenShot(game, "Exception")    
        raise 
