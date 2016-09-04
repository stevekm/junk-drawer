#!/usr/bin/env python
# python 2.7


# have: a table concatenated into a single line separated by \t
# want: an actual table, with 5 columns
# need to convert every 5th \t into a \n



import sys
import os
import collections
import pandas as pd

def list_file_lines(file_path):
    # not blank lines, no trailing \n
    with open(file_path, 'r') as f:
        entries = [line.strip() for line in f if line.strip()]
    return entries

# read the file; 
loans_table_path = "/Users/steve/Downloads/loan_transactions2.txt"
loans_string = list_file_lines(loans_table_path)

# print loans_string
# ['Date\tDescription\tPrincipal\tInterest\tFees\tTotal\t08/16/2016\ .... ]

# split on '\t'
loans_split = loans_string[0].split('\t')

# categories for the final table
categories = ['Date', 'Description', 'Principal', 'Interest', 'Fees', 'Total']

# load into dict for conversion to df later
# loans_dict = {}
loans_dict = collections.OrderedDict()

for item in categories:
	loans_dict[item] = []

# number of categories
q = len(loans_dict.keys())
print q, 'is q'
# category iterator
k = 0

# iterate over the items, add each into the corresponding dict key
for item in loans_split:
	key = loans_dict.keys()[k]
	if k < (q - 1):
		loans_dict[key].append(item)
		k += 1
	else:
		loans_dict[key].append(item)
		k = 0

# convert dict to df
loans_df = pd.DataFrame.from_dict(loans_dict).drop([0]) # 1st row = old colnames

print loans_df

# save it
loans_df.to_csv('/Users/steve/Downloads/loan_transactions3.tsv', sep = '\t', index = False)

# $ python format_table.py
# 6 is q
#           Date   Description   Principal Interest   Fees       Total
# 1   08/16/2016       PAYMENT    -$459.78   -$0.87  $0.00    -$460.65
# 2   08/05/2016       PAYMENT    -$248.04   -$1.96  $0.00    -$250.00
# 3   07/20/2016       PAYMENT     -$49.83   -$0.52  $0.00     -$50.35
