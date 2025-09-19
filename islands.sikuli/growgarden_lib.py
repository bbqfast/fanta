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


buyBox=None
buyArea=None


def mysleep(sec):
    sleep(sec)

def log(msg, isEvt=False, lpad=0):
    if not isinstance(msg, str):
        msg = str(msg)
    print(msg)

#,,f1
def myClickSafe(area, imgName):
    try:
        img=area.find(imgName)
        myClickImg(img)    
    except Exception as e:
        log(e)
        sleep(2)
    except FindFailed as f:
        log(f)
        sleep(2)
        pass    

def myClick(area, imgName):
    img=area.find(imgName)
    myClickImg(img)    

def myClick(area, img):
    m = area.find(img)
    #m.click()
    m.hover()
    #mysleep(0.5)
    times=1
    while times > 0:
        m.mouseDown(Button.LEFT)
        mysleep(.3)
        m.mouseUp(Button.LEFT)
        mysleep(.5)
        times = times - 1
    m = None

def myClickTillGone(area, imgName):
    try:
        cnt=50
        while(cnt > 0):
            # img=area.find(imgName)
            # myClickImg(img)
            myClick(area, imgName)
            SCREEN.hover()
            sleep(.2)
            cnt-=1
            log("myClickTillGone:"+str(cnt))
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


#buyArea=initBuy()

def resetScroll(): 
    cnt=15
    while(cnt>0):
        Mouse.wheel(Button.WHEEL_DOWN, 3)
        #sleep(1)
        cnt-=1

def upScroll(): 
    cnt=15
    while(cnt>0):
        Mouse.wheel(Button.WHEEL_UP, 3)
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

def handleNoStock(area, no_stock_btn):
    try:
        nsArea=noStock(area)
        myClick(buyArea, growgarden_img.imgNoStock)
    except:
        #print("no stock not found")
        pass

def handleEnd(img, msg, scroll_icon):
    if buyBox.exists(img, 0.1):
        # log(msg)
        resetScroll()
        sleep(1)
        SCREEN.hover()

        myClick(buyBox, scroll_icon)
        # click(growgarden_img.scrollIcon)
        # click(growgarden_img.scrollIcon)
        
def handleNoStock2(area):
    nsArea=noStock(area)
    myClick(buyArea, growgarden_img.imgNoStock)


# buyBox=initBuy()
# buyArea=initBuyArea()

def keydown(c):
    # log('kd=' + str(c))
    # type(c)
    keyDown(c)

    mysleep(.1)
    keyUp(c)
    mysleep(.1)

# ,,lib
def myWait(area , imgs, totalWaits, takeshot=False):
    log('myWait()' )
    if area==None:
        area=SCREEN
    waitCount=0
    while not area.exists(imgs):
        waitCount = waitCount + 1
        log('wait ' + str(waitCount))
        if (waitCount > totalWaits):
            if takeshot:
                screenShot(area)
            #log('wait ' + imgs + ' exceeded ' + str(totalWaits), lpad=lpad)
            return False
        sleep(.3)    
    return True    


class SeedShop():
    def __init__(self):
        # self.dialogXOff=670    
        self.dialogXOff=680
        self.dialogWidth=735

    def initBuy(self):
        ub = find(growgarden_img.imgX)
        ub.setX(ub.x - self.dialogXOff)
        ub.setW(self.dialogWidth)
        ub.setH(650)
        ub.highlight(1)
        #hover(growgarden_img.imgX) 
        return ub

    def initBuyArea(self):
        ub = find(growgarden_img.imgX)
        ub.setX(ub.x - self.dialogXOff)
        ub.setY(ub.y + 300)
        
        ub.setW(self.dialogWidth)
        ub.setH(350)
        ub.highlight(1)
        #hover(growgarden_img.imgX) 
        return ub

    # ,,m1
    def scrollFind(self):
        log("--------------seed scrollFind starts---------")
        # click(growgarden_img.scrollIcon)
        myClick(buyBox, growgarden_img.scrollIcon)
        #resetScroll()
        
        cnt=1000
        while(cnt>0):

            #,,x1
            # handleEnd(growgarden_img.imgTomato, "found Tomato")
            handleEnd(growgarden_img.imgCarrot, "found Carrot", growgarden_img.scrollIcon)
            if buyArea.exists(growgarden_img.imgDollar, 0.1):
                #buyArea.click(growgarden_img.imgDollar)
                myClick(buyArea, growgarden_img.imgDollar)

                #buyArea.click(growgarden_img.imgDollar)
                sleep(1)
                #buyArea.click(growgarden_img.imgBuyButton)
                #buyArea.click(growgarden_img.imgBuyButton)
                myClickTillGone(buyArea, growgarden_img.imgBuyButton)
                
                sleep(.5)

            handleNoStock(buyArea, growgarden_img.imgNoStock)
            Mouse.wheel(Button.WHEEL_UP, 1)
            if cnt % 2 == 0:
                keydown("o")
            #sleep(1)
            
            cnt-=1

