import pymongo

class Maintenance:

    def __init__(self,db):
        self.my_db = db
        self.inventory = self.my_db["Inventory"]
        

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
        a = input("Enter the name of Drink : ")
        b = int(input("Enter the price : "))
        c = int(input("Enter the Quantity : "))

        item = {"Name":a , "Price":b , "Quantity":c , "Available":"A"}
        self.inventory.insert_one(item)

if __name__ == '__main__':

    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    mydb = client['Vending_Machine']
    
    m = Maintenance(mydb)
    m.view_inventory()
    m.re_stock()   
    
