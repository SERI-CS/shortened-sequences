import pandas as pd
import pprint
import jaro 
import random
import collections


def create_table(filename):
	df = pd.read_csv(filename,header=None)
	char_sequence = ''
	penn_id = 0
	table = dict()

	for _, row in df.iterrows():
		grade = 0
		rank = 0
		for col in range(0, len(row)):
			if col == 0:
				penn_id = row[col]
			elif col == len(row) - 2:
				grade = row[col]
			elif col == len(row) - 1:
				rank = row[col]
			elif row[col] == 0:
				char_sequence += 'Y'
			else:
				mod = (col - 1) % 5

				if mod == 0:
					char_sequence += 'C' # Canvas
				elif mod == 1:
					char_sequence += 'A' # CodioAssign
				elif mod == 2:
					char_sequence += 'L' # CodioLecture
				elif mod == 3:
					char_sequence += 'T' # OHQ
				else: # mod == 4
					char_sequence += 'G' # Piazza
	 	
		table[int(penn_id)] = [char_sequence, grade, rank]
		char_sequence = ''

	return table


def shorten_sequence(table):
	seq_map = {
		'CYYYY': 'A',
		'YAYYY': 'B',
		'YYLYY': 'C',
		'YYYTY': 'D',
		'YYYYG': 'E',

		'CAYYY': 'F',
		'CYLYY': 'G',
		'CYYTY': 'H',
		'CYYYG': 'I',

		'YALYY': 'J',
		'YAYTY': 'K',
		'YAYYG': 'L',

		'YYLTY': 'M',
		'YYLYG': 'N',

		'YYYTG': 'O',

		'CALYY': 'P',
		'CAYTY': 'Q',
		'CAYYG': 'R',

		'CYLTY': 'S',
		'CYLYG': 'T',
		'CYYTG': 'U',

		'YALTY': 'V',
		'YALYG': 'W',
		'YAYTG': 'X',

		'YYLTG': 'Y',

		'YYYYY': '0',
		'CALTG': '1',

		'YALTG': '2',
		'CYLTG': '3',
		'CAYTG': '4',
		'CALYG': '5',
		'CALTY': '6'
	}

	for key in table.keys():

		seq = table[key][0]
		week = ''

		start = 0
		end = 5

		for i in range(7):
			subseq = seq[start:end]
			day = seq_map[subseq]

			week += day

			start = end
			end += 5

		table[key][0] = week
		table[key] = tuple(table[key])

	# pprint.pprint(table)

	return table


def jaro_cluster(table):
	clusters = dict()

	# while table !empty
	while table:

		table_list = list(table.items())
		random_seed = random.choice(table_list) 
		# random_seed format: (56518271, ('YYYYYYAYYYYYYYGYYYYYYYYYGYYYTGYYYYG', 95, 212))

		clusters[random_seed] = []
		seq1 = random_seed[1][0]

		for item in table_list:
			seq2 = item[1][0]

			jaro_sim = jaro.jaro_metric(seq1, seq2)

			if jaro_sim > 0.90:
				clusters[random_seed].append((seq2, item[0], item[1][1], item[1][2], jaro_sim))
				del table[item[0]]

	pprint.pprint(clusters)

	return clusters


def compute_cluster_stats(clusters):	
	avg_rank = {}
	outliers = 0

	for key in clusters.keys():
		running_total = 0
		count = 0

		for tup in clusters[key]:
			running_total += tup[3]
			count += 1

		if count > 0:
			avg_rank[(key[0], key[1][0])] = (round(running_total / count, 2), len(clusters[key]))

			if avg_rank[(key[0], key[1][0])][1] == 1:
				outliers += 1

	sorted_rank = sorted(avg_rank.items(), key=lambda item: item[1])
	sorted_rank_dict = collections.OrderedDict(sorted_rank)
	print('\n***** AVG RANK - SORTED *****\n')
	pprint.pprint(sorted_rank_dict)

	total_clusters = len(avg_rank)

	print('\nTotal Clusters: ' + str(total_clusters))
	print('Clusters with just 1 student: ' + str(outliers))
	print('Clusters with more than 1 student: ' + str(total_clusters - outliers))


def main():
	table = create_table('hw5_reformatted_data_grades-ranked.csv')
	updated_table = shorten_sequence(table)

	clusters = jaro_cluster(updated_table)
	compute_cluster_stats(clusters)

	
if __name__== "__main__":
	main()
