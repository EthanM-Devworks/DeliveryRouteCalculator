# Ethan McKerrocher
# 0015311844
import datetime
from file_reader import *
from sort import truck1_delivery


# The main function of the program, also handles the interface and initializes the sort.
# O(n) * O(n^3) = O(n^3)
def main():
    # Initializes global package table.
    global package_table
    # This is the code for the interface.
    while True:
        print("Welcome. Please select an option:")
        print("\n1.) View all packages")
        print("\n2.) Track a package")
        print("\n3.) Time lookup")
        print("\n4.) Distance traveled")
        print("\n5.) Quit")
        response = input("> ")
        if response == str(1):
            for package in package_table.get_all():
                print(package)
            print()
        elif response == str(2):
            print(package_table.get(package_tracker()))
        elif response == str(3):
            print("\nNOTE: Time must be inputted in 24 hour format.")
            hour = input("Hour: ")
            minute = input("Minute: ")
            print()
            given_time = datetime.datetime(datetime.datetime.today().year, datetime.datetime.today().month, datetime.datetime.today().day, int(hour), int(minute))
            for package in package_table.get_all():
                if given_time < package.get_left_hub_time():
                    print(f"Package #{package.get_id()} has not left the station yet.")
                elif package.get_left_hub_time() < given_time < package.get_delivery_time():
                    print(f"Package #{package.get_id()} is on truck #{package.get_truck_id()} and left the hub at {package.get_left_hub_time()}.")
                elif package.get_delivery_time() < given_time:
                    print(f"Package #{package.get_id()} was delivered by truck #{package.get_truck_id()} at {str(package.get_delivery_time())}.")
            print()
        elif response == str(4):
            print(f"Truck 1 distance: {truck1_distance}")
            print(f"Truck 2 distance: {truck2_distance}")
            print(f"Total distance: {truck1_distance + truck2_distance}")
            print()
        elif response == str(5):
            exit()
        else:
            print("\nPlease input a valid number 1-5.")


# Handles the interface of the package tracker.
# O(1)
def package_tracker():
    print("\nPlease insert package ID:")
    return input("> ")


# Sets up the distance and package tables using the csv files.
distance_table, package_table = table_setup("data/distance.csv",
                                            open("data/packages.csv", "r"))

# Sets up the distance both trucks move to deliver the packages, as well is initializes the final delivery data.
truck1_distance, truck2_distance = truck1_delivery(package_table, distance_table)

# Runs the program.
if __name__ == "__main__":
    main()
