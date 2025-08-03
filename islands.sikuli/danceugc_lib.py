from sikuli import *
import math
import datetime
import shutil
import time
start = time.time()


#Settings.MoveMouseDelay = 0


imgClose="1685154294825.png"

imgPt1="1715222717493.png"

imgPt2="1715222731411.png"


imgPt3="1715222773786.png"

imgPt4="1715222783545.png"

imgSp="1715609179670.png"


imgSpin1="1715707979681.png"

imgSpin2="1715708005611.png"

imgFr1="1716238655779.png"

imgFr2="1716238667046.png"

imgFr3="1716238695325.png"
existsTimeout=0.5


imgList=[imgPt4,imgPt1,imgPt2,imgPt3,imgSp,imgFr1,imgFr2]
#imgList=[imgSpin1,imgSpin2]
#imgList=[imgSp]
gsleep=20
cnt=0

def log(msg, isEvt=False, lpad=0):
    if not isinstance(msg, str):
        msg = str(msg)
    print(msg)

def clickWithCatchScn(img2):
   clickWithCatch(SCREEN, img2) 

def clickWithCatch(game, img2):
    global cnt
    try:
        #if exists(imgPlay):
        game.click(img2)
        print("clickWithCatch " + img2)
        cnt+=1
        log("FOUND " + str(cnt))
    except Exception as e:
        #log(e)
        pass
    except FindFailed as f:
        #log(f)
        pass


#click(imgPt1)

while True:
    for im in imgList:
        clickWithCatchScn(im)
    sleep(gsleep)


    

    