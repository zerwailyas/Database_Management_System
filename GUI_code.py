import os   
import json    
from tkinter import *    
from tkinter import messagebox, ttk, simpledialog, Tk  


dbms_root=Tk()  

os.chdir(os.path.dirname(__file__))

# GUI Colors and Fonts
PRIMARY_COLOR = "#849cb2"  # Background color
SECONDARY_COLOR = "#b4c8cc"  # Button and highlight color
TEXT_COLOR = "#FAFAFA" 
FONT_PRIMARY = ("Times Roman", 20, "bold")
FONT_SECONDARY = ("Times Roman", 16)
BACK_BUTTON_COLOR="#0a2344" #RGB hexadecimal code

# Setting up the GUI
dbms_root.geometry("800x600")   
dbms_root.title("DBMS")  
dbms_root.configure(bg=PRIMARY_COLOR)   

def add_record_gui(database_info, database_records):
    clear_screen()
    fields = database_info["fields"]
    lengths = database_info["length"]
    db_name = database_info.get("name", "unknown_database")  

    # Create a frame for dynamic input
    Label(dbms_root, text="Enter the number of records to add:", font=("Arial", 14), bg="lightblue").pack(pady=20)  

    # Entry widget to take number of records
    record_input = Entry(dbms_root, font=("Arial", 14), justify="center")  
    record_input.pack(pady=10)

    def ask_records():     
        try:
            num_records = int(record_input.get().strip())  
            if num_records <= 0:
                raise ValueError("Number of records must be greater than zero.")
        except ValueError as ve:
            messagebox.showerror("Error", f"Invalid input: {ve}")   
            return

        def save_single_record(record_index):   
            clear_screen()
            Label(dbms_root, text=f"Add Record {record_index + 1}/{num_records} to {db_name}", font=("Arial", 14), bg="lightblue").pack(pady=20)

            
            entries = {}     

            # Create input fields for each column
            for index, field in enumerate(fields):  
                Label(dbms_root, text=f"{field} (Max {lengths[index]} chars):", font=("Arial", 12), bg="lightblue").pack(pady=5)
                entry = Entry(dbms_root, font=("Arial", 12), width=30)
                entry.pack(pady=5)
                entries[field] = entry

            def save_and_next():
                # Create a new record
                new_record = {}
                for index, field in enumerate(fields):  
                    value = entries[field].get().strip()   

                    # Validate ID
                    if database_records:  
                        if field == "ID":
                            if len(value) > lengths[index]:
                                messagebox.showerror("Error", f"ID length exceeds {lengths[index]} characters.")
                                return
                            if any(record["ID"] == value for record in database_records):
                                messagebox.showerror("Error", "ID already exists. Please enter a unique ID.")
                                return

                    # Validate other fields
                    if len(value) > lengths[index]:  
                        messagebox.showerror("Error", f"{field} exceeds maximum length of {lengths[index]} characters.")
                        return

                    # Store the field value
                    new_record[field] = value

                # Add new record to the database
                database_records.append(new_record)

                # Save the record to the file
                folder_path = f"database_names/{db_name}"
                record_file_path = os.path.join(folder_path, "record.txt")
                try:
                    with open(record_file_path, "w") as record_file:
                        json.dump(database_records, record_file, indent=4)
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred while saving the records: {e}")
                    return

                if record_index + 1 < num_records:
                    save_single_record(record_index + 1)   
                else:
                    messagebox.showinfo("Success", "All records added successfully!")
                    open_database()

            # Buttons for saving and navigating
            Button(dbms_root, text="Save and Next", font=("Arial", 12), bg="green", command=save_and_next).pack(pady=10)
            Button(dbms_root, text="Cancel", font=("Arial", 12), bg="red", command=global_functions).pack(pady=10)

        # Start adding the first record
        save_single_record(0)   

    # Button to proceed after entering the number of records
    Button(dbms_root, text="Proceed", font=("Arial", 12),fg="white", bg="blue", command=ask_records).pack(pady=20)
    Button(dbms_root, text="Back", font=("Arial", 12), fg="white", bg=BACK_BUTTON_COLOR, command=global_functions).pack(pady=10)


