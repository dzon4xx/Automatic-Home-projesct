import pyfirmata
from sys import platform as _platform

interval =   3

if _platform == "win32":
    PORT    = 'COM25'



#board  = pyfirmata.Arduino(PORT)
#it = pyfirmata.util.Iterator(board)
#it.start() 
#test_pin   =  board.get_pin('a:0:i')             # A0 Input      (LM35)

#print "conecting to arduino"     
#while test_pin.read() is None:
#    pass 
#print "arduino ready"

