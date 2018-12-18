import pandas as pd
import csv

match_id_list = []
def trim_columns(data_frame):
	"""
	:param data_frame:
	:return: trimmed data frame
	"""
	trim = lambda x: x.strip() if type(x) is str else x
	return data_frame.applymap(trim)

def raw():
	data = pd.read_csv("aggregate/agg_match_stats_4.csv", encoding = 'utf-8')
	data_raw  = data.loc[data['date'].str.startswith('2018-01-10')]
	data_raw.to_csv("agg_raw.csv", encoding = 'utf-8' )

def agg():
	data = pd.read_csv("agg_raw.csv", encoding = 'utf-8')
	#data_raw  = data.loc[data['date'].str.startswith('2018-01-10T10') | data['date'].str.startswith('2018-01-10T09') | data['date'].str.startswith('2018-01-10T08') ]
	data_raw  = data.loc[data['date'].str.startswith('2018-01-10T10')]
	data_raw.to_csv("agg.csv", encoding = 'utf-8' )
	return data_raw['match_id'].unique()

def death(list):
	data = pd.read_csv("deaths/kill_match_stats_final_4.csv", encoding = 'utf-8')
	data_new = data[data['match_id'].isin(list)]
	data_new.to_csv("death.csv", encoding = 'utf-8')

def create_map():
	data = pd.read_csv("death.csv", encoding = "utf-8")
	data_map = data.groupby('map', as_index=False).last()
	data_map[['map']].to_csv("map.csv", encoding = 'utf-8', index = False)

def create_weapon():
	data = pd.read_csv("death.csv", encoding = "utf-8")
	data_weapon = trim_columns(data.groupby('killed_by', as_index = False).last())
	data_weapon[['killed_by']].to_csv("weapon.csv", encoding = 'utf-8', index = False)

def create_match():
	agg = pd.read_csv("agg.csv", encoding = 'utf-8')
	death = pd.read_csv("death.csv", encoding = 'utf-8')
	agg_gb = agg.groupby('match_id', as_index = False).last()
	agg_gb = agg_gb[['match_id', 'date', 'game_size', 'match_mode', 'party_size']]
	#agg_gb.to_csv("match.csv", encoding = 'utf-8', index = False)
	death_gb = death.groupby('match_id', as_index = False).last()[['match_id', 'map']]
	m_m_diction = {}
	for index, row in death_gb.iterrows():
		m_m_diction[row['match_id']] = row['map']

	list = ['match_id', 'date', 'game_size', 'match_mode', 'party_size', 'map']
	length = len(agg_gb.index)
	df = pd.DataFrame(columns = list, index = range(length))
	for i in range(length):
		for item in list[:-1]:
			df.loc[i][item] = agg_gb.loc[i][item]
		df.loc[i]['map'] = m_m_diction[df.loc[i]['match_id']]

	df.to_csv("match.csv", encoding = 'utf-8', index = False)

def create_player():
	pl = pd.read_csv("agg.csv", encoding = 'utf-8')
	pl = pl[['player_name', 'player_kills', 'player_dbno', 'player_assists', 'player_dmg', 'player_dist_ride', 'player_dist_walk', 'player_survive_time']].groupby('player_name', as_index = False).mean()
	pl.to_csv("player.csv", encoding = 'utf-8', index = False)

def create_death():
	dt = pd.read_csv("death.csv", encoding = 'utf-8')
	dt = trim_columns(dt[['killed_by', 'killer_name', 'killer_placement', 'match_id', 'time', 'victim_name', 'victim_placement' ]])
	dt.to_csv("death_edit.csv", encoding = 'utf-8', index = False)

def create_team():
	t = pd.read_csv("agg.csv", encoding = 'utf-8')
	t = trim_columns(t[['match_id', 'team_id', 'team_placement']])
	t = t.groupby(['match_id', 'team_id'], as_index = False).last()
	t.to_csv("team.csv", encoding = 'utf-8', index = False)

def create_player_in_team():
	pit = pd.read_csv('agg.csv', encoding = 'utf-8')
	pit = trim_columns(pit[['match_id', 'team_id', 'player_name']])
	pit.to_csv('player_in_team.csv', encoding = 'utf-8', index = False)

def create_player_participate():
	pp = pd.read_csv('agg.csv', encoding = 'utf-8')
	pp = trim_columns(pp[['match_id', 'player_name']])
	pp.to_csv('player_participate.csv', encoding = 'utf-8', index = False)



if __name__ == '__main__':
	#match_id_list = agg()
	#death(match_id_list)
	#create_map()
	#create_weapon()
	#create_match()
	#create_player()
	#create_death()
	#create_team()
	#create_player_in_team()
	create_player_participate()