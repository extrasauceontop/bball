from basketball_reference_web_scraper import client
import pandas as pd
import os
import pickle
from pprint import pprint
import datetime as DT
import json

with open('model_pickle.pickle', 'rb') as pickle_file:
    model = pickle.load(pickle_file)

today = DT.date.today()

response = client.season_schedule(season_end_year=2020)
games = []
for x in range(7):
    active_date = today + DT.timedelta(days=x)
    for game in response:
        game_day = game["start_time"].day
        game_month = game["start_time"].month
        game_year = game["start_time"].year

        if active_date.day == game_day and active_date.month == game_month and active_date.year == game_year:
            team_1 = str(game["away_team"])
            team_1 = team_1.split(".")
            team_1 = team_1[1]

            team_2 = str(game["home_team"])
            team_2 = team_2.split(".")
            team_2 = team_2[1]

            contest = [team_1, team_2, active_date]

            games.append(contest)

count = 0
dates = []
for game in games:
    dates.append(str(game[2].day) + "_" + str(game[2].month) + "_" + str(game[2].year))
    if count == 0:
        team_1 = game[0]
        team_2 = game[1]

        path_1 = "../../data/" + team_1 + "/game_avg.csv"
        path_2 = "../../data/" + team_2 + "/game_avg.csv"

        df_1 = pd.read_csv(path_1)
        df_2 = pd.read_csv(path_2)

        last_row_1 = pd.concat([df_1.tail(1)])
        last_row_2 = pd.concat([df_2.tail(1)])

        master_df = last_row_1.merge(last_row_2, on="date")
        master_df["name_x"].fillna(team_1, inplace=True)
        master_df["name_y"].fillna(team_2, inplace=True)
        master_df["status_x"].fillna(1, inplace=True)
        master_df["status_y"].fillna(0, inplace=True)
        count = count + 1
    else:
        team_1 = game[0]
        team_2 = game[1]

        path_1 = "../../data/" + team_1 + "/game_avg.csv"
        path_2 = "../../data/" + team_2 + "/game_avg.csv"

        df_1 = pd.read_csv(path_1)
        df_2 = pd.read_csv(path_2)

        last_row_1 = pd.concat([df_1.tail(1)])
        last_row_2 = pd.concat([df_2.tail(1)])

        contest_df = last_row_1.merge(last_row_2, on="date")
        contest_df["name_x"].fillna(team_1, inplace=True)
        contest_df["name_y"].fillna(team_2, inplace=True)
        contest_df["status_x"].fillna(1, inplace=True)
        contest_df["status_y"].fillna(0, inplace=True)

        master_df = master_df.append(contest_df)

master_df.to_csv("../../../master_df.csv")

master_df = master_df.drop(["outcomes_y", "opp_name_y", "points_actual_y"], axis=1)
master_test = master_df.drop(["name_x", "name_y", "date", "opp_name_x", "points_actual_x", "outcomes_x"], axis=1)

y_pred = model.predict(master_test)
master_df["pred_value"] = y_pred

preds = master_df["pred_value"].to_list()

winners = []
for pred in preds:
    index = preds.index(pred)
    if pred < 0.5:
        winner = games[index][1]
    else:
        winner = games[index][0]

    winners.append(winner)

master_df["pred_team"] = winners
final_df = master_df[["name_x", "name_y", "pred_value", "pred_team"]]
final_df["date"] = dates
final_df.to_csv("../../data/week_test.csv", index=False)

final_df = final_df.reset_index()
final_df = final_df.drop(["index"], axis=1)

df_anal = master_df[["outcomes_x", "pred_value"]]
df_anal["pred_outcome"] = master_df["pred_value"].round(0)

df_anal["pred_absolute"] = df_anal["pred_value"]-0.5
df_anal["pred_absolute"] = df_anal["pred_absolute"].abs()

outcome_list = df_anal["outcomes_x"].to_list()
pred_list = df_anal["pred_outcome"].to_list()

corrects = []
counter = 0
for outcome in outcome_list:
    pred = pred_list[counter]
    
    if outcome == pred:
        correct = 1
    else:
        correct = 0
    
    corrects.append(correct)
    counter = counter+1

df_anal["correct"] = corrects

bins = [0, 0.07999, 0.1599, 0.2399, 0.3199, 0.3999, 1]
group_names = ["F", "D", "C", "B", "A", "S"]

df_anal["pred_val_summary"] = pd.cut(df_anal["pred_absolute"], bins, labels=group_names, include_lowest=True)
df_anal = df_anal.reset_index()


final_df["confidence"] = df_anal["pred_val_summary"]

final_json = final_df.to_json(orient="index")
final_json = json.loads(final_json)

with open('../../data/week_picks.json', 'w') as output_file:
    json.dump(final_json, output_file)