def list_record_gui(database_info: dict, database_records: list):  
    clear_screen()
    # Get field names
    fields = database_info['fields']
    num_records = len(database_records)

    if num_records == 0:
        # Handle case where there are no records
        Label(dbms_root, text="No records available", font=("Arial", 14), bg=PRIMARY_COLOR, fg="red").pack(pady=20)   
        Button(dbms_root, text="Back", font=("Arial", 12),  fg="white", bg=BACK_BUTTON_COLOR, command=global_functions).pack(pady=10)
        return

    # Calculate table width dynamically based on fields
    column_width = 20  
    total_width = len(fields) * column_width  

    # Create container frame for table
    container_frame = Frame(dbms_root, bg=PRIMARY_COLOR)  
    container_frame.pack(expand=True, fill=BOTH)  

    # Title
    Label(
        container_frame, 
        text="List of Records", 
        font=("Arial", 16, "bold"), 
        bg=PRIMARY_COLOR, 
        anchor="center"
    ).pack(pady=10)

    # Table frame for headers and rows
    table_frame = Frame(container_frame, bg="white", width=total_width)  
    table_frame.pack(anchor="center", pady=10)

    # Header frame
    header_frame = Frame(table_frame, bg=SECONDARY_COLOR, width=total_width)
    header_frame.pack(fill=X)

    for field in fields:
        Label(             
            header_frame, 
            text=field, 
            font=("Arial", 12, "bold"), 
            bg=SECONDARY_COLOR, 
            width=column_width, 
            anchor="center"
        ).pack(side=LEFT)

    # Separator
    Label(
        table_frame, 
        text="-" * total_width, 
        font=("Arial", 10), 
        bg="white", 
        fg="black"
    ).pack(fill=X)

    # Populate records
    for record in database_records:      
        record_frame = Frame(table_frame, bg="white")  
        record_frame.pack(fill=X)

        for field in fields:
            value = record.get(field, "")
            Label(
                record_frame, 
                text=value, 
                font=("Arial", 12), 
                bg="white", 
                width=column_width, 
                anchor="center"
            ).pack(side=LEFT)

    # Back button
    Button(
        container_frame, 
        text="Back", 
        font=("Arial", 12), 
         fg="white",
        bg=BACK_BUTTON_COLOR, 
        command=global_functions
    ).pack(pady=20)

   

def search_record_gui(database_info, database_records):
    
    clear_screen()

    fields = database_info["fields"]

    # Title
    Label(dbms_root, text="Search Record", font=("Arial", 20, "bold"), bg="lightblue").pack(pady=20)

    # List all records
    list_record_gui(database_info, database_records)

    # Search input
    Label(dbms_root, text="Enter the ID to search:", font=("Arial", 14), bg="lightblue").pack(pady=10)
    search_entry = Entry(dbms_root, font=("Arial", 14))
    search_entry.pack(pady=5)

    def search():
        """Search for a record by ID and display the result."""
        search_id = search_entry.get().strip()
        if not search_id:
            messagebox.showerror("Error", "Search ID cannot be empty.")
            return

        # Search logic
        for record in database_records:
            if record["ID"] == search_id:
                # Display search result
                clear_screen()
                result_frame = Frame(dbms_root, bg="#dae0d4", padx=10, pady=10)
                result_frame.pack(pady=10)

                Label(result_frame, text="Record Found:", font=("Arial", 14, "bold"), bg="#dae0d4").pack(pady=5)
                for field in fields:
                    Label(result_frame, text=f"{field}: {record[field]}", font=("Arial", 12), bg="#dae0d4").pack(anchor="w")
                Button(dbms_root, text="Back", font=("Arial", 14), fg="white", bg=BACK_BUTTON_COLOR, command=global_functions).pack(pady=10)
                return

        # If no record is found
        messagebox.showinfo("Not Found", "No record found with the given ID.")
        

        # Search and back buttons
    Button(dbms_root, text="Search", font=("Arial", 14), bg="grey", command=search).pack(pady=10)
        

