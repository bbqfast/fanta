from sikuli import *
import datetime
import shutil
import time
import traceback
import random

DefaultHoldDur=.2
DefaultAfter=0
DefaultTypeSleep=.3

class XP(Pattern):
    def fx(self, _name):
        self.f  = _name
        return self

class Ref:
    def __init__(self, _name, _val):
        self.val = _val
        self.name = _name
    def s(self):
        return str(self.val)
    def get(self):
        log("get " + self.name + "=" + self.s())
        return self.val
    def set(self, _val):
        self.val = _val
        log("set " + self.name + "=" + self.s())

class X(str):
    def __new__(self, value, _fname = "unknown"):
        self.f = _fname
        return str.__new__(self, value)
    def fx(self, _name):
        #print "img " + _name
        self.f  = _name
        return self
    
class Pts:
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y

class Pts:
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y

class Image1:
    # while not area.exists(img)
    def __init__(self, _img):
        self.img1 = _img
    def existsOr(self, area):
        return area.exists(self.img1)
    def name(self):
        return strimg(self.img1)

class Image2:
    def __init__(self, _img1, _img2):
        self.img1 = _img1
        self.img2 = _img2
    def existsOr(self, area):
        return area.exists(self.img1) or area.exists(self.img2)
    def name(self):
        return strimg(self.img1) + ' or ' + strimg(self.img2)

class Image3:
    def __init__(self, _img1, _img2, _img3):
        self.img1 = _img1
        self.img2 = _img2
        self.img3 = _img3
    def existsOr(self, area):
        return area.exists(self.img1) or area.exists(self.img2) or area.exists(self.img3)
    def name(self):
        return strimg(self.img1) + ' or ' + strimg(self.img2) + ' or ' + strimg(self.img3)

class Image4:
    def __init__(self, _img1, _img2, _img3, _img4):
        self.img1 = _img1
        self.img2 = _img2
        self.img3 = _img3
        self.img4 = _img4
    def existsOr(self, area):
        return area.exists(self.img1) or area.exists(self.img2) or area.exists(self.img3) or area.exists(self.img4) 
    def name(self):
        return strimg(self.img1) + ' or ' + strimg(self.img2) + ' or ' + strimg(self.img3) + ' or ' + strimg(self.img4)

class MyExcept(Exception):
    def __init__(self, message, errors):
        super(MyExcept, self).__init__(message)
        self.msg = message
        self.errors = errors
    def msgstr(self):
        return self.msg

class LoginError(MyExcept):
    def __init__(self, message):
        super(LoginError, self).__init__(message, [])

class LoginFail(MyExcept):
    def __init__(self, message):
        super(LoginFail, self).__init__(message, [])

class FreshAcctError(MyExcept):
    def __init__(self, message):
        super(FreshAcctError, self).__init__(message, [])

class NoAllyError(MyExcept):
    def __init__(self, message):
        super(NoAllyError, self).__init__(message, [])

class SkipError(MyExcept):
    def __init__(self, message):
        super(SkipError, self).__init__(message, [])

class InfiniteLoop(MyExcept):
    def __init__(self, message):
        super(InfiniteLoop, self).__init__(message, [])

class ClickExcept(MyExcept):
    def __init__(self, message):
        super(ClickExcept, self).__init__(message, [])

def canSkip(skip, msg):
    if skip:
        sleeplogx(1)
        raise SkipError(msg)

def logExcept(msg):
    log(msg + " " +traceback.format_exc())

def ctime():
    return str(datetime.datetime.today())

def strimg(img):
    #if (img.__class__.__name__ == 'X'):
    if hasattr(img, 'f'):
        return img.f
    else:
        return str(img)

def logimg(msg, img, lpad=0):
#    f = open('TrainLog.txt', 'a', 0)
    #f.write(ctime() + ' ' + msg + ' ' + strimg(img) + '\n')
    log(msg + ' ' + strimg(img), lpad)
#    f.close()


def logc(msg):
    f = open('TrainLog.txt', 'a', 0)
    f.write(msg)
    f.close()


def log(msg, lpad=0):
    f = open('TrainLog.txt', 'a', 0)
    msg=''.ljust(lpad * 2) + msg
    lmsg = ctime() + ' ' + msg + '\n' 
    print(lmsg)
    f.write(lmsg)
    f.close()

