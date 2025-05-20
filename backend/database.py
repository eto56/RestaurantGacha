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



def init_db():
    # --- ① master DB (postgres) に接続して App DB を作成 ---
    engine_master = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@localhost/postgres', echo=True)
    db_name = DB_NAME  # PostgreSQL は未引用識別子を小文字にする
    table_name = "temp"
    with engine_master.begin() as conn:
        # CREATE DATABASE はトランザクション外で実行する必要がある
        conn.execute(text("COMMIT"))

        # DB 存在チェック
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

    # --- ② App DB に接続してテーブルを作成 ---
    engine_app = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@localhost/{db_name}', echo=True)
    with engine_app.begin() as conn:
        conn.execute(text(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id         INTEGER     NOT NULL,
                name       VARCHAR(30) NOT NULL,
                kana       VARCHAR(50),
                prefecture VARCHAR(50) NOT NULL,
                station    VARCHAR(10) NOT NULL,
                genre      VARCHAR(20) NOT NULL,
                subgenre   VARCHAR(20),
                url        VARCHAR(100)
            )
        """))
        print(f"Table {table_name} ensured.")

    engine_app.dispose()

def add_data():
    data_path = "../data/hotpepper_data.csv"
    df = pd.read_csv (data_path)
    df = df.rename(columns={
    'name_kana': 'kana',
    'address': 'prefecture',
    'sub_genre': 'subgenre'
    })
    engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@localhost/postgres', echo=True)
    # 必要なカラムだけに絞る
    cols = ['id','name','kana','prefecture','station','genre','subgenre','url']
    df = df[cols]
    # ④ データ INSERT
    df.to_sql(
        name='restaurant',
        con=engine,
        if_exists='append',   # 既存テーブルに追記
        index=False,
        method='multi',       # バルク INSERT
        chunksize=500
    )
    



if __name__ == "__main__":
     init_db()