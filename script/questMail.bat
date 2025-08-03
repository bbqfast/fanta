call skull.bat
set sub=0
if not (%1)==() set sub=%1

rem mailsend -to bb9now@gmail.com -from bb9now@gmail.com -ssl -port 465 -auth -smtp smtp.gmail.com -sub fantastat%sub% +cc +bc -v -user "bb9now@gmail.com" -pass %myname% -attach "C:\Skull\TrainLog.txt" 
rem mailsend -to bb9now@gmail.com -from bb9now@gmail.com -ssl -port 465 -auth -smtp smtp.gmail.com -sub fantastat-%sub% +cc +bc -v -user "bb9now@gmail.com" -pass %myname% -attach "C:\Skull\mail.png" -attach "C:\Skull\TrainLog.txt"
tail -n 1500 C:\Skull\TrainLog.txt > C:\Skull\ShortLog.txt
mailsend -to bb9now@gmail.com -from bb9now@gmail.com -ssl -port 465 -auth -smtp smtp.gmail.com -sub fantastat-%sub% +cc +bc -v -user "bb9now@gmail.com" -pass %myname% -attach "C:\Skull\mail.png" -attach "C:\Skull\ShortLog.txt" -attach "C:\Skull\TrainLog.txt"
 