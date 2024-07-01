# Explore datetime Module 
from datetime import datetime, timedelta

def display_current_datetime():
    current_date =  datetime.now()
    print("Current date and time: ", f"{current_date.year}-{current_date.month}-{current_date.day}  {current_date.hour}:{current_date.minute}:{current_date.second}")
    

def calculate_future_date():
    num_days = int(input("Enter the number of days to add to the current date: "))
    current_date = datetime.now()
    
    future_date = current_date + timedelta(days=num_days)
    print("Future date: ", f"{future_date.year}-{future_date.month}-{future_date.day}")
    


display_current_datetime()
calculate_future_date()
