#Robust Division Calculator with Command Line Arguments 
def safe_divide(numerator, denominator):
    try:
        num = float(numerator)
        den = float(denominator)   
        try:
           result = num / den
           print("The result of the division is ", end='')
           return result
        except ZeroDivisionError:
            msg = "Error: Cannot divide by zero."
            return msg
        
    except ValueError:
      msg = "Please enter numeric values only."
      return msg