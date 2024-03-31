import sys
import math
import os

def shannon_diversity_index(data):
	total_count = sum(data)
	if total_count == 0:
		raise ValueError("The data list is empty.")
	
	probabilities = [count / total_count for count in data]
	shannon_index = -sum(p * math.log(p) for p in probabilities if p != 0)
	
	return shannon_index

# # Example usage:
# data = [10, 20, 5, 15, 30]
# shannon_index = shannon_diversity_index(data)
# print("Shannon Diversity Index:", shannon_index)


import math

def scaled_shannon_diversity_index(data):
	total_count = sum(data)
	if total_count == 0:
		raise ValueError("The data list is empty.")
	
	probabilities = [count / total_count for count in data]
	shannon_index = -sum(p * math.log(p) for p in probabilities if p != 0)
	
	# Scale the Shannon Diversity Index from 1 to 10
	scaled_index = (shannon_index - 1) / (math.log(len(data))) * 9 + 1
	
	return scaled_index


def gini_coefficient(data):
	# Sort the data in ascending order
	sorted_data = sorted(data)
	n = len(data)
	if n == 0:
		raise ValueError("The data list is empty.")
	
	# Calculate the cumulative proportion of values and cumulative proportion of income
	cumulative_values = [i * value for i, value in enumerate(sorted_data, 1)]
	cumulative_income = sum(cumulative_values)
	
	# Calculate the Gini Coefficient
	gini_coefficient = (n + 1 - 2 * sum(cumulative_values)) / (n * sum(sorted_data))
	
	return gini_coefficient

def htb(data):
	"""
	Applies the head/tail breaks algorithm to an array of data.

	Params
	------
	data : list
		Array of data to apply ht-breaks

	Returns
	-------
	results : list 
		List of data representing break points
	"""
	# test input
	assert data, "Input must not be empty."
	assert all(isinstance(datum, int) or isinstance(datum, float) for datum in data), "All input values must be numeric."

	results = []  # array of break points

	def htb_inner(data):
		"""
		Inner ht breaks function for recursively computing the break points.
		"""
		# Add mean to results
		data_length = float(len(data))
		data_mean = sum(data) / data_length
		results.append(data_mean)

		# Recursive call to get next break point
		head = [datum for datum in data if datum > data_mean]
		while len(head) > 1 and len(head) / data_length < 0.40:
			return htb_inner(head)

	htb_inner(data)

	return results


def main():
	oFile = open("data/shannon_index.tsv", "w")
	print("program starts ...")
	files = os.listdir("geo_result")
	for file in files:
		print(file)
		idx = file.split("_")[0]
		print(idx)
		data = []
		mFile = open("geo_result/" + file, "r")
		for ele in mFile:
			data.append(int(ele.rstrip()))
		shannon_index = shannon_diversity_index(data)
		scaled_shannon_index = scaled_shannon_diversity_index(data)
		gini = gini_coefficient(data)
		ht_index = htb(data)
		mString = idx + "\t" + str(len(data)) + "\t" + str(shannon_index) + "\t" + str(scaled_shannon_index) + "\t" + str(gini) + "\t" + str(ht_index) +"\n"
		oFile.write(mString)
	oFile.close()


def join_tables():
	table_org ={}
	file_org = open("data/sample.tsv","r")
	for ele in file_org:
		data = ele.rstrip().split("\t")
		table_org[data[0]] = [data[3],data[4]]
	print(table_org)
	file_org.close()
	file_index = open("data/shannon_index.tsv", "r")
	oFile = open("data/shannon_index_scenic.tsv", "w")
	for ele2 in file_index:
		data2 = ele2.rstrip().split("\t")
		if data2[0] in table_org:
			mString = "\t".join(data2) + "\t" + table_org[data2[0]][0] + "\t" + table_org[data2[0]][1] + "\n"
			print(mString)
			oFile.write(mString)
	oFile.close() 
	file_index.close()

def join_category():
	table_org ={}
	file_org = open("data/category.tsv", "r")
	for ele in file_org:
		print(ele)
		data = ele.rstrip().split("\t")
		table_org[data[0]] = data[1]
	print(table_org)
	file_org.close()
	file_index = open("data/shannon_index_scenic.tsv", "r")
	oFile = open("data/shannon_index_scenic_category.tsv", "w")
	for ele2 in file_index:
		data2 = ele2.rstrip().split("\t")
		print(data2)
		if data2[0] in table_org:
			print(table_org[data2[0]])
			mString = "\t".join(data2) + "\t" + table_org[data2[0]] + "\n"
			print(mString)
			oFile.write(mString)
	oFile.close() 
	file_index.close()




if __name__ == '__main__':
	main()
	join_tables()
	join_category()