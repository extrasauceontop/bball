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
        print(team)