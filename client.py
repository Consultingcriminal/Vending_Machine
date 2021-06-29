import pymongo

class Vending_Machine:

    def __init__(self,db):
        self.my_db = db
        self.inventory = self.my_db["Inventory"]
        self.denominations = self.my_db["Denominations"]

    def vend(self):
        
        print("Welcome To The Vending Machine...")
        print("--- Currently Offering ---")
        self.items = self.inventory.find({ "Available": "A" })
        self.len = self.inventory.count_documents({ "Available": "A" })
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

        if quantity < self.available["Quantity"]:
            self.amount = self.available["Price"]*quantity
            new_quan = self.available["Quantity"] - quantity

            update_dict = {"Name":drink,"Quantity":new_quan}
            self.orders.append(update_dict)
            return self.amount

        elif quantity == self.available["Quantity"]:
                self.amount = self.available["Price"]*quantity
                update_dict = {"Name":drink,"Quantity":0,"Available":"N"}
                self.orders.append(update_dict)
                return self.amount

        else:
                print("Sorry we have only {} {} Available ... Do you want to continue with this many...".format(self.available["Quantity"],self.drink))
                c = int(input("Input -1 for yes.. or enter lower quantity "))

                if c == -1:
                    self.amount = self.available["Price"]*self.available["Quantity"]
                    update_dict = {"Name":drink,"Quantity":0,"Available":"N"}
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
            flag = 0
            for _ in range(tries):
                amt_inserted = sum(list(map(int,input('insert ' + str(-1*self.change - 0) + ': in denominations of 1,5,25,50 (space separated)  - ').split())))

                if amt_inserted >= -1*self.change:
                    flag = 1
                    print("Processing Change")
                    break        
            
            if flag == 0:
                print("Transaction Terminated")
        else:
            print("Processing Your Change")
       
        



if __name__ == '__main__':
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    mydb = client['Vending_Machine']
    cl = Vending_Machine(mydb)
    cl.vend()
    cl.take_order()