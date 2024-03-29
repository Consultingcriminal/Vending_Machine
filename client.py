import pymongo

class Vending_Machine:

    def __init__(self,db):
        self.my_db = db
        self.inventory = self.my_db["Inventory"]
        self.denominations = self.my_db["Denominations"]

    def vend(self):
        
        print("Welcome To The Vending Machine...")
        print("--- Currently Offering ---")
        self.items = self.inventory.find({"Quantity": {"$gt": 0 } })
        self.len = self.inventory.count_documents({"Quantity": {"$gt": 0 } })
        print("Name---Price")

        for item in self.items:
            print("{} --- {}".format(item["Name"],item["Price"]))


    def take_order(self):
        n = int(input("Enter the types of drinks you want to order : "))
        self.order_amount = 0
        self.orders = []
        for _ in range(min(self.len,n)):
            self.drink =  input("Enter The Name of the Drink  :  ")
            self.quantity = int(input("Enter the Quantity : "))
            self.order_amount = self.order_amount + self.get_order_quan(self.drink,self.quantity)
        print("Your order value is : {}".format(self.order_amount))
        print(self.orders)
        confirm = input("Enter Y for continuing with this transaction : ").upper()

        if confirm == "Y":
            print("Processing...")
            self.initiate_trans(self.order_amount)
        else:
            print("Transaction Aborted...")

        # Cleaning the orders list
        #self.orders = []

    def get_order_quan(self,drink,quantity):
        
        self.drinks_query = {"Name":drink}
        self.available = self.inventory.find_one(self.drinks_query)

        if quantity <= self.available["Quantity"]:
            self.amount = self.available["Price"]*quantity
            new_quan = self.available["Quantity"] - quantity

            update_dict = {"Name":drink,"Quantity":new_quan}
            self.orders.append(update_dict)
            return self.amount

        else:
                print("Sorry we have only {} {} Available ... Do you want to continue with this many...".format(self.available["Quantity"],self.drink))
                c = int(input("Input -1 for yes.. or enter lower quantity "))

                if c == -1:
                    self.amount = self.available["Price"]*self.available["Quantity"]
                    update_dict = {"Name":drink,"Quantity":0}
                    self.orders.append(update_dict)
                    return self.amount

                elif c < self.available["Quantity"] and c > 0:
                    self.amount = self.available["Price"]*c
                    new_quan = self.available["Quantity"] - c
                    update_dict = {"Name":drink,"Quantity":new_quan}
                    self.orders.append(update_dict)
                    return self.amount

                else:
                    print("The Transaction for {} could not be processed".format(drink))
                    return 0             

    def initiate_trans(self,price):
        print("Your cart value is {}".format(price))
        self.cust_amount = sum(list(map(int,input('insert ' + str(price - 0) + ': in denominations of 1,5,25,50 (space separated)  - ').split())))
        self.change = self.cust_amount - price
        print("Change amount  =  {}".format(self.change))

        if self.change < 0:
            print("Insert {} in denominations of 1,5,25,50 ".format(-1*self.change))
            tries = 3
            flag = False
            for _ in range(tries):
                amt_inserted = sum(list(map(int,input('insert ' + str(-1*self.change - 0) + ': in denominations of 1,5,25,50 (space separated)  - ').split())))

                if amt_inserted > -1*self.change:
                    flag = True
                    print("Processing Change")
                    if self.make_change(amt_inserted + self.change) is None:
                        print("Transaction Unsuccessful not enough coins try again...")
                    else:
                        print("Collect Items")
                        print(self.make_change(amt_inserted + self.change))
                        self.update_inventory()
                        self.update_denominations()
                
                elif amt_inserted == -1*self.change:
                    flag = True
                    print("Collect Your Items")
                    self.update_inventory()

                break        
            
            if flag is False:
                print("Transaction Terminated")

        elif self.change == 0:
            print("Collect Your Items")
            self.update_inventory()
        else:
            print("Processing Your Change")
            if self.make_change(self.change) is None:
                print("Transaction Unsuccessful not enough coins try again...")
            else:
                print("Collect Items")
                print("Collect Change ={}".format(self.make_change(self.change)))
                self.update_inventory()
                self.update_denominations() 


    def make_change(self,change_amt):
        
        denom_aval = []
        self.coins_quan = self.denominations.find({"Quan": {"$gt": 0 } })

        for coins in self.coins_quan:
            coins_dict = {"Deno":coins["Deno"],"Quan":coins["Quan"]}
            denom_aval.append(coins_dict)
        self.result = self.getchange(denom_aval,change_amt)
        return self.result

    def getchange(self,coins, amount):
        
        minCount = None

        def recurse(amount, coinIndex, coinCount):
            nonlocal minCount
            if amount == 0:
                if minCount == None or coinCount < minCount:
                    minCount = coinCount
                    return [] # success
                return None # not optimal
            if coinIndex >= len(coins):
                return None # failure
            bestChange = None
            coin = coins[coinIndex]
            # Start by taking as many as possible from this coin
            cantake = min(amount // coin["Deno"], coin["Quan"])
            # Reduce the number taken from this coin until 0
            for count in range(cantake, -1, -1):
                # Recurse, taking out this coin as a possible choice
                change = recurse(amount - coin["Deno"] * count, coinIndex + 1, 
                                                                coinCount + count)
                # Do we have a solution that is better than the best so far?
                if change != None: 
                    if count: # Does it involve this coin?
                        change.append({ "Deno": coin["Deno"], "Quan": count })
                    bestChange = change # register this as the best so far
            return bestChange

        return recurse(amount, 0, 0)

    def update_inventory(self):
        for item in self.orders:
            self.inventory.update_one(
                    {"Name":item["Name"]},
                    {"$set":{"Quantity":item["Quantity"]}})
                        
    def update_denominations(self):
        for item in self.result:
            new_quan = self.denominations.find_one({"Deno":item["Deno"]})["Quan"] - item["Quan"]
            self.denominations.update_one({"Deno":item["Deno"]},
                    {"$set":{"Quan":new_quan}})

class run_client:

    def __init__(self,mydb):
        self.mydb = mydb

    def run(self):
        choice = -1
        cl = Vending_Machine(self.mydb)

        while choice == -1:
            cl.vend()
            cl.take_order()
            choice = int(input("Enter -1 for continuing Vending Mode = "))

        print("Exiting Vending Mode ... Thank You....")    

if __name__ == '__main__':
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    mydb = client['Vending_Machine']
    rc = run_client(mydb)
    rc.run()

   
    

    