def clear_screen():
    
    if dbms_root.winfo_exists():  
        for widget in dbms_root.winfo_children():   
            widget.destroy()   

def find_database(db_name: str):
    
    if not db_name:  
        return None

    path = f"database_names/{db_name}"  

    if os.path.isdir(path):  
        files = [os.path.join(path, file) for file in os.listdir(path)]  
        return files  
    else:
        return None  

# Functions for actions
def create_database_gui():
    clear_screen()

    dic={}
    dic_values={}

    fields = ["ID"]
    lengths = [5]

    def save_database():
        database_name = name_entry.get().strip()
        if not database_name:
            messagebox.showerror("Error", "Database name cannot be empty.")
            return

        database_path = os.path.join("database_names", database_name)

        # Check if database already exists
        if os.path.exists(database_path):
            messagebox.showerror("Error", "Database with the same name already exists. Please try a different name.")
            return

        # Get the number of fields
        try:
            field_number = int(fields_entry.get().strip())
            if field_number <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of fields.")
            return

        # Create database directory
        os.makedirs(database_path, exist_ok=True)

        # Adding field names to the list
        for i in range(1, field_number + 1):
            field_name = field_entries[i - 1].get().strip()
            field_length = field_length_entries[i - 1].get().strip()

            if not field_name:
                messagebox.showerror("Error", f"Field name {i} cannot be empty.")
                return

            try:
                length = int(field_length)
                if length <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", f"Field {i} length must be a positive integer.")
                return

            fields.append(field_name)
            lengths.append(length)

        # Save database information
        dic_values['name'] = database_name
        dic_values['field_no'] = field_number
        dic_values['length'] = lengths
        dic_values['fields'] = fields
        dic[database_name] = dic_values

        # Create info file
        info_file_path = os.path.join(database_path, 'info.txt')
        with open(info_file_path, 'w') as file:
            json.dump(dic[database_name], file, indent=4)

        messagebox.showinfo("Success", f"Database '{database_name}' created successfully!")
        main_menu()
        

    # Input for database name
    Label(dbms_root, text="Enter the name of the new database:", bg="lightblue", font=("Arial", 14)).pack(pady=10)
    name_entry = Entry(dbms_root, font=("Arial", 14))
    name_entry.pack(pady=5)

    # Input for the number of fields
    Label(dbms_root, text="Enter the number of fields:", bg="lightblue", font=("Arial", 14)).pack(pady=10)
    fields_entry = Entry(dbms_root, font=("Arial", 14))
    fields_entry.pack(pady=5)

    # Dynamic field entry section
    def add_fields():
        try:
            field_number = int(fields_entry.get().strip())
            if field_number <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of fields.")
            return

        # Create dynamic fields input
        Label(dbms_root, text="Enter field details:", bg="lightblue", font=("Arial", 14, "bold")).pack(pady=10)
        
        global field_entries, field_length_entries
        field_entries = []
        field_length_entries = []

        for i in range(1, field_number + 1):
            frame = Frame(dbms_root, bg="lightblue")
            frame.pack(pady=2)

            Label(frame, text=f"Field {i} Name:", bg="lightblue", font=("Arial", 12)).pack(side=LEFT, padx=5)
            field_name_entry = Entry(frame, font=("Arial", 12))
            field_name_entry.pack(side=LEFT, padx=5)
            field_entries.append(field_name_entry)

            Label(frame, text="Length:", bg="lightblue", font=("Arial", 12)).pack(side=LEFT, padx=5)
            field_length_entry = Entry(frame, font=("Arial", 12))
            field_length_entry.pack(side=LEFT, padx=5)
            field_length_entries.append(field_length_entry)

        Button(dbms_root, text="Save Database", font=("Arial", 12), bg="grey", command=save_database).pack(pady=10)

    Button(dbms_root, text="Next", font=("Arial", 12), bg="grey", command=add_fields).pack(pady=10)
    Button(dbms_root, text="Back", font=FONT_SECONDARY, fg="white", bg=BACK_BUTTON_COLOR, command=main_menu).pack(pady=10)
    

