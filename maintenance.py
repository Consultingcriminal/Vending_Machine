import pymongo

class Maintenance:

    def __init__(self,db):
        self.my_db = db
        self.inventory = self.my_db["Inventory"]
        self.denominations = self.my_db["Denominations"]
        
        
    def view_inventory(self):
        self.items = self.inventory.find()
        print("Name---Quantity")

        for item in self.items:
            print("{} --- {}".format(item["Name"],item["Quantity"]))

    def re_stock(self):
        self.items = self.inventory.find()
        for item in self.items:
            quan = int(input("Enter the Quantity of {} : ".format(item["Name"])))
            quan = self.input_check_cycles(quan,2,item["Name"]) 
            if quan == 0:
                print("Could not update {}".format(item["Name"]))
            else:    
                self.inventory.update_one(
                    {"Name":item["Name"]},
                    {"$set":{"Quantity":quan}})

                print("Item = {} updated".format(item["Name"]))

    def add_drink(self):

        ## Add The Feature of asking How Many Drinks in the common function
        a = input("Enter the name of Drink : ")
        b = int(input("Enter the price : "))
        c = int(input("Enter the Quantity : "))

        item = {"Name":a , "Price":b , "Quantity":c}
        self.inventory.insert_one(item)

    def add_denomination(self):

        a = int(input("Enter the denomination : "))
        b = int(input("Enter Quantity : "))

        deno = {"Deno":a , "Quan":b}
        self.denominations.insert_one(deno)

    def refresh_change(self):
        self.deno_list = self.denominations.find()
        for item in self.deno_list:
            quan = int(input("Enter the Quantity of {} : ".format(item["Deno"])))
            quan = self.input_check_cycles(quan,2,item["Deno"]) 
            
            if quan == 0:
                print("Could not update {}".format(item["Deno"]))
            
            else:    
                quan = quan + item["Quan"]
                self.denominations.update_one(
                    {"Deno":item["Deno"]},
                    {"$set":{"Quan":quan}})
                print("Item = {} updated".format(item["Deno"]))    
              
    @staticmethod
    def check_input(a):
        if a>0:
            return True
        return False

    def input_check_cycles(self,ip,cycles,i_name):
        flag = False
        count = 0

        while count < cycles:
            if self.check_input(ip) == True:
                flag = True
                return ip
            else:
                count = count + 1
                ip = int(input("Enter the Appropriate Quantity of {} : ".format(i_name))) 
        
        if flag is False:
            return 0

## Add a single function for running maintenance    
class run_maintenance:

    def __init__(self,mydb):
        self.mydb = mydb
    
    def run(self):
        choice = -1
        m = Maintenance(self.mydb)

        while choice == -1:
            
            print("Welcome to Maintenance Mode!!!!")
            print("1. View_Inventory")
            print("2. Re_Stock")
            print("3. Refresh_Change")
            print("4. Add_drink")
            print("5. Add Denomination")

            n = int(input("Enter your choice..."))

            if n==1:
                m.view_inventory()
            elif n==2:
                m.re_stock()
            elif n==3:
                m.refresh_change()
            elif n==4:
                m.add_drink()
            elif n==5:
                m.add_denomination()
            else:
                print("Invalid Input")

            choice = int(input("Enter -1 for continuing = "))

        print("Exiting ... Thank You....")        

                        
if __name__ == '__main__':

    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    mydb = client['Vending_Machine']
    rm = run_maintenance(mydb)
    rm.run()


    
