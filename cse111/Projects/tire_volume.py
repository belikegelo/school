#Enhancement #1: After the program prints the tire volume to the terminal window, 
# the program should ask the user if she wants to buy tires with the dimensions that she entered. 
# If the user answers “yes”, the program should ask for her phone number and store her phone number in the volumes.txt file.

#ENhancement #2: If error occurs, the program should print an error message and ask the user to enter the value again.
# I used a while loop to keep asking the user for input until valid input is provided.



from datetime import datetime
import math

print("Welcome to the tire volume calculator!")

while True:
    
    try:
        width = int(input("Enter the width of the tire in mm (ex 205): "))
        aspect_ratio = int(input("Enter the aspect ratio of the tire (ex 60): "))
        diameter = int(input("Enter the diameter of the wheel in inches (ex 15): "))
        break

    except ValueError:
        print("Invalid input.")

volume = (math.pi * width ** 2 * aspect_ratio * (width * aspect_ratio + 2540 * diameter)) / 10000000000
current_date_and_time = datetime.now()
print (f"The approximate volume is {volume:.2f} liters.")
print()

while True:
    buy = input("Do you want to buy this tire? (yes/no): ").strip().lower()
    if buy == "yes":
        contact = (input("Please enter your contact number: "))
        with open("volume.txt", "at") as file:
            print(f"{current_date_and_time:%Y-%m-%d }, {width}, {aspect_ratio}, {diameter}, {volume:.2f}, {contact}", file=file)
            print("Thank you, we will contact you soon.")
        break


    elif buy == "no":
        #save the data to a file
        print("Ok, Thank you! Have a nice day!")
        with open("volume.txt", "at") as file:
            print(f"{current_date_and_time:%Y-%m-%d }, {width}, {aspect_ratio}, {diameter}, {volume:.2f}", file=file)
        break


    else:
        print("Invalid input. Please enter 'yes' or 'no'.")
        continue

