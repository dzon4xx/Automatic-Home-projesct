import sqlite3


class Client():

    def __init__(self, ):
        self.db = sqlite3.connect('database/automatic_home', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self.cursor = self.db.cursor()
        print self.db

    def reset_table(self, name):
        
        drop = '''DROP TABLE {0}'''.format(name)
        create = ''' CREATE TABLE {0}(id INTEGER PRIMARY KEY, time_stamp DATETIME, CALOSC REAL, KUCHNIA REAL, DOM_LEWY REAL, DOM_PRAWY REAL )  '''.format(name)

        self.cursor.execute(drop)                                                                                      
        self.cursor.execute(create)
        self.db.commit()


    def update_database(self, id, time_stamp, meters_data):
        
        entry_data = [(id, time_stamp, meters_data['CALOSC'], meters_data['KUCHNIA'], meters_data['DOM_LEWY'], meters_data['DOM_PRAWY']),]
        print entry_data
        try:
            self.cursor.executemany('''INSERT INTO energy_consumption(id, time_stamp, CALOSC, KUCHNIA, DOM_LEWY, DOM_PRAWY) VALUES(?,?,?,?,?,?)''', entry_data)
            self.db.commit()
        except Exception as e:
            print e
            self.db.rollback()
        