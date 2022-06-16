from basketball_reference_web_scraper import client
from pprint import pprint
import pandas as pd
import os

response = client.season_schedule(season_end_year=2018)

teams = []

for item in response:
    team = str(item["away_team"])
    team = team.split(".")
    team = team[1]

    if team in teams:
        pass
    else:
        teams.append(team)

df = pd.DataFrame({"Teams": teams})

teams = df["Teams"]
for team in teams:
    os.mkdir("../../data/" + team)

months = [10, 11, 12, 1, 2, 3, 4, 5, 6]

for month in months:
    for day in range(32):
        if day == 0:
            pass
        else:
            if month >=10:
                year = 2017
            else:
                year = 2018
            
            try:
                response = client.team_box_scores(day=day, month=month, year=year)
            except:
                response = client.team_box_scores(day=day, month=month, year=year)
            
            for game in response:
                index = response.index(game)
                if index % 2 == 0:
                    myteam_status = "away"
                    oppteam_status = "home"
                    opp = response[index+1]

                    oppteam_name = str(opp["team"])
                    oppteam_name = oppteam_name.split(".")
                    oppteam_name = oppteam_name[1]
                    
                    oppteam_assists = opp["assists"]
                    oppteam_attempted_field_goals = opp["attempted_field_goals"]
                    oppteam_attempted_free_throws = opp["attempted_free_throws"]
                    oppteam_attempted_three_point_field_goals = opp["attempted_three_point_field_goals"]
                    oppteam_blocks = opp["blocks"]
                    oppteam_defensive_rebounds = opp["defensive_rebounds"]
                    oppteam_made_field_goals = opp["made_field_goals"]
                    oppteam_made_free_throws = opp["made_free_throws"]
                    oppteam_made_three_point_field_goals = opp["made_three_point_field_goals"]
                    oppteam_offensive_rebounds = opp["offensive_rebounds"]
                    oppteam_personal_fouls = opp["personal_fouls"]
                    oppteam_points = opp["points"]
                    oppteam_steals = opp["steals"]
                    oppteam_turnovers = opp["turnovers"]

                    oppteam_outcome = str(opp["outcome"])
                    oppteam_outcome = oppteam_outcome.split(".")
                    oppteam_outcome = oppteam_outcome[1]

                else:
                    myteam_status = "home"
                    oppteam_status = "away"
                    opp = response[index-1]

                    oppteam_name = str(opp["team"])
                    oppteam_name = oppteam_name.split(".")
                    oppteam_name = oppteam_name[1]
                    
                    oppteam_assists = opp["assists"]
                    oppteam_attempted_field_goals = opp["attempted_field_goals"]
                    oppteam_attempted_free_throws = opp["attempted_free_throws"]
                    oppteam_attempted_three_point_field_goals = opp["attempted_three_point_field_goals"]
                    oppteam_blocks = opp["blocks"]
                    oppteam_defensive_rebounds = opp["defensive_rebounds"]
                    oppteam_made_field_goals = opp["made_field_goals"]
                    oppteam_made_free_throws = opp["made_free_throws"]
                    oppteam_made_three_point_field_goals = opp["made_three_point_field_goals"]
                    oppteam_offensive_rebounds = opp["offensive_rebounds"]
                    oppteam_personal_fouls = opp["personal_fouls"]
                    oppteam_points = opp["points"]
                    oppteam_steals = opp["steals"]
                    oppteam_turnovers = opp["turnovers"]

                    oppteam_outcome = str(opp["outcome"])
                    oppteam_outcome = oppteam_outcome.split(".")
                    oppteam_outcome = oppteam_outcome[1]
                
                myteam_name = str(game["team"])
                myteam_name = myteam_name.split(".")
                myteam_name = myteam_name[1]
                
                myteam_assists = game["assists"]
                myteam_attempted_field_goals = game["attempted_field_goals"]
                myteam_attempted_free_throws = game["attempted_free_throws"]
                myteam_attempted_three_point_field_goals = game["attempted_three_point_field_goals"]
                myteam_blocks = game["blocks"]
                myteam_defensive_rebounds = game["defensive_rebounds"]
                myteam_made_field_goals = game["made_field_goals"]
                myteam_made_free_throws = game["made_free_throws"]
                myteam_made_three_point_field_goals = game["made_three_point_field_goals"]
                myteam_offensive_rebounds = game["offensive_rebounds"]
                myteam_personal_fouls = game["personal_fouls"]
                myteam_points = game["points"]
                myteam_steals = game["steals"]
                myteam_turnovers = game["turnovers"]

                myteam_outcome = str(game["outcome"])
                myteam_outcome = myteam_outcome.split(".")
                myteam_outcome = myteam_outcome[1]
                
                if myteam_outcome == "WIN":
                    myteam_outcome = 1
                else:
                    myteam_outcome = 0

                date = str(month) + "_" + str(day) 

                dates = [date]
                names = [myteam_name]
                assists = [myteam_assists]
                att_field_goals = [myteam_attempted_field_goals]
                att_free_throws = [myteam_attempted_free_throws]
                att_three_points = [myteam_attempted_three_point_field_goals]
                blocks = [myteam_blocks]
                defensive_rebounds = [myteam_defensive_rebounds]
                made_field_goals = [myteam_made_field_goals]
                made_free_throws = [myteam_made_free_throws]
                made_three_point = [myteam_made_three_point_field_goals]
                offensive_rebounds = [myteam_offensive_rebounds]
                personal_fouls = [myteam_personal_fouls]
                points = [myteam_points]
                steals = [myteam_steals]
                turnovers = [myteam_turnovers]
                outcomes = [myteam_outcome]
                status = [myteam_status]

                opp_names = [oppteam_name]
                opp_assists = [oppteam_assists]
                opp_att_field_goals = [oppteam_attempted_field_goals]
                opp_att_free_throws = [oppteam_attempted_free_throws]
                opp_att_three_points = [oppteam_attempted_three_point_field_goals]
                opp_blocks = [oppteam_blocks]
                opp_defensive_rebounds = [oppteam_defensive_rebounds]
                opp_made_field_goals = [oppteam_made_field_goals]
                opp_made_free_throws = [oppteam_made_free_throws]
                opp_made_three_point = [oppteam_made_three_point_field_goals]
                opp_offensive_rebounds = [oppteam_offensive_rebounds]
                opp_personal_fouls = [oppteam_personal_fouls]
                opp_points = [oppteam_points]
                opp_steals = [oppteam_steals]
                opp_turnovers = [oppteam_turnovers]


                df = pd.DataFrame({"name": names,
                                    "status": status,
                                    "date": dates,
                                    "assists": assists,
                                    "att_field_goals": att_field_goals,
                                    "att_free_throws": att_free_throws,
                                    "att_three_points": att_three_points,
                                    "blocks": blocks,
                                    "defensive_rebounds": defensive_rebounds,
                                    "made_field_goals": made_field_goals,
                                    "made_free_throws": made_free_throws,
                                    "made_three_point": made_three_point,
                                    "offensive_rebounds": offensive_rebounds,
                                    "personal_fouls": personal_fouls,
                                    "points": points,
                                    "steals": steals,
                                    "turnovers": turnovers,
                                    "outcomes": outcomes,
                                    "opp_name": opp_names,
                                    "opp_assists": opp_assists,
                                    "opp_att_field_goals": opp_att_field_goals,
                                    "opp_att_free_throws": opp_att_free_throws,
                                    "opp_att_three_points": opp_att_three_points,
                                    "opp_blocks": opp_blocks,
                                    "opp_defensive_rebounds": opp_defensive_rebounds,
                                    "opp_made_field_goals": opp_made_field_goals,
                                    "opp_made_free_throws": opp_made_free_throws,
                                    "opp_made_three_point": opp_made_three_point,
                                    "opp_offensive_rebounds": opp_offensive_rebounds,
                                    "opp_personal_fouls": opp_personal_fouls,
                                    "opp_points": opp_points,
                                    "opp_steals": opp_steals,
                                    "opp_turnovers": opp_turnovers})
                
                file_list = os.listdir("../../data/" + myteam_name)
                number_files = len(file_list)
                
                df.to_csv("../../data/" + myteam_name + "/" + str(number_files) + "_game_" + str(month) + "_" + str(day) + ".csv", index=False)