class HashTable:
    # Initializes the variables for the hash table.
    # O(n)
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.table = []
        for i in range(capacity):
            self.table.append([])

    # Lookup a value in a hash table using a given key.
    # O(n)
    def get(self, key):
        bucket = self.get_hash(key)
        if self.table[bucket] is not None:
            bucket_list = self.table[bucket]
            for index, value in bucket_list:
                if index == key:
                    return value
        else:
            print("No value found.")
            return None

    # Returns a hashed key.
    # O(1)
    def get_hash(self, key):
        hash_key = hash(key) % self.capacity
        return hash_key

    # Returns all values in the hash table.
    # O(n^2)
    def get_all(self):
        package_list = []
        for bucket in self.table:
            for item in bucket:
                package_list.append(item[1])
        return package_list

    # Returns the size of the hash table.
    # O(1)
    def get_size(self):
        return self.size

    # Inserts a new value into the hash table using a key.
    # O(1)
    def insert(self, key, value):
        bucket = self.get_hash(key)
        self.table[bucket].append([key, value])
        self.size += 1

