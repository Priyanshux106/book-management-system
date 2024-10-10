import mysql.connector
import time  # For simulating the payment delay

# Connect to MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="shinoy2013",
    database="movie_ticket_db"
)

cursor = connection.cursor()

# Function to select city (just for interaction, not used)
def select_city():
    print("Enter your city:")
    city = input("City: ")
    print(f"Welcome from {city}!")

# Function to select movie
def select_movie():
    movies = {
        1: "The Dark Knight",
        2: "No Country for Old Men",
        3: "Goodfellas",
        4: "Once Upon a Time in Hollywood",
        5: "Kalki 2898AD"
    }
    while True:
        print("Available Movies:")
        for k, v in movies.items():
            print(f"{k}. {v}")
        choice = int(input("Select a movie (S No.1-5): "))
        if choice in movies:
            return movies[choice]
        else:
            print("Invalid choice. Please select a valid movie.")

# Function to select theater
def select_theater():
    theaters = {
        1: "PVR",
        2: "INOX",
        3: "IMAX",
        4: "Star World Cinema",
        5: "The Palace"
    }
    while True:
        print("Available Theaters:")
        for k, v in theaters.items():
            print(f"{k}. {v}")
        choice = int(input("Select a theater (1-5): "))
        if choice in theaters:
            return theaters[choice]
        else:
            print("Invalid choice. Please select a valid theater.")

# Function to select showtime (renamed variable to avoid conflict with time module)
def select_show_time():
    times = {
        1: "9:45",
        2: "12:00",
        3: "15:00",
        4: "18:00",
        5: "21:00"
    }
    while True:
        print("Available Showtimes:")
        for k, v in times.items():
            print(f"{k}. {v}")
        choice = int(input("Select a showtime (1-5): "))
        if choice in times:
            return times[choice]
        else:
            print("Invalid choice. Please select a valid showtime.")

import re

# Function to select seat (coordinate system with validation)
def select_seat():
    while True:
        seat = input("Enter seat (e.g., A-12): ")
        # Regex pattern to match valid seat format (A-N for rows, 1-14 for numbers)
        if re.match(r"^[A-N]-(1[0-4]|[1-9])$", seat):
            return seat
        else:
            print("Invalid seat format. Please choose a valid seat between A-N and 1-14 (e.g., A-12, B-9, D-7).")

# Example usage within the main flow
def main():
    select_city()
    user_name = input("Enter your name: ")
    movie = select_movie()
    theater = select_theater()
    show_time = select_show_time()  # Updated variable name here
    seat = select_seat()  # Seat validation happens here
    payment_method = process_payment()
    confirm_ticket(user_name, movie, theater, show_time, seat, payment_method)

# Function to process payment
def process_payment():
    print("Payment Options:")
    print("1. UPI")
    print("2. Card")
    while True:
        choice = int(input("Choose payment method (1 or 2): "))
        if choice == 1:
            return "UPI"
        elif choice == 2:
            return "Card"
        else:
            print("Invalid choice. Please select a valid payment method.")

# Function to confirm ticket
def confirm_ticket(user_name, movie, theater, show_time, seat, payment_method):
    print("Please wait! The payment is being completed...")
    time.sleep(5)  # Simulating payment delay
    print("Payment completed!")
    
    # Insert ticket info into database
    cursor.execute(
        "INSERT INTO Confirmed_Tickets (user_name, movie_name, theater_name, show_time, seat, payment_method) VALUES (%s, %s, %s, %s, %s, %s)",
        (user_name, movie, theater, show_time, seat, payment_method)
    )
    connection.commit()

    # Ticket confirmation
    print("\n--- Ticket Confirmation ---")
    print(f"Movie: {movie}")
    print(f"Theater: {theater}")
    print(f"Time: {show_time}")
    print(f"Seat: {seat}")
    print(f"Payment Method: {payment_method}")
    print("---------------------------")

# Main function to run the program
def main():
    select_city()
    user_name = input("Enter your name: ")
    movie = select_movie()
    theater = select_theater()
    show_time = select_show_time()  # Updated variable name here
    seat = select_seat()
    payment_method = process_payment()
    confirm_ticket(user_name, movie, theater, show_time, seat, payment_method)

# Run the program
if __name__ == "__main__":
    main()

# Close the connection after completion
cursor.close()
connection.close()
