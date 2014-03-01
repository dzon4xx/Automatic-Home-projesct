import u3
from LabJackPython import * 

d = u3.U3()

AddRequest (d.handle, LJ_ioPUT_DIGITAL_BIT, 4, 1, 0, 0)
GoOne( d.handle )