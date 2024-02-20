# Admin acc
admin_username = "admin"
admin_password = "admin123"

# number of student must be enroll
student = 10

# list of students number
student_number = [0] * student
student_number_count = 0

# amount to pay per-units
perUnit = 850
totalPays = 0

# used to check if numbers has commas
def has_commas(input_string):
    return ',' in input_string

# Used to check if the student number has already been typed in.
def isInTheList(stud_number):
    for studNum in student_number:
        if studNum == stud_number:
            return True
    return False

# once a student has login
def login_student():
    global totalPays, student_number_count
    if student_number_count < student:
        studName = input(f"\n\tBSIT Student {student_number_count + 1}/10\nEnter your name: ")
        studNumber_str = input("Student No.: ")
        if len(studNumber_str) == 9:
            if not isInTheList(int(studNumber_str)):
                student_number[student_number_count] = int(studNumber_str)
                while True:
                    units_str = input("\n\thow many units do you need to enroll?\n: ")
                    try:
                        units = int(units_str)
                        break
                    except ValueError:
                        print("\n\tUnit must be a number.")
                totalAmountToPay = perUnit * int(units)
                while True:
                    amount_str = input(f"\n\tYou need to pay {totalAmountToPay:,}\namount: ")
                    if has_commas(amount_str):
                    # Remove commas from the input string
                        amount_str = amount_str.replace(',', '')
                    try:
                        amount = int(amount_str)
                        if amount >= totalAmountToPay:
                            totalPays += totalAmountToPay
                            change = amount - totalAmountToPay
                            print(f"\n\t\tRECEIPT\n\tYOUR MONEY: {amount:,}\n\tPAY: {totalAmountToPay:,}\n\tCHANGE: {change:,}\n*******LOG OUT*******\n")
                            break
                        else:
                            print(f"\n\tPlease provide an amount equal to or greater than PHP {totalAmountToPay:,}")
                    except ValueError:
                        print(f"\n\tInvalid amount \"{amount_str}\". Please enter a number.")
                student_number_count += 1
            else:
                print('\nPlease type a different student number')
        else:
            print("\n\tERROR Format. Ex. 220100443")
    else:
        print("\n\tThe maximum number of students has been reached.\n")

# to check admin credentials
def check_credentials(username, password):
    return username == admin_username and password == admin_password

def adminAccess():
    username = input("\n\tADMIN\nusername: ")
    password = input("password: ")

    # Check credentials
    if check_credentials(username, password):
        while True:
            choice = input("\n\tAdmin!\n1. Records\n2. Cashier\n3. Back\n: ")
            if choice == "3":
                break
            if choice == "1":
                print(f"\n\tTotal Payment: {totalPays:,}")
            elif choice == "2":
                student_id_str = input("\n\tHave you paid?\nStudent ID: ")
                try:
                    student_id = int(student_id_str)
                    if isInTheList(student_id):
                        print("\n\tThanks, you are paid")
                    else:
                        print("\n\tSorry, you haven't paid yet. Did you perhaps enter the wrong student ID?")
                except ValueError:
                    print("\n\tInvalid ID")
            else:
                print("\n\tInvalid Input.")

    else:
        print("\tInvalid credentials. Access denied.\n")

# Main program
def main():
    while True:
        select = input("\tTuition Fee Payment System\n1. Student\n2. Admin\n3. Exit\n: ")
        if select == "3":
            print("\tExiting...")
            break
        if select == "1":
            login_student()
        elif select == "2":
            adminAccess()

# Run the program
if __name__ == "__main__":
    main()
