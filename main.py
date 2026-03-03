from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from booking_agent import (
    llm_parse_booking_request,
    parse_policies,
    get_room_details,
    get_all_bookings,
    check_availability,
    find_split_stay_options,
    calculate_price,
)

app = FastAPI(title="Hotel AI Booking Agent")


class BookingRequest(BaseModel):
    request_text: str


@app.get("/")
def root():
    return {
        "service": "Hotel AI Booking Agent",
        "endpoints": {
            "POST /booking": "Process a natural-language booking request",
            "GET /health": "Health check",
        },
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/booking")
def booking(req: BookingRequest):
    parsed = llm_parse_booking_request(req.request_text)
    if not parsed:
        raise HTTPException(
            status_code=422,
            detail="Could not parse booking dates from the request.",
        )

    guest_name = parsed["guest_name"]
    check_in = parsed["check_in_date"]
    check_out = parsed["check_out_date"]
    num_guests = parsed["num_guests"]
    stay_duration = (check_out - check_in).days

    policies = parse_policies()
    room_details = get_room_details()
    all_bookings = get_all_bookings()

    available_rooms = check_availability(
        check_in, check_out, all_bookings, room_details, num_guests
    )

    result = {
        "guest_name": guest_name,
        "check_in": check_in.isoformat(),
        "check_out": check_out.isoformat(),
        "num_guests": num_guests,
        "stay_nights": stay_duration,
        "booking_possible": False,
        "available_rooms": [],
        "split_stay": None,
        "estimated_price": 0,
        "discount_applied": None,
    }

    if available_rooms:
        result["booking_possible"] = True
        result["available_rooms"] = available_rooms
        result["estimated_price"] = calculate_price(
            room_details, [available_rooms[0]], check_in, check_out, policies
        )
    else:
        split_option = find_split_stay_options(
            check_in, check_out, all_bookings, room_details, num_guests
        )
        if split_option and len(split_option) > 1:
            result["booking_possible"] = True
            result["split_stay"] = [
                {
                    "room": seg["room"],
                    "check_in": seg["check_in"].isoformat(),
                    "check_out": seg["check_out"].isoformat(),
                    "nights": (seg["check_out"] - seg["check_in"]).days,
                }
                for seg in split_option
            ]
            result["estimated_price"] = calculate_price(
                room_details, split_option, check_in, check_out, policies
            )

    # Check for applicable discount
    if result["booking_possible"]:
        for rule in policies:
            if stay_duration >= rule["nights"]:
                result["discount_applied"] = {
                    "nights_threshold": rule["nights"],
                    "percentage": rule["percentage"],
                }
                break

    return result
