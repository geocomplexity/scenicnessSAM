import sys


def main():
	table = []
	mFile = open("data/sample2.tsv", "r")
	for ele in mFile:
		data = ele.strip().split("\t")
		mID = data[0]
		mPhotoID = data[-1].split("/")[-1]
		table.append(mID)
	mFile.close()
	mFile2 = open("data/votes2.tsv", "r")
	oFile = open("data/votes3.tsv", "w")
	for ele2 in mFile2:
		data2 = ele2.rstrip().split("\t")
		if data2[0] in table:
			pass
		else:
			oFile.write(ele2)
	mFile2.close()
	oFile.close()




if __name__ == '__main__':
	main()