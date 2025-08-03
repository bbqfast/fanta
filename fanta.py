import os
os.system("su")
os.rename("/sdcard/Android/data/com.mobage.ww.a793.fanta_test_Android","/sdcard/Android/data/4com.mobage.ww.a793.fanta_test_Android")


import os
os.rename("/sdcard/Android/data/4com.mobage.ww.a793.fanta_test_Android","/sdcard/Android/data/com.mobage.ww.a793.fanta_test_Android")



#qpy:qpyapp
import os
os.rename("/sdcard/Android/data/com.mobage.ww.a793.fanta_test_Android","/sdcard/Android/data/4com.mobage.ww.a793.fanta_test_Android")
print('renamed')
os.system("adb uninstall com.mobage.ww.a793.fanta_test_Android")
print('uninstalled')
os.system("adb install '/sdcard/Android/com.mobage.ww.a793.fanta_test_Android-1.apk'")
print('installed')
os.rename("/sdcard/Android/data/4com.mobage.ww.a793.fanta_test_Android","/sdcard/Android/data/com.mobage.ww.a793.fanta_test_Android")



print('rename back')
os.system("adb shell monkey -p com.mobage.ww.a793.fanta_test_Android -v 500")
print('launch')













# shell commands

# mv '/sdcard/Android/data/com.mobage.ww.a793.fanta_test_Android' '/sdcard/Android/data/51com.mobage.ww.a793.fanta_test_Android'
# am start -n com.mobage.ww.a793.fanta_test_Android
# adb shell "cmd package resolve-activity --brief om.mobage.ww.a793.fanta_test_Android | tail -n 1"
# adb shell "monkey -p com.mobage.ww.a793.fanta_test_Android -v 500"
# adb shell monkey -p com.mobage.ww.a793.fanta_test_Android -v 500

