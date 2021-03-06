import pyfirmata

#Constants
PORT    = 'COM25'
UP      = 1
DOWN    = 0

DAY     = 1
NIGHT   = 0

HIGH    = 1
LOW     = 0

board = pyfirmata.Arduino(PORT)
# start an iterator thread so that serial buffer doesn't overflow
it = pyfirmata.util.Iterator(board)
it.start()
 
test_pin   =  board.get_pin('a:0:i')             # A0 Input      (LM35)
                
while test_pin.read() is None:
    pass 

   