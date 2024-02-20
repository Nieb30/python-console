import threading
import time

# admin account
adminUsername = "admin"
adminPassword = "admin123"

# list of car had park
cars = []
count = 0

# remaining slot to reserve
carSlots = 40

# records of transaction history
records = []
recordsCount = 0

# to store timers for each element
timers = {}
Time = 3600

# total daily and weekly sales
todaySales = 0
weeklySales = 0


def print_records():
    for record in records:
        for plate_number, values in record.items():
            print(f"PLATE NUMBER: {plate_number}")
            print(f"    - Brand: {values['Brand']}")

            # Format the time consumption
            time_consume_hours, time_consume_minutes = map(int, values['TimeConsume'].split(':'))
            print(f"    - Total consume time: {time_consume_hours} hours and {time_consume_minutes} minutes")

            # Check if 'Paid' key is present in values dictionary
            if 'Paid' in values and values['Paid'] is not None:
                # Format the payment amount with two decimal places
                print(f"    - Paid: {values['Paid']:.2f}")
            else:
                print("    - Paid: Not paid yet, it's still there in parking lot")

            print()

# payment method after exiting from the parking lot
def payment(totalAmount):
    global recordsCount, todaySales, weeklySales
    pay = "{:.2f}".format(totalAmount)
    while True:
        amount_str = input(f"\n\tHave you paid? you need to pay PHP {pay}\n: ")
        try:
            amount = float(amount_str)
            if amount >= float(pay):
                change = amount - float(pay)
                recordsCount += 1
                todaySales += float(pay)
                weeklySales += float(pay)
                print(f"\t\tPAYMENT SLIP\n\tYOUR MONEY: {amount}\n\tPAY: {pay}\n\tCHANGE: {round(change, 2)}")
                break
            else:
                print(f"\n\tPlease provide an amount equal to or greater than PHP {pay}")
        except ValueError:
            # If the conversion to float fails, it's not a valid number
            print(f"\n\tERROR: \"{amount_str}\" is not a valid amount. Please input a number only")

def exitingFromTheParkingLot(count):
    global carSlots, records

    isPaid = False
    while True:
        # it checks if the customer is paid or not before going out from the parking lot
        if isPaid:
            break

        decision = input("\tYou getting out in this parking lot?(yes/no)\n: ")
        if decision == "no":
            break
        if decision == "yes":
            yourPlateNumber = input("Enter your Plate Number: ")
            isFound = False
            for car in cars:
                plateNumber, brand, total_amount, timeConsume = car
                if plateNumber == yourPlateNumber:
                    # Remove the car and timer entry
                    cars.remove(car)
                    key = yourPlateNumber  # Assuming yourPlateNumber is the key in your records
                    if key in timers:
                        del timers[key]

                    count -= 1
                    carSlots += 1
                    isFound = True
                    payment_amount = car[2]  # Adjusted the index for payment amount

                    # Update the record in the records list
                    for record in records:
                        if yourPlateNumber in record:
                            record[yourPlateNumber]["Paid"] = payment_amount
                            record[yourPlateNumber]["TimeConsume"] = timeConsume

                    payment(payment_amount)  # to store its amount to pay
                    isPaid = True
                    break

            print("\n\tcan't find the plate number\n" if not isFound else "\n\tGoodbye, please come again!\n\t\tRECORD SAVED\n******YOU'VE BEEN SIGN OUT******\n")

def start_timer(plateNumber, seconds):
    global carSlots
    time.sleep(seconds)
    print(f"\tTimer ended for {plateNumber}!\n\n")
    carSlots += 1

# used to check if the plateNumber is already in the park
def isInThePark(plateNumber):
    for car in cars:
        if car[0] == plateNumber:
            return True
    return False

# used to calculate the amount depends on how much time did he spend in the parking lot
def calculate_amount(entry_time, exit_time, rate_per_hour=10):
    entry_hours, entry_minutes = map(int, entry_time.split(':'))
    exit_hours, exit_minutes = map(int, exit_time.split(':'))

    entry_in_minutes = entry_hours * 60 + entry_minutes
    exit_in_minutes = exit_hours * 60 + exit_minutes

    duration_in_hours = (exit_in_minutes - entry_in_minutes) / 60
    total_amount = duration_in_hours * rate_per_hour

    return total_amount

def getDifferenceHour(entry, exit):
    firstTwoNumEn = entry[:2]
    firstTwoNumEx = exit[:2]
    return int(firstTwoNumEx) - int(firstTwoNumEn)

def getDifferenceMinutes(entry, exit):
    firstTwoNumEn = entry[3:]
    firstTwoNumEx = exit[3:]
    return abs(int(firstTwoNumEx) - int(firstTwoNumEn))