def logx(msg):
    f = open('TrainLog.txt', 'a', 0)
    lmsg = ctime() + ' ' + msg + '\n' 
    print(lmsg)
    f.write(lmsg)
    f.close()

def logExists(area, img, dur = 0, lpad=0):
    start_t=time.time()
    exts = area.exists(img, dur)
    dur=time.time() - start_t
    if exts:
        logimg('Exists=true dur=' + str(dur), img, lpad)
    else:
        logimg('Exists=false dur' + str(dur), img, lpad)
    return exts

def clickHere0():
    mouseDown(Button.LEFT)
    mysleep(.5)
    mouseUp(Button.LEFT)
    mysleep(.5)

def clickHere(hold = .5):
    mouseDown(Button.LEFT)
    mysleep(hold)
    mouseUp(Button.LEFT)
    mysleep(.5)

def clicklogNoError(img, after=.5, lpad=0):
    try:
        clicklog(img, after, lpad)
    except:
        log('clicklogNoError() except OK')
        pass   

def clicklog(img, after=1, lpad=0):
    log('click for ' + str(img.f) + ' after=' + str(after), lpad)
    click(img)
    mysleep(after)

def mysleep(sec):
    sleep(sec)

def mysleep4(sec):
    start_t=datetime.datetime.now()
    cycle=0

    while True:
        # sqrt = random.randint(1000,5000)**(.5)
        cycle+=1
        now_t=datetime.datetime.now()
        dur=(now_t-start_t).total_seconds()
        if dur > sec:
            log('mysleep2() cycle=' + str(cycle))
            return

def mysleep3(sec):
    start_t=time.time()
    while True:
        dur=time.time() - start_t
        if dur > sec:
            return

def sleeplogx(sec, lpad=0):
    log('sleep for ' + str(sec), lpad)
    mysleep(sec)

def sleepMinute(min):
    log('sleep for ' + str(min) + ' Minute')
    for x in range(1, min + 1):
        logc('...' + str(x))
        mysleep(60)

def by_y(match):
   return match.y

def locate(img):
    tt=find(img)
    hover(tt)
    log("Relative pos:  x= " + str(tt.getX() - game.getX() + tt.getW() / 2) + " y= " + str(tt.getY() - game.getY() + tt.getH() / 2 ) )

def locateg(game, img):
    tt=find(img)
    hover(tt)
    #Pts(146, 281)
    log("lib.Pts(" + str(tt.getX() - game.getX() ) + "," + str(tt.getY() - game.getY() ) + ")" ) 
    log("lib.Pts(" + str(tt.getX() - game.getX() + tt.getW() / 2) + "," + str(tt.getY() - game.getY() + tt.getH() / 2 ) + ")" ) 


def locatebr(game, img):
    tt=find(img)
    hover(tt)
    log("Relative pos:  x= " + str(tt.getX() - game.getX() + tt.getW()) + " y= " + str(tt.getY() - game.getY() + tt.getH()) )

def screenSize():
    ar=SCREEN
    log("Screen: " + str(ar.getW()) + " ," + str(ar.getH()) )

def printImgSize(ar):
    log("size: " + str(ar.getW()) + " ," + str(ar.getH()) )


# debug region
def hoverBox(box):
    hover(Location(box.x, box.y))
    sleep(.5)
    hover(Location(box.x + box.w, box.y))
    sleep(.5)
    hover(Location(box.x, box.y + box.h))
    sleep(.5)
    hover(Location(box.x + box.w, box.y + box.h))
    sleep(.5)


def myWaitInternal(area , imgs, totalWaits, takeshot=False, lpad=0):
    log('myWait() ' + imgs.name(), lpad)
    if area==None:
        area=SCREEN
    waitCount=0
    while not imgs.existsOr(area):
        waitCount = waitCount + 1
        log('wait ' + str(waitCount), lpad=lpad)
        if (waitCount > totalWaits):
            if takeshot:
                screenShot(area)
            log('wait ' + imgs.name() + ' exceeded ' + str(totalWaits), lpad=lpad)
            return False
        sleeplogx(.3, lpad=lpad)    
    return True    

