from database import init_database,make_table,add_data 

 

if __name__ == "__main__":
    init_database()
    print("Database initialized successfully.")
    make_table()
    print("Table created successfully.")
    add_data()
    print("Data added successfully.")

 
