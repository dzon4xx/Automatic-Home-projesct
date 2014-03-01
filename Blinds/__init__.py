import pyfirmata
from sys import platform as _platform

if _platform == "linux" or _platform == "linux2":
    PORT    = '/dev/ttyACM1'
    slash = '/'
if _platform == "win32":
    PORT    = 'COM27'
    slash = '\\'
UP      = 1
DOWN    = 0

DAY     = 1
NIGHT   = 0

HIGH    = 1
LOW     = 0


files_dir = {'schedule':"settings_files{0}schedule.txt".format(slash),
             'cycle_times': "settings_files{0}cycle_time.txt".format(slash),
             'pins_map': "settings_files{0}pins_map.txt".format(slash),}

board = pyfirmata.Arduino(PORT)

it = pyfirmata.util.Iterator(board)
it.start()
 
test_pin   =  board.get_pin('a:0:i')             # A0 Input      (LM35)

print "conecting to arduino"     
while test_pin.read() is None:
    pass 
print "arduino ready"

   