import os
import json

dic={}
dic_values={}
#Create a new database


os.chdir(os.path.dirname(__file__))

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear') #cls command used to clear the screen on Windows.
                                                     

#taking input
def create_database():
    fields=["ID"]
    length=[5]

    database_name=input('Enter the name of the new database: ')
    if os.path.exists(os.path.abspath(f'database_names\\{database_name}')):
        print('Database with same name already exists!!')
        print('Please try with a different name ')
        create_database()
        return
    field_number=int(input('Enter no. of fields: '))

    database_name_path=os.path.join('database_names')
    os.makedirs(database_name_path, exist_ok=True)
    # Constructing the full path to create the new database directory inside 'pr0'
    database_path = os.path.join(database_name_path,database_name)
    os.makedirs(database_path, exist_ok=True)

    
#adding field names to list
    for i in range(1,field_number+1):
        field_name=input(f'Enter the name of the field{i}: ')
        lengths=int(input('Enter the length of fields: '))
        length.append(lengths)
        fields.append(field_name)
  
    dic_values['name']=database_name
    dic_values['field_no'] = field_number
    dic_values['length'] = length
    dic_values['fields'] = fields
    dic[database_name] = dic_values

    #print(dic)

#creating info file inside directory
    info_file_path = os.path.join(database_path, 'info.txt')

#writing this to file
    with open(info_file_path, 'w') as file:
        json.dump(dic[database_name], file, indent=4)


def add_record(database_info: dict, database_records: list): 
    if not(database_info or database_records):
        print('Error: Database not found')

    fields=database_info['fields'] 
    lengths=database_info['length']

    no_of_records=int(input('Enter the number of records you want to add: ')) 
    
    for i in range(no_of_records): 
        print(f'FOR RECORD NO{i+1}')
        
        while True:
            record_id=input('Enter value for ID: ')
            if len(record_id)<=lengths[0]:
                id_exists = False  # Flag to track if ID exists 
                
                for dic in database_records:
                    if record_id== dic['ID']:
                        print('-'*50)
                        print('Error: ID already exists')
                        print('-'*50)
                        id_exists = True
                        break
                    
                if not id_exists:  
                    break
            else:
                print('-'*50)
                print('Error: ID length does not match the specified length')
                print('-'*50)
        
        records = {}
        for field, length in zip(fields, lengths):
            if field == "ID":
                records[field] = record_id
            else:
                while True:
                    input_val = input(f"Enter value for {field} (max length {length}): ")
                    if len(input_val) <= length:
                        records[field] = input_val
                        break  
                    else:
                        print('-'*50)
                        print(f"Error: {field} exceeds maximum length of {length}. Please try again.") 
                        print('-'*50)
        database_records.append(records) 

    print('Record added successfully')
    print('x'*20)

    folder_path = f"database_names/{database_info['name']}" 
    record_file_path = os.path.join(folder_path, 'record.txt')  #initializing the path for record file

    try:
        with open(record_file_path,'w') as record_file: #writing record file
            json.dump(database_records, record_file, indent=4)
    except Exception as e:
        print('Error occured')

def list_record(database_info: dict, database_records: list): 

    for field in database_info['fields']: 
                                        
        print(f"\t{field:<20}",end='|')

    print()
    print("-"*(len(database_info['fields'])*25))
                                                
                                            
#printing records
    for record in database_records:              
        for field in database_info['fields']:    
            print(f'\t{record[field]:<20}',end='|')    
        print()

def search_record(database_info: dict, database_records: list):
    if not(database_info or database_records):
        print('Database information missing')

    fields=database_info['fields']

    list_record(database_info, database_records)

    search=input('Enter the ID you want to search: ')
    
    for record in database_records:
        if search==record['ID']:
            print('Record found')
            for field in fields:
                print(f'{field}: {record[field]}')
            print('-'*20)
            break
    else:
        print('Record not found')
        



def find_database(db_name:str): 
    if not db_name: 
        return None

    path=f"database_names/{db_name}" 

    if os.path.isdir(path): 
        files=[os.path.join(path,file) for file in os.listdir(path)]  
        return files 
    else:
        return None 

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


    
def delete_record(database_info: dict, database_records: list):

    list_record(database_info, database_records) 

    record_id = input("Enter the ID of the record you want to delete: ").strip()

    for record in database_records:
        if record['ID']==record_id:  
            database_records.remove(record)   
            print(f"Record with ID {record_id} sucessfully deleted.")
            break
    else:
        print(f"Record with ID {record_id} not found.")

    folder_path = f"database_names/{database_info['name']}" #initializing the path for folder file
    record_file_path = os.path.join(folder_path, 'record.txt')  #initializing the path for record file

    with open(record_file_path, 'w') as record_file:
            json.dump(database_records, record_file, indent=4) 