# def myWait0(area ,img, totalWaits):
#     log('myWait() ' + str(img))
#     if area==None:
#         area=SCREEN
#     waitCount=0
#     while not area.exists(img):
#         waitCount = waitCount + 1
#         log('wait ' + str(waitCount))
#         if (waitCount > totalWaits):
#             log('wait ' + str(img) + ' exceeded ' + str(totalWaits))
#             return False
#         mysleep(.5)    
#     return True


def myWait(area ,img, totalWaits, takeshot=False, lpad=0):
    comp=Image1(img)
    return myWaitInternal(area, comp, totalWaits, takeshot, lpad=lpad)

def myWaitFor2(area ,img1, img2, totalWaits, lpad=0):
    comp=Image2(img1, img2)
    return myWaitInternal(area, comp, totalWaits, lpad=lpad)

def myWaitFor3(area ,img1, img2, img3, totalWaits, lpad=0):
    comp=Image3(img1, img2, img3)
    return myWaitInternal(area, comp, totalWaits, lpad=lpad)

def myWaitFor4(area ,img1, img2, img3, img4, totalWaits, lpad=0):
    comp=Image4(img1, img2, img3, img4)
    return myWaitInternal(area, comp, totalWaits, lpad=lpad)

def myClickImg(imgObj):
    m = imgObj
    m.hover()
    m.mouseDown(Button.LEFT)
    mysleep(1)
    m.mouseUp(Button.LEFT)
    mysleep(.5)
    m = None

# def myClickTillGone0(area, img, wait=False, dur=30, retry=30):
#     log('deprecated ClickTillGone wait=False, dur=30')
#     if wait:
#         myClickTillGone(area, img, waitForImgAppear=0, retryIfNotGone=30)
#     else:
#         myClickTillGone(area, img, waitForImgAppear=dur, retryIfNotGone=30)
       
#ctg

def clickTillGone(area, img, maxRetry=30, lpad=0, throw=False):
    log('clickTillGone() ' + str(img.f))
    c=0
    # while area.exists(img, 0):
    while logExists(area, img, lpad=lpad+1):
        # clicklog(img)
        clicklogNoError(img, lpad=lpad+1)
        c=c+1
        if(c > maxRetry):
            log('fastClickTillGone() ' + str(img.f) + ' exceeded')
            if throw:
                raise ClickExcept("clickTillGone")
            return False
    return True        

#mctn2
def myClickTillNext(area, img, nextImg
    , waitForImgAppear=0, holdDur=DefaultHoldDur, after=DefaultAfter, retryIfNotGone=10, nextArea=None
    , idx=None, isLast=False, lpad=0):
    log('myClickTillNext() ' + str(img.f) + ' nextImg=' +  str(nextImg.f) + ' after=' + str(after))
    # myClick(area, img, waitForImgAppear)
    # sleeplogx(waitAfterClick)
    c=0
    # while not area.exists(nextImg):
    if not nextArea:
        nextArea=area
    while not logExists(nextArea, nextImg, lpad=lpad+1):
        log('myClickTillNext while:' + str(c))
        try:
            # clicklog(img)
            if idx != None:
                myClickIdx(area, img, idx, waitForImgAppear, holdDur, after, isLast, lpad=lpad+1)
            else:
                myClick(area, img, waitForImgAppear, holdDur, after, lpad=lpad+1)
            # clicklogNoError(img)
            # sleeplogx(after)
        except:
            log('myClickTillNext() except OK')
            pass
        # myClick(area, img, 2)
        sleeplogx(.3, lpad=lpad+1)
        c=c+1
        if(c > retryIfNotGone):
            log('myClickTillNext() ' + str(img.f) + 'exceeded')
            return False
    return True        


# retryIfNotGone=10
def clickTillNext(area, img, nextImg, retryIfNotGone=2, after=.3, lpad=0, throw=False):
    log('clickTillNext() ' + str(img.f) + ' nextImg=' +  str(nextImg.f) + ' after=' + str(after))
    # myClick(area, img, waitForImgAppear)
    # sleeplogx(waitAfterClick)
    c=0
    # while not area.exists(nextImg, 0):
    while not logExists(area, nextImg, lpad=lpad+1):
        log('clickTillNext while:' + str(c))
        try:
            # clicklog(img)
            clicklogNoError(img, after, lpad=lpad+1)
            # sleeplogx(after)
        except:
            log('clickTillNext() except OK')
            pass
        # myClick(area, img, 2)
        sleeplogx(after, lpad=lpad+1)
        c=c+1
        if(c > retryIfNotGone):
            log('clickTillNext() ' + str(img.f) + 'exceded')
            if throw:
                raise ClickExcept("clickTillNext")
            return False
    return True        


