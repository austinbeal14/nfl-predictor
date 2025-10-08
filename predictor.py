import duckdb
import pandas as pd
from get_team_record import get_team_record
from util import team_codes

def predictor():
    con = duckdb.connect("examples/test_database.db")
    df = con.execute("SELECT * from schedule_2025 WHERE week = '6' and day = 'Thu';").fetchdf()
    
    team1= df['Winner/tie'][0]
    team2 = df['Loser/tie'][0]
    print(f"Predicting {team1} @ {team2}")
    away_record =get_team_record(team_code=team_codes[team1])
    home_record = get_team_record(team_code=team_codes[team2])
    away_score = away_record[0]*0.6 + away_record[1] * 0.3 + away_record[2]*.1
    home_score = home_record[0]*0.6 + home_record[1] * 0.30 + home_record[2]*.1
    if away_score > home_score:
        print(f"{team1} will win!")
    elif away_score < home_score:
        print(f"{team2} will win!")
    else:
        print("It's a toss up!")
    
    

if __name__ == "__main__":
    predictor()