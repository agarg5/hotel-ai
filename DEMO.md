# AI Hotel Booking Agent - Demo

Welcome to the AI Hotel Booking Agent demo! This tool helps you quickly and easily book hotel rooms. Think of it as a smart assistant that understands your requests and finds the best options for your stay.

## What can it do?

Our AI Booking Agent can:

*   **Understand what you need:** Just tell it when you want to check in and check out, and for how many people. You can use natural language, just like you're talking to a person!
    *   *Example:* "I need a room for 2 people for two nights in July."
    *   *Example:* "Can I book a room from January 10th to January 15th for my family of 4?"
    *   *Example:* "I'm looking for a room for a week next month."
*   **Check room availability:** It knows which rooms are free and when, and can match rooms based on the number of guests.
*   **Suggest "split stays":** If a single room isn't available for your entire trip, it can suggest splitting your stay between two different rooms to make your booking work.
*   **Apply hotel policies:** It automatically checks for and applies any special rules, like discounts for longer stays.
*   **Estimate Prices:** It provides an estimated cost for the stay based on the room and duration.

## How do you use it?

You simply provide your booking request, and the agent will process it.

### Example Booking Request:

Let's say you want to book a room. You might provide a request like this:

> "I'd like to book a room for John Smith and his partner for three nights, checking in on March 1st. My email is john.smith@example.com."

### Multilingual Examples:

The agent leverages advanced natural language processing to understand booking requests in various languages. Here are some examples:

*   **Spanish:**
    *   *Request:* "Quisiera reservar una habitación para dos personas por dos noches, entrando el 15 de abril." (I would like to book a room for two people for two nights, checking in on April 15th.)
    *   *Expected understanding:* Check-in: April 15th, Duration: 2 nights, Guests: 2.

*   **French:**
    *   *Request:* "Je voudrais réserver une chambre pour 3 personnes du 1er au 7 juin." (I would like to book a room for 3 people from June 1st to June 7th.)
    *   *Expected understanding:* Check-in: June 1st, Check-out: June 7th, Guests: 3.

*   **German:**
    *   *Request:* "Ich brauche ein Zimmer für fünf Nächte ab dem 10. Juli." (I need a room for five nights starting July 10th.)
    *   *Expected understanding:* Check-in: July 10th, Duration: 5 nights, Guests: 1.

### What happens next?

The agent will read your request, figure out the dates, number of guests, check for a suitable and available room, calculate an estimated price, and then confirm your booking or offer alternatives.

### Example Responses:

*   **Successful Booking:**
    > "Great news, John Smith! We have a room available for 2 guests from March 1st to March 4th. The estimated total price is 1980 DIRHAMS. Would you like to confirm?"

*   **Split-Stay Suggestion:**
    > "Unfortunately, we don't have a single room for 4 guests for your entire stay. However, we can offer you Room 1 from January 10th to January 12th, and then Room 7 from January 12th to January 15th. Would you like to proceed with this split stay? The estimated price is 3570 DIRHAMS."

*   **Policy Applied:**
    > "Your 7-night stay qualifies for our extended stay discount, saving you 10% on your booking!"

This agent makes booking a hotel room straightforward and efficient, handling all the complex availability checks and policy applications for you!

---

## Technical Note

**Data Management:** The `bookings.csv` file serves as the source of truth for all hotel reservations. When the owner confirms a booking (after reviewing the AI-generated draft), the system automatically updates this CSV file to maintain accurate, real-time availability information. All availability checks and split-stay suggestions are based on the current state of this file.
