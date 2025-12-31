# AI Hotel Booking Agent - Demo

Welcome to the AI Hotel Booking Agent demo! This tool helps you quickly and easily book hotel rooms. Think of it as a smart assistant that understands your requests and finds the best options for your stay.

## What can it do?

Our AI Booking Agent can:

*   **Understand what you need:** Just tell it when you want to check in and check out, and for how many people. You can use natural language, just like you're talking to a person!
    *   *Example:* "I need a room for two nights in July."
    *   *Example:* "Can I book a room from January 10th to January 15th?"
    *   *Example:* "I'm looking for a room for a week next month."
*   **Check room availability:** It knows which rooms are free and when.
*   **Suggest "split stays":** If a single room isn't available for your entire trip, it can suggest splitting your stay between two different rooms to make your booking work.
*   **Apply hotel policies:** It automatically checks for and applies any special rules, like discounts for longer stays.

## How do you use it?

You simply provide your booking request, and the agent will process it.

### Example Booking Request:

Let's say you want to book a room. You might provide a request like this:

> "I'd like to book a room for John Smith for three nights, checking in on March 1st. My email is john.smith@example.com."

### What happens next?

The agent will read your request, figure out the dates (March 1st for three nights means checking out on March 4th), check for an available room, and then confirm your booking or offer alternatives.

### Example Responses:

*   **Successful Booking:**
    > "Great news, John Smith! Your booking for room 5 from March 1st to March 4th has been confirmed. A confirmation email has been sent to john.smith@example.com."

*   **Split-Stay Suggestion:**
    > "Unfortunately, Room 10 is not available for your entire stay. However, we can offer you Room 10 from January 10th to January 12th, and then Room 12 from January 12th to January 15th. Would you like to proceed with this split stay?"

*   **Policy Applied:**
    > "Your 7-night stay qualifies for our extended stay discount, saving you 15% on your booking!"

This agent makes booking a hotel room straightforward and efficient, handling all the complex availability checks and policy applications for you!

---

## Technical Note

**Data Management:** The `bookings.csv` file serves as the source of truth for all hotel reservations. When the owner confirms a booking (after reviewing the AI-generated draft), the system automatically updates this CSV file to maintain accurate, real-time availability information. All availability checks and split-stay suggestions are based on the current state of this file.
