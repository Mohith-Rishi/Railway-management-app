import tkinter as tk
from tkcalendar import DateEntry
from datetime import datetime
import mysql.connector
from tkinter import messagebox, simpledialog

from ticket_avail_desc import  book_ticket
from train_tracking import track_train

def open_homepage(root, passenger_id):
    # Create a new window
    homepage = tk.Toplevel(root)
    homepage.title("Book your Journey")
    homepage.geometry("300x500")
    homepage.configure(bg="#27ae60")

    # Heading label
    heading_label = tk.Label(homepage, text="Book your Journey", font=("Arial", 18, "bold"), bg="#27ae60", fg="white")
    heading_label.pack(pady=(20, 10))


    # Departure city entry
    departure_label = tk.Label(homepage, text="Departure City", font=("Arial", 10), bg="#27ae60", fg="white")
    departure_label.pack(pady=(10, 5))
    departure_entry = tk.Entry(homepage, font=("Arial", 16), width=20)
    departure_entry.insert(0, "")
    departure_entry.pack(pady=5)

    # Destination city entry
    destination_label = tk.Label(homepage, text="Destination City", font=("Arial", 10), bg="#27ae60", fg="white")
    destination_label.pack(pady=5)
    destination_entry = tk.Entry(homepage, font=("Arial", 16), width=20)
    destination_entry.insert(0, "")
    destination_entry.pack(pady=5)

    # Date selection label
    date_label = tk.Label(homepage, text="Select Departure Date", font=("Arial", 10), bg="#27ae60", fg="white")
    date_label.pack(pady=(10, 0))

    # Date Entry (Calendar Picker)
    date_entry = DateEntry(homepage, width=15, background="white", foreground="black", borderwidth=2)
    date_entry.pack(pady=10)

    # Result display area
    results_frame = tk.Frame(homepage, bg="white")
    results_frame.pack(fill="both", expand=True, padx=10, pady=(10, 0))

   
    bottom_button_frame = tk.Frame(homepage, bg="#27ae60")
    bottom_button_frame.pack(side="bottom", fill="x", pady=10)               


    # Function to search for available trains
    def search_trains():
        departure_city = departure_entry.get()
        destination_city = destination_entry.get()
        departure_date = date_entry.get_date()

        try:
            # Database connection
            connection = mysql.connector.connect(
                host='localhost',         # Replace with your MySQL server address
                user='root',              # Replace with your MySQL username
                password='Rishi@1922',    # Replace with your MySQL password
                database='railwayscheduling'  # Replace with your database name
            )
            cursor = connection.cursor()
            #GetJourneyDuration(T1.Departure_time, T2.Arrival_time)
            # SQL query to find trains with available seats
            query ="""
                SELECT Train.Train_id, Train.Train_name, 
                    DepartureStation.station_name AS Departure_Station,
                    ArrivalStation.station_name AS Arrival_Station,
                    T1.Departure_time, T2.Arrival_time,
                    Train.No_of_seats,
                    (T2.Arrival_time-T1.Departure_time) AS journey_duration
                FROM Timing T1
                JOIN Timing T2 ON T1.Train_id = T2.Train_id
                JOIN Train ON T1.Train_id = Train.Train_id
                JOIN Station DepartureStation ON T1.station_id = DepartureStation.station_id
                JOIN Station ArrivalStation ON T2.station_id = ArrivalStation.station_id
                WHERE DepartureStation.city = %s
                AND ArrivalStation.city = %s
                AND DATE(T1.Departure_time) = %s
                AND T1.Arrival_time < T2.Arrival_time
                ORDER BY T1.Departure_time
            """

            cursor.execute(query, (departure_city, destination_city, departure_date))
            results = cursor.fetchall()

            # Clear previous results
            for widget in results_frame.winfo_children():
                widget.destroy()
            if results:
                # Add route label
                route_label = tk.Label(
                    results_frame, 
                    text=f"{departure_city} to {destination_city}", 
                    font=("Arial", 12, "bold"), 
                    bg="white", 
                    fg="#27ae60"
                )
                route_label.pack(pady=(10, 10))

                for idx, row in enumerate(results, start=1):
                    train_id, train_name, departure_station, arrival_station, departure_time, arrival_time, no_of_seats, journey_duration = row

                    # Format result text
                    result_text = (
                        f"{train_id} - {train_name}\n"
                        f"{departure_time.strftime('%Y-%m-%d %H:%M')} {departure_station[:3].upper()}  "
                        f"--- {journey_duration} ---  "
                        f"{arrival_time.strftime('%Y-%m-%d %H:%M')} {arrival_station[:3].upper()}\n"
                        f"Seats Left: {no_of_seats}"
                    )

                    # Display each train result
                    result_label = tk.Label(results_frame, text=result_text, font=("Arial", 10), bg="white", anchor="w", justify="left")
                    result_label.pack(fill="x", padx=10, pady=(5, 0))

                    # Create a frame to hold the Book and Track buttons side-by-side
                    button_frame = tk.Frame(results_frame, bg="white")
                    button_frame.pack(fill="x", padx=10, pady=(0, 10))

                    # Book Button with prompt for number of seats
                    book_button = tk.Button(
                        button_frame,
                        text="Book",
                        font=("Arial", 10),
                        fg="white",
                        bg="#27ae60",
                        command=lambda tid=train_id: book_ticket_prompt(tid)
                    )
                    book_button.pack(side="left", padx=5, pady=5)

                    # Track Button
                    track_button = tk.Button(
                        button_frame,
                        text="Track",
                        font=("Arial", 10),
                        fg="white",
                        bg="#1f78d1",
                        command=lambda tid=train_id, tdate=departure_date: track_train(tid, tdate, homepage)  # Pass homepage and date
                    )
                    track_button.pack(side="left", padx=5, pady=5)


            else:
                no_result_label = tk.Label(results_frame, text="No trains available", font=("Arial", 10), bg="white", fg="red")
                no_result_label.pack(pady=10)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    # Function to prompt for seats and book a ticket
    def book_ticket_prompt(train_id):
        no_of_seats = simpledialog.askinteger("Seats", "Enter number of seats:", minvalue=1, maxvalue=10)
        if no_of_seats:
            # Call the book_ticket function
            print(f"Booking Ticket -> Train ID: {train_id}, Seats: {no_of_seats}, Passenger ID: {passenger_id}")

            book_ticket(train_id, no_of_seats, passenger_id)
            search_trains()
    
    search_button = tk.Button(homepage, text="Search", font=("Arial", 14), bg="white", fg="#27ae60", width=15, command=search_trains)
    search_button.pack(pady=20)
    def cancel_ticket(train_id, password):
        try:
            # Establish database connection
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Rishi@1922',
                database='railwayscheduling'
            )
            cursor = connection.cursor()

            # Fetch `passengerId` from the `Passenger` table based on the provided password
            passenger_query = "SELECT passengerId FROM Passenger WHERE Password = %s"
            cursor.execute(passenger_query, (password,))
            passenger = cursor.fetchone()

            if passenger:
                passenger_id = passenger[0]  # Extract `passengerId`

                # Verify if a ticket exists for the given `Train_Id` and `passengerId`
                ticket_check_query = """
                    SELECT COUNT(*) FROM Tickets 
                    WHERE Train_id = %s AND passengerId = %s
                """
                cursor.execute(ticket_check_query, (train_id, passenger_id))
                ticket_count = cursor.fetchone()[0]

                if ticket_count > 0:
                    # Delete the ticket(s) for the specified `Train_Id` and `passengerId`
                    cancel_query = """
                       CALL DeleteTicket(%s,%s);

                    """
                    cursor.execute(cancel_query, (train_id, passenger_id))
                    deleted_tickets_count = cursor.rowcount

                    # Confirm cancellation
                    messagebox.showinfo("Cancellation Success", f"All tickets for Train ID {train_id} have been canceled.")
                else:
                    messagebox.showerror("Cancellation Error", "No tickets found for the provided Train ID and credentials.")
                update_seats_query = """
                UPDATE Train 
                SET No_of_seats = No_of_seats + %s 
                WHERE Train_id = %s
                """
                cursor.execute(update_seats_query, (deleted_tickets_count, train_id))
                connection.commit()
            else:
                messagebox.showerror("Authentication Error", "Incorrect password. Cancellation failed.")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


    def cancel_ticket_prompt():
            # Ask for train ID and password
            train_id = simpledialog.askstring("Cancel Ticket", "Enter Train ID:")
            password = simpledialog.askstring("Cancel Ticket", "Enter Password:", show="*")
            
            if train_id and password:
                cancel_ticket(train_id, password)
            else:
                messagebox.showwarning("Input Error", "Please provide both Train ID and Password.")  

    cancel_button = tk.Button(
            bottom_button_frame, 
            text="Cancel Ticket", 
            font=("Arial", 14), 
            bg="white", 
            fg="#27ae60", 
            width=15, 
            command=cancel_ticket_prompt
        )
    cancel_button.grid(row=0, column=2, padx=30, pady=10, sticky="ew")

    view_journey(homepage)

    homepage.mainloop()
    
