# main.py
import tkinter as tk
from tkinter import messagebox
from login import open_signup_popup  # Import the sign-up function
import mysql.connector
from homepage import open_homepage  # Import the homepage function

# Function to handle sign-in with database check
def sign_in():
    username = username_entry.get()
    password = password_entry.get()

    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Rishi@1922',
            database='railwayscheduling'
        )
        cursor = connection.cursor()

        # Query to validate the login and get passenger_id
        query = "SELECT PassengerId FROM Passenger WHERE ContactNo = %s AND Password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result:
            passenger_id = result[0]  # Get the PassengerId from the query result
           # messagebox.showinfo("Login Successful", "Welcome!") 
            
            # Hide the login window
           # root.withdraw()

            # Open the homepage with the passenger_id
            open_homepage(root, passenger_id)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Main window setup (root)
root = tk.Tk()
root.title("User Login")

# Set the window geometry and center it on the screen
root.geometry("400x400")
root.eval('tk::PlaceWindow . center')  # Center the window on the screen

# Add a heading at the top of the login window
heading_label = tk.Label(root, text="Ticket Booking Platform", font=('Arial', 16, 'bold'))
heading_label.pack(pady=20)

# Create a frame for login form
login_frame = tk.Frame(root)
login_frame.pack(pady=20)

# Username label and entry
username_label = tk.Label(login_frame, text="Username", width=10, anchor='e')
username_label.grid(row=0, column=0, padx=5, pady=5)
username_entry = tk.Entry(login_frame, width=25)
username_entry.grid(row=0, column=1, padx=5, pady=5)

# Password label and entry
password_label = tk.Label(login_frame, text="Password", width=10, anchor='e')
password_label.grid(row=1, column=0, padx=5, pady=5)
password_entry = tk.Entry(login_frame, width=25, show='*')
password_entry.grid(row=1, column=1, padx=5, pady=5)

# Sign In button
sign_in_button = tk.Button(login_frame, text="Sign In", command=sign_in)
sign_in_button.grid(row=2, column=0, columnspan=2, pady=20, ipadx=30)

# Label and Sign Up button for new users
new_user_label = tk.Label(login_frame, text="New user?")
new_user_label.grid(row=3, column=0, columnspan=2)
signup_button = tk.Button(login_frame, text="Sign Up", command=lambda: open_signup_popup(root))
signup_button.grid(row=4, column=0, columnspan=2, pady=10, ipadx=15)

# Start the GUI event loop
root.mainloop()