def read_file_info(db_name: str): 
    files=find_database(db_name) 

    if files: 
        for file in files: 
            if file.endswith('info.txt'): 
                try:
                    with open(file, 'r') as f: 
                        data=json.load(f) 
                        return data 
                except Exception as e:
                    print(f'Error: Something went wrong while reading the info file')
                    return None
    else:
        print(f'Error: No info file of {db_name} found')
        return None

def read_file_records(db_name:str): 
    files=find_database(db_name)  

    # everything is similar to read_file_info
    if files:
        for file in files:
            if file.endswith('record.txt'):
                try:
                    with open(file, 'r') as f:
                        data=json.load(f)
                    return data
                except Exception as e:
                    print('Error: something went wrong while reading')
    else:
        print(f'No record file for database {db_name} found')
        return None
    
def delete_record_gui(database_info: dict, database_records: list):
   
    def handle_delete():
        record_id = entry_id.get().strip()  
        if not record_id:
            messagebox.showerror("Error", "Please enter a valid record ID.")
            return

        for record in database_records:
            if record['ID'] == record_id:
                database_records.remove(record)  
                messagebox.showinfo("Success", f"Record with ID {record_id} successfully deleted.")
                
                # Update the file
                folder_path = f"database_names/{database_info['name']}"  
                record_file_path = os.path.join(folder_path, 'record.txt')  
                with open(record_file_path, 'w') as record_file:
                    json.dump(database_records, record_file, indent=4)

                list_record_gui(database_info, database_records)
                return  # Exit after deleting
        else:
            messagebox.showerror("Error", f"Record with ID {record_id} not found.")


    # Display current records
    Label(dbms_root, text="Current Records:").pack(pady=5)
    record_list =Listbox(dbms_root, width=50, height=10)
    record_list.pack(pady=5)
    list_record_gui(database_info, database_records)

    # Entry field for record ID
    Label(dbms_root, text="Enter Record ID to Delete:").pack(pady=5)
    entry_id =Entry(dbms_root, width=30)
    entry_id.pack(pady=5)

    # Delete button
    Button(dbms_root, text="Delete Record", command=handle_delete).pack(pady=10)

def update_record(database_info: dict, database_records: list):
   
    def handle_update():
        record_id = entry_id.get().strip()  
        if not record_id:
            messagebox.showerror("Error", "Please enter a valid record ID.")
            return

        for record in database_records:
            if record['ID'] == record_id:
                # Found the record, open dialog for updating fields
                updated_record = open_update_dialog(record)
                if updated_record:
                    # Update the record and save changes to the file
                    record.update(updated_record)
                    messagebox.showinfo("Success", f"Record with ID {record_id} successfully updated.")

                    # Save changes to the file
                    folder_path = f"database_names/{database_info['name']}"  
                    os.makedirs(folder_path, exist_ok=True)
                    record_file_path = os.path.join(folder_path, 'record.txt')  
                    with open(record_file_path, 'w') as record_file:
                        json.dump(database_records, record_file, indent=4)

                    list_record_gui(database_info, database_records)
                return
        
        # If ID not found
        messagebox.showerror("Error", f"Record with ID {record_id} not found.")

    def open_update_dialog(record):
        
        update_window = Toplevel(dbms_root)
        update_window.title("Update Record")
        updated_values = {}

        # Create entry fields for each key in the record
        entries = {}
        for i, (key, value) in enumerate(record.items()):
            Label(update_window, text=f"{key} (current: {value}):").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = Entry(update_window, width=30)
            entry.insert(0, value) 
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[key] = entry

        # Function to handle the save action
        def save_changes():
            for key, entry in entries.items():
                updated_values[key] = entry.get().strip()  
            update_window.destroy()  
        # Function to handle the cancel action
        def cancel_changes():
            nonlocal updated_values
            updated_values = None
            update_window.destroy()  

        # Add Save and Cancel buttons
        Button(update_window, text="Save", command=save_changes).grid(row=len(record), column=0, padx=10, pady=10)
        Button(update_window, text="Cancel", command=cancel_changes).grid(row=len(record), column=1, padx=10, pady=10)

        # Wait for the dialog to close
        update_window.transient(dbms_root)  
        update_window.grab_set()   
        update_window.wait_window()    

        return updated_values

    # Display current records
    Label(dbms_root, text="Current Records:").pack(pady=5)
    record_list =Listbox(dbms_root, width=50, height=10)
    record_list.pack(pady=5)
    list_record_gui(database_info,database_records)

    # Entry field for record ID
    Label(dbms_root, text="Enter Record ID to Update:").pack(pady=5)
    entry_id = Entry(dbms_root, width=30)
    entry_id.pack(pady=5)

    # Update button
    Button(dbms_root, text="Update Record", command=handle_update).pack(pady=10)

