from astral import Astral
import datetime
import copy

import logging
from apscheduler.scheduler import Scheduler
from blinds import *
from __init__ import *  

      

class Sun():

    def __init__(self,):

        a = Astral()
        self.location = a['Warsaw']
        
    def get_sunset(self, d):

        sun = self.location.sun(local=True, date=d)    
        return sun['sunset']

    def get_sunrise(self, d):

        sun = self.location.sun(local=True, date=d)
        return sun['sunrise']

class My_Scheduler():
    
    def __init__ (self, sun):
        
        self.sun    =   sun
        logging.basicConfig()
        self.sched  =   Scheduler()               
        self.sched.start()

    def blind_tasks(self, blinds):
        today = datetime.date.today()
        blind_daily_tasks = []
        
        for blind in blinds.values():

            for wake_time, open_level in self.get_plan(today, blind):
                
                if wake_time == 's':
                    down_time = sun.get_sunset(today)
                    down_time = down_time.replace(tzinfo=None)
                    task_time = down_time

                else:
                    wake_time = wake_time.split(":")
                    hour = int(wake_time[0])
                    min = int(wake_time[1])
                    task_time = datetime.datetime(today.year, today.month, today.day, hour, min)

                
                try:
                    self.sched.add_date_job(blind.set_blind, task_time, [open_level] )
                    print "blind_name: {0} task time: {1} open_level {2}".format(blind.name, task_time, open_level)
                except ValueError as e:
                    print "task not add because of error: ", e 
                      
    def get_plan(self, date, blind): 
        
        weekday = date.weekday()
        plans = blind.wake_sched[weekday]
         
        return plans.iteritems() 
                                         
class Init_data_reader():
    
    def __init__ (self, ):
        pass
           
    def open_file(self,file_name, mode= 'r'):
   
        try:       
            file_handle     = open(file_name, mode)
            return (file_handle)

        except IOError: 
            print "Configuration file: {0} not found press any button to exit".format(file_name)
            exit = raw_input()
            sys.exit( 0 )

    def read_wake_plan(self, file_name):

        file_handle = self.open_file(file_name)
        wake_plan = {}
        line = ""
        blind_name = ""
        for line in file_handle:

            line = line.strip('\t\n\r')
            line = line.split('\t')
            
            if line[0] == '#':
                continue
            if line[0] == '~':
                blind_name = line[1]
                wake_plan[blind_name] = []
                continue

            else:
                day_plan = {}
                for task in line[1:]:                    
                    task = task.split('-')
                    time = task[0]
                    open_level = float(task[1])
                    day_plan[time] = open_level
                wake_plan[blind_name].append(day_plan)
        print wake_plan
        return wake_plan

    def read_cycle_time(self, file_name):
        
        file_handle = self.open_file(file_name)
        cycle_times = {}
        for line in file_handle:

            line = line.strip('\n\t\r')
            line = line.split('\t')
            blind_name = line[0]

            try:
                cycle_time = float(line[1])
            except ValueError:
                cycle_time = None

            cycle_times[blind_name] = cycle_time

        return cycle_times

    def read_pin_map(self, file_name):

        file_handle = self.open_file(file_name)

        all_relays = {}
        blind_name = ""
        relays = []
        for line in file_handle:
            line = line.strip('\n\t\r')
            line = line.split('\t')

            if line[0] == '~':               
                blind_name = line[1]
                continue

            if line[0] == '$':
                all_relays[blind_name] = relays
                relays = []                
                continue

            if line[0] == '':
                continue

            else:
                pin_number = line[0]
                type       = line[1]
                IO         = line[2]
                relay_data = ':'.join(type+pin_number+IO)

                relays.append(board.get_pin(relay_data))

        return all_relays

                
init_data_reader = Init_data_reader()

wake_plan   = init_data_reader.read_wake_plan("schedule.txt")
cycle_times = init_data_reader.read_cycle_time("cycle_time.txt")
relays      = init_data_reader.read_pin_map("pins_map.txt")

single_blinds = {blind_name:Single_Blind(blind_name, relays[blind_name], cycle_times[blind_name], plan) for blind_name, plan in wake_plan.iteritems() if blind_name not in ("MAIN")}
multiple_blinds  =   {"MAIN" : Multiple_Blind("MAIN", relays["MAIN"], cycle_times["MAIN"], wake_plan["MAIN"], single_blinds)} 
blinds = dict(single_blinds.items() + multiple_blinds.items()) 
       
sun = Sun()
my_sched = My_Scheduler( sun )


today = datetime.datetime.today()
yesterday = None
while True:
    today = datetime.date.today()

    if today != yesterday:
        print "today {0} yesterday {1}".format(today, yesterday)
        yesterday = copy.copy(today)        
        my_sched.blind_tasks(blinds)

    time.sleep(1)
    

    