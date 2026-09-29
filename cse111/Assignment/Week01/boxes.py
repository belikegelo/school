import math

items = int(input("Enter the number of items: "))
boxes = int(input("Enter the number of items per box: "))
num_boxes = math.ceil(items / boxes)
print(f"For {items} items, packing {boxes} items in each box, you will need {num_boxes} boxes.")