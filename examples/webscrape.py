import pandas as pd
import numpy as np
def example_data_fetch():
    url = 'https://www.pro-football-reference.com/years/2025/games.htm'
    data = pd.read_html(url, flavor='html5lib')
    print(data)

if __name__ == "__main__":
    example_data_fetch()