#,,mctg
def myClickTillGone(area, img, waitForImgAppear=0, retryIfNotGone=30, waitAfterClick=1, holdDur=DefaultHoldDur, lpad=0, skipIfNotExist=0, moveAway=False):
    log('myClickTillGone2() ' + str(img.f))
    if skipIfNotExist==0:
        myClick(area, img, waitForImgAppear=waitForImgAppear, holdDur=holdDur, lpad=lpad+1)
        sleeplogx(waitAfterClick)

    if moveAway:
        SCREEN.hover()
    c=0
    # while area.exists(img):
    while logExists(area, img, lpad=lpad+1):
        log('myClickTillGone2() LOOP ' + str(img.f))
        myClickNoerror(area, img, 1, lpad=lpad+1)
        sleeplogx(waitAfterClick)
        SCREEN.hover()
        c=c+1
        if(c > retryIfNotGone):
            log('myClickTillGone2() ' + str(img.f) + ' exceded')
            return False
    return True        
    
# def myClick(area, img, wait=False, dur=30):
#     log('deprecated myClick wait=False, dur=30')
#     if wait:
#         myClick(area, img, waitForImgAppear=dur)
#     else:
#         myClick(area, img, waitForImgAppear=0)

def quickClick(area, img):
    locateg(area, img)
    clickHere(hold = 0)    

def myClickHold(area, img, waitForImgAppear=0):    
    logimg('myClickHold() ', img)
    myClick(area, img, waitForImgAppear=0, holdDur=3)

def myClickNoerror(area, img, waitForImgAppear=0, holdDur=DefaultHoldDur, after=0, lpad=0, times=1, moveAway=False):   
    try:
        myClick(area, img, waitForImgAppear=waitForImgAppear, holdDur=holdDur, after=after, lpad=lpad+1, times=times, moveAway=moveAway)
    except:
        log('myClickNoerror() except OK')
        pass             

# ,,mc1 ,,mck1
def myClick(area, img, waitForImgAppear=0, holdDur=DefaultHoldDur, after=DefaultAfter, lpad=0, times=1, moveAway=False):
    logimg('myClick() wait=' + str(waitForImgAppear) + ' hold=' + str(holdDur) + ' after=' + str(after), img, lpad=lpad)

    if not waitForImgAppear == 0:
        log('myClick() wait non zero')
        myWait(area, img, waitForImgAppear, lpad=lpad)
    else:
        log('myClick() wait=False', lpad)
    m = area.find(img)
    #m.click()
    m.hover()
    #mysleep(0.5)
    while times > 0:
        m.mouseDown(Button.LEFT)
        mysleep(holdDur)
        m.mouseUp(Button.LEFT)
        mysleep(after)
        times = times - 1
    m = None
    if moveAway:
        SCREEN.hover()

# more than one
def myClickIdx(area, img, idx, waitForImgAppear=0, holdDur=DefaultHoldDur, after=DefaultAfter, isLast=False, lpad=0):
    logimg('myClickIdx() wait=' + str(waitForImgAppear) + ' hold=' + str(holdDur) + ' after=' + str(after), img, lpad=lpad)

    if not waitForImgAppear == 0:
        log('myClickIdx() wait non zero', lpad=lpad)
        myWait(area, img, waitForImgAppear)
    else:
        log('myClickIdx() wait=False', lpad=lpad)
    # m = area.find(img)
    m = findByOrder(area, img, idx, isLast)
    #m.click()
    m.hover()
    #mysleep(0.5)
    m.mouseDown(Button.LEFT)
    mysleep(holdDur)
    m.mouseUp(Button.LEFT)
    mysleep(after)
    m = None    

def myClickExact(area, img):
    m = area.find(Pattern(img).exact())
    #m.click()
    m.hover()
    #mysleep(0.5)
    m.mouseDown(Button.LEFT)
    mysleep(1)
    m.mouseUp(Button.LEFT)
    mysleep(1.5)
    m = None


