import datetime

# Initializing global values.
package_table = None
distance_table = None
packages_remaining = None
packages_delivered = 0
truck2_packages = ['6', '25', '28', '32', '31', '3', '18', '36', '38']
priority_packages = ['15', '30', '14', '34', '16', '13', '19', '29']


# This function handles truck #1's delivery of packages, while also starting truck #2's function when the incorrectly-labeled package is corrected.
# O(n^2) + O(n) + O(n^3) = O (n^3)
def truck1_delivery(pack_table, dis_table):
    # Initializing values.
    global package_table, distance_table, packages_remaining, packages_delivered, truck2_packages, priority_packages
    package_table = pack_table
    distance_table = dis_table
    packages_remaining = get_packages(package_table.get_all())
    truck1_list = list()
    priority_list = list()
    # Time is initialized using the date it is run on for simplicity.
    time = datetime.datetime(datetime.datetime.today().year, datetime.datetime.today().month, datetime.datetime.today().day, 8)
    # left_hub_time will keep track of when the truck last left the hub.
    left_hub_time = time
    # Booleans for if a package can be delivered by truck #1.
    package_deliverable = False
    truck1_deliverable = False
    # Boolean to keep truck #2 from running multiple times.
    truck2_has_run = False
    # Boolean to keep package 9 from being skipped more than once.
    package_9_skipped = False

    # A list of packages with strict deadlines are chosen to be delivered by truck #1 first, starting with package 15.
    current_package = package_table.get('15')
    total_distance = distance_table[current_package.get_full_address()]['HUB']
    time = add_time(time, total_distance)
    add_delivery(current_package, priority_list, time, 1, left_hub_time)
    while len(priority_list) < 8:
        for address, distance in distance_table[current_package.get_full_address()].items():
            if packages_remaining.get(address):
                for package_id, package in packages_remaining[address].items():
                    if package_id in priority_packages:
                        current_package = package
                        truck1_deliverable = True
                        break
                if truck1_deliverable:
                    total_distance += distance
                    time = add_time(time, distance)
                    add_delivery(current_package, priority_list, time, 1, left_hub_time)
                    packages_delivered += 1
                    truck1_deliverable = False
                    break

    # This while loop is responsible for loading packages onto the truck. Removes package from packages_remaining once loaded.
    # O(n) * O(n^2) + O(n^2) = O(n^3)
    while len(packages_remaining) > 0:
        # Finds the address with the lowest distance from the current package's address.
        for address, distance in distance_table[current_package.get_full_address()].items():
            # Checks whether a deliverable package's address is equal to the current closest address.
            # If not, the next closest address is chosen instead.
            if packages_remaining.get(address):
                # Checks whether an address is associated with more than one package. I
                # If so, attempts to add any packages associated with said address.
                for package_id, package in packages_remaining[address].items():
                    # Sets a package as eligible to be delivered.
                    if package_id not in truck2_packages:
                        current_package = package
                        package_deliverable = True
                        break
                # Delivers a package, and updates the total distance and time accordingly.
                if package_deliverable:
                    # Swaps package #9 for package #1 when it is called up to prevent it from being put on truck #1's first load.
                    if current_package.get_id() == '9' and package_9_skipped is False:
                        current_package = package_table.get('1')
                        new_distance = distance_table[truck1_list[-1].get_full_address()][current_package.get_full_address()]
                        total_distance += new_distance
                        current_time = add_time(time, new_distance)
                        package_9_skipped = True
                    # Adds the distance from the hub to the next package to the total distance if the amount of packages delivered in one set of 16 packages is 0.
                    if packages_delivered == 0:
                        total_distance += distance_table[current_package.get_full_address()]['HUB']
                        time = add_time(time, distance_table[current_package.get_full_address()]['HUB'])
                        packages_delivered += 1
                    # If the truck is not inbound or outbound to or from the hub, adds the distance between locations as normal.
                    else:
                        total_distance += distance
                        time = add_time(time, distance)
                        packages_delivered += 1
                    # Returns the truck to the hub if all packages in a set are delivered, and adds the distance from the current location to hub to the total.
                    # This also sets the amount of packages in a set delivered to 0.
                    if packages_delivered == 16:
                        total_distance += distance_table[current_package.get_full_address()]['HUB']
                        packages_delivered = 0
                        left_hub_time = time
                        time = add_time(time, distance_table[current_package.get_full_address()]['HUB'])
                    # Starts deliveries for truck 2 once the delayed packages arrive.
                    if time.time() >= datetime.time(9, 5) and truck2_has_run is False:
                        total_distance2, truck2_packages = truck2(time)
                        # Makes it so truck 2 doesn't attempt to run twice.
                        truck2_has_run = True
                    add_delivery(current_package, truck1_list, time, 1, left_hub_time)
                    # Resets the loop.
                    package_deliverable = False
                    break

    if package_9_skipped:
        if current_package == package_table.get('9'):
            current_package = package_table.get('10')
            package_9_skipped = True

    # Manually reroutes package 9 due to the incorrect address.
    current_package = package_table.get('9')
    # Calculates the distance from the incorrect address to the correct address.
    reroute_distance = distance_table[truck1_list[-1].get_full_address()][current_package.get_full_address()] + distance_table[current_package.get_full_address()]["410 S State St,84111"]
    time = add_time(time, reroute_distance)
    # Corrects package 9's information.
    current_package.set_address("410 S State St")
    current_package.set_zip("84111")
    current_package.set_delivery_time(time)
    # Returns the total distances for both trucks, including the distance required for the reroute.
    return total_distance + distance_table["410 S State St,84111"]['HUB'] + reroute_distance, total_distance2


