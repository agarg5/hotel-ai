# AI Hotel Booking Agent

This project implements a simulated AI hotel booking agent designed to process booking requests, check room availability, suggest split stays, and apply hotel policies. It leverages the OpenAI API for natural language understanding to parse booking requests from various sources like email or messaging platforms.

## Project Overview

The core of the project is `booking_agent.py`, which orchestrates the booking process. It interacts with:
-   `bookings.csv`: A CSV file simulating the hotel's existing reservations for 25 rooms.
-   `hotel_policy.txt`: A plain text file defining hotel rules, such as discount policies for long stays.
-   OpenAI API: Used for advanced natural language processing to understand diverse date formats and languages in booking requests.

Key features include:
-   **Booking Data Management:** `bookings.csv` stores reservation details, and `bookings_calendar_view.csv` provides a visual, calendar-like overview of room occupancy.
-   **Flexible Room Numbering:** Rooms are numbered 1 through 25 for simplicity.
-   **Split-Stay Suggestions:** If a single room isn't available for the entire duration of a request, the agent attempts to find a solution by suggesting a room change during the stay.
-   **Multilingual Natural Language Understanding:** Utilizes the OpenAI API to extract check-in and check-out dates from free-form text requests, supporting multiple languages and relative date expressions.
-   **Policy Application:** Reads and applies rules defined in `hotel_policy.txt`, such as offering discounts for extended stays.

## Building and Running

This project uses Python and requires an OpenAI API key. It is recommended to use a Python virtual environment to manage dependencies.

### Setup

1.  **Create a Virtual Environment (if not already done):**
    ```bash
    python3 -m venv venv
    ```

2.  **Activate the Virtual Environment:**
    *   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
    *   **Windows (Command Prompt):**
        ```bash
        venv\Scripts\activate.bat
        ```
    *   **Windows (PowerShell):**
        ```bash
        venv\Scripts\Activate.ps1
        ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    (Note: `requirements.txt` should contain `openai` and `python-dotenv`.)

4.  **Configure OpenAI API Key:**
    Create a file named `.env` in the root directory of the project and add your OpenAI API key to it:
    ```
    OPENAI_API_KEY='your_openai_api_key_here'
    ```
    Replace `'your_openai_api_key_here'` with your actual key. This file is ignored by Git (`.gitignore`) for security.

### Data Generation (Optional)

The project includes scripts to generate simulated booking data:

-   **`create_bookings_csv.py`:** Generates `bookings.csv` with simulated reservations.
    ```bash
    python3 create_bookings_csv.py
    ```
-   **`create_calendar_view.py`:** Generates `bookings_calendar_view.csv`, a calendar-style view of the bookings.
    ```bash
    python3 create_calendar_view.py
    ```

### Running the Agent

With the virtual environment activated and the `.env` file configured, run the main booking agent:

```bash
python3 booking_agent.py
```

This will execute several predefined test cases demonstrating its functionality.

## Development Conventions

-   **Language:** Python 3.x
-   **Data Storage:** Booking data is managed in CSV files (`bookings.csv`). Hotel policies are stored in a plain text file (`hotel_policy.txt`).
-   **Dependencies:** Managed via `requirements.txt` and Python virtual environments.
-   **Natural Language Processing:** Leverages the OpenAI API for date and intent extraction.
-   **Code Structure:** Functions are organized within `booking_agent.py` for parsing requests, checking availability, finding split-stay options, and applying policies.
