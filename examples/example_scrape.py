import pandas as pd
import numpy as np
import duckdb
def example_data_fetch():
    url = 'https://www.pro-football-reference.com/years/2025/games.htm'
    data = pd.read_html(url, flavor='html5lib')
    df = data[0]
    print(df)
    # data= data["Week"]
    # print(data)
    conn = duckdb.connect("test_database.db")
    conn.execute("Create table if not exists schedule_2025 as select * from df")




if __name__ == "__main__":
    example_data_fetch()