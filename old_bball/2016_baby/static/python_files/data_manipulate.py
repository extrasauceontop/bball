import pandas as pd
import os

rootdir = '../../data'
x = 0
for dirs in os.walk(rootdir):
    if x > 0:
        break
    if x == 0:
        x = 1
    teams = dirs[1]
    for team in teams:
        path = "../../data/" + team + "/"
        for num in range(110):
            for file in os.listdir(path):
                if file == "combined_games.csv" or file == "ten_ma.csv" or file == "game_avg.csv" or file == "10_ma.csv" or file == "merge_opp.csv":
                    pass
                else:
                    order = file.split("_")
                    order = int(order[0])
                    if int(order) == num:
                        df = pd.read_csv(path + file)
                        if num == 0:
                            mega_df = df
                        else:
                            mega_df = mega_df.append(df, sort=False)
        mega_df["total_rebounds"] = mega_df["offensive_rebounds"] + mega_df["defensive_rebounds"]
        mega_df["opp_total_rebounds"] = mega_df["opp_offensive_rebounds"] + mega_df["opp_defensive_rebounds"]
        
        mega_df.to_csv("../../data/" + team + "/combined_games.csv", index = False)

x = 0
for dirs in os.walk(rootdir):
    if x > 0:
        break
    if x == 0:
        x = 1
    teams = dirs[1]
    for team in teams:
        df = pd.read_csv("../../data/" + team + "/combined_games.csv")
        for column in df:
            if column in ["name", "status", "date", "opp_name"]:
                pass
            else:
                df[column + "_10MA"] = df[column].rolling(window=10).mean()
        df.to_csv("../../data/" + team + "/ten_ma.csv", index=False)

x = 0
for dirs in os.walk(rootdir):
    if x > 0:
        break
    if x == 0:
        x = 1
    teams = dirs[1]
    for team in teams:
        final_df = 0
        df = pd.read_csv("../../data/" + team + "/ten_ma.csv")

        final_dict = {}

        for column in df:
            col_list = df[column].to_list()
            col_words = column.split("_")

            if "10MA" in col_words:
                col_list.insert(0, "")
                final_dict[column] = col_list

            elif column in ["name", "status", "date", "opp_name"]:
                col_list.append("")
                final_dict[column] = col_list
            
            elif column in ["assists", "blocks", "points", "total_rebounds", "opp_assists", "opp_blocks", "opp_points", "opp_total_rebounds", "outcomes"]:
                stats_total = 0
                counter = 0

                avg_stats = []

                for stat in col_list:
                    counter = counter + 1
                    stats_total = stats_total + stat
                    stats_avg = stats_total/counter

                    avg_stats.append(stats_avg)
                
                avg_stats.insert(0,"")
                col_list.append("")

                final_dict[column + "_game"] = col_list
                final_dict[column + "_avg"] = avg_stats
            
            else:
                stats_total = 0
                counter = 0

                avg_stats = []

                for stat in col_list:
                    counter = counter + 1
                    stats_total = stats_total + stat
                    stats_avg = stats_total/counter

                    avg_stats.append(stats_avg)
            
                avg_stats.insert(0,"")
                final_dict[column + "_avg"] = avg_stats
        
        avg_df = pd.DataFrame(final_dict)

        avg_df.to_csv("../../data/" + team + "/game_avg.csv", index=False)

x = 0
for dirs in os.walk(rootdir):
    if x > 0:
        break
    if x == 0:
        x = 1
    teams = dirs[1]
    for team in teams:
        path = "../../data/" + team + "/game_avg.csv"
        df = pd.read_csv(path)

        df = df.drop(df.index[0])
        df = df.drop(df.index[-1])

        for index, row in df.iterrows():
            date = row["date"]
            opp = row["opp_name"]

            opp_df = pd.read_csv("../../data/" + opp + "/game_avg.csv")
            game_row = opp_df.loc[opp_df['date'] == date]

            if index == 1:
                opp_rows = pd.DataFrame(game_row)
            else:
                new_row = pd.DataFrame(game_row)
                opp_rows = opp_rows.append(game_row)
        opp_dict = {}
        for column in opp_rows:
            new_c = opp_rows[column].to_list()
            column_name = column + "_opp"
            opp_dict[column_name] = new_c
        
        df_opp = pd.DataFrame(opp_dict)
        new_df = df.merge(opp_rows, on="date")
        new_df.to_csv("../../data/" + team + "/merge_opp.csv", index=False)

x = 0
for dirs in os.walk(rootdir):
    if x > 0:
        break
    if x == 0:
        x = 1
    teams = dirs[1]
    counter = 0
    for team in teams:
        path = "../../data/" + team + "/game_avg.csv"
        if counter == 0:
            master_df = pd.read_csv("../../data/" + team + "/merge_opp.csv")
        else:
            df = pd.read_csv("../../data/" + team + "/merge_opp.csv")
            master_df = master_df.append(df)
        counter = counter +1

master_df = master_df.drop(["outcomes_game_y", "opp_name_y", "opp_points_game_y", "opp_points_game_x", "opp_assists_game_x", "opp_assists_game_y", "opp_blocks_game_x", "opp_blocks_game_y"], axis=1)

status_df = master_df[["status_x", "status_y"]]

new = []
mydict = {}
for column in status_df:
    name = column
    mylist = status_df[column].to_list()
    new = []
    for item in mylist:
        if item == "home":
            new.append(1)
        else:
            new.append(0)
    master_df[name] = new

master_df = master_df.dropna()
master_df = master_df.drop("opp_total_rebounds_game_x", axis=1)
master_df = master_df.drop("opp_total_rebounds_game_y", axis=1)

master_df.to_csv("../../data/master.csv", index=False)