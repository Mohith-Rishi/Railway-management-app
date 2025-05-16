import tkinter as tk
from tkcalendar import DateEntry
from datetime import datetime
import mysql.connector
from tkinter import messagebox, simpledialog
import random

def book_ticket(train_id, no_of_seats, passenger_id):
    try:
        # Database connection
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Rishi@1922',
            database='railwayscheduling'
        )
        cursor = connection.cursor()

        # Start a transaction
        connection.start_transaction()

        # Check train details (pickup and destination stations)
        check_query = """
            SELECT DepartureStation.station_name AS PickupStation, ArrivalStation.station_name AS DestinationStation
            FROM Availability A
            JOIN Station DepartureStation ON A.pickup_station = DepartureStation.station_id
            JOIN Station ArrivalStation ON A.destination_station = ArrivalStation.station_id
            WHERE A.Train_id = %s
        """

        cursor.execute(check_query, (train_id,))                                    
        result = cursor.fetchone()

        if not result:
            messagebox.showerror("Booking Error", "Train not found.")
            return

        pickup_station = result[0]  # Departure station
        destination_station = result[1]  # Arrival station

        # **Ensure no unread results remain in the cursor**
        cursor.fetchall()

        # Check seat availability
        seat_check_query = "SELECT No_of_seats FROM Train WHERE Train_id = %s"
        cursor.execute(seat_check_query, (train_id,))
        available_seats = cursor.fetchone()

        if not available_seats or no_of_seats > available_seats[0]:
            messagebox.showerror("Booking Error", "Not enough seats available.")
            return

        # **Ensure no unread results remain in the cursor**
        cursor.fetchall()

        # Deduct seats from the Train table
        update_query = "UPDATE Train SET No_of_seats = No_of_seats - %s WHERE Train_id = %s"
        cursor.execute(update_query, (no_of_seats, train_id))

        # Insert rows into Tickets table for each booked seat
        ticket_query = """
            INSERT INTO Tickets (ticket_id, passengerId, pickup_station, destination_station, train_id)
            VALUES (%s, %s, %s, %s, %s)
        """

        for _ in range(no_of_seats):
            # Generate a unique ticket ID
            while True:
                ticket_id = random.randint(1000, 9999)
                cursor.execute("SELECT COUNT(*) FROM Tickets WHERE ticket_id = %s", (ticket_id,))
                if cursor.fetchone()[0] == 0:  # Ensure unique ID
                    break

            # **Ensure no unread results remain in the cursor**
            cursor.fetchall()

            cursor.execute(ticket_query, (ticket_id, passenger_id, pickup_station, destination_station, train_id))

        # Commit the transaction
        connection.commit()
        messagebox.showinfo("Booking Success", f"Successfully booked {no_of_seats} seat(s) on Train ID {train_id}.")

    except mysql.connector.Error as err:
        # Rollback in case of any error
        connection.rollback()
        messagebox.showerror("Dbase Error", f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
