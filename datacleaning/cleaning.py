import pandas as pd
import numpy as np

def load_data(filename):
    return pd.read_csv(filename)

def filter_data(df):
    # filter out unneeded columns
    # used_columns = [['date'], ['season'],['team1'],['team2'],['elo1_post'],['elo2_post'],['qbelo1_post'],['qbelo2_post']]
    filtered = df[['date','season','team1','team2','elo1_post','elo2_post','qbelo1_post','qbelo2_post']]
    # narrow rows by year
    filtered = filtered[filtered['season'] >= 2013]
    return filtered

elo_data = load_data('nfl_elo.csv')
elo_data = filter_data(elo_data)

list_of_seasons = sorted(list(set(elo_data['season'])))
list_of_teams = list(set(elo_data['team1']))

# get the latest elo rating per team, per year
def get_elo_datapoints(df):

    seasons = np.array(df['season'])
    team1 = np.array(df['team1'])
    team2 = np.array(df['team2'])
    elo1_post = np.array(df['elo1_post'])
    elo2_post = np.array(df['elo2_post'])
    qbelo1_post = np.array(df['qbelo1_post'])
    qbelo2_post = np.array(df['qbelo2_post'])

    team_dict = {}
    # fill with array of 0s len(list_of_seasons) for each team
    for team in list_of_teams:
        team_dict[team] = np.zeros((len(list_of_seasons), 2))

    for i in range(len(team1)):
        team_dict[team1[i]][list_of_seasons.index(seasons[i])] = [elo1_post[i], qbelo1_post[i]]
        team_dict[team2[i]][list_of_seasons.index(seasons[i])] = [elo2_post[i], qbelo2_post[i]]
    
    return team_dict

team_names = {'Eagles':'PHI',
                'Cowboys':'DAL',
                'Giants':'NYG',
                'Commanders':'WSH',
                'Rams':'LAR',
                '49ers':'SF',
                'Cardinals':'ARI',
                'Seahawks':'SEA',
                'Packers':'GB',
                'Vikings':'MIN',
                'Bears':'CHI',
                'Lions':'DET',
                'Buccaneers':'TB',
                'Panthers':'CAR',
                'Saints':'NO',
                'Falcons':'ATL',
                'Dolphins':'MIA',
                'Patriots':'NE',
                'Bills':'BUF',
                'Jets':'NYJ',
                'Chiefs':'KC',
                'Chargers':'LAC',
                'Raiders':'OAK',
                'Broncos':'DEN',
                'Steelers':'PIT',
                'Ravens':'BAL',
                'Browns':'CLE',
                'Bengals':'CIN',
                'Colts':'IND',
                'Titans':'TEN',
                'Texans':'HOU',
                'Jaguars':'JAX',}

def add_data_by_year(elo_dict, year):
    cap_data = load_data('PosSpending'+str(year)+'.csv')
    # print(cap_data.head())
    teams = np.array(cap_data['Team'])
    teamnick = []
    elo1 = []
    elo2 = []
    season = []
    for team in teams:
        teamnick.append(team)
        season.append(year)
        elos = elo_dict[team_names.get(team)][list_of_seasons.index(year)]
        elo1.append(elos[0])
        elo2.append(elos[1])
        # print(elos[0], elos[1])
        # print(year, '\t', team, '\t', elo_dict[team_names.get(team)][list_of_seasons.index(year)])
    
    mergedf = pd.DataFrame({'Team':teamnick, 'Season':season,
                    'EndSeasonELO':elo1, 'QBAdjEndSeasonElo':elo2})

    newdf = mergedf.merge(cap_data, how='inner',on='Team')
    return newdf

def merge_dfs(elo_dict_by_team):
    
    df_list = []

    for season in list_of_seasons:
        df_list.append(add_data_by_year(elo_dict_by_team, season))

    complete_df = pd.DataFrame()

    for df in df_list:
        complete_df = complete_df.append(df)
    
    return complete_df

# next steps:
    # figure out what analysis I am going to do, what questions I can answer
        # clustering
        # what will I do with powerbi?

elo_dict_by_team = get_elo_datapoints(elo_data)
elo_cap_total_df = merge_dfs(elo_dict_by_team)
elo_cap_total_df.to_csv('elo_and_cap_data.csv')

# print(elo_data.head())