# import tkinter as tk
# import mysql.connector
# from tkinter import messagebox

# def view_journey(train_id, password):
#     try:
#         # Establish database connection
#         connection = mysql.connector.connect(
#             host='localhost',
#             user='root',
#             password='Rishi@1922',
#             database='railwayscheduling'
#         )
#         cursor = connection.cursor()

#         # Validate passenger using the password
#         passenger_query = "SELECT PassengerId FROM Passenger WHERE Password = %s"
#         cursor.execute(passenger_query, (password,))
#         passenger = cursor.fetchone()

#         if passenger:
#             pass_id = passenger[0]  # Extract PassengerId

#             # Fetch the journey details for the provided train ID and PassengerId
#             journey_query = """
#                 SELECT T.ticket_id, T.pickup_station, T.destination_station, Tr.Train_name, Tr.No_of_seats
#                 FROM Tickets T
#                 JOIN Train Tr ON T.train_id = Tr.Train_id
#                 WHERE T.train_id = %s AND T.PassengerId = %s
#             """
#             cursor.execute(journey_query, (train_id, pass_id))
#             journeys = cursor.fetchall()

#             if journeys:
#                 # Display journey details in a new window
#                 journey_window = tk.Toplevel(root)
#                 journey_window.title("Your Journey")
#                 journey_window.geometry("400x300")
#                 journey_window.configure(bg="#ecf0f1")

#                 heading_label = tk.Label(journey_window, text="Your Journey Details", font=("Arial", 16, "bold"), bg="#ecf0f1")
#                 heading_label.pack(pady=10)

#                 for journey in journeys:
#                     ticket_id, pickup_station, destination_station, train_name, seats_left = journey
#                     journey_details = (
#                         f"Ticket ID: {ticket_id}\n"
#                         f"Train Name: {train_name}\n"
#                         f"From: {pickup_station}\n"
#                         f"To: {destination_station}\n"
#                         f"Seats Left: {seats_left}\n"
#                         "----------------------------------"
#                     )
#                     journey_label = tk.Label(journey_window, text=journey_details, font=("Arial", 12), bg="#ecf0f1", anchor="w", justify="left")
#                     journey_label.pack(pady=5, padx=10)
#             else:
#                 messagebox.showerror("No Journey Found", "No journeys found for the provided Train ID and password.")
#         else:
#             messagebox.showerror("Authentication Error", "Incorrect password.")

#     except mysql.connector.Error as err:
#         messagebox.showerror("Database Error", f"Error: {err}")
#     finally:
#         if connection.is_connected():
#             cursor.close()
#             connection.close()