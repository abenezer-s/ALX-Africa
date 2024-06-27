#Personal Daily Reminder 

#promt for user input

task = input("Enter your task: ")
priority = input("Priority (high/medium/low): ")
time_bound = input("Is it time-bound? (yes/no): ")

reminder = f"\'{task}' is a {priority} priority task"
msg1 = " that requires immediate attention today!"
msg2 =  ". Consider completing it when you have free time."

match priority:
    case "high":
        if time_bound == "yes":
        
            reminder += msg1
            print("Reminder:", reminder)
        else:
           
            reminder += msg2
            print("Note:", reminder)
        
    case "medium":
        if time_bound == "yes":
           
            reminder += msg1
            print("Reminder:", reminder)
        else:
           
            reminder += msg2
            print("Note:", reminder)
    case  "low":
        if time_bound == "yes":
           
            reminder += msg1
            print("Reminder:", reminder)
        else:
           
            reminder += msg2
            print("Note:", reminder)