import module  # import the module containing arithmetic functions



# main function to execute the calculator operations
def main():

    val1 = int(input("Enter the value 1: ")) # get the first input value from the user

    val2 = int(input("Enter the value 2: ")) # get the second input value from the user

    while True: # infinite loop to keep the program running until the user chooses to exit
        print("Choose an Operation")
        print("1. Sum")
        print("2. Difference")
        print("3. Multiplication")
        print("4. Division")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1': 
            result_sum = module.sum_val(val1 , val2) # store the return value in result_sum
            print("The Sum is: ", result_sum)
        elif choice == '2':
            result_diff = module.diff_val(val1 , val2)
            print("The Difference is: ", result_diff) # store the return value in result_diff
        elif choice == '3':
            result_mul = module.mul_val(val1 , val2)
            print("The Multiplication is: ", result_mul) # store the return value in result_mul
        elif choice == '4':
            result_div = module.div_val(val1 , val2)
            print("The Division is: ", result_div) # store the return value in result_div
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

main()