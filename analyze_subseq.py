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

	unique_seqs = set()

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
		unique_seqs.add(week)
		table[key] = tuple(table[key])

	pprint.pprint(table)

	print('\n***** UNIQUE SEQUENCES *****\n')
	pprint.pprint(unique_seqs)
	print('\nTotal unique sequences: ' + str(len(unique_seqs)))
	print('Total students: ' + str(len(table)))

	return table


def compute_subseq_stats(table):
	map_count = {
		'A': 0,
		'B': 0,
		'C': 0,
		'D': 0,
		'E': 0,
		'F': 0,
		'G': 0,
		'H': 0,
		'I': 0,
		'J': 0,
		'K': 0,
		'L': 0,
		'M': 0,
		'N': 0,
		'O': 0,
		'P': 0,
		'Q': 0,
		'R': 0,
		'S': 0,
		'T': 0,
		'U': 0,
		'V': 0,
		'W': 0,
		'X': 0,
		'Y': 0,
		'0': 0,
		'1': 0,
		'2': 0,
		'3': 0,
		'4': 0,
		'5': 0,
		'6': 0
	}

	for key in table.keys():
		seq = table[key][0]

		for char in seq:
			map_count[char] += 1

	sorted_count = sorted(map_count.items(), key=lambda item: item[1], reverse=True)
	sorted_count_dict = collections.OrderedDict(sorted_count)

	print('\n***** COUNT - SORTED *****\n')
	pprint.pprint(sorted_count_dict)


def main():
	table = create_table('hw5_reformatted_data_grades-ranked.csv')
	updated_table = shorten_sequence(table)
	compute_subseq_stats(updated_table)

	
if __name__== "__main__":
	main()