global_functions = None   
def open_database():
    clear_screen()

    # Fetch the list of databases (mocked here)
    databases = os.listdir('database_names')

    # Display database options
    Label(dbms_root, text="Select a Database", font=FONT_PRIMARY, bg=PRIMARY_COLOR).pack(pady=20)
    
    # Dropdown menu for database selection
    selected_db = StringVar()     
    selected_db.set("Select Database")   
    dropdown = OptionMenu(dbms_root, selected_db, *databases)    
    dropdown.pack(pady=10)

    def open_selected_database():
        global global_functions  ## Access the global variable inside the nested function

        db_name = selected_db.get()
        if db_name == "Select Database":
            messagebox.showerror("Error", "Please select a database!")
            return

        database_info = read_file_info(db_name)
        database_records = read_file_records(db_name) or []

        # Database Operations Menu
        clear_screen()
        Label(dbms_root, text=f"Database: {db_name}", font=FONT_PRIMARY, bg=PRIMARY_COLOR).pack(pady=10)
        Label(dbms_root, text=f"Fields: {', '.join(database_info['fields'])}", font=FONT_SECONDARY, bg=PRIMARY_COLOR).pack(pady=10)

        # Buttons for operations
        def functions():
            clear_screen()
            Label(dbms_root, text=f"Database: {db_name}", font=FONT_PRIMARY, bg=PRIMARY_COLOR).pack(pady=10)
            Label(dbms_root, text=f"Fields: {', '.join(database_info['fields'])}", font=FONT_SECONDARY, bg=PRIMARY_COLOR).pack(pady=10)
            Button(dbms_root, text="1. Add Record", font=FONT_SECONDARY, bg=SECONDARY_COLOR,
       command=lambda: add_record_gui(database_info, database_records)).pack(pady=5)
            Button(dbms_root, text="2. Search Record", font=FONT_SECONDARY, bg=SECONDARY_COLOR,
               command=lambda: search_record_gui(database_info, database_records)).pack(pady=5)
            Button(dbms_root, text="3. Update Record", font=FONT_SECONDARY, bg=SECONDARY_COLOR,
               command=lambda: update_record(database_info, database_records)).pack(pady=5)
            Button(dbms_root, text="4. Delete Record", font=FONT_SECONDARY, bg=SECONDARY_COLOR,
               command=lambda: delete_record_gui(database_info, database_records)).pack(pady=5)
            Button(dbms_root, text="5. List Records", font=FONT_SECONDARY, bg=SECONDARY_COLOR,
               command=lambda: list_record_gui(database_info, database_records)).pack(pady=5)
            Button(dbms_root, text="6. Back", font=FONT_SECONDARY, bg=SECONDARY_COLOR, command=main_menu).pack(pady=20)
        
        global_functions=functions  
        functions()

    # Button to open the selected database
    Button(dbms_root, text="Open Database", font=FONT_SECONDARY, bg=SECONDARY_COLOR, command=open_selected_database).pack(pady=20)
    Button(dbms_root, text="Back", font=FONT_SECONDARY, fg="white", bg=BACK_BUTTON_COLOR, command=main_menu).pack(pady=10)


