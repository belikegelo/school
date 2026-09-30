#Exceeding the Requirements
#Countdown for New year's sale 


import csv
from datetime import datetime

def read_dictionary(filename, key_column_index):
    Dictionary={}
    with open(filename, 'rt') as csvfile:
        csvreader = csv.reader(csvfile,delimiter=",")
        next(csvreader)
        for row in csvreader:
            key_value=row[key_column_index]
            Dictionary[key_value]=row
    return Dictionary

def main():
    PRODUCT_INDEX = 0
    NAME_INDEX = 1
    PRICE_INDEX = 2
    QUANTITY_INDEX = 1

    try:
        products_dict = read_dictionary('products.csv' ,PRODUCT_INDEX)
        # print(products_dict)

        with open('request.csv', 'rt') as csvfile: 
            csvreader = csv.reader(csvfile, delimiter=",")

            next(csvreader)
            print("________________________")
            print("Welcome to Gelo's Store!")
            print("________________________")

            print("Requested Items:")

            total_items = 0
            subtotal = 0

            for row in csvreader:
                product_number = row[PRODUCT_INDEX] 
                quantity = int(row[QUANTITY_INDEX])

                product = products_dict[product_number] 
                
                product_name = product[NAME_INDEX] 
                
                product_price = float(product[PRICE_INDEX])
                print(f"{product_name}: {quantity} @ {product_price}")

                total_items += quantity
                subtotal += quantity * product_price

            sales_tax = subtotal * 0.06 
            total = subtotal + sales_tax

            print(f"Number of Items: {total_items}") 
            print(f"Subtotal: {subtotal:.2f}") 
            print(f"Sales Tax: {sales_tax:.2f}") 
            print(f"Total: {total:.2f}") 
            print("_______________________________________")
            print("Thank you for shopping at Gelo's Store!") 
            print(datetime.now().strftime("%a %b %d %H:%M:%S %Y"))

            now = datetime.now()
            new_year = datetime(now.year + 1, 1, 1)
            countdown = (new_year - now).days

            print(f"{countdown} days Before the New Year's Sale!")

    except FileNotFoundError:
        print("Error - File not found! ")

    except PermissionError:
        print("Error - No permission! ")

    except KeyError:
        print("Error - Key not found! ")

if __name__ == "__main__":
    main()