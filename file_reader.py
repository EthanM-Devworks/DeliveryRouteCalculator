from package import Package
from hash_table import HashTable
import csv
import operator


# Handles the initialization and filling of the package hash table using a given CSV file.
# O(n)
def init_package_table(package_file):
    new_table = HashTable(100)
    lines = package_file.readlines()
    for line in lines:
        package = Package(line.split(","))
        new_table.insert(package.get_id(), package)
    return new_table


# Handles the deletion of the origin row of the distance table.
# O(n) + O(n) = O(2n) = O(n)
def row_sort(row):
    distance_dict = dict()
    del row["ORIGIN"]
    for key, value in row.items():
        row[key] = float(value)
    for item in sorted(row.items(), key=operator.itemgetter(1)):
        distance_dict.update({item[0]: item[1]})
    return distance_dict


# Handles the initialization and filling of the distance table using a given CSV file.
# O(n) * O(n) = O(n^2)
def init_distance_table(distance_file):
    with open(distance_file, newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        distance_dict = dict()
        for row in reader:
            distance_dict.update({row["ORIGIN"]: row_sort(row)})
        return distance_dict


# Returns the package and distance tables.
def table_setup(distance_file, package_file):
    package_table = init_package_table(package_file)
    distance_table = init_distance_table(distance_file)
    return distance_table, package_table