def update_record(database_info: dict, database_records: list):

    list_record(database_info, database_records) #this will list all the records

    record_id = input("Enter the ID of the record you want to update: ").strip()

    for record in database_records:          
        if record['ID']==record_id:         
                                            
            print(f"updating record for ID {record['ID']}")
            for key in record:                                        
                updated_value=input(f'enter value for the {key}: ')   
                record[key]=updated_value                             
            for field in record:
                print(f'{field}: {record[field]}')                     
            print('-'*20)
            break                               
    else:
        print("ID not found")

    folder_path = f"database_names/{database_info['name']}" #initializing the path for folder file
    record_file_path = os.path.join(folder_path, 'record.txt')  #initializing the path for record file

    with open(record_file_path, 'w') as record_file:
            json.dump(database_records, record_file, indent=4) 

def next_or_back_option():
     choice=int(input('Press "0" to go back or "1" to go to the main menu: '))
     if choice==0:
         clear_screen()
         open_database()
     elif choice==1:
         clear_screen()
         return

def open_database():
    databases=os.listdir('database_names') 

    print("".join(f'{i+1}-{databases[i]}\n' for i in range(len(databases))))  

    db_name=input('enter the name of database you want to open: ')

    database_info=read_file_info(db_name) 
    fields=database_info['fields']
    database_records = read_file_records(db_name) or []     

    if db_name in databases: 
        clear_screen()
        print(f'Opening database {db_name} with fields: {fields}') 
        print('1-Add record')
        print('2-search record')
        print('3-update record')
        print('4-delete record')
        print('5-list record')
        print('6-back')

    choice=int(input('Enter the number of operation you want to perform: ')) 

    if choice==1:
        clear_screen()
        add_record(database_info, database_records) 
        next_or_back_option()
    elif choice==2:
        clear_screen()
        search_record(database_info, database_records)
        next_or_back_option()
    elif choice==3:
        clear_screen()
        update_record(database_info, database_records)
        next_or_back_option()
    elif choice==4:
        clear_screen()
        delete_record(database_info, database_records)
        next_or_back_option()
    elif choice==5:
        clear_screen()
        list_record(database_info, database_records) 
        next_or_back_option()
    elif choice==6:
        clear_screen()
        main()

def back_option():
    choice=int(input('Press "1" to go to the main menu: '))
    if choice==1:
        clear_screen()
        return

#Main Program
def main():
    while True:
        print('Welcome to DBMS:')
        print('1- Create new database')
        print('2-Open an existing databse')
        print('3-Exit')

        choice=int(input('Enter your choice number: '))
        if choice==1:
            clear_screen()
            create_database()
            back_option()
        elif choice==2:
            clear_screen()
            open_database()
        else:
            print('Exiting DBMS')
            print('THANK YOU FOR VISITING')
            return True

def startup():
    exit_program = False
    # User authentication loop
    while not exit_program:
        if not os.path.exists('usernames.txt'):
            # Create the file if it does not exist
            with open('usernames.txt', 'w') as f:
                json.dump({}, f)
        
        with open('usernames.txt', 'r') as f:
            usernames = json.load(f)

        print('Welcome to DBMS')
        username = input('Enter username: ')
        password = input('Enter password: ')

        if username in usernames and usernames[username] == password:
            print("Login successful!")
            exit_program = main()  # If main() returns True, exit_program is set to True
        else:
            print('Invalid username or password')
            choice = input('Do you want to sign up? (y/n): ')
            if choice.lower() == 'y':
                new_username = input('Enter new username: ')
                new_password = input('Create new password: ')
                confirm = input('Re-write password: ')
                if confirm == new_password:
                    usernames[new_username] = new_password
                    with open('usernames.txt', 'w') as file:
                        json.dump(usernames, file, indent=4)
                    print(f'User {new_username} registered successfully!')
                else:
                    print("Passwords do not match.")
            elif choice.lower() == 'n':
                print("Please try again.")
            else:
                print("Invalid option. Please try again.")

if __name__ == "__main__":
    startup()  
     

