#calculate the user’s age in a future year

cur_year = 2023
#Prompt the user to input their current age 
user_age = int(input("How old are you?\n"))
future_age = user_age + (2050 - cur_year)

print("In 2050, you will be {} years old.".format(future_age))


