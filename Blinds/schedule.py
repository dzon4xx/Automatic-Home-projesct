from astral import Astral
import logging
import datetime
from apscheduler.scheduler import Scheduler

from dateutil import easter
from dateutil.relativedelta import *

class Sun():

    a = Astral()
    global location 
    location = a['Warsaw']
        
    def get_sunset(self, d):
        
       

        sun =location.sun(local=True, date=d)    
        return sun['dusk']

    def get_sunrise(self, d):

        sun = location.sun(local=True, date=d)
        return sun['sunrise']

class My_Scheduler(Sun):
    
    def __init__ (self):
        
        logging.basicConfig()
        self.sched  =   Scheduler()               
        self.sched.start()

    def blind_tasks(self, blinds):
        today = datetime.date.today()
        blind_daily_tasks = []
        
        for blind in blinds.values():

            for wake_time, open_level in self.get_plan(today, blind):
                
                if wake_time == 's':
          
                    down_time = self.get_sunset(today)
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
        
        holiday = self.check_holiday(date)

        if holiday:
            plans = blind.wake_sched[6]
            return plans.iteritems()
         
        else:
            weekday = date.weekday()
            plans = blind.wake_sched[weekday]
         
            return plans.iteritems() 
                                         

 
    def check_holiday(self, date):
        
        year = date.year
        easter_sunday = easter.easter(year)
        holidays = {'New Year': datetime.date(year,1,1),
                    'Trzech Kroli': datetime.date(year,1,6),
                    'Easter Sunday': easter_sunday,
                    'Easter Monday': easter_sunday + datetime.timedelta(days=1),
                    'Labor Day': datetime.date(year,5,1),
                    'Constitution Day': datetime.date(year,5,3),
                    # 7th Sunday after Easter
                    # (notice days+1 - this is 7th Sunday excluding Easter Sunday
                    'Pentecost Sunday': easter_sunday + relativedelta(days=+1, weekday=SU(+7)),
                    # 9th Thursday after Easter
                    'Corpus Christi': easter_sunday + relativedelta(weekday=TH(+9)),
                    'Assumption of the Blessed Virgin Mary': datetime.date(year,8,15),
                    'All Saints\' Day': datetime.date(year,11,1),
                    'Independence Day': datetime.date(year,11,11),
                    'Christmas  Day': datetime.date(year, 12, 25),
                    'Boxing Day': datetime.date(year, 12, 26),
                    }

        if date in holidays.itervalues():
            print "Today is Holiday"
            return True
        else:
            return False
 
