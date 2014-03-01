import random
import time 
import threading

from collections import namedtuple
from datetime import datetime
from copy import deepcopy
from labjack import LabJack

from database import database_client 

print database_client
from __init__ import *

d = LabJack()

class Pulse_gen():

    def __init__(self, name, port, period):
        
        self.name           =   name
        self.pulse_port     =   port
        self.time_base      =   float(1000)
        self.period_length  =   period*self.time_base
        self.pulse_length   =   float(90)

        self.prev_pulse_count   =   0
        self.pulse_count        =   0

    def generate_pulse( self, ):
        
        while True:

            time_before_pulse   =   random.randint(0, self.period_length-self.pulse_length)        
            off_time0   =   (time_before_pulse/self.time_base)
            on_time     =   self.pulse_length/self.time_base
            off_time1   =   self.period_length/self.time_base - on_time - off_time0

            time.sleep( off_time0 )
            d.set_DO(self.pulse_port , True)
            time.sleep( on_time )
            d.set_DO(self.pulse_port , False)
            time.sleep(off_time1)

            self.pulse_count    =   self.pulse_count + 1

    def get_power(self, ):
        power = (self.pulse_count - self.prev_pulse_count)/(3.6*interval)
        self.prev_pulse_count   =   deepcopy(self.pulse_count)
        return power

class Pulse_count():
    
    def __init__(self, name, port,):
        
        self.name   = name
        self.count_pin      = board.get_pin('d:%s:i'%port)
        self.prev_pulse_count = 0 
        self.pulse_count = 0
       
    def count(self,):

        state0 = 0
        while True:

            state1 = self.count_pin.read()
            
            if state1 != state0 and state1 == 1:
                self.pulse_count = self.pulse_count + 1
            
            state0 = deepcopy(state1)

    def get_power(self, ):
        power = (self.pulse_count - self.prev_pulse_count)/(3,6*interval)
        self.prev_pulse_count   =   deepcopy(self.pulse_count)
        return power



class Data_reader():
    
    def __init__(self,):
        self.energy_meters_names    = ['CALOSC', 'KUCHNIA','DOM_LEWY', 'DOM_PRAWY',]                  
        self.count_ports            = [ '6',       '7',       ' 8',              9,]
        self.gen_ports              = [  4,          5,         6,               7,]
        self.periods                = [  1,        1,         1,                 1,]

class Simulation_creator():

    def __init__(self,    ):

        pass

    def start_pulse_gen_and_count(self, energy_meters_names, arduino_ports, pulse_gen_ports, periods,):

        energy_meters = {}
        gen_and_meters = namedtuple('ports', 'gen meter')
        for (arduino_port, pulse_gen_port, name, period) in zip(arduino_ports, pulse_gen_ports, energy_meters_names, periods ):
    
            pulse_gen   =  Pulse_gen(name, pulse_gen_port, period)
            #pulse_count =  Pulse_count(name, arduino_port)

            generation = threading.Thread(target = pulse_gen.generate_pulse, args = ())
            #counting   = threading.Thread(target = pulse_count.count, args = ())

            generation.start()
            #counting.start()

            #energy_meters[name] = gen_and_meters(pulse_gen , pulse_count)
            energy_meters[name] = gen_and_meters(pulse_gen , None)

        return energy_meters

class Count_server():

    def __init__(self):

        self.client =   database_client.Client()
        self.id     =   0
        

    def run(self,):
        self.client.reset_table('energy_consumption')
        while True:
            print "debug"
            try:
                time_stamp = datetime.now()

                meters_data = {}
                for name, gen_and_meter in energy_meters.iteritems():
                    
                        power = gen_and_meter.gen.get_power()
                        meters_data[name] = round(power,3)
                        #print "Name: {0} real pulse num: {1} \t measured pulse num {2}".format(name, gen_and_meter.gen.pulse_count, gen_and_meter.meter.pulse_count)
               
                self.client.update_database(self.id, time_stamp, meters_data)
                self.id += 1
                time.sleep(interval)
                print self.id, time_stamp, meters_data
            except KeyboardInterrupt:
                self.client.db.close()

d_r = Data_reader()
simulation  = Simulation_creator()

energy_meters = simulation.start_pulse_gen_and_count(d_r.energy_meters_names, d_r.count_ports, d_r.gen_ports, d_r.periods)

server = Count_server()
server.run()

print "Finish"

    
        