# ,,pet
class PetShop():
    def __init__(self):
        # self.dialogXOff=670
        # self.dialogWidth=735
        self.dialogXOff=470
        self.dialogWidth=535
        

    def activateDialog(self):
        loc = Location(957 - 50, 594)
        Mouse.move(loc)  # moves mouse
        # click(loc)
        myClickOnly()

    def initBuy(self):
        ub = find(growgarden_img.imgX)
        ub.setX(ub.x - self.dialogXOff)
        ub.setW(self.dialogWidth)
        ub.setH(650)
        ub.highlight(1)
        #hover(growgarden_img.imgX) 
        return ub

    def initBuyArea(self):
        ub = find(growgarden_img.imgX)
        ub.setX(ub.x - self.dialogXOff)
        ub.setY(ub.y + 300)
        
        ub.setW(self.dialogWidth)
        ub.setH(350)
        ub.highlight(1)
        #hover(growgarden_img.imgX) 
        return ub

    # ,,m2
    def scrollFind(self):
        log("--------------scrollFind PETS starts---------")
        # click(growgarden_img.scrollIcon)
        # SCREEN.hover()
        # myClick(buyArea, growgarden_img.scrollIconPet)
        self.activateDialog()
        resetScroll()
        
        cnt=10
        while(cnt>0):

            #handleEnd(growgarden_img.imgCommonEgg, "found common egg, going back", growgarden_img.scrollIconPet)
            if buyBox.exists(growgarden_img.imgDollarPet, 0.1):
                myClick(buyBox, growgarden_img.imgDollarPet)

                sleep(1)


                myClickTillGone(buyArea, growgarden_img.imgBuyButton)
                
                sleep(.5)

            handleNoStock(buyArea, growgarden_img.imgNoStockPet)
            Mouse.wheel(Button.WHEEL_UP, 1)
            sleep(.3)
            cnt-=1

    def main(self):
        print("pet main")
        global buyBox,  buyArea
        buyBox=self.initBuy()
        buyArea=self.initBuyArea()
        # petshop.initBuy()
        print("img version="+str(growgarden_img.varVersion))
        while(True):
            try:
                self.scrollFind()
            except Exception as e:
                log(e)
                sleep(2)
            except FindFailed as f:
                log(f)
                sleep(2)
                pass

#,,gear
class GearShop():
    def __init__(self):
        self.dialogXOff=470
        self.dialogWidth=535
        

    def activateDialog(self):
        loc = Location(957 - 50, 594)
        Mouse.move(loc)  # moves mouse
        # click(loc)
        myClickOnly()

    def initBuy(self):
        ub = find(growgarden_img.imgX)
        ub.setX(ub.x - self.dialogXOff)
        ub.setW(self.dialogWidth)
        ub.setH(650)
        ub.highlight(1)
        #hover(growgarden_img.imgX) 
        return ub

    def initBuyArea(self):
        ub = find(growgarden_img.imgX)
        ub.setX(ub.x - self.dialogXOff)
        ub.setY(ub.y + 300)
        
        ub.setW(self.dialogWidth)
        ub.setH(350)
        ub.highlight(1)
        #hover(growgarden_img.imgX) 
        return ub

    # ,,mg
    def scrollFind(self):
        log("--------------scrollFind GEAR starts---------")
        # click(growgarden_img.scrollIcon)
        # SCREEN.hover()
        # myClick(buyArea, growgarden_img.scrollIconPet)
        self.activateDialog()
        resetScroll()
        
        cnt=10
        while(cnt>0):

            #handleEnd(growgarden_img.imgCommonEgg, "found common egg, going back", growgarden_img.scrollIconPet)
            if buyBox.exists(growgarden_img.imgDollarPet, 0.1):
                myClick(buyBox, growgarden_img.imgDollarPet)

                sleep(1)
                myClickTillGone(buyArea, growgarden_img.imgBuyButton)
                sleep(.5)

            handleNoStock(buyArea, growgarden_img.imgNoStockPet)
            Mouse.wheel(Button.WHEEL_UP, 1)
            sleep(.3)
            cnt-=1

    def main(self):
        print("gear main")
        global buyBox,  buyArea
        buyBox=self.initBuy()
        buyArea=self.initBuyArea()
        # petshop.initBuy()
        print("img version="+str(growgarden_img.varVersion))
        while(True):
            try:
                self.scrollFind()
            except Exception as e:
                log(e)
                sleep(2)
            except FindFailed as f:
                log(f)
                sleep(2)
                pass