def scrollPos(game, posDrag, posDrop, speed, dir=1):
    if dir==-1:
        temp=posDrag
        posDrag=posDrop
        posDrop=temp
    log('scrollPos() x=' + str(posDrag.x) + 'y=' + str(posDrag.y))
    #oldDelay=Settings.MoveMouseDelay
    hover(Location(game.getX() + posDrag.x, game.getY() + posDrag.y))
    #Settings.MoveMouseDelay = speed
    dragDrop(Location(game.getX() + posDrag.x, game.getY() + posDrag.y), Location(game.getX() + posDrop.x, game.getY() + posDrop.y))
    #Settings.MoveMouseDelay=oldDelay

def exactExists(area, img):
    return area.exists( Pattern(img).exact())

def existsTest(img, label):
    if game.exists(img):
        log(label + ' exists')
    else:
        log(label + ' exists')


def slowType(msg):
    for c in msg:
        log('c=' + str(c))
        type(str(c))
        mysleep(DefaultTypeSleep)

def keydown(c):
    log('kd=' + str(c))
    # type(c)
    keyDown(c)

    # mysleep(.3)
    keyUp(c)
    keyUp(c)
    mysleep(.5)

def slowTypeChar(c):
    # log('sc=' + str(c))
    type(c)
    mysleep(DefaultTypeSleep)

def tryImgsByOrder(img):
    try:
        return imgsByOrder(img)
    except:
        log('tryImgsByOrder- not found ' + str(img.f))
        return []

def imgsByOrder(img):
    tt = game.findAll(img)
    tts  = sorted(tt, key=by_y)
    log('imgByOrder: total image found:' + str(len(tts)))
    #hover(tts[0])    
    return tts

def imgByOrder(img, idx):
    tt = findAll(img)
    tts  = sorted(tt, key=by_y)
    log('imgByOrder: total image found:' + str(len(tts)))
    #hover(tts[0]) 
    if idx + 1 > len(tts) :
        return None
    else:
        return tts[idx]

def findByOrder(area, img, idx, isLast=False):
    tt = area.findAll(img)
    tts  = sorted(tt, key=by_y)
    log('findByOrder: total image found:' + str(len(tts)))
    #hover(tts[0]) 
    if isLast:
        idx=len(tts)-1
    if idx + 1 > len(tts) :
        return None
    else:
        return tts[idx]

def by_y(match):
   return match.y

def imgFirst(area, img):
    if not logExists(area, img):
        return None
    tt = findAll(img)
    tts  = sorted(tt, key=by_y)
    hover(tts[0])
    return tts[0]

def imgLast(img):
    log('imgLast')
    tt = findAll(img)
    tts  = sorted(tt, key=by_y)
    #log(str(len(tts)))
    button=tts[len(tts)-1]
    hover(button)    
    return button


def timestamp():
    curDate = datetime.datetime.now().date() #.time()
    curTime = datetime.datetime.now().time()
    return str(curDate.year) + str(curDate.month) + str(curDate.day) + "-" + str(curTime.hour) + ";" + str(curTime.minute) + ";" + str(curTime.second)


def screenShot(area, name="screenshot"):
    log('screenShot():' + name)
    #img = find(gImgScore) 
    # file=capture(area)
    # shutil.move(file,  name + "=Shot=" + timestamp() + ".png")
    screenShotNoTime(area, name + "=Shot=" + timestamp() + ".png")

def screenShotNoTime(area, name):
    log('screenShot():' + name)
    #img = find(gImgScore) 
    file=capture(area)
    shutil.move(file,  name)


def saveStatsShot(img, name):
    #img = find(gImgScore) 
    img.setW(400)
    img.setH(600)
    img.hover()
    file=capture(img)
    #shutil.move(file, name + "=" + timestamp() + ".png")
    shutil.move(file, name + ".png")
    img = None # clean up

def sendMail(body):
    os.system("C:\\SikuliX\\fanta\\script\\questMail.bat " + body)

def sendMailTItle(body):
    os.system("C:\\SikuliX\\fanta\\script\\subjectMail.bat " + body)


def dur(sec):
    # return str(datetime.timedelta(seconds=sec))
    return time.strftime("%H:%M:%S", time.gmtime(sec))

def ixact(img, sim=0.9):
    return XP(img).fx(img.f+"Exact").similar(sim)    
