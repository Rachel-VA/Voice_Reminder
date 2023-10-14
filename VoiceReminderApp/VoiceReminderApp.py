"""
Rachael Savage
CSC235-Python I
Professor John Hamilton
6/06/23
"""

# import libs
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import pyttsx3

# define the first class and a constructor method __init__ with 2 para
# The self parameter represents the instance of the class being created.
class Reminder:
    def __init__(self, time, content):
        self.time = time # the time parameter is assigned to the instance variable self.time
        self.content = content # the content parameter is assigned to the instance variable self.content

    """
    use python special method __str__ and str() to work with string/text.
    The __str__ method returns a string that represents the Reminder object.
     date/time is concatenated with the content attribute of the Reminder object,
     date/time format must match computer format for it to compare and match to trigger the reminder
    """
    def __str__(self):
        return self.time.strftime("%m/%d/%Y %I:%M %p") + " - " + self.content

class ReminderList:
    def __init__(self):
        self.reminders = []  # Initialize an empty list to store reminders

    def add_reminder(self, reminder):
        self.reminders.append(reminder)  # Add a reminder to the list

    def remove_reminder(self, reminder):
        self.reminders.remove(reminder)  # Remove a reminder from the list

    def clear(self):
        self.reminders.clear()  # Clear all reminders from the list

    def get_all_reminders(self):
        return self.reminders  # Get all reminders in the list

class ReminderApp:
    def __init__(self):
        self.reminder_list = ReminderList()  # Create an instance of the ReminderList class
        self.voice_engine = pyttsx3.init()  # Initialize the text-to-speech engine
        self.window = tk.Tk()
        self.window.title("************ WELCOME TO THE VOICE REMINDER APP *********")
        self.window.geometry("800x700")  # Set the window size to 1000x800

        self.canvas = tk.Canvas(self.window, bg="purple", width=900, height=800)  # Create a canvas with purple background
        self.canvas.pack()

        self.reminder_label = tk.Label(self.canvas, text="Enter Reminder below:", font=("Arial", 15))  # Create a label for the reminder input
        self.reminder_label.place(relx=0.5, rely=0.1, anchor="center")  # Position the label on the canvas

        self.reminder_text = tk.Text(self.canvas, font=("Arial", 12), width=40, height=5)  # Create a text box for the reminder input
        self.reminder_text.place(relx=0.5, rely=0.2, anchor="center")  # Position the text box on the canvas

        self.date_label = tk.Label(self.canvas, text="Date (MM/DD/YYYY):", font=("Arial", 12))  # Create a label for the date input
        self.date_label.place(relx=0.3, rely=0.4, anchor="center")  # Position the label on the canvas

        self.date_entry = tk.Entry(self.canvas, font=("Arial", 12), width=12)  # Create an entry field for the date input
        self.date_entry.place(relx=0.5, rely=0.4, anchor="center")  # Position the entry field on the canvas

        self.time_label = tk.Label(self.canvas, text="Time (HH:MM AM/PM):", font=("Arial", 12))  # Create a label for the time input
        self.time_label.place(relx=0.3, rely=0.5, anchor="center")  # Position the label on the canvas

        self.time_entry = tk.Entry(self.canvas, font=("Arial", 12), width=12)  # Create an entry field for the time input
        self.time_entry.place(relx=0.5, rely=0.5, anchor="center")  # Position the entry field on the canvas

        self.add_button = tk.Button(self.canvas, text="Add Reminder", font=("Arial", 12), bg="yellow", command=self.add_reminder)  # Create a button to add a reminder
        self.add_button.place(relx=0.4, rely=0.6, anchor="center")  # Position the button on the canvas

        self.delete_button = tk.Button(self.canvas, text="Delete Reminder", font=("Arial", 12), bg="red", command=self.delete_selected_reminder)  # Create a button to delete a reminder
        self.delete_button.place(relx=0.6, rely=0.6, anchor="center")  # Position the button on the canvas

        self.reminder_listbox = tk.Listbox(self.canvas, font=("Arial", 12), width=50, height=10)  # Create a listbox to display reminders
        self.reminder_listbox.place(relx=0.5, rely=0.8, anchor="center")  # Position the listbox on the canvas

        self.load_reminders()  # Load existing reminders

        self.window.after(1000, self.check_reminders)  # Check reminders every second (mili sec)
        # load the GUI window
        self.window.mainloop()

    def load_reminders(self):
        # Load existing reminders from a file or database if needed
        pass

    def update_reminder_list(self):
        self.reminder_listbox.delete(0, tk.END)  # Clear the listbox
        for reminder in self.reminder_list.get_all_reminders():  # Iterate over all reminders
            self.reminder_listbox.insert(tk.END, str(reminder))  # Insert each reminder into the listbox

    # reminder that already reminded will be auto delete
    def reset_inputs(self):
        self.reminder_text.delete("1.0", tk.END)  # Clear the reminder text box
        self.date_entry.delete(0, tk.END)  # Clear the date entry field
        self.time_entry.delete(0, tk.END)  # Clear the time entry field

    def add_reminder(self):
        date_time = self.date_entry.get() + " " + self.time_entry.get()  # Get the date and time input from the user
        try:
            reminder_time = datetime.strptime(date_time, "%m/%d/%Y %I:%M %p")  # Convert the date and time input to a datetime object
            reminder_content = self.reminder_text.get("1.0", tk.END).strip()  # Get the reminder content from the text box
            reminder = Reminder(reminder_time, reminder_content)  # Create a Reminder object
            self.reminder_list.add_reminder(reminder)  # Add the reminder to the list
            self.update_reminder_list()  # Update the listbox to display the updated list of reminders
            self.reset_inputs()  # Reset the input fields
            self.voice_engine.say(reminder_content)  # Speak the reminder content
            self.voice_engine.runAndWait()  # Wait for the voice to finish speaking
            messagebox.showinfo("Reminder Added", "Reminder successfully added!")  # Show a message box to indicate successful addition
            # handle error
        except ValueError:
            messagebox.showerror("Invalid Date/Time", "Please enter a valid date and time format: MM/DD/YYYY HH:MM AM/PM.")

    # allow user to delete a reminder message after set
    def delete_selected_reminder(self):
        selected_index = self.reminder_listbox.curselection()  # Get the index of the selected item in the listbox
        if selected_index:
            reminder = self.reminder_list.get_all_reminders()[selected_index[0]]  # Get the reminder object based on the selected index
            self.reminder_list.remove_reminder(reminder)  # Remove the selected reminder from the list
            self.update_reminder_list()  # Update the listbox to display the updated list of reminders
            messagebox.showinfo("Reminder Deleted", "Reminder successfully deleted!")  # Show a message box to indicate successful deletion
        else:
            messagebox.showerror("No Reminder Selected", "Please select a reminder to delete.")  # Show an error message if no reminder is selected

     # keep checking the time constantly to find match
    def check_reminders(self):
        current_time = datetime.now()  # Get the current time
        for reminder in self.reminder_list.get_all_reminders():  # Iterate over all reminders
            reminder_time = reminder.time
            if current_time >= reminder_time:
                self.voice_engine.say(reminder.content)  # Speak the reminder content
                self.voice_engine.runAndWait()  # Wait for the voice to finish speaking
                self.reminder_list.remove_reminder(reminder)  # Remove the reminder from the list
                self.update_reminder_list()  # Update the listbox to display the updated list of reminders
        self.window.after(1000, self.check_reminders)  # Schedule the next reminder check after 1 second

if __name__ == "__main__":
    ReminderApp()