class BeanShop():
    def __init__(self):
        self.dialogXOff=670
        self.dialogWidth=735

    def activateDialog(self):
        loc = Location(957, 594)
        Mouse.move(loc)  # moves mouse
        # click(loc)
        myClickOnly()
  
    # ,,m3
    def main(self):
        while(True):
            log("main BEGIN")
            # try:
            upScroll()
            keydown("o")
            keydown("o")
            keydown("e")
            # myClickSafe(SCREEN, growgarden_img.imgSelling)
            # myWait(SCREEN, growgarden_img.imgSelling, 1000)
            self.openShop()
            sleep(2)

            found=myWait(SCREEN , growgarden_img.imgX, 5)
            if not found:
                continue
            
            global buyBox,  buyArea
            buyBox=self.initBuy()
            buyArea=self.initBuyArea()
            scroll_try=10
            while(scroll_try>0):
                try:
                    sf = self.scrollFind()
                    if not sf:
                        break
                except Exception as e:
                    scroll_try-=1
                    log(e)
                    sleep(2)
                except FindFailed as f:
                    scroll_try-=1
                    log(f)
                    sleep(2)
                    pass
            log("Inner loop exit")


            # except Exception as e:
            #     log(e)

            #     log("main error, sleeping for . . .")
            #     sleep(30)

    def initBuy(self):
        ub = find(growgarden_img.imgX)
        ub.setX(ub.x - self.dialogXOff)
        ub.setW(self.dialogWidth)
        ub.setH(650)
        ub.highlight(1)
        #hover(growgarden_img.imgX) 
        return ub

    def initBuyArea(self):
        ub = find(growgarden_img.imgX)
        ub.setX(ub.x - self.dialogXOff)
        ub.setY(ub.y + 300)
        
        ub.setW(self.dialogWidth)
        ub.setH(350)
        ub.highlight(1)
        #hover(growgarden_img.imgX) 
        return ub

    def openShop(self):
        loc = Location(1780, 774)
        Mouse.move(loc)  # moves mouse
        # click(loc)
        myClickOnly()
   
    def scrollFind(self):
        log("--------------scrollFind starts---------")
        # click(growgarden_img.scrollIcon)
        # SCREEN.hover()
        log("scrollIconBean")
        # myClick(buyBox, growgarden_img.scrollIconBean)
        self.activateDialog()
        resetScroll()
        #resetScroll()
        
        # ,,l3
        cnt=17
        while(cnt>0):

            #handleEnd(growgarden_img.imgCommonEgg, "found common egg, going back", growgarden_img.scrollIconPet)
            if buyBox.exists(growgarden_img.imgDollarPet, 0.1):
                myClick(buyBox, growgarden_img.imgDollarPet)

                sleep(1)

                myClickTillGone(buyArea, growgarden_img.imgBuyButton)
                
                sleep(.5)

            handleNoStock(buyArea, growgarden_img.imgNoStockPet)
            sleep(.3)
            cnt-=1

            if exists(growgarden_img.imgX):
                Mouse.wheel(Button.WHEEL_UP, 1)
            else:
                return False
        log("scrollFind exits")
        return True

def main1():
    print("main1")
    print("img version="+str(growgarden_img.varVersion))
    global buyBox,  buyArea
    seed_shop=SeedShop()
    buyBox=seed_shop.initBuy()
    buyArea=seed_shop.initBuyArea()

    while(True):
        try:
            seed_shop.scrollFind()
        except Exception as e:
            log(e)
            sleep(2)
        except FindFailed as f:
            log(f)
            sleep(2)
            pass
            
def main2():
    print("main2")
    global buyBox,  buyArea
    petshop=PetShop()
    petshop.main()
    # buyBox=petshop.initBuy()
    # buyArea=petshop.initBuyArea()
    # # petshop.initBuy()
    # print("img version="+str(growgarden_img.varVersion))
    # while(True):
    #     try:
    #         petshop.scrollFind()
    #     except Exception as e:
    #         log(e)
    #         sleep(2)
    #     except FindFailed as f:
    #         log(f)
    #         sleep(2)
    #         pass

def main3():
    print("main3")
    global buyBox,  buyArea
    eventshop=BeanShop()
    # buyBox=eventshop.initBuy()
    # buyArea=eventshop.initBuyArea()
    # eventshop.initBuy()
    print("img version="+str(growgarden_img.varVersion))
    # while(True):
    #     try:
    #         eventshop.scrollFind()
    #     except Exception as e:
    #         log(e)
    #         sleep(2)
    #     except FindFailed as f:
    #         log(f)
    #         sleep(2)
    #         pass
    eventshop.main()

def main4():
    print("main4")
    print(growgarden_img.varTest)

from org.sikuli.script import Mouse
def mouse_pos():
    sleep(5)
    pos = Mouse.at()
    print("Mouse is at:", pos)      # Example: (x=512, y=384)
    print("X:", pos.getX())
    print("Y:", pos.getY())    

# ('Mouse is at:', L[1558,573]@S(0))
# ('X:', 1558)
# ('Y:', 573)

# ('X:', 1813)
# ('Y:', 556)

def run():
    # mouse_pos()
    #main3()
    main2()


#main1()
#main2()
print("lib loaded")