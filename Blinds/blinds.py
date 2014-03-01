import time
from __init__ import *  
import math

class General_Blind():
    
    def __init__(self, ):
        pass

    def set_relays(self,):
        for rel in self.relay:
            rel.write(1)
            pass
    
    def move(self, direction):

        self.relay[direction].write(0)
        time.sleep(self.rel_time)
        self.relay[direction].write(1)

class Single_Blind(General_Blind):

    def __init__(self, name, relay_pins, cycle_time, wake_sched):

        self.name       =   name
        self.relay      =   relay_pins
        self.set_relays()
        self.wake_sched =   wake_sched

        self.position   =   0 
        self.rel_time   =   1
        self.cycle_time =   cycle_time

    def set_blind(self, end_position):

        end_position = float(end_position)
        if end_position < 0 or end_position > 1:
            raise Exception("position must be set between 0 and 1")
       
        else:
            work_time = self.cycle_time*(float((math.fabs(end_position-self.position))))

            if end_position > self.position:                
                self.move(1)
                time.sleep(work_time-self.rel_time)
                self.move(0)
                print "Blind {0} open in {1}%".format(self.name, end_position*100) 
            if end_position < self.position:               
                self.move(0)
                time.sleep(work_time-self.rel_time)
                self.move(1)
                print "Blind {0} open in {1}%".format(self.name, end_position*100) 
                     
            self.position   =   end_position

class Multiple_Blind(General_Blind):

    def __init__(self, name, relay_pins, cycle_time, wake_sched, single_blinds):

        self.name       =   name
        self.relay      =   relay_pins
        self.set_relays()
        self.wake_sched =   wake_sched
        self.single_blinds = single_blinds

        self.position   =   0 
        self.rel_time   =   2
        self.cycle_time =   cycle_time

    def set_blind(self, end_position):

        try:
            end_position = int(end_position)
        except ValueError:
            if end_position == 'r':
                self.untight()
                return

        if end_position < 0 or end_position > 1:
                
                raise Exception("you set {0} position. Position must be set between 0 and 1".format(end_position))
        
        else:
            if end_position > 0:
                end_position = 1
            
            self.move(end_position)
            if end_position == 0:
                print "All blinds closed"
            if end_position == 1:
                print "All blinds opened"

            self.position = end_position

            for blind in self.single_blinds.values():
                blind.position = end_position

    def untight(self,):

        untight_level = 5
        self.set_blind(DOWN)
        time.sleep(30)
        self.move(1)
        time.sleep(untight_level-self.rel_time)
        self.move(0)

        for blind in self.single_blinds.values():            
            blind.position = (untight_level*self.rel_time)/blind.cycle_time
            print "blind {0} position {1}".format(blind.name, blind.position)