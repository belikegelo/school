import csv

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

    products_dict = read_dictionary('products.csv' ,PRODUCT_INDEX)
    print(products_dict)

    with open('request.csv', 'rt') as csvfile: 
        csvreader = csv.reader(csvfile, delimiter=",")

        next(csvreader)

        print("Requested Items")

        for row in csvreader:
            product_number = row[PRODUCT_INDEX] 
            quantity = row[QUANTITY_INDEX]

            product = products_dict[product_number] 
            
            product_name = product[NAME_INDEX] 
            
            product_price = product[PRICE_INDEX]
            print(f"{product_name}: {quantity} @ {product_price}")

if __name__ == "__main__":
    main()