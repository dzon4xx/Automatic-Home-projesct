import os
from __init__ import *

class Init_data_reader():
    
    def __init__ (self, ):

        self.files_change_time = {name: 0 for name in files_dir.keys()}
           
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
                    open_level = task[1]
                    day_plan[time] = open_level
                wake_plan[blind_name].append(day_plan)

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




        

