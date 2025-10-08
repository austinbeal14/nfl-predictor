import duckdb
import pandas as pd
def example_data_read():
    con = duckdb.connect("test_database.db")
    df = con.execute("SELECT * from schedule_2025;").fetchdf()
    print(df)
    
if __name__ == "__main__":
    example_data_read()