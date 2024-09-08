class Package(object):
    # Initializes the package variables.
    # O(1)
    def __init__(self, new_package):
        self.id = new_package[0]
        self.address = new_package[1]
        self.city = new_package[2]
        self.zip = new_package[4]
        self.deadline = new_package[5]
        self.weight = new_package[6]
        if new_package[7] == "\n":
            self.notes = "N/A"
        else:
            self.notes = new_package[7].rstrip()
        self.status = "Waiting to be shipped"
        self.delivery_time = None
        self.left_hub_time = None
        self.truck_id = None

    # Returns a package's address.
    # O(1)
    def get_address(self):
        return self.address

    # Sets a package's address.
    # O(1)
    def set_address(self, address):
        self.address = address

    # Returns a package's ID.
    # O(1)
    def get_id(self):
        return self.id

    # Returns a package's ZIP code.
    # O(1)
    def get_zip(self):
        return self.zip

    # Sets a package's ZIP code..
    # O(1)
    def set_zip(self, zipcode):
        self.zip = zipcode

    # Returns a package's status.
    # O(1)
    def get_status(self):
        return self.status

    # Sets a package's status.
    # O(1)
    def set_status(self, status):
        self.status = status

    # Returns a package's delivery time.
    # O(1)
    def get_delivery_time(self):
        return self.delivery_time

    # Sets a package's delivery time.
    # O(1)
    def set_delivery_time(self, delivery_time):
        self.delivery_time = delivery_time

    # Returns the time at which a package left the hub.
    # O(1)
    def get_left_hub_time(self):
        return self.left_hub_time

    # Sets the time at which a package left the hub.
    # O(1)
    def set_left_hub_time(self, left_hub_time):
        self.left_hub_time = left_hub_time

    # Returns the package's truck ID.
    # O(1)
    def get_truck_id(self):
        return self.truck_id

    # Sets the package's truck ID.
    # O(1)
    def set_truck_id(self, truck_id):
        self.truck_id = truck_id

    # Returns a package's special notes.
    # O(1)
    def get_notes(self):
        return self.notes

    # Returns a package's address and zip code. Used as a key in some cases.
    # O(1)
    def get_full_address(self):
        return self.address + "," + self.zip

    # This is what is used when a package is called into the interface.
    # O(1)
    def __str__(self):
        package = f"Package ID: {self.id}\tAddress: {self.address}, {self.city}, {self.zip}\tWeight: " \
                  f"{self.weight}\tDeadline: {self.deadline}\tStatus: {self.status} by truck #{self.truck_id} at {str(self.delivery_time)}\t Left hub at {str(self.left_hub_time)}"
        return package
