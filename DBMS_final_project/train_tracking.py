# train_tracking.py
import tkinter as tk
import mysql.connector
from tkinter import messagebox

def track_train(train_id, track_date, parent_window):
    try:
        # Database connection
        connection = mysql.connector.connect(
            host='localhost',         # Replace with your MySQL server address
            user='root',              # Replace with your MySQL username
            password='Rishi@1922',    # Replace with your MySQL password
            database='railwayscheduling'  # Replace with your database name
        )
        cursor = connection.cursor()

        # SQL query to fetch train route
        query = """
            SELECT Station.station_name, T.Arrival_time, T.Departure_time, T.Platform_number
            FROM Timing T
            JOIN Station ON T.station_id = Station.station_id
            WHERE T.Train_id = %s
              AND DATE(T.Arrival_time) = %s
            ORDER BY T.Arrival_time;
        """
        cursor.execute(query, (train_id, track_date))
        results = cursor.fetchall()

        # Create a new window to display train route
        track_window = tk.Toplevel(parent_window)
        track_window.title(f"Track Train {train_id}")
        track_window.geometry("400x400")
        tk.Label(track_window, text=f"Train ID: {train_id}", font=("Arial", 14, "bold")).pack(pady=10)

        if results:
            for row in results:
                station_name, arrival_time, departure_time, platform = row
                platform_text = f"Platform: {platform}" if platform else "Platform: Info unavailable"
                tk.Label(
                    track_window,
                    text=f"{station_name}\nArrival: {arrival_time.strftime('%H:%M')}\n"
                         f"Departure: {departure_time.strftime('%H:%M') if departure_time else 'N/A'}\n{platform_text}",
                    font=("Arial", 10),
                    bg="white",
                    anchor="w",
                    justify="left"
                ).pack(fill="x", padx=10, pady=5)
        else:
            tk.Label(track_window, text="No route information available", font=("Arial", 10), fg="red").pack(pady=10)

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()