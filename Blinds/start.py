
import datetime
import copy


from __init__ import *
from file_reader import *
from blinds import *
  
from schedule import *

class Start():

    def __init__(self,):
                     
        init_data_reader = Init_data_reader()
        self.my_sched = My_Scheduler()

        wake_plan   = init_data_reader.read_wake_plan(files_dir['schedule'])
        cycle_times = init_data_reader.read_cycle_time(files_dir['cycle_times'])
        relays      = init_data_reader.read_pin_map(files_dir['pins_map'])

        single_blinds = {blind_name:Single_Blind(blind_name, relays[blind_name], cycle_times[blind_name], plan) for blind_name, plan in wake_plan.iteritems() if blind_name not in ("MAIN")}
        multiple_blinds  =   {"MAIN" : Multiple_Blind("MAIN", relays["MAIN"], cycle_times["MAIN"], wake_plan["MAIN"], single_blinds)} 
        self.blinds = dict(single_blinds.items() + multiple_blinds.items())
                            
    def loop(self,):        
        check_file_interval = 5

        today = datetime.datetime.today()
        yesterday = None
        while True:
            today = datetime.date.today()

            if today != yesterday:
                print "\n\ntoday {0} yesterday {1}".format(today, yesterday)
                yesterday = copy.copy(today)        
                self.my_sched.blind_tasks(self.blinds)

            time.sleep(1)
    
start = Start()
start.loop()
    