def exit_dbms():
    response = messagebox.askyesno("Exit", "Are you sure you want to exit?")
    if response:
        clear_screen()  # Instead of destroying the root, just clear it
        Label(dbms_root, text="THANK YOU FOR VISITING", font=FONT_PRIMARY, bg=PRIMARY_COLOR).pack(pady=30)
        dbms_root.after(2000, dbms_root.destroy)  # Optionally, destroy after some time

def main_menu():
    # Main Menu
    clear_screen() # Instead of destroying the root, just clear it
    Label(dbms_root, text="WELCOME TO DBMS", font=FONT_PRIMARY, bg=PRIMARY_COLOR).pack(pady=30)
    Button(dbms_root, text="1. Create New Database", font=FONT_SECONDARY, bg=SECONDARY_COLOR, command=create_database_gui).pack(pady=10)
    Button(dbms_root, text="2. Open Existing Database", font=FONT_SECONDARY, bg=SECONDARY_COLOR, command=open_database).pack(pady=10)
    Button(dbms_root, text="3. Exit", font=FONT_SECONDARY, bg=SECONDARY_COLOR, command=exit_dbms).pack(pady=10)


def startup():
    # Ensure the user data file exists
    if not os.path.exists('usernames.txt'):
        with open('usernames.txt', 'w') as f:
            json.dump({}, f)
    
    # Function to handle login
    def login():
        username = username_entry.get()
        password = password_entry.get()

        with open('usernames.txt', 'r') as file:
            usernames = json.load(file)

        if username in usernames and usernames[username] == password:
            messagebox.showinfo("Login Successful", "Welcome to the DBMS Main Application!")
            clear_screen()  
            main_menu()  
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    # Function to handle sign up
    def sign_up():
        def register():
            new_username = username_entry.get()
            new_password = password_entry.get()
            confirm_password = confirm_password_entry.get()

            if new_password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match!")
                return

            with open('usernames.txt', 'r') as file:
                usernames = json.load(file)

            if new_username in usernames:
                messagebox.showerror("Error", "Username already exists!")
            else:
                usernames[new_username] = new_password
                with open('usernames.txt', 'w') as file:
                    json.dump(usernames, file, indent=4)
                messagebox.showinfo("Success", f"User {new_username} registered successfully!")
                signup_window.destroy()

        signup_window = Toplevel(dbms_root)
        signup_window.title("Sign Up")

        Label(signup_window, text="New Username:").pack(pady=5)
        username_entry = Entry(signup_window)
        username_entry.pack(pady=5)

        Label(signup_window, text="New Password:").pack(pady=5)
        password_entry = Entry(signup_window, show="*")
        password_entry.pack(pady=5)

        Label(signup_window, text="Confirm Password:").pack(pady=5)
        confirm_password_entry = Entry(signup_window, show="*")
        confirm_password_entry.pack(pady=5)

        Button(signup_window, text="Register", command=register).pack(pady=10)

    # Login form
    Label(dbms_root, text="Username:").grid(row=0, column=0, padx=10, pady=10)
    username_entry = Entry(dbms_root)
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    Label(dbms_root, text="Password:").grid(row=1, column=0, padx=10, pady=10)
    password_entry = Entry(dbms_root, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    # Login and Sign Up buttons
    Button(dbms_root, text="Login", command=login).grid(row=2, column=0, padx=10, pady=10)
    Button(dbms_root, text="Sign Up", command=sign_up).grid(row=2, column=1, padx=10, pady=10)

startup()   

dbms_root.mainloop()     