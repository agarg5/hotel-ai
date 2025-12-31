import csv
import random
from datetime import date, timedelta

def generate_bookings():
    """Generates a CSV file with simulated hotel bookings."""

    FIELDNAMES = [
        "booking_id",
        "room_number",
        "guest_name",
        "check_in_date",
        "check_out_date",
        "booking_source",
        "language",
    ]
    
    NUM_ROOMS = 25
    ROOM_NUMBERS = [1 + i for i in range(NUM_ROOMS)]
    
    START_DATE = date(2026, 1, 1)
    END_DATE = date(2026, 1, 31)
    
    NUM_BOOKINGS = 65
    
    GUEST_NAMES = [
        "John Smith", "Maria Garcia", "Wei Li", "Fatima Al-Fassi", 
        "Hans Müller", "Yuki Tanaka", "Olga Petrova", "Ali Hassan",
        "Jane Doe", "Carlos Rodriguez", "Mei Lin", "Isabella Rossi",
        "Ahmed Khan", "Sophie Dubois", "Ivan Ivanov", "Priya Sharma"
    ]
    
    BOOKING_SOURCES = ["email", "whatsapp", "booking.com"]
    LANGUAGES = ["en", "es", "fr", "de", "it", "pt"]

    bookings = []
    booking_id_counter = 1
    
    # Keep track of booked dates for each room
    room_availability = {room: [] for room in ROOM_NUMBERS}

    for _ in range(NUM_BOOKINGS):
        stay_duration = random.randint(1, 5)
        
        # Try to find an available room for a random date
        for _ in range(100): # Max 100 tries to find a slot
            room = random.choice(ROOM_NUMBERS)
            
            check_in_offset = random.randint(0, (END_DATE - START_DATE).days - stay_duration)
            check_in = START_DATE + timedelta(days=check_in_offset)
            check_out = check_in + timedelta(days=stay_duration)

            # Check for availability
            is_available = True
            for day in range(stay_duration):
                if (check_in + timedelta(days=day)) in room_availability[room]:
                    is_available = False
                    break
            
            if is_available:
                # Book the room
                for day in range(stay_duration):
                    room_availability[room].append(check_in + timedelta(days=day))
                
                bookings.append({
                    "booking_id": f"B_{booking_id_counter:04d}",
                    "room_number": room,
                    "guest_name": random.choice(GUEST_NAMES),
                    "check_in_date": check_in.isoformat(),
                    "check_out_date": check_out.isoformat(),
                    "booking_source": random.choice(BOOKING_SOURCES),
                    "language": random.choice(LANGUAGES),
                })
                booking_id_counter += 1
                break # Move to next booking

    # Write to CSV
    with open("bookings.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(bookings)

    print(f"Generated {len(bookings)} bookings in bookings.csv")

if __name__ == "__main__":
    generate_bookings()
