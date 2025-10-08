import pandas as pd

def get_team_record(team_code: str) -> tuple:
    url = f'https://www.pro-football-reference.com/teams/{team_code}/2025.htm'
    
    # Read HTML with multi-level headers
    data = pd.read_html(url, flavor='html5lib', header=[0, 1])
    results = data[1]  # Schedule/results table

    # Flatten MultiIndex column headers
    results.columns = ['_'.join(col).strip() for col in results.columns.values]

    # Find which column holds the W/L record
    # (It might be named 'Unnamed: 5_level_0_Unnamed: 5_level_1' or similar)
    for col in results.columns:
        if 'Unnamed: 5_level_0' in col:
            wl_col = col
            break

    # Count Wins and Losses
    wins = len(results[results[wl_col] == "W"])
    losses = len(results[results[wl_col] == "L"])
    ties = len(results[results[wl_col] == "T"])

    print(f"{team_code.upper()} Record: {wins}-{losses}-{ties}")
    return (wins, losses, ties)

def main():
    get_team_record("phi")

if __name__ == "__main__":
    main()
