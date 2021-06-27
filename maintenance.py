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

            # Add A Checking Module

            if item["Available"] == "A":
                quan = quan + item["Quantity"]
                self.inventory.update_one(
                    {"Name":item["Name"]},
                    {"$set":{"Quantity":quan}})
            
            else:
                self.inventory.update_one(
                    {"Name":item["Name"]},
                    {"$set":{"Quantity":quan,"Available":"A"}})

    def add_drink(self):

        ## Add The Feature of asking How Many Drinks in the common function
        a = input("Enter the name of Drink : ")
        b = int(input("Enter the price : "))
        c = int(input("Enter the Quantity : "))

        item = {"Name":a , "Price":b , "Quantity":c , "Available":"A"}
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

            # Add A Checking Module
            quan = quan + item["Quan"]
            self.denominations.update_one(
                {"Deno":item["Deno"]},
                {"$set":{"Quan":quan}})
              

    ## Add a single function for running maintenance    

if __name__ == '__main__':

    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    mydb = client['Vending_Machine']
    
    m = Maintenance(mydb)
    #m.view_inventory()
    #m.re_stock()
    #m.add_drink()
    #m.add_denomination()  
    m.refresh_change()



    
