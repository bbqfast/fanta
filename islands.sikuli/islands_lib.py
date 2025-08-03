from sikuli import *
import math
import datetime
import shutil
import time
start = time.time()


#Settings.MoveMouseDelay = 0

imgIslands="1674186971451.png"

#imgIslands="1676694266266.png"
#imgIslands="1685413240172.png"

#imgIslands="1685413486037.png"

imgPlay="1674187063932.png"
#imgPlay="1685314912569.png"
imgPlay2="1685414658443.png"

imgDis="1674228980756.png"

imgLine="1674228996377.png"

imgLeave="1674229017743.png"


imgTeleportError="1674621339440.png"

imgJoinError="1674630488417.png"

imgConnError="1676094517567.png"
imgConnRetry="1676094598986.png"

imgRetry="1674630519002.png"

imgRbxIcon="1675053245047.png"

imgLoginBtn="1675125352021.png"

imgLoginText="1675125417998.png"

imgLoginBtn2="1675125928390.png"


imgClose="1685154294825.png"

existsTimeout=0.5

appBase='C:\Users\dev\AppData\Local\Roblox' + "\\"
settingsFile="GlobalBasicSettings_13.xml"
windowsloc=["GlobalBasicSettings_13-bottom-left.xml", "GlobalBasicSettings_13-bottom-right.xml" ]

accts=[
{"num":1,"loc":Location(300, 188), "user":"busnow3", "pass":"yyyyyyyy"
    , "file":"GlobalBasicSettings_13-top-left.xml"},
# {"num":2,"loc":Location(920, 188), "user":"bb9now2", "pass":"yyyyyyyy", "reboot":True
#     , "file":"GlobalBasicSettings_13-top-mid.xml"},
{"num":2,"loc":Location(920, 248), "user":"bb9now2", "pass":"yyyyyyyy", "reboot":True
    , "file":"GlobalBasicSettings_13-top-mid.xml"},
{"num":3,"loc":Location(1450, 188), "user":"bb9now1", "pass":"yyyyyyyy"},
#{"loc":Location(300, 670), "user":"bbqfast", "pass":"faygay77r"},
#{"loc":Location(100, 670), "user":"bbqfast", "pass":"faygay77r"},
{"num":4,"loc":Location(100, 670), "user":"busnow2", "pass":"yyyyyyyy", "reboot":True
    , "file":"GlobalBasicSettings_13-bottom-left.xml"},
{"num":5,"loc":Location(920, 670), "user":"bb9now3", "pass":"yyyyyyyy"},
{"num":6,"loc":Location(1450, 670), "user":"URTBUH4", "pass":"yyyyyyyy", "reboot":True
    , "file":"GlobalBasicSettings_13-bottom-right.xml"}
]

for a in accts:
    a["sttime"]=start

posCache={}

def ctime():
    return str(datetime.datetime.today())


def log(msg, isEvt=False, lpad=0):
    if not isinstance(msg, str):
        msg = str(msg)
    f = open('islands.txt', 'a', 0)
    msg=''.ljust(lpad * 2) + msg
    lmsg = ctime() + ' ' + msg + '\n' 
    print(lmsg)
    f.write(lmsg)
    f.close()
    if (isEvt):
        event(msg)        

def event(msg):
    if not isinstance(msg, str):
        msg = str(msg)
    f = open('islands-events.txt', 'a', 0)
    lmsg = ctime() + ' ' + msg + '\n' 
    f.write(lmsg)
    f.close()
    # print(msg)
    log(msg)


def shouldReset(info):
    end = time.time()
    dur=end - info["sttime"]
    # timeout=60*3*60
    timeout=60*30
    global start
    #,,x3
    
    print("elapsed: " + str(dur ))
    if (dur > timeout):
        info["sttime"] = time.time()
        dur = 0
        return True
    return False

def copyConfig(confFile):
    try:
        f1=appBase+confFile
        f2=appBase+'GlobalBasicSettings_13.xml'
        shutil.copy (f1, f2)
        return True
    except:
        event("Copy FAILED")
        return False
    
