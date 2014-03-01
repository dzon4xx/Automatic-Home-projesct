import u3, ue9
from LabJackPython import *   
from threading import Lock
   
try:
    d = ue9.UE9()
    labjack_class = ue9.UE9
    d.close()
except:

    d = u3.U3()
    labjack_class = u3.U3
    d.close()

class LabJack(labjack_class):

        def __init__(self, ):
            self.d = labjack_class()
            
 
        def read_AIN(self, port):

            AddRequest (self.d.handle, LJ_ioGET_AIN, port, 0, 0, 0);
            GoOne( self.d.handle )
            result = GetFirstResult(self.d.handle)
            return result[2]

        def set_DO(self, port, state):
            lock = Lock()            
            lock.acquire()
            AddRequest (self.d.handle, LJ_ioPUT_DIGITAL_BIT, port, state, 0, 0)
            GoOne( self.d.handle )
            lock.release()


