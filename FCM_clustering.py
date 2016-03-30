from nhlDataParser import process_players
import skfuzzy
import numpy
import random

features = ["Goals vs Assists", "Takeaways v Giveaways", "Corsi For %", "Points/game", "Penalties/game", "Hits/game"]# "Blocks/game"]

def get_data_points(start, feature, data):
	data_points = []
	names = []
	players = []
	min_features = feature(data[0][data[0].keys()[0]])
	max_features = feature(data[0][data[0].keys()[0]])

	for player in data:
		sorted_y = sorted(player.keys())
		years = [y for y in sorted_y if y >= 2008]
		full_vector = player[sorted_y[start]] if sorted_y[start] >= 2008 else player[years[0]]
		feature_v = feature(full_vector)
		for i,f in enumerate(feature_v):
			if f < min_features[i]:
				min_features[i] = f
			if f > max_features[i]:
				max_features[i] = f
	for player in data:
		sorted_y = sorted(player.keys())
		years = [y for y in sorted_y if y >= 2008]
		full_vector = player[sorted_y[start]] if sorted_y[start] >= 2008 else player[years[0]]

		data_points.append(feature(full_vector, maxf=max_features, minf=min_features))
		names.append(full_vector['Player'])
		players.append((feature(full_vector),feature(full_vector, maxf=max_features, minf=min_features)))
	return numpy.transpose(numpy.array(data_points)), data_points, names, players, min_features, max_features

def extract_forward_features(full_vector, maxf=None, minf=None):
	# goals vs assists
	g_v_a = float(full_vector['G'])/(float(full_vector['A']) if float(full_vector['A']) > 0 else 1.0)

	# takeaways vs giveaways
	t_v_g = (float(full_vector['TK']) if 'TK' in full_vector else 0.0)/(float(full_vector['GW']) if float(full_vector['GW']) > 0 else 1.0)

	# corsi
	c_perc = float(full_vector['CF%'])/100.0

	# points per game
	p_v_g = float(full_vector['PTS'])/float(full_vector['GP'])

	# penalties per game
	pn_v_g = float(full_vector['PIM'])/float(full_vector['GP'])

	# hits per game
	h_v_g = float(full_vector['HIT'])/float(full_vector['GP'])

	# blocks per game
	#b_v_g = float(full_vector['BLK'])/float(full_vector['GP'])

	stat = [g_v_a, t_v_g, c_perc, p_v_g, pn_v_g, h_v_g] #b_v_g]

	if minf and maxf:
		for i,s in enumerate(stat):
			stat[i] = (stat[i] - minf[i])/maxf[i]

	return stat

def get_clustering(points, data, min_cluster, max_cluster, error=0.00005, iters=1000000):
	fpcs = []
	cntrs = []
	us = []
	print min_cluster
	print max_cluster
	for c in range(min_cluster,max_cluster + 1):
		cntr, u, u0, d, jm, p, fpc = skfuzzy.cluster.cmeans(points, c, 2, error=error, maxiter=iters, init=None)
		random.shuffle(data)
		for i in range(10):
			prev_u = u
			cntr, u, u0, d, jm, p, fpc = skfuzzy.cluster.cmeans(numpy.transpose(numpy.array(data)), c, 2, error=error, maxiter=iters, init=prev_u)
			random.shuffle(data)
		cntr, u, u0, d, jm, p, fpc = skfuzzy.cluster.cmeans(points, c, 2, error=error, maxiter=iters, init=prev_u)
		fpcs.append((c,fpc))
		cntrs.append(cntr)
		us.append(u)
	return cntrs, fpcs, us

def print_details(center, minf, maxf):
	line = ""
	for i,attr in enumerate(center):
		val = attr * (maxf[i] - minf[i]) + minf[i]
		line += features[i] + " " + str(val) + "\n"
	print line
	print "-------------------------------------------------------------------"

def write_details(f, center, minf, maxf, i, players):
	line = ""
	for i,attr in enumerate(center):
		val = attr * (maxf[i] - minf[i]) + minf[i]
		line += features[i] + " " + str(val) + "\n"
	f.write("Cluster" + str(i) + ":\n")
	f.write(line)
	f.write(str(players) + '\n')
	f.write("-------------------------------------------------------------------\n")

def cluster():
	p,f,d = process_players()
	data, data_points, names, players, minf, maxf = get_data_points(2, extract_forward_features, f)
	c, fpc, u = get_clustering(data, data_points, 2, 12)
	clusters = []
	g_names = []
	g_players = []
	for i,part in enumerate(u):
		clusters.append(numpy.argmax(part, axis=0))
		groups = [[] for j in range(i+2)]
		groups_p = [[] for j in range(i+2)]
		for j,arg in enumerate(names):
			groups[clusters[i][j]].append((j,arg))
			groups_p[clusters[i][j]].append(players[j])
		g_names.append(groups)
		g_players.append(groups_p)

	return c, fpc, u, clusters, g_names, names, data, players, minf, maxf

def do_clustering():
	c, fpc, u, clusters, g_names, names, data, players, minf, maxf = cluster()
	num_clusters = 7
	part = u[num_clusters - 2]
	part = numpy.transpose(part)
	f = open('playstyle.csv','w')
	for i,name in enumerate(names):
		f.write('%s,%f,%f,%f,%f,%f,%f,%f\n' % (name, part[i][0], part[i][1], part[i][2], part[i][3], part[i][4], part[i][5], part[i][6]))
	f.close()








