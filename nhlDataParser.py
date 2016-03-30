
import csv
def is_number(s):
    try:
        return int(s)
    except ValueError:
        return 100

playerDict = {}
playerData = {}

def gamePlayedBefore2008():
	flist = ['basic_stats/leagues_NHL_2004_skaters_stats.csv','basic_stats/leagues_NHL_2006_skaters_stats.csv',
			 'basic_stats/leagues_NHL_2007_skaters_stats.csv']
	year = 2004
	for fname in flist:
		with open(fname, 'r') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				gamesPlayed = is_number(row['GP'])
				age = is_number(row['Age'])
				p = row['Player']
				if (p in playerDict):
					playerDict[p] += gamesPlayed
				elif (age < 24):
					playerDict[p] = gamesPlayed
					playerData[p] = {}

			year += 1
			if year == 2005:
				year += 1
		csvfile.close()

def findNonRookies():
	ret = []
	for player in playerDict:
		if playerDict[player] > 90:
			#print player, playerDict[player]
			ret.append(player)
	return ret

def findPlayers():
	fileList = ['adv_stats/leagues_NHL_2008_skaters-advanced_stats_adv.csv', 'adv_stats/leagues_NHL_2009_skaters-advanced_stats_adv.csv', \
	'adv_stats/leagues_NHL_2010_skaters-advanced_stats_adv.csv', 'adv_stats/leagues_NHL_2011_skaters-advanced_stats_adv.csv', \
	'adv_stats/leagues_NHL_2012_skaters-advanced_stats_adv.csv', 'adv_stats/leagues_NHL_2013_skaters-advanced_stats_adv.csv', \
	'adv_stats/leagues_NHL_2014_skaters-advanced_stats_adv.csv']
	# 'adv_stats/leagues_NHL_2015_skaters-advanced_stats_adv.csv']
	year = 2008
	for fname in fileList:
		with open(fname, 'r') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				age = is_number(row['Age'])
				gamesPlayed = is_number(row['GP'])
				p = row['Player']
				if (p in playerDict):
					playerDict[p] += gamesPlayed
					playerData[p][year] = row
				elif (age < 24):
					playerDict[p] = gamesPlayed
					tmp =  "\n%d: %s" %(year, row)
					playerData[p] = {}
					playerData[p][year] = row
				#	print row['Player'], row['Age'], row['GP'], row['CF%'], row['CF% rel'], row["FF%"],\
				#		row["FF% rel"], row['oiSH%'], row['oiSV%'], row['oZS%'], row['dZS%']
			year += 1
		csvfile.close()

def deletePlayers(plist):
	for p in plist:
		del playerDict[p]
		del playerData[p]

def playersWithTooFewGames(deletePlayers):
	for p in playerDict:
		if playerDict[p] < 82:
			deletePlayers.append(p)
	#return p
def addBasicStats():
	fileList = ['basic_stats/leagues_NHL_2008_skaters_stats.csv', 'basic_stats/leagues_NHL_2009_skaters_stats.csv', 
				'basic_stats/leagues_NHL_2010_skaters_stats.csv', 'basic_stats/leagues_NHL_2011_skaters_stats.csv',
				'basic_stats/leagues_NHL_2012_skaters_stats.csv', 'basic_stats/leagues_NHL_2013_skaters_stats.csv',
				'basic_stats/leagues_NHL_2014_skaters_stats.csv']
				#'basic_stats/leagues_NHL_2015_skaters_stats.csv']

	year = 2008
	for fname in fileList:
		with open(fname, 'r') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				player = row['Player']
				if player in playerData:
					tmp = playerData[player][year]
					for attri in row:
						if not(attri in tmp):
							playerData[player][year][attri] = row[attri]
		year += 1
		csvfile.close()

def process_players():
	gamePlayedBefore2008()
	deleting = findNonRookies()
	findPlayers()
	playersWithTooFewGames(deleting)
	deletePlayers(deleting)
	addBasicStats()

	forwardList = []
	defenseList = []
	for p in playerData:
		player = playerData[p]
		if len(player) >= 4:
			#print player
			for year in player:
				if (player[year]['Pos'] == 'D'):
					defenseList.append(player)
				else:
					forwardList.append(player)
				break
	return playerData, forwardList, defenseList

if __name__ == '__main__':
	playerData, forwardList, defenseList = process_players()
	print len(playerData)
	print len(forwardList)
	print len(defenseList)	

'''
PlayerData[playerName][Year] = attributes


#print(row[1], row[2], row[5], row[8], row[9], row[14], row[15], row[16], row[17], row[19], row[20]) 
		#"Rk","Player","Age","Tm","Pos","GP","CF","CA","CF%","CF%rel","C/60","Crel/60","FF","FA","FF%",
		#"FF% rel","oiSH%","oiSV%","PDO","oZS%","dZS%","TOI/60","TOI(EV)","TK","GV","SAtt.","Thru%"

classification of players:
PP time vs SH time, shot attempts, 

Notes
scope: any NHL player under age of 23 and less than 82 games played at the start of the period
Collect up to first 3 season of data from player
If a player has less than 82 games of data in total, the sample size is too small for evaluation
Then compare projected growth to the average result up until present

The most popular of such statistics is Corsi, which counts the number
of events that are goals, shots on goal, missed shots, or blocked shots. Fenwick is another
statistic; it is Corsi but without counting blocked shots.

QoC	Quality of Competition - Average Corsi of one's opponents
QoT	Quality of Temmates - Average Corsi of one's teammates
RQoC	Quality of Competition Relative to teammates
RQoT	Quality of Teammates Relative to other teammates

'''