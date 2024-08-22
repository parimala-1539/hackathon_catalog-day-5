import random
import time
from datetime import datetime
from colorama import Fore, Style

# Step 1: Define Classes and Data Structures
class ChargingStation:
    def __init__(self, name, location, speed, price_per_hour):
        self.name = name
        self.location = location  # (latitude, longitude)
        self.speed = speed  # "Fast", "Slow"
        self.price_per_hour = price_per_hour  # in dollars
        self.slots = self.generate_slots()  # Generate slots for the next 24 hours

    def generate_slots(self):
        slots = {}
        current_hour = datetime.now().hour
        for i in range(24):
            hour_slot = f"{(current_hour + i) % 24}:00-{(current_hour + i + 1) % 24}:00"
            slots[hour_slot] = random.choice([True, False])  # Random availability
        return slots

    def calculate_distance(self, user_location):
        # Simplified distance calculation for demo purposes
        return round(((self.location[0] - user_location[0])**2 + (self.location[1] - user_location[1])**2)**0.5, 2)

class User:
    def __init__(self, name, location):
        self.name = name
        self.location = location  # (latitude, longitude)

class Booking:
    def __init__(self, user, station, slot_time, total_price):
        self.user = user
        self.station = station
        self.slot_time = slot_time
        self.total_price = total_price
        self.confirmation_code = self.generate_confirmation_code()

    def generate_confirmation_code(self):
        return f"{self.user.name[:2].upper()}{random.randint(1000, 9999)}"

    def send_confirmation(self):
        print(Fore.CYAN + f"\nBooking confirmed for {self.user.name} at {self.station.name} for {self.slot_time}.")
        print(f"Total Price: ${self.total_price:.2f}")
        print(f"Confirmation Code: {self.confirmation_code}" + Style.RESET_ALL)

# Step 2: Create Dynamic Data
def generate_stations(num_stations):
    stations = []
    for i in range(num_stations):
        name = f"Station {chr(65 + i)}"
        location = (random.uniform(-90, 90), random.uniform(-180, 180))
        speed = random.choice(["Fast", "Slow"])
        price_per_hour = round(random.uniform(10, 30), 2)
        stations.append(ChargingStation(name, location, speed, price_per_hour))
    return stations

# Step 3: Implement Advanced Search and Booking Functions
def find_stations(user, stations, max_distance=None, speed=None, availability=True):
    results = []
    for station in stations:
        distance = station.calculate_distance(user.location)
        if max_distance and distance > max_distance:
            continue
        if speed and station.speed != speed:
            continue
        if availability and not any(station.slots.values()):
            continue
        results.append((station, distance))
    return results

def book_slots(user, station, slots_requested):
    available_slots = [slot for slot, available in station.slots.items() if available]
    slots_to_book = available_slots[:slots_requested]
    if len(slots_to_book) < slots_requested:
        print(Fore.YELLOW + f"Only {len(slots_to_book)} slots available at {station.name}." + Style.RESET_ALL)
    total_price = len(slots_to_book) * station.price_per_hour
    for slot in slots_to_book:
        station.slots[slot] = False
    booking = Booking(user, station, ", ".join(slots_to_book), total_price)
    booking.send_confirmation()
    return booking

# Step 4: Integrate CLI and User Interaction
def main():
    print(Fore.GREEN + "Welcome to the Enhanced EV Charging Station Finder and Slot Booking System" + Style.RESET_ALL)
    user = User(name=input("Enter your name: "), location=(random.uniform(-90, 90), random.uniform(-180, 180)))
    
    stations = generate_stations(5)
    
    while True:
        print("\n1. Find Charging Stations\n2. Book a Charging Slot\n3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            max_distance = float(input("Enter max distance (in degrees, e.g., 10.0) (or leave blank to skip): ") or 0)
            speed = input("Enter the charging speed (Fast/Slow) (or leave blank to skip): ")
            results = find_stations(user, stations, max_distance=max_distance if max_distance else None, speed=speed if speed else None)
            if results:
                print(Fore.YELLOW + "\nAvailable Charging Stations:" + Style.RESET_ALL)
                for station, distance in results:
                    print(f"- {station.name} ({station.speed} charging) - {distance} degrees away, ${station.price_per_hour}/hour")
            else:
                print(Fore.RED + "\nNo matching stations found." + Style.RESET_ALL)
        
        elif choice == '2':
            station_name = input("Enter the station name: ")
            slots_requested = int(input("Enter the number of slots you want to book: "))
            station = next((s for s in stations if s.name == station_name), None)
            if station:
                book_slots(user, station, slots_requested)
            else:
                print(Fore.RED + f"No station found with the name {station_name}." + Style.RESET_ALL)
        
        elif choice == '3':
            print(Fore.BLUE + "Exiting the system. Goodbye!" + Style.RESET_ALL)
            break
        
        else:
            print(Fore.RED + "Invalid choice, please try again." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
