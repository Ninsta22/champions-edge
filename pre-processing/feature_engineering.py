import pandas as pd
import numpy as np
import os
import warnings

# Ignore all warnings
warnings.filterwarnings("ignore")

pd.set_option("mode.copy_on_write", True)

# Replace this with the path to your downloads folder
downloads_folder = "/content/drive/MyDrive/OE Public Match Data"

# Initialize an empty list to hold dataframes
dfs = []

# Iterate over each year and read the corresponding CSV file
for year in range(2017, 2024):
    file_path = os.path.join(
        downloads_folder, f"{year}_LoL_esports_match_data_from_OraclesElixir.csv"
    )
    df = pd.read_csv(file_path)
    dfs.append(df)

# Concatenate all dataframes into one
df = pd.concat(dfs, ignore_index=True)

df = df[df["datacompleteness"] == "complete"]

# Create Team Participation Feature
df["team_participation"] = ((df["kills"] + df["assists"]) / df["teamkills"]) - (
    df["deaths"] / df["teamdeaths"]
)

# Create a Dataframe of Recent Games Played
sorted = df.sort_values(["year", "date"], ascending=False)
meta_df = sorted.groupby("champion").head(10)
recent_df = meta_df.groupby("champion").agg(
    {"result": "mean", "team_participation": "mean", "earnedgoldshare": "mean"}
)
recent_df = recent_df.rename(
    columns={
        "result": "recent_result",
        "team_participation": "recent_team_participation",
        "earnedgoldshare": "recent_earnedgoldshare",
    }
)

# Create Dataframe for Average Features per Champion
champ_career_stats = (
    df.groupby("champion")
    .agg(
        {
            "result": "mean",
            "team_participation": "mean",
            "earnedgoldshare": "mean",
        }
    )
    .reset_index()
)
champ_career_stats.set_index("champion", inplace=True)
champ_career_stats = champ_career_stats.join(recent_df, on="champion")

# Filter out only the rows for team records (not individual player records)
team_records = df[df["participantid"] > 10]

# Drop unnecessary columns
team_records = team_records[
    [
        "gameid",
        "participantid",
        "pick1",
        "pick2",
        "pick3",
        "pick4",
        "pick5",
        "result",
    ]
]

team_records = team_records.dropna()

# Add opponent's picks as new columns
for i, row in team_records.iterrows():
    # Find the opponent's row for the same game
    opponent_row = team_records[
        (team_records["gameid"] == row["gameid"])
        & (team_records["participantid"] != row["participantid"])
    ]
    if not opponent_row.empty:  # Check if the opponent row exists
        for pick in ["pick1", "pick2", "pick3", "pick4", "pick5"]:
            team_records.loc[i, f"opp_{pick}"] = opponent_row[pick].values[0]
    else:
        # Handle the case where no opponent row is found
        for pick in ["pick1", "pick2", "pick3", "pick4", "pick5"]:
            team_records.loc[i, f"opp_{pick}"] = None  # or use 'Unknown', etc.

# Define the columns for picks and opponent picks
pick_columns = ["pick1", "pick2", "pick3", "pick4", "pick5"]
opp_pick_columns = ["opp_pick1", "opp_pick2", "opp_pick3", "opp_pick4", "opp_pick5"]

# Iterate over each pick column
for pick_col, opp_pick_col in zip(pick_columns, opp_pick_columns):
    # Join the career stats for the team's picks
    team_records = team_records.join(
        champ_career_stats, on=pick_col, rsuffix=f"_stats_{pick_col}"
    )

    # Join the career stats for the opponent's picks
    team_records = team_records.join(
        champ_career_stats, on=opp_pick_col, rsuffix=f"_stats_{opp_pick_col}"
    )

# Correct Weird Occurance
team_records = team_records.rename(
    columns={
        "team_participation": "team_participation_pick1",
        "earnedgoldshare": "earnedgoldshare_pick1",
        "recent_result": "recent_result_pick1",
        "recent_team_participation": "recent_team_participation_pick1",
        "recent_earnedgoldshare": "recent_earnedgoldshare_pick1",
    }
)

# Concatenate all pick columns and opp_pick columns into two separate series
team_picks = pd.concat([team_records[f"pick{i}"] for i in range(1, 6)])
opp_picks = pd.concat([team_records[f"opp_pick{i}"] for i in range(1, 6)])

# One-hot encode the concatenated series
team_picks_encoded = pd.get_dummies(team_picks, prefix="TeamPick")
opp_picks_encoded = pd.get_dummies(opp_picks, prefix="OppPick")

# Group by the index (gameid) and sum the one-hot encoded columns
team_picks_encoded = team_picks_encoded.groupby(team_picks_encoded.index).sum()
opp_picks_encoded = opp_picks_encoded.groupby(opp_picks_encoded.index).sum()

# Join the one-hot encoded columns with the team_records dataframe
final_df = team_records.join(team_picks_encoded).join(opp_picks_encoded)

# Save the final dataframe to a CSV file
final_df.to_csv("final_df.csv", index=False)
# Save the Champion Career Stats dataframe to a CSV file
champ_career_stats.reset_index().to_csv("champ_career_stats.csv", index=False)
