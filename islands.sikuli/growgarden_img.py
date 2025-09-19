from sikuli import *
import math
import datetime
import shutil
import time
start = time.time()
from org.sikuli.script import Mouse, Button


script_dir = os.path.dirname(getBundlePath())
if script_dir not in sys.path:
    sys.path.append(script_dir)

#import growgarden_lib
#reload(growgarden_lib)

imgNewSeed="1753042461899.png"

imgNewSeed="1753042784116.png"


evtFriend="1756354659438.png"

evtMain="1756354669531.png"

imgX="1753044403206.png"

imgSelling="1756307136736.png"

imgSelling="1756307121690.png"

imgMaster="1757218587418.png"
imgHarvest="1757218632771.png"
imgGodly="1757218927025.png"

scrollIcon="1753046357389.png"

scrollIconPet="1755139169719.png"


scrollIconBean="1756283415812.png"

imgDollar="1753046475585.png"
imgDollarPet="1755141539648.png"

imgBuyButton="1753048077186.png"

imgBuyButton="1753938975907.png"
imgBuyButton="1753954585860.png"

imgBuyButton="1753954694432.png"
imgNoStockBtn="1753061385485.png"


imgNoStock="1753062484265.png"
imgNoStockPet="1755138109728.png"

imgCarrot="1753066188628.png"
imgOrange="1753066583746.png"

imgTomato="1753067557291.png"

imgCommonEgg="1755137140024.png"

varTest="img"
varVersion=11
#main2()
#growgarden_lib.main1()
#handleNoStock(buyArea)

print("img loaded")