import csv
from datetime import date, timedelta

def create_calendar_view():
    """
    Reads the bookings.csv file and creates a calendar-view CSV
    showing room bookings for a specific period.
    """
    
    # --- Configuration ---
    SOURCE_FILE = "bookings.csv"
    OUTPUT_FILE = "bookings_calendar_view.csv"
    START_DATE = date(2026, 1, 1)
    END_DATE = date(2026, 1, 31)
    NUM_ROOMS = 25
    ROOM_NUMBERS = [1 + i for i in range(NUM_ROOMS)]
    
    # --- Data Structures ---
    
    # Generate the list of dates for the header
    date_range = [START_DATE + timedelta(days=i) for i in range((END_DATE - START_DATE).days + 1)]
    date_strings = [d.isoformat() for d in date_range]
    
    # Initialize the calendar grid
    # calendar[room_number][date_string] = booking_id
    calendar = {room: {dt: "" for dt in date_strings} for room in ROOM_NUMBERS}

    # --- Read Bookings and Populate Calendar ---
    try:
        with open(SOURCE_FILE, "r", newline="") as f:
            reader = csv.DictReader(f)
            for booking in reader:
                room_number = int(booking["room_number"])
                booking_id = booking["booking_id"]
                check_in = date.fromisoformat(booking["check_in_date"])
                check_out = date.fromisoformat(booking["check_out_date"])

                # Fill in the dates for this booking
                current_date = check_in
                while current_date < check_out:
                    date_str = current_date.isoformat()
                    if room_number in calendar and date_str in calendar[room_number]:
                        calendar[room_number][date_str] = booking_id
                    current_date += timedelta(days=1)
    except FileNotFoundError:
        print(f"Error: The file '{SOURCE_FILE}' was not found.")
        return
        
    # --- Write Calendar View to CSV ---
    header = ["room_number"] + date_strings

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for room_number in ROOM_NUMBERS:
            row = [room_number] + [calendar[room_number][dt] for dt in date_strings]
            writer.writerow(row)

    print(f"Successfully generated '{OUTPUT_FILE}'")

if __name__ == "__main__":
    create_calendar_view()