# Creates a table of packages to be delivered, instead to be keyed via address and zip code instead of package ID.
# Also handles any potential hash collisions this way.
# O(n)
def get_packages(package_list):
    address_table = dict()
    for package in package_list:
        if address_table.get(package.get_full_address()):
            address_table[package.get_full_address()].update({package.get_id(): package})
        else:
            address_table.update({package.get_full_address(): {package.get_id(): package}})
    return address_table


# Adds a package to the current set of packages to be delivered, removes it from the list of packages remaining, and updates the package status.
# O(1)
def add_delivery(package, delivery_list, current_time, truck_id, left_hub_time):
    update_list(package)
    package_table.get(package.get_id()).set_left_hub_time(left_hub_time)
    if truck_id == 1:
        package_table.get(package.get_id()).set_status('Delivered')
        package_table.get(package.get_id()).set_truck_id(1)
    elif truck_id == 2:
        package_table.get(package.get_id()).set_status('Delivered')
        package_table.get(package.get_id()).set_truck_id(2)
    package_table.get(package.get_id()).set_delivery_time(current_time)
    delivery_list.append(package)


# Handles removing a package from the list of remaining packages.
# O(1)
def update_list(package):
    if len(packages_remaining[package.get_full_address()]) > 1:
        package_list = packages_remaining[package.get_full_address()]
        del package_list[package.get_id()]
    else:
        del packages_remaining[package.get_full_address()]


# Updates the current time according to the distance traveled between locations.
# O(1)
def add_time(current_time, miles):
    seconds = 3600 / 18 * miles
    current_time = current_time + datetime.timedelta(seconds=seconds)
    return current_time


# Handles packages quite similarly to truck 1, but only for a certain few packages, so it only runs once.
# O(n^2)
def truck2(time):
    delivery_list = list()
    package_deliverable = False
    left_hub_time = time
    # Starts with package 25 manually to avoid the time it would require to calculate which package is closest to the hub.
    current_package = package_table.get('25')
    total_distance = distance_table[current_package.get_full_address()]['HUB']
    time = add_time(time, total_distance)
    add_delivery(current_package, delivery_list, time, 2, left_hub_time)
    while len(delivery_list) < 9:
        for address, distance in distance_table[current_package.get_full_address()].items():
            if packages_remaining.get(address):
                for package_id, package in packages_remaining[address].items():
                    if package_id in truck2_packages:
                        current_package = package
                        package_deliverable = True
                        break
                if package_deliverable:
                    total_distance += distance
                    time = add_time(time, distance)
                    add_delivery(current_package, delivery_list, time, 2, left_hub_time)
                    package_deliverable = False
                    break
    return total_distance + distance_table[delivery_list[-1].get_full_address()]['HUB'], delivery_list
