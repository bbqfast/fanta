from sikuli.Sikuli import *
import sys
import datetime
import shutil
import traceback
import time
import os
from cStringIO import StringIO

myScriptPath = "c:\\fanta\\islands.sikuli"

# all systems
if not myScriptPath in sys.path: sys.path.append(myScriptPath)

import islands
reload(islands)
from islands import islands