def view_journey(root):
    def view_journey_prompt():
        # Prompt for Train ID and Password
        train_id = simpledialog.askstring("View Journey", "Enter Train ID:")
        password = simpledialog.askstring("View Journey", "Enter Password:", show="*")

        if train_id and password:
            fetch_journey_details(train_id, password)
        else:
            messagebox.showwarning("Input Error", "Please provide both Train ID and Password.")

    def fetch_journey_details(train_id, password):
        try:
            # Establish database connection
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Rishi@1922',
                database='railwayscheduling'
            )
            cursor = connection.cursor()

            # Validate passenger using the password
            passenger_query = "SELECT passengerId FROM Passenger WHERE Password = %s"
            cursor.execute(passenger_query, (password,))
            passenger = cursor.fetchone()

            if passenger:
                passengerId = passenger[0]  # Extract passengerId

                # Fetch the journey details for the provided train ID and passengerId
                journey_query = """
                    SELECT 
                        T.pickup_station, T.destination_station, Tr.Train_name,count(*)
                    FROM Tickets T
                    JOIN Train Tr ON T.train_id = Tr.Train_id
                    WHERE T.train_id = %s AND T.passengerId = %s
                    group by T.pickup_station, T.destination_station, Tr.Train_name
                """
                cursor.execute(journey_query, (train_id, passengerId))
                journeys = cursor.fetchall()

                if journeys:
                    # Display journey details in a new window
                    journey_window = tk.Toplevel(root)
                    journey_window.title("Your Journey")
                    journey_window.geometry("400x300")
                    journey_window.configure(bg="#ecf0f1")

                    heading_label = tk.Label(journey_window, text="Your Journey Details", font=("Arial", 16, "bold"), bg="#ecf0f1")
                    heading_label.pack(pady=10)

                    for journey in journeys:
                        pickup_station, destination_station, train_name, seats_left = journey
                        journey_details = (
                            f"Train Name: {train_name}\n"
                            f"From: {pickup_station}\n"
                            f"To: {destination_station}\n"
                            f"Seats booked: {seats_left}\n"
                            "----------------------------------"
                        )
                        journey_label = tk.Label(journey_window, text=journey_details, font=("Arial", 12), bg="#ecf0f1", anchor="w", justify="left")
                        journey_label.pack(pady=5, padx=10)
                else:
                    messagebox.showerror("No Journey Found", "No journeys found for the provided Train ID and password.")
            else:
                messagebox.showerror("Authentication Error", "Incorrect password.")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    # Use `pack` inside a frame to place the button at the bottom-left corner
    bottom_frame = tk.Frame(root, bg="#27ae60")  # Create a bottom frame
    bottom_frame.pack(side="bottom", fill="x")   # Place it at the bottom of the window

    view_journey_button = tk.Button(
        bottom_frame,
        text="View Your Journey",
        font=("Arial", 14),
        bg="white",
        fg="#27ae60",
        width=20,
        command=view_journey_prompt
    )
    view_journey_button.grid(row=0, column=0, padx=30, pady=10, sticky="ew") # Align to the left inside the bottom frame

