from database import init_database 
from database import add_data

 

if __name__ == "__main__":
    init_database()
    print("Database initialized successfully.")
    add_data()
    print("Data added successfully.")

 