def waitAny(game, any):
    cnt=8
    while not game.exists(any, 1):
        #sleep(1)
        cnt-=1
        if(cnt <= 0):
            log("wait timeout")
            return False
            break
    return True

def closeGame():
    type(Key.ESC)
    sleep(1)
    type("l")
    sleep(1)
    type(Key.ENTER)
    sleep(5)

def play(game):
    try:
        game.click(imgPlay)
    except:
        log("play not found")

#,,sg
def startGame(game, info):
    playIfexists(game)
    if not waitAny(game, imgIslands):
        loginIfNeeded(game, info)
    print("Clicking imgIslands")
    clickWithCatch(game, imgIslands)
    print("Clicking imgIslands FINISH")
    sleep(3)
    waitAny(game, imgPlay)
    clickWithCatch(game, imgPlay)
    event("game started: " + info["user"])

def mousePos():
    getmouseLoc = Env.getMouseLocation()
    x = getmouseLoc.getX()
    y = getmouseLoc.getY()
    #print getmouseLoc
    print("{} {}".format(x,y))
    return (x,y)

def clickWithCatch(img2):
   clickWithCatch(SCREEN, img2) 
def clickWithCatch(game, img2):
    try:
        print("clickWithCatch " + img2)
        #if exists(imgPlay):
        game.click(img2)
    except Exception as e:
        log(e)
    except FindFailed as f:
        log(f)
 
def playIfexists(game):
    clickWithCatch(game, imgPlay2)
    
def closeGameX(game, closeLoc):
    try:
        print("closeGameX")
        #game.hover(imgClose)
        game.hover(closeLoc)
        game.mouseDown(Button.LEFT)
        sleep(.5)
        game.mouseUp(Button.LEFT)
        sleep(1)
        game.mouseDown(Button.LEFT)
        sleep(.5)
        game.mouseUp(Button.LEFT)        
    except Exception as e:
        log(e)
    except FindFailed as f:
        log(f)    

#,,gr
def gameRegion():
    game=cloest()
    hover(game)
    game.setX(game.x - 15)
    game.setY(game.y - 5)
    game.setW(805)
    game.setH(620)
    #game.highlight(1)
    return game

def near(loc1, loc2):
    if (loc1 == None or loc2 == None):
        return True
    xdiff = abs(loc1.getX() - loc2.getX())
    ydiff = abs(loc1.getY() - loc2.getY())
    #ydiff = abs(loc1.getY{) - loc2.getY())

    if (xdiff < 100 and ydiff < 100):
        return True
    else:
        return False

#,,gg
def getGame(info):
    gid=info["num"]
    log("Activate user=" + info["user"] + " gid=" + str(gid))
    if gid not in posCache or posCache[info["num"]] == None:
        game=gameRegion()
        posCache[gid]=game
        closeLoc=game.find(imgClose)
        info['closeloc']=closeLoc
    else:
        game=posCache[gid]
        game.highlight(1)
        if (not game.exists(imgRbxIcon)):
            event("Game MISSING " + str(info["user"]))
            return game, False
        else:
            game.hover(imgRbxIcon)
            log("Game Found")
            return game, True

    #if not near (game, posCache[gid]):
        #event("Game MISSING " + str(gid))
        #return (game, False)
    return (game, True)

def closeAndOpen(info, game):
    print("closeAndOpen: " + info["user"] + " " + str(info["reboot"]))
    if  (not "reboot" in info or info["reboot"]==False):
        print("Skip rebooting")
        return
    if copyConfig(info["file"]):
        event("REBOOTING " + info["user"])
        closeGameX(game, info['closeloc'])
        sleep(5)
        play(game)
        sleep(45)

