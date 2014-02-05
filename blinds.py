from astral import Astral
import datetime
import serial
import time
import copy
import math
import threading

from __init__ import *        

class Sun():

    def __init__(self,):
        a = Astral()
        self.location = a['Warsaw']
        
    def get_sunset(self, d):
        sun = self.location.sun(local=True, date=d)    
        #print('Sunset:    s', sun['sunset'])
        return sun['sunset']

    def get_sunrise(self, d):
        sun = self.location.sun(local=True, date=d)
        #print('Sunrise:    ',  sun['sunrise'])
        return sun['sunrise']

class Daytime():

    def __init__(self, sun):

        self.prev_day_time  = None
        self.day_time       = NIGHT # 0 night  1 day

        self.sun        = sun

    def check(self, blind):

        dtime       =   datetime.datetime.today()      
        date        =   datetime.date.today()

        wake_time           =   self.get_wake_time(date, blind)
        wake_time_tomorrow  =   self.get_wake_time(date + datetime.timedelta(days=1), blind)
        sunset              =   sun.get_sunset(date)
        sunset              =   sunset.replace(tzinfo=None)

        sunrise             =   sun.get_sunrise(date) 
        sunrise             =   sunrise.replace(tzinfo=None)

        sunrise_tommorow     =   sun.get_sunrise(date + datetime.timedelta(days=1))
        sunrise_tommorow     =   sunrise_tommorow.replace(tzinfo=None)

        sunset_yesterday     =   sun.get_sunset(date - datetime.timedelta(days=1)) 
        sunset_yesterday     =   sunset_yesterday .replace(tzinfo=None)


        #print "name: {3} \t time: {0} \t wake_time \t {1} \t sunset: {2}".format(dtime, wake_time, sunset, blind.name )

        if dtime > wake_time and dtime < sunset:  # If daylight
 
            blind.day_time  = DAY
            if blind.day_time != blind.prev_day_time:
                move = threading.Thread(target = blind.move, args=( UP, ))
                move.start()

                blind.prev_day_time = copy.copy(blind.day_time)
    
        night_evening = dtime > sunset and dtime < wake_time_tomorrow
        night_morning = dtime < wake_time and dtime > sunset_yesterday 

        if night_evening or night_morning: 
                  
            blind.day_time  = NIGHT
            if blind.day_time != blind.prev_day_time:

                move = threading.Thread(target = blind.move, args=( DOWN, ))
                move.start()
                blind.prev_day_time = copy.copy(blind.day_time)

        return str(self.day_time )
                               
    def get_wake_time(self, date, blind): 
        wd_hour =   blind.wake_time[0]
        wd_min  =   blind.wake_time[1]
        hd_hour =   blind.wake_time[2]
        hd_min  =   blind.wake_time[3]
        if date.weekday() in range(0, 4):
            return datetime.datetime(date.year, date.month, date.day, wd_hour, wd_min )
        else:
            return datetime.datetime(date.year, date.month, date.day, hd_hour, hd_min)
                            
class Blind():
    
    def __init__(self, name, relay_pins, wake_time):
        
        self.name       =   name
        self.relay      =   relay_pins
        for rel in self.relay:
            rel.write(1) 
        self.wake_time  =   wake_time

        self.prev_day_time  = None
        self.day_time       =   DAY

        self.position   =   0 
        self.rel_time   =   1.5
        self.cycle_time =   20
        

    def set_blind(self, end_position):
       
        end_position = int(end_position)

        if end_position < 0 or end_position > 100 or self.position==end_position:
            raise Exception("position must be set between 0 and 100")

        work_time = self.cycle_time*(float((math.fabs(end_position-self.position)))/100)

        print "work_time: ", work_time

        if end_position > self.position:
            print "Blind is opening"
            self.move(1)
            board.pass_time(work_time-self.rel_time)
            self.move(0) 
        if end_position < self.position:
            print "Blind is closing"
            self.move(0)
            board.pass_time(work_time-self.rel_time)
            self.move(1) 
                     
        self.position   =   end_position

    def move(self, direction,):

        print "Blind: {0} moving {1}".format(self.name, direction)
        self.relay[direction].write(0)
        board.pass_time(self.rel_time)
        self.relay [direction].write(1)  

       
sun = Sun()
daytime = Daytime(sun)

#blind1 = Blind("JASIO",  [board.get_pin('d:2:o'), board.get_pin('d:3:o')], [6, 45, 8, 30])
blind2 = Blind("PIOTR", [board.get_pin('d:4:o'), board.get_pin('d:5:o')], [7, 00, 8, 35])
blind3 = Blind("MAIN", [board.get_pin('d:6:o'), board.get_pin('d:7:o')], [7, 05, 8, 40])

blinds = [blind2, blind3]
#blind1.set_blind(30)


while True:
    for blind in blinds:
        daytime.check(blind)

    time.sleep(1)