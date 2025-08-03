call skull.bat
set sub=0
if not (%1)==() set sub=%1

mailsend -to bb9now@gmail.com -from bb9now@gmail.com -ssl -port 465 -auth -smtp smtp.gmail.com -sub fantabeat-%sub% +cc +bc -v -user "bb9now@gmail.com" -pass %myname% -M messagebody
 