print("lib start")

from sikuli import *
import math
import datetime
import shutil
import time
start = time.time()
from org.sikuli.script import Mouse, Button

import growgarden_img
reload(growgarden_img)

# growgarden_img.imgNewSeed="1753042461899.png"

# growgarden_img.imgNewSeed="1753042784116.png"


# growgarden_img.imgX="1753044403206.png"

# growgarden_img.scrollIcon="1753046357389.png"

# growgarden_img.imgDollar="1753046475585.png"

# growgarden_img.imgBuyButton="1753048077186.png"

# growgarden_img.imgBuyButton="1753938975907.png"

# growgarden_img.imgBuyButton="1753954585860.png"

# growgarden_img.imgBuyButton="1753954694432.png"

# growgarden_img.imgNoStockBtn="1753061385485.png"


# growgarden_img.imgNoStock="1753062484265.png"

# growgarden_img.imgCarrot="1753066188628.png"
# growgarden_img.imgOrange="1753066583746.png"

# growgarden_img.imgTomato="1753067557291.png"


# find(growgarden_img.imgNewSeed)
#,,i1

def mysleep(sec):
    sleep(sec)

def log(msg, isEvt=False, lpad=0):
    if not isinstance(msg, str):
        msg = str(msg)
    print(msg)

#,,f1
def myClick(area, imgName):
    img=area.find(imgName)
    myClickImg(img)    

def myClickTillGone(area, imgName):
    try:
        while(True):
            img=area.find(imgName)
            myClickImg(img)
            sleep(1)
    except:
        return

def myClickOnly():
    mouseDown(Button.LEFT)
    mysleep(0.5)
    mouseUp(Button.LEFT)
                
def myClickImg(imgObj):
    m = imgObj
    m.hover(imgObj)
    m.mouseDown(Button.LEFT)
    mysleep(.5)
    m.mouseUp(Button.LEFT)
    mysleep(.1)
    m = None

dialogXOff=680
dialogWidth=730

def initBuy():
    ub = find(growgarden_img.imgX)
    ub.setX(ub.x - dialogXOff)
    ub.setW(dialogWidth)
    ub.setH(650)
    ub.highlight(1)
    #hover(growgarden_img.imgX) 
    return ub

def initBuyArea():
    ub = find(growgarden_img.imgX)
    ub.setX(ub.x - dialogXOff)
    ub.setY(ub.y + 300)
    
    ub.setW(dialogWidth)
    ub.setH(350)
    ub.highlight(1)
    #hover(growgarden_img.imgX) 
    return ub

    

#buyArea=initBuy()



def resetScroll(): 
    cnt=15
    while(cnt>0):
        Mouse.wheel(Button.WHEEL_DOWN, 3)
        #sleep(1)
        cnt-=1

noStockXOff=150
#,,f2
def noStock(area):
    ub = area.find(growgarden_img.imgNoStockBtn)
    ub.setX(ub.x - noStockXOff)
    ub.setY(ub.y - 150)
    
    ub.setW(750)
    ub.setH(300)
    ub.highlight(1)
    hover(growgarden_img.imgNoStockBtn) 
    return ub

def handleNoStock(area):
    try:
        nsArea=noStock(area)
        myClick(buyArea, growgarden_img.imgNoStock)
    except:
        #print("no stock not found")
        pass

def handleEnd(img, msg):
    if buyBox.exists(img, 0.1):
        # log(msg)
        resetScroll()
        sleep(1)
        click(growgarden_img.scrollIcon)
        click(growgarden_img.scrollIcon)
        
def handleNoStock2(area):
    nsArea=noStock(area)
    myClick(buyArea, growgarden_img.imgNoStock)

buyBox=initBuy()

buyArea=initBuyArea()


def scrollFind():
    log("--------------scrollFind starts---------")
    click(growgarden_img.scrollIcon)
    #resetScroll()
    
    cnt=1000
    while(cnt>0):

        #,,x1
#        if buyBox.exists(growgarden_img.imgCarrot, 0.1):
#            log("found carrot")
#            myClickOnly()
#            resetScroll()
#            sleep(1)
#            click(growgarden_img.scrollIcon)
#        if buyBox.exists(growgarden_img.imgTomato, 0.1):
#            log("found tomato")
    #            resetScroll()
#            sleep(1)
#            click(growgarden_img.scrollIcon)
        handleEnd(growgarden_img.imgTomato, "found Tomato")
        if buyArea.exists(growgarden_img.imgDollar, 0.1):
            #buyArea.click(growgarden_img.imgDollar)
            myClick(buyArea, growgarden_img.imgDollar)

            #buyArea.click(growgarden_img.imgDollar)
            sleep(1)
            #buyArea.click(growgarden_img.imgBuyButton)
            #buyArea.click(growgarden_img.imgBuyButton)
            myClickTillGone(buyArea, growgarden_img.imgBuyButton)
            
            sleep(.5)

        handleNoStock(buyArea)
        Mouse.wheel(Button.WHEEL_UP, 1)
        #sleep(1)
        cnt-=1

def main1():
    print("main1")
    print("img version="+str(growgarden_img.varVersion))
    while(True):
        try:
            scrollFind()
        except Exception as e:
            log(e)
            sleep(2)
        except FindFailed as f:
            log(f)
            sleep(2)
            pass
            

def main2():
    print("main2")
    print(growgarden_img.varTest)

#main1()
#handleNoStock(buyArea)
print("lib loaded")