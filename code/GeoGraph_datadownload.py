import sys
import requests
import xml.etree.ElementTree as ET
import os

apikey = "e6de3d2431"


def get_pic_details(photo_id):
	mString = "https://api.geograph.org.uk/api/photo/" + photo_id + "/" + apikey
	print(mString)
	response = requests.get(mString)
	if response.status_code == 200:
		users = response.text
		return(users)
	else:
		print('Error: {}'.format(response.status_code))
		return("")


def save_image_to_local(img_url, save_path):
    try:
        response = requests.get(img_url)
        if response.status_code == 200:
            with open("../download/" + save_path + ".jpg", 'wb') as f:
                f.write(response.content)
            print("Image saved successfully.")
        else:
            print("Failed to download the image.")
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)


def get_pic_url(text):
	pass



def get_image_paths():
	mFile = open("../data/sample.tsv", "r")
	# next(mFile)
	table = {}
	for ele in mFile:
		data = ele.rstrip().split("\t")
		mID = data[0]
		mPhotoID = data[-1].split("/")[-1]
		# print(mPhotoID)
		table[mID] = mPhotoID
	return table


def test():
	# files = os.listdir("../download")
	# existing = []
	# for file in files:
	# 	data = file.split(".")[0]
	# 	existing.append(data)
	# # print(existing)
	oFile = open("category.tsv", "w")
	ww = get_image_paths()
	for key, value in ww.items():
		data = get_pic_details(ww[key])
		if data != "":
			root = ET.fromstring(data)
			print(ET.tostring(root, encoding='utf-8').decode('utf-8'))
			img_src = root.findtext('category')
			mString = str(key) + "\t" + img_src + "\n"
			oFile.write(mString)
	oFile.close()
			
			


# def main():
# 	print("program starts ...")
# 	files = os.listdir("../download")
# 	existing = []
# 	for file in files:
# 		data = file.split(".")[0]
# 		existing.append(data)
# 	# print(existing)
# 	ww = get_image_paths()
# 	for key, value in ww.items():
# 		if key in existing:
# 			pass
# 		else:
# 			data = get_pic_details(ww[key])
# 			if data != "":
# 				root = ET.fromstring(data)
# 				print(ET.tostring(root, encoding='utf-8').decode('utf-8'))
# 				img_src = root.find('img').get('src')
# 				print(img_src)
# 				save_image_to_local(img_src, key)

if __name__ == '__main__':
	# main()
	test()