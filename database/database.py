import psycopg2
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError
from dotenv import load_dotenv

import pandas as pd
import os

### get env values
env_path  = "../.env"

load_dotenv(dotenv_path=env_path)

DB_USER = os.environ["DB_USER"]
DB_PASS = os.environ["DB_PASS"]
DB_NAME = os.environ["DB_NAME"]

SERVICE_NAME = "db"



class DatabaseConfig:
    def __init__(self, db_user, db_pass, db_name, service_name):
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_name = db_name
        self.service_name = service_name


    def get_init_string(self):
        return f'postgresql://{self.db_user}:{self.db_pass}@{self.service_name}/postgres'

    def get_connection_string(self):
        return f'postgresql://{self.db_user}:{self.db_pass}@{self.service_name}/{self.db_name}'


DBconfig = DatabaseConfig(DB_USER, DB_PASS, DB_NAME, SERVICE_NAME)



def init_database(): 

    
    init_string = DBconfig.get_init_string()

    engine_master = create_engine(init_string, echo=True)
    print(f"connecting to: {init_string}")
    db_name = DB_NAME   
    with engine_master.begin() as conn:
  
        conn.execute(text("COMMIT"))

        exists = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :name"),
            {"name": db_name}
        ).first()

        if not exists:
            try:
                conn.execute(text(f"CREATE DATABASE {db_name}"))
                print(f"Database '{db_name}' created.")
            except ProgrammingError as e:
                if 'already exists' in str(e):
                    print(f"Database '{db_name}' already exists, skipping creation.")
                else:
                    raise
        else:
            print(f"Database '{db_name}' already exists, skipping creation.")

    engine_master.dispose()


def make_table(table_name="restaurant"): 
    connection_string = DBconfig.get_connection_string()
    print(f"Connecting to database: {connection_string}")
    engine_app = create_engine(connection_string, echo=True)
    with engine_app.begin() as conn:
        conn.execute(text(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id         TEXT NOT NULL,
                name       TEXT  NOT NULL,
                kana       TEXT ,
                address    TEXT  NOT NULL,
                station    TEXT NOT NULL,
                genre      TEXT  NOT NULL,
                subgenre   TEXT ,
                url        TEXT 
            )
        """))
        print(f"Table {table_name} ensured.")

    engine_app.dispose()



def add_data():
    data_path = "./../data/hotpepper_data.csv"
    db_name = DB_NAME  
    df = pd.read_csv (data_path)
    df = df.rename(columns={
    'name_kana': 'kana',
    'sub_genre': 'subgenre'
    })
    df = drop_null(df)
    connection_string = DBconfig.get_connection_string()
    try:
        print (f"Connecting to database: {connection_string}")
        engine = create_engine(connection_string, echo=False) 
        cols = ['id','name','kana','address','station','genre','subgenre','url']
        df = df[cols]

        df.to_sql(
            name='restaurant',
            con=engine,
            if_exists='replace',    
            index=False,
            method='multi',     
            chunksize=500
        )
    except Exception as e:
        print(f"Error adding data: {e}")
        

def drop_null(df):
    null = df[df['station'].isnull()]

    # Drop rows where 'station' is null
    df = df.dropna(subset=['station'])
    print(f"Dropped {len(null)} rows with null 'station' values.")
    return df

 
