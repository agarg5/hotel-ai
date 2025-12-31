# booking_agent.py

import csv
import os
import json
from datetime import date, timedelta, datetime
import re
from collections import defaultdict
from dotenv import load_dotenv
from openai import OpenAI

# --- INITIALIZATION ---
load_dotenv()
try:
    client = OpenAI()
    print("[INFO] OpenAI client initialized successfully.")
except Exception as e:
    print(f"[ERROR] Failed to initialize OpenAI client: {e}")
    client = None

def llm_parse_booking_request(text, today=date(2026, 1, 5)):
    """
    Uses the OpenAI API to parse a natural language booking request.
    """
    if not client:
        print("[ERROR] OpenAI client not available. Cannot process request.")
        return None

    prompt_template = """
You are an expert booking assistant. Your task is to extract booking information from a user's request.
The current date is {today}.
Analyze the following user request and provide the check-in date and check-out date in a strict JSON format.

The JSON output must have two keys: "check_in_date" and "check_out_date", with dates in "YYYY-MM-DD" format.
If you cannot determine the dates from the text, return a JSON object with null values for both keys.

User Request:
---
{request}
---

JSON Output:
"""
    prompt = prompt_template.format(today=today.strftime('%Y-%m-%d'), request=text)

    print("[INFO] Calling OpenAI API to parse dates...")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts dates and returns JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=150,
        )
        
        response_text = response.choices[0].message.content
        print(f"[INFO] Received API response: {response_text}")
        
        name_match = re.search(r"(?:my name is|i'm|i am|mi nombre es|je m'appelle)\s+([a-zA-Z\.\s]+)(?=,|$|\s+I'd|\s+and|\s+we)", text, re.IGNORECASE)
        guest_name = name_match.group(1).strip() if name_match else "Guest"
        
        date_data = json.loads(response_text)
        check_in_str = date_data.get("check_in_date")
        check_out_str = date_data.get("check_out_date")

        if check_in_str and check_out_str:
            return {
                "guest_name": guest_name,
                "check_in_date": date.fromisoformat(check_in_str),
                "check_out_date": date.fromisoformat(check_out_str)
            }
        else:
            return None

    except Exception as e:
        print(f"[ERROR] An error occurred during OpenAI API call: {e}")
        return None

def parse_policies(policy_file="hotel_policy.txt"):
    discount_rules = []
    try:
        with open(policy_file, "r") as f:
            for line in f:
                match = re.search(r"-\s*for stays of (\d+) nights or longer, a (\d+)% discount", line, re.IGNORECASE)
                if match:
                    nights, percentage = map(int, match.groups())
                    discount_rules.append({"nights": nights, "percentage": percentage})
    except FileNotFoundError:
        pass
    return sorted(discount_rules, key=lambda x: x["nights"], reverse=True)

def get_all_bookings(bookings_file="bookings.csv"):
    try:
        with open(bookings_file, "r") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        print(f"Error: The bookings file '{bookings_file}' was not found.")
        return []

def check_availability(check_in, check_out, all_bookings):
    NUM_ROOMS = 25
    ALL_ROOMS = {str(i) for i in range(1, NUM_ROOMS + 1)}
    booked_rooms = set()
    stay_dates = {check_in + timedelta(days=i) for i in range((check_out - check_in).days)}
    for booking in all_bookings:
        booking_check_in = date.fromisoformat(booking["check_in_date"])
        booking_check_out = date.fromisoformat(booking["check_out_date"])
        booking_dates = {booking_check_in + timedelta(days=i) for i in range((booking_check_out - booking_check_in).days)}
        if not stay_dates.isdisjoint(booking_dates):
            booked_rooms.add(booking["room_number"])
    return sorted(list(ALL_ROOMS - booked_rooms), key=int)

def find_split_stay_options(check_in, check_out, all_bookings):
    NUM_ROOMS = 25
    ALL_ROOMS = {str(i) for i in range(1, NUM_ROOMS + 1)}
    daily_booked_rooms = defaultdict(set)
    for booking in all_bookings:
        current_date = date.fromisoformat(booking["check_in_date"])
        end_date = date.fromisoformat(booking["check_out_date"])
        while current_date < end_date:
            daily_booked_rooms[current_date].add(booking["room_number"])
            current_date += timedelta(days=1)
    solution, current_date = [], check_in
    while current_date < check_out:
        available_rooms_today = sorted(list(ALL_ROOMS - daily_booked_rooms[current_date]), key=int)
        if not available_rooms_today: return None
        room_for_segment = available_rooms_today[0]
        segment_start_date = current_date
        segment_end_date = current_date
        while segment_end_date < check_out:
            if room_for_segment in daily_booked_rooms[segment_end_date]: break
            segment_end_date += timedelta(days=1)
        solution.append({"room": room_for_segment, "check_in": segment_start_date, "check_out": segment_end_date})
        current_date = segment_end_date
    return solution

def handle_booking_request(request_text):
    print(f"--- Handling Request ---\n'{request_text}'")
    
    parsed_request = llm_parse_booking_request(request_text)
    policies = parse_policies()
    
    if not parsed_request:
        print("\n[CONCLUSION]\nI'm sorry, I could not understand the dates in your request.")
        return
        
    guest_name = parsed_request['guest_name']
    check_in = parsed_request['check_in_date']
    check_out = parsed_request['check_out_date']
    stay_duration = (check_out - check_in).days
    
    print(f"\n[PARSED]\nGuest: {guest_name}, Check-in: {check_in}, Check-out: {check_out} ({stay_duration} nights)")
    
    all_bookings = get_all_bookings()
    if not all_bookings: return

    available_rooms = check_availability(check_in, check_out, all_bookings)
    
    booking_possible = False
    if available_rooms:
        booking_possible = True
        print(f"\n[CONCLUSION]\nGood news! We have {len(available_rooms)} rooms available for your requested dates.")
        print(f"Available rooms: {', '.join(available_rooms)}")
    else:
        print("\n[INFO]\nNo single room is available for the entire duration. Checking for a split-stay option...")
        split_option = find_split_stay_options(check_in, check_out, all_bookings)
        if split_option and len(split_option) > 1:
            booking_possible = True
            print("\n[CONCLUSION]\nWe can accommodate your request, but it would require a room change.")
            for i, segment in enumerate(split_option):
                duration = (segment['check_out'] - segment['check_in']).days
                print(f"  - Part {i+1}: Stay in Room {segment['room']} from {segment['check_in']} to {segment['check_out']} ({duration} night/s)")
        else:
            print("\n[CONCLUSION]\nSorry, we are fully booked and cannot accommodate your request even with a room change.")

    if booking_possible:
        for rule in policies:
            if stay_duration >= rule["nights"]:
                print(f"\n[POLICY APPLIED]\nThis booking of {stay_duration} nights qualifies for a {rule['percentage']}% discount!")
                break

if __name__ == "__main__":
    
    print("--- DEMONSTRATING REAL LLM DATE PARSING AND POLICY ---")
    print("\n" + "="*40 + "\n")
    request_1 = "Hi, my name is Alex. I'd like to book a room for tomorrow for a week."
    handle_booking_request(request_1)
    print("\n" + "="*40 + "\n")
    request_2 = "Hola, mi nombre es Maria. Necesito una habitación para 2 noches a partir de mañana."
    handle_booking_request(request_2)
    print("\n" + "="*40 + "\n")
    request_3 = "Bonjour, je m'appelle Pierre. Je voudrais une chambre du 10 au 12 février."
    handle_booking_request(request_3)
    print("\n" + "="*40 + "\n")
    request_4 = "Do you have any rooms?"
    handle_booking_request(request_4)