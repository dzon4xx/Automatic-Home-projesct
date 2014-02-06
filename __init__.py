import pyfirmata
from sys import platform as _platform

if _platform == "linux" or _platform == "linux2":
    PORT    = '/dev/ttyACM0'
if _platform == "win32":
    PORT    = 'COM25'
UP      = 1
DOWN    = 0

DAY     = 1
NIGHT   = 0

HIGH    = 1
LOW     = 0

board = pyfirmata.Arduino(PORT)

it = pyfirmata.util.Iterator(board)
it.start()
 
test_pin   =  board.get_pin('a:0:i')             # A0 Input      (LM35)

print "conecting to arduino"     
while test_pin.read() is None:
    pass 

print "arduino ready"

   