#,,hd
def handleDisconnect(info):
    #game=gameRegion()
    #posCache[info["num"]]=game
    (game, active)=getGame(info)
    if not active:
        event("INACTIVE")
        if copyConfig(info["file"]):
            print("PLAY")
            play(game)
            sleep(10)
            return
    game.highlight(1)
    #closeGameX(game)

    #,,x2
    if shouldReset(info):
        closeAndOpen(info, game)
    
    #playIfexists(game)
    if game.exists(imgIslands, 0):
        startGame(game, info)
    if game.exists(imgConnError, 0):
        clickWithCatch(game, imgConnRetry)
        closeGame()
        startGame(game, info)
        log("game restarted from conn error")
    if game.exists(imgDis, 0):
        clickWithCatch(game, imgDis)
        closeGame()
        startGame(game, info)
        log("game restarted")
    # imgConnError
    if game.exists(imgTeleportError, 0):
        clickWithCatch(game, imgTeleportError)
        closeGame()
        startGame(game, info)
        log("game restarted")
    #log("check login button")
    if game.exists(imgLoginBtn, 0):
        clickWithCatch(game, imgLoginBtn)
        loginIfNeeded(game, info)
        sleep(10)
        startGame(game, info)
    #log("check login textbox")
    if game.exists(imgLoginText, 0):
        doLogin(game, info["user"], info["pass"])
        sleep(10)
        startGame(game, info)
    if game.exists(imgJoinError, 0):
        clickWithCatch(game, imgLeave)
        


#startGame()
#closeGame()

def activate(info):
    click(atMouse())
    #cloest()
    handleDisconnect(info)
    
def window_t1():
    info=accts[0]
    mouseMove(info["loc"])
    #mouseMove(Location(300, 188))
    activate(info)

def window_t2():
    info=accts[1]
    mouseMove(info["loc"])
    #mouseMove(Location(920, 188))
    activate(info)

def window_t3():
    info=accts[2]
    mouseMove(info["loc"])
    #mouseMove(Location(1450, 188))
    activate(info)

def window_b3():
    info=accts[5]
    mouseMove(info["loc"])
    #mouseMove(Location(1450, 670))
    activate(info)

def window_b2():
    info=accts[4]
    mouseMove(info["loc"])
    #mouseMove(Location(920, 670))
    activate(info)

def window_b1():
    info=accts[3]
    mouseMove(info["loc"])
    #mouseMove(Location(info["loc"].getX(), 0))
    #mouseMove(Location(300, 670))
    activate(info)

   
#mouseMove(1450,188)
#mouseDown()

def cycle():
    while(True):
        #,,w
        window_b3()
        #window_b2()
        window_b1()
        # window_t3()
        # window_t2()
        #window_t1()
        sleep(5)

def dist(x1,y1,x2,y2):
    d1=math.sqrt(pow(x2-x1,2) + pow(y2-y1,2))
    return d1
   
def cloest():
    (x1,y1)=mousePos()
    log("mousePos = " + str(x1) + " " + str(y1))
    rlist=findAll(imgRbxIcon)
    log(rlist)
    mind=1000000000
    minx=1000000000
    miny=1000000000
    minr=None
    cnt=0
    for r in rlist:
        #log(r)
        log(str(cnt) + ": " + str(r.x) + " -- " + str(r.y) )
        #d2=dist(x1,r.x,y1,r.y)
        d2=dist(x1,y1, r.x,r.y)

        #if (r.x > x1):
        #    d2=d2+300
        
        if d2 < mind:
            mind = d2
            minx = r.x
            miny = r.y
            minr = r
        log(d2)
        cnt+=1
        #hover(Location(r.x,r.y))
    #mouseMove(Location(minx,miny))
    log("min mousePos = " + str(minx) + " " + str(miny))
    hover(Location(minx,miny))
    return minr

def cleartext():
    for x in range(20):
        type(Key.BACKSPACE)

def loginIfNeeded(game, info):
    # imgLoginText
    if (game.exists(imgLoginBtn)):
        doLogin(game, info["user"], info["pass"])

def doLogin(game, user,passw):
    clickWithCatch(game, imgLoginText)
    sleep(1)
    cleartext()
    type(user)
    type(Key.TAB)
    cleartext()
    type(passw)
    sleep(1)
    event("login: " + user)
    clickWithCatch(game, imgLoginBtn2)

sleep(2)
log("islands started", True)
#cycle()



print("WELCOME")
cycle()

#playIfexists()
#sleep(1)
#cloest()

#doLogin("bb9now2","yyyyyyyy")
#mousePos()

# 1908 6211

 
#waitAny(SCREEN, imgIslands)  11
#adf
#asdf2