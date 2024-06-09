
import csv
from _datetime import datetime, timedelta

# Ref: https://stackoverflow.com/questions/41585078/how-do-i-read-and-write-csv-files
# Load distanceCSV file
with open('distanceCSV.csv') as distCSV:
    reader = csv.reader(distCSV, delimiter=",")
    distanceCSV = [row for row in reader]
#print(distanceCSV)
# Load addressCSV file
address_index_map = {}  # Dictionary maps address to row number
with open('addressCSV.csv') as addCSV:
    reader = csv.reader(addCSV, delimiter=",")
    for index, row in enumerate(reader):
        address = row[2]  # address is in the 3rd index
        address_index_map[address] = index
#print(address_index_map)

# Ref: https://wgu.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=f08d7871-d57a-496e-a6a1-ac7601308c71
# HashTable class using chaining.
class ChainingHashTable:
    # Constructor with optional initial capacity parameter.
    # Assigns all buckets with an empty list.
    def __init__(self, initial_capacity=50):
        # initialize the hash table with empty bucket list entries.
        self.initial_capacity = initial_capacity
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Inserts a new item into the hash table.
    def insert(self, key, item):  # does both insert and update
        # get the bucket list where this item will go.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # update key if it is already in the bucket
        for kv in bucket_list:
            # print (key_value)
            if kv[0] == key:
                kv[1] = item
                return True

        # if not, insert the item to the end of the bucket list.
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Searches for an item with matching key in the hash table.
    # Returns the item if found, or None if not found.
    def search(self, key):
        # get the bucket list where this key would be.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # print(bucket_list)

        # search for the key in the bucket list
        for kv in bucket_list:
            # print (key_value)
            if kv[0] == key:
                return kv[1]  # value
        return None

    # Removes an item with matching key from the hash table.
    def remove(self, key):
        # get the bucket list where this item will be removed from.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # remove the item from the bucket list if it is present.
        for kv in bucket_list:
            # print (key_value)
            if kv[0] == key:
                bucket_list.remove([kv[0], kv[1]])

# Package object
class Package:
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, notes, status, departureTime, deliveryTime, truck=None):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.delivery_status = status
        self.departure_time = departureTime
        self.delivery_time = deliveryTime
        self.truck = truck

    def __str__(self):
        delivery_time_str = self.delivery_time.strftime('%H:%M:%S') if self.delivery_time else "Not Delivered"
        return (
            f"PackageID: {self.package_id}, Address: {self.address}, City: {self.city}, State: {self.state}, Zip: {self.zip_code}, "
            f"Delivery Deadline: {self.deadline}, Weight: {self.weight}, Notes: {self.notes}, "
            f"Status: {self.delivery_status}, {self.truck}, DeliveryTime: {delivery_time_str}")

    # Method to update the address for package 9
    def update_address(self, new_address):
        self.address = new_address

# Ref: https://srm--c.vf.force.com/apex/CourseArticle?id=kA03x000000e1g4CAA&groupId=&searchTerm=&courseCode=C950&rtn=/apex/CommonsExpandedSearch
# Load the package CSV data
def loadPackageData(filename):
    with open(filename) as packages:
        packageInfo = csv.reader(packages,delimiter=',')
        next (packageInfo)
        for row in packageInfo:
            pID = int(row[0])
            pStreet = row[1]
            pCity = row[2]
            pState = row[3]
            pZip = row[4]
            pDeadline = row[5]
            pWeight = row[6]
            pNotes = row[7]
            pStatus = "At the Hub"
            pDepartureTime = None
            pDeliveryTime = None

            if pID == 9:
                pStatus = "At the Hub"

            # Inserting Package info into the hash
            p = Package(pID, pStreet, pCity, pState, pZip, pDeadline, pWeight, pNotes, pStatus, pDepartureTime, pDeliveryTime)
            myHash.insert(pID, p)

myHash = ChainingHashTable()
loadPackageData("packageCSV.csv")

# Truck object
class Truck:
    def __init__(self, miles, speed, currentLocation, departTime, packages):
        self.miles = miles
        self.speed = speed
        self.currentLocation = currentLocation
        self.time = departTime
        self.departTime = departTime
        self.packages = packages

    def __str__(self):
        return (f" {self.miles}, {self.speed}, {self.currentLocation}, {self.time}, {self.departTime}, {self.packages}")


# Manually loading the trucks and assigning a departure time
departure_time1 = datetime.combine(datetime.today(), datetime.min.time()) + timedelta(hours=8)
departure_time2 = datetime.combine(datetime.today(), datetime.min.time()) + timedelta(hours=9, minutes=5)
departure_time3 = datetime.combine(datetime.today(), datetime.min.time()) + timedelta(hours=10, minutes=20)
truck1 = Truck(0.0, 18, "4001 South 700 East", departure_time1,[1,13,14,15,16,20,29,30,31,34,37,40])
truck2 = Truck(0.0, 18, "4001 South 700 East", departure_time2,[2,3,6,8,25,10,12,18,21,23,27,28,32,36,38])
truck3 = Truck(0.0, 18, "4001 South 700 East", departure_time3,[4,5,7,9,11,17,19,22,24,26,33,35,39])

# Finds the distance between 2 addresses
def distanceBetween(address1, address2):
        index1 = address_index_map[address1]
        index2 = address_index_map[address2]
        distBet = distanceCSV[index1][index2]
        if distBet == '':
            distBet = distanceCSV[index2][index1]  # 2D list [i][j] = [j][i]
        return float(distBet)

# Finds minimum distance between two addresses
def minDistanceFrom(fromAddress, truckPackages):
    min_distance = float('inf')
    min_address = None

    # Loop over each package ID in the truck packages
    for package_id in truckPackages:
        package = myHash.search(package_id)
        if package is not None:
            # Compute the distance from 'fromAddress' to this package's address
                distance = distanceBetween(fromAddress, package.address)
                if distance < min_distance:
                    min_distance = distance
                    min_address = package.address

    return min_address, min_distance

# print(f'Minimum distance address: {min_address} with a distance of {min_distance}')

# Function to update packages with wrong addresses
def update_package_address_at_time(current_time, update_time_str, package_id, new_address):
    update_time = datetime.strptime(update_time_str, '%H:%M')
    # Only update the address if the current time matches the update time
    if current_time.time() == update_time.time():
        package = myHash.search(package_id)
        if package:
            package.update_address(new_address)

# Function to deliver the packages: Nearest Neighbor Algorithm
# Ref: https://stackoverflow.com/questions/30552656/python-traveling-salesman-greedy-algorithm
def truckDeliverPackages(truck, truckID):
    current_address = truck.currentLocation  # Set the starting point
    hub_address = truck.currentLocation
    remaining_packages = [pkg for pkg in truck.packages]  # List of packages that still to be delivered
    total_miles = 0

    while remaining_packages:
        # Check if Package 25 is among the remaining and prioritize it
        # If not the package isn't delivered on time
        if 25 in remaining_packages:
            nearest_package_id = 25
        else:
            # If package not there then find the nearest package address from the current location
            nearest_address, nearest_distance = minDistanceFrom(current_address, remaining_packages)
            nearest_package_id = None
            # Check each package in the remaining list to match the nearest address found
            for package_id in remaining_packages:
                package = myHash.search(package_id)
                if package and package.address == nearest_address:
                    nearest_package_id = package_id
                    break

        if nearest_package_id is None:
            break

        # Search the hash table using the nearest package id
        package = myHash.search(nearest_package_id)
        if package:
            # Calculate the distance
            nearest_distance = distanceBetween(current_address, package.address)
            # Calculate the delivery time by adding the departure time and travel time to next location
            delivery_time = truck.departTime + timedelta(hours=(nearest_distance / truck.speed))

            # Update package status and time
            package.delivery_time = delivery_time
            package.departure_time = truck.departTime
            package.truck = truckID
            package.delivery_status = 'Delivered'

            # Update the hash table with the new package status
            myHash.insert(package.package_id, package)

            # Update truck's current location and total mileage
            current_address = package.address
            truck.currentLocation = current_address
            total_miles += nearest_distance
            truck.miles += nearest_distance
            truck.departTime = delivery_time

            # Remove the delivered package from the list
            remaining_packages.remove(nearest_package_id)

    # Calculate return to hub distance and add it to the total mileage
    return_distance = distanceBetween(current_address, hub_address)
    return_time = truck.departTime + timedelta(hours=(return_distance / truck.speed))
    truck.miles += return_distance
    truck.departTime = return_time  # Update the truck's time to when it returns to the hub

    #print(f"Total miles traveled by Truck {truck_id}, including return to hub: {truck.miles} at {truck.departTime}")

current_time = datetime.combine(datetime.today(), datetime.min.time()) + timedelta(hours=10, minutes=20)
update_package_address_at_time(current_time, '10:20', 9, '410 S State St')
truckDeliverPackages(truck1, 1)
truckDeliverPackages(truck2, 2)
truckDeliverPackages(truck3, 3)

# The user-interface
def print_all_packages_status():
    total_miles = sum(truck.miles for truck in [truck1, truck2, truck3])
    print(f"Total miles traveled by all trucks: {total_miles}")
    for i in range(myHash.initial_capacity):
        for package in myHash.table[i]:
            print_package(package[1])
def print_all_packages_status_at_time(time_str):
    input_time = datetime.strptime(time_str, '%H:%M')
    formatted_input_time = input_time.strftime('%H:%M')

    for bucket in myHash.table:
        for package_key, package in bucket:
            status = "At the Hub"
            truck_ID = ""

            if package.departure_time:
                departure_time = datetime.strptime(package.departure_time.strftime('%H:%M'), '%H:%M')
                if input_time < departure_time:
                    status = "At the Hub"
                    if package.truck:
                        truck_ID = f" on Truck-{package.truck}"
                elif package.delivery_time:
                    delivery_time = datetime.strptime(package.delivery_time.strftime('%H:%M'), '%H:%M')
                    if input_time >= delivery_time:
                        status = "Delivered"
                        if package.truck:
                            truck_ID = f" by Truck-{package.truck}"

                    else:
                        status = "En Route"
                        if package.truck:
                            truck_ID = f" on Truck-{package.truck}"

            print(f"Package {package.package_id} - Status: {status}{truck_ID} at {formatted_input_time}")
def print_package(package):
    delivery_time_str = package.delivery_time.strftime('%H:%M:%S') if package.delivery_time else "Not Delivered"
    print(f"PackageID: {package.package_id}, Address: {package.address}, City: {package.city}, State: {package.state}, Zip: {package.zip_code}, Delivery Deadline: {package.deadline}, Weight: {package.weight}, Notes: {package.notes}, Status: {package.delivery_status}, Truck # {package.truck}, DeliveryTime: {delivery_time_str}")


def main_menu():
    while True:
        print("***************************************")
        print("1. Print All Package Status and Total Mileage")
        print("2. Get All Package Status with a Time")
        print("3. Exit the Program")
        print("***************************************")

        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            print_all_packages_status()
        elif choice == '2':
            time_str = input("Enter the time (HH:MM, 24-hour format): ")
            print_all_packages_status_at_time(time_str)
        elif choice == '3':
            print("Thank You")
            break
        else:
            print("Invalid choice. Please choose between 1-3.")

if __name__ == '__main__':
    main_menu()

