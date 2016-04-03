import csv
'''
flist = ['results/hidden_layer_0.txt','results/hidden_layer_40.txt','results/hidden_layer_80.txt',\
'results/hidden_layer_120.txt','results/hidden_layer_160.txt','results/hidden_layer_200.txt',\
'results/hidden_layer_240.txt', 'results/hidden_layer_280.txt', 'results/hidden_layer_320.txt',\
'results/hidden_layer_360.txt', 'results/hidden_layer_400.txt',\
 'results/hidden_layer_440.txt', 'results/hidden_layer_480.txt']
 '''
flist = ['vary_stepRate/sr_0.01.txt', 'vary_stepRate/sr_0.05.txt',\
 	'vary_stepRate/sr_0.1.txt', 'vary_stepRate/sr_0.25.txt']
with open('sr.csv', 'w') as fout:
	for f in flist:
		with open(f) as fin:
		    o=csv.writer(fout)
		    for line in fin:
		        o.writerow(line.split())