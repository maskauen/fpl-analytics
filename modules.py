
import csv, json
import pandas as pd  

def make_json(csvFilePath,k): 
    data = {} 
    with open(csvFilePath, encoding='utf-8') as csvf: 
        csvReader = csv.DictReader(csvf)   
        for rows in csvReader:
            rows = eval(json.dumps(rows)) 
            key = rows[k] 
            data[key] = rows 
    return data
 
def make_fixture_json(csvFilePath,k): 
    data = {} 
    finished = []
    with open(csvFilePath, encoding='utf-8') as csvf: 
        csvReader = csv.DictReader(csvf)   
        for rows in csvReader:
            rows = eval(json.dumps(rows))
            if rows["finished"] == 'True':
              if int(float(rows[k])) not in finished:
                finished.append(int(float(rows[k])))  
            key = rows[k]
            if key not in data.keys():
              data[key] = {}
              data[key][rows['id']] = rows
            else: data[key][rows['id']] = rows
    return data, finished


def program(team,gw,fixtures,n):
  program = {}
  for gw in range(gw+1,gw+n+1):
      for match_id,match in fixtures[str(gw)+".0"].items():
        a = match["team_a"]
        h = match["team_h"]
        if team in [a,h]:
          if team == a:
            program[gw] = [match['team_h'],match['team_a_difficulty']]
          else: 
            program[gw] = [match['team_a'],match['team_h_difficulty']]
  return program
 
def team_program(fixtures,finished,n):
  all_programs = {}
  for id in range(1,21):
      all_programs[str(id)] = program(str(id),len(finished),fixtures,n)
  return all_programs
 
 
def player_program(player,n,players,teams,fixtures,finished):
  team = players[player]['team']
  gw = len(finished)
  program_player = program(team,gw,fixtures,n)  
  return program_player
 
def print_player_program(player,n,program,teams):
  print("Program for "+player+" next "+str(n)+" gameweeks:\n")
  for gw,match in program.items():
      print("Gameweek "+str(gw)+": "+teams[match[0]]['name']+", difficulty "+match[1])
 
def print_team_program(all_programs,teams,n):
  avg_diff = {}
  for id,program in all_programs.items():
      #print(id)
      #print(program)
      #a=input()
      difficulty = round(sum([int(stat[1]) for opp,stat in program.items()])/int(n),2)
      team = teams[id]['name']
      avg_diff[team] = difficulty
  
  df_sorted = pd.Series(avg_diff).to_frame('Difficulty next '+str(n)).sort_values(by=['Difficulty next '+str(n)],ascending=False)
  return df_sorted

def understat(season_path,team):
  csvFilePath = season_path+'understat/understat_'+team+'.csv'
  data = {} 
  with open(csvFilePath, encoding='utf-8') as csvf: 
      csvReader = csv.DictReader(csvf)
      gw = 1   
      for rows in csvReader:
          rows = eval(json.dumps(rows))
          data[str(gw)] = rows 
          gw = gw + 1
  
  df = pd.DataFrame.from_dict(data)
  return df

def pre_process_season(fixtures, lower_game_streak_threshold, upper_difficulty_threshold):

  team_dict = {}
  team_count = {str(t):0 for t in range(1,21)}

  start = 1
  end = 39

  for gw in range(start,end):
      for match_id,match in fixtures[str(gw)+".0"].items():
        a = match["team_a"]
        h = match["team_h"]          
        home_team_opponent_diff = int(match['team_a_difficulty'])
        away_team_opponent_diff = int(match['team_h_difficulty'])

        for t,diff in zip([a,h],[home_team_opponent_diff,away_team_opponent_diff]):
          if gw < 4:
            if t not in team_dict.keys():
              team_dict[t] = []
          

          if diff < upper_difficulty_threshold:
            team_count[t] += 1
          else:
            if team_count[t] > lower_game_streak_threshold:
              team_dict[t].append({"start":gw-team_count[t],"length":team_count[t]})            
            team_count[t] = 0
  return team_dict


def sort_pre_process(team_dict,teams,lower_game_streak_threshold, upper_difficulty_threshold,longest_streaks):
  entries = []
  for team_id,list_streaks in team_dict.items():
    team = teams[team_id]["name"]
    for streak_data in list_streaks:
      entries.append({"team":team,"length":streak_data["length"],"start":streak_data["start"]})

  try:
    df = pd.DataFrame(entries)
    df = df.sort_values(by=['length'],ascending=False)
  except:
    print("No hits for these specifications")
  print(df.iloc[:longest_streaks+1,:])

def process_injuries(players):
    null = None
    list_25 = []
    list_null = []
    list_50 = []
    list_75 = []
    list_100 = []

    for element in players:
        chance_of_playing = element["chance_of_playing_next_round"]
        if chance_of_playing == 25:
            list_25.append(element["second_name"])
        if chance_of_playing == 50:
            list_50.append(element["second_name"]) 
        if chance_of_playing == 75:
            list_75.append(element["second_name"]) 
        if chance_of_playing == 100:
            list_100.append(element["second_name"]) 
        if chance_of_playing == null:
            list_null.append(element["second_name"]) 
        
    return list_null,list_75,list_100,list_50,list_25