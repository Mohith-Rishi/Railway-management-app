# login.py
import tkinter as tk
from tkinter import Toplevel, messagebox
import random
import mysql.connector

# Function to open the sign-up popup
def open_signup_popup(root):
    popup = Toplevel(root)
    popup.title("User Sign Up")
    popup.geometry("400x300")

    label = tk.Label(popup, text="Enter User Details", font=('Arial', 14))
    label.pack(pady=10)

    # Labels and input fields
    labels = ['First Name', 'Last Name', 'Aadhar Id', 'Date of Birth', 'Contact No', 'Email Id', 'Create Password']
    entries = []

    for label_text in labels:
        frame = tk.Frame(popup)
        frame.pack(pady=5)

        lbl = tk.Label(frame, text=label_text, width=15, anchor='w')
        lbl.pack(side='left', padx=5)

        entry = tk.Entry(frame, width=30)
        entry.pack(side='left')
        entries.append(entry)

    # Generate a unique PassengerId
    def generate_passenger_id():
        return random.randint(100000, 999999)

    # Function to handle sign-up
    def signup():
        user_details = [entry.get() for entry in entries]
        if all(user_details):
            passenger_id = generate_passenger_id()
            try:
                connection = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='Rishi@1922',
                    database='railwayscheduling'
                )
                cursor = connection.cursor()

                # Insert data into the Passenger table
                insert_query = """
                
                CALL InsertPassenger(%s, %s, %s, %s, %s, %s, %s, %s);

                """
                cursor.execute(insert_query, (passenger_id, *user_details))
                connection.commit()
                
                fetch_log_query = """
                SELECT Message FROM ActionLog
                ORDER BY CreatedAt DESC
                LIMIT 1;
                """
                cursor.execute(fetch_log_query)
                result = cursor.fetchone()

                if result:
                    messagebox.showinfo("Trigger Message", result[0])
                else:
                    messagebox.showinfo("Sign Up", "User registered successfully, but no trigger message found.")

                popup.destroy()
                
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
        else:
            messagebox.showwarning("Missing Info", "Please fill in all fields.")

    signup_button = tk.Button(popup, text="Sign Up", command=signup)
    signup_button.pack(pady=20)
