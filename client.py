import pymongo

class Vending_Machine:

    def __init__(self,db):
        self.my_db = db
        self.inventory = self.my_db["Inventory"]
        self.denominations = self.my_db["Denominations"]

    def vend(self):
        
        print("Welcome To The Vending Machine...")
        print("--- Currently Offering ---")
        self.adrinks = { "Available": "A" }
        self.items = self.inventory.find(self.adrinks)
        print("Name---Price")

        for item in self.items:
            print("{} --- {}".format(item["Name"],item["Price"]))


    def take_order(self):
        ## Add a check that there is atleast 1 item available and modify the range(n) to min(num_items,n)
        n = int(input("Enter the types of drinks you want to order : "))
        self.order_amount = 0

        for _ in range(n):
            self.drink =  input("Enter The Name of the Drink  :  ")
            self.quantity = int(input("Enter the Quantity : "))
            self.order_amount = self.order_amount + self.check_inventory(self.drink,self.quantity)
        print(self.order_amount)    

    def check_inventory(self,drink,quantity):        
            self.drinks_query = {"Name":drink}
            self.available = self.inventory.find_one(self.drinks_query)

            if quantity < self.available["Quantity"]:
                self.amount = self.available["Price"]*quantity
                new_quan = self.available["Quantity"] - quantity
                self.inventory.update_one(
                        {"Name":drink},
                        {"$set":{"Quantity":new_quan}})
                return self.amount

            elif quantity == self.available["Quantity"]:
                self.amount = self.available["Price"]*quantity
                self.inventory.update_one(
                        {"Name":drink},
                        {"$set":{"Quantity":0,"Available":"N"}})
                return self.amount

            else:
                print("Sorry we have only {} {} Available ... Do you want to continue with this many...".format(self.available["Quantity"],self.drink))
                c = int(input("Input -1 for yes.. or enter lower quantity "))

                if c == -1:
                    self.amount = self.available["Price"]*self.available["Quantity"]
                    self.inventory.update_one(
                            {"Name":drink},
                            {"$set":{"Quantity":0,"Available":"N"}})
                    return self.amount

                elif c < self.available["Quantity"] and c > 0:
                    self.amount = self.available["Price"]*c
                    new_quan = self.available["Quantity"] - c
                    self.inventory.update_one(
                        {"Name":drink},
                        {"$set":{"Quantity":new_quan}})
                    return self.amount

                else:
                    print("The Transaction for {} could not be processed".format(drink))
                    return 0    


if __name__ == '__main__':
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    mydb = client['Vending_Machine']
    cl = Vending_Machine(mydb)
    cl.vend()
    cl.take_order()