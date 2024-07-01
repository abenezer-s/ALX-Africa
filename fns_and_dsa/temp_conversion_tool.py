# Temperature Conversion Tool 

FAHRENHEIT_TO_CELSIUS_FACTOR = 5 / 9
CELSIUS_TO_FAHRENHEIT_FACTOR = 9 / 5

def convert_to_celsius(fahrenheit):
    return (fahrenheit - 32) * FAHRENHEIT_TO_CELSIUS_FACTOR

def convert_to_fahrenheit(celsius):
    return (celsius * CELSIUS_TO_FAHRENHEIT_FACTOR) + 32

#promt user for input
try:
    temprature = float(input("Enter the temperature to convert: "))
except ValueError:
    raise ValueError("Invalid temperature. Please enter a numeric value.")

unit = input("Is this temperature in Celsius or Fahrenheit? (C/F): ")

if unit == "C":
    print(f"{temprature}°C is {convert_to_fahrenheit(temprature)}°F")
elif unit == "F":
    print(f"{temprature}°F is {convert_to_celsius(temprature)}°C")
else:
    print("Invalid unit. Use C or F")


