import sys
import math
import os
import pandas as pd

def category():
	df = pd.read_csv("data_rmr/shannon_index_scenic_category.tsv", sep="\t")
	# print(df.head())
	env = df['category'].to_list()
	print(len(env))
	u_env = set(env)
	print(len(u_env))
	print(u_env)




if __name__ == '__main__':
	category()