def format_time(input_time):
    try:
        # Parse the input time
        hours, minutes = map(int, input_time.split(':'))

        # Format the time
        time_str = f"{hours} hours and {minutes} minutes"

        # Check for plural forms
        if hours == 1:
            time_str = time_str.replace("hours", "hour")
        if minutes == 1:
            time_str = time_str.replace("minutes", "minute")

        return time_str

    except ValueError:
        return "Invalid time format. Please use HH:MM format."

def storePlateNumber():
    global cars, count, carSlots, timers, records

    plateNumber = input("\n\tRemaining Parking Slot: " + str(carSlots) + "\nPlate Number: ")
    brand = input("Brand: ")
    entry_time_str = input(f"\n\tHi, plate number {plateNumber}!\nEnter the entry time (HH:MM): ")
    exit_time_str = input("Enter the exit time (HH:MM): ")

    try:
        # Calculate the time consumption
        entry_hours, entry_minutes = map(int, entry_time_str.split(':'))
        exit_hours, exit_minutes = map(int, exit_time_str.split(':'))

        total_minutes = (exit_hours - entry_hours) * 60 + (exit_minutes - entry_minutes)

        # Ensure that total_minutes is non-negative
        total_minutes = max(total_minutes, 0)

        time_consume_hours = total_minutes // 60
        time_consume_minutes = total_minutes % 60

        timeConsume = f"{time_consume_hours:02}:{time_consume_minutes:02}"

        if exit_time_str >= entry_time_str:
            total_amount = calculate_amount(entry_time_str, exit_time_str)
            if len(plateNumber.strip()) == 0:
                print("\tYou must have a plate number")
            elif len(plateNumber) < 7:
                print("Invalid format. It must contain 7 characters, e.g., NBC 1234")
            elif isInThePark(plateNumber):
                print("\n\tSorry, the plateNumber that you entered is already in the parking")
            else:
                if not len(brand.strip()) == 0:
                    # Store plateNumber and brand as a list [plateNumber, brand]
                    cars.append([plateNumber, brand, total_amount, timeConsume])
                    timers[count] = threading.Thread(target=start_timer, args=(plateNumber, Time))
                    timers[count].start()
                    carSlots -= 1
                    count += 1
                    print(f"\n\tYou about to spend: {format_time(timeConsume)}\n\tTotal Amount: 10 per-hour PHP {total_amount:.2f}")

                    # Append the record to the records list
                    record = {"Brand": brand, "Paid": None, "TimeConsume": timeConsume}
                    records.append({plateNumber: record})
                else:
                    print("\tYou must have a brand")

        else:
            print(f"\n\tERROR: The exit time is less than {entry_time_str}, is supposed to be greater.")
            return

    except ValueError:
        print("\n\tInvalid time format. Please use HH:MM format.")


def reserveSlot():
    while True:
        choice = input("\nDo you want to continue?(yes/no)\n: ")
        if choice == "no":
            break
        if choice == "yes":
            storePlateNumber()

# used to check if the account is correct
def isCorrect(username, password):
    return username == adminUsername and password == adminPassword

def dailySales():
    print(f"\tDaily Sales\nToday: {todaySales}")

def wklySales():
    print(f"\tWeekly Sales\nTotal: {weeklySales}")
def main():
    global count, carSlots

    while True:
        print("\tParking Lot System\n[1] Driver Login\n[2] Admin\n[0] Exit")
        select = input(": ")

        # to exit the program
        if select == "0":
            print("\texiting program..")
            break

        # driver login
        if select == "1":
            while True:
                print("\tDriver Login\n[1] Reserve Slot\n[2] Exit from the parking lot\n[0] Back")
                select = input(": ")
                if select == "0":
                    print("\n")
                    break
                if select == "1":
                    # used to check if there's still a vacancy or not
                    if carSlots != 0:
                        reserveSlot()
                    else:
                        print("\tNo Available slot.\n")
                elif select == "2":
                    exitingFromTheParkingLot(count)


        elif select == "2":
            username = input("\n\tAdmin\nusername: ")
            password = input("password: ")
            if isCorrect(username, password):
                while True:
                    print("\n\tTRANSACTION HISTORY\n[1] Records\n[2] Daily Sales\n[3] Weekly Sales\n[0] Back")
                    adminInput = input(": ")
                    if adminInput == "0":
                        break
                    if adminInput == "1":
                        if recordsCount != 0:
                            print_records()
                        else:
                            print("\n\tNO RECORDS PAID YET")
                    elif adminInput == "2":
                        dailySales()

                    elif adminInput == "3":
                        wklySales()

            else:
                print("\tAccess Denied\n")

        else:
            print("\tError, invalid choice\n\n")

# run the program
if __name__ == "__main__":
    main()