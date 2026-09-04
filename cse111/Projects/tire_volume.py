from datetime import datetime
import math

width = int(input("Enter the width of the tire in mm (ex 205): "))
aspect_ratio = int(input("Enter the aspect ratio of the tire (ex 60): "))
diameter = int(input("Enter the diameter of the wheel in inches (ex 15): "))

volume = (math.pi * width ** 2 * aspect_ratio * (width * aspect_ratio + 2540 * diameter)) / 10000000000
current_date_and_time = datetime.now()

print (f"The approximate volume is {volume:.2f} liters")

with open("volume.txt", "at") as file:
    print(f"{current_date_and_time:%Y-%m-%d }, {width}, {aspect_ratio}, {diameter}, {volume:.2f}", file=file)

