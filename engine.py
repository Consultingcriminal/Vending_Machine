from maintenance import run_maintenance
from client import run_client
import pymongo

class Engine:

    def __init__(self,mydb):
        self.mydb = mydb

    def run(self):
        choice = -1
        
        while choice == -1:
            print("1. Vending Mode ")
            print("2. Maintenance Mode ")
        
            n = int(input("Enter your choice..."))

            if n == 1:
                rc =run_client(self.mydb)
                rc.run()

            elif n == 2:
                rm = run_maintenance(self.mydb)
                rm.run()

            choice = int(input("Enter -1 for continuing = "))        
            

        print("Exiting ... Thank You....")  

if __name__ == '__main__':

    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    mydb = client['Vending_Machine']
    e = Engine(mydb)
    e.run()
    