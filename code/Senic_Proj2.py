import sys
import torch
import torchvision
print("PyTorch version:", torch.__version__)
print("Torchvision version:", torchvision.__version__)
print("CUDA is available:", torch.cuda.is_available())
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor
import numpy as np
import torch
import matplotlib.pyplot as plt
import cv2
import base64
import supervision as sv
import os

sam_checkpoint = "sam_vit_h_4b8939.pth"
model_type = "vit_h"
device = "cuda"

sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device=device)
mask_generator = SamAutomaticMaskGenerator(sam)


def encode_image(filepath):
	with open(filepath, 'rb') as f:
		image_bytes = f.read()
	encoded = str(base64.b64encode(image_bytes), 'utf-8')
	return "data:image/jpg;base64,"+encoded

def show_anns(anns):
	if len(anns) == 0:
		return
	sorted_anns = sorted(anns, key=(lambda x: x['area']), reverse=True)
	ax = plt.gca()
	ax.set_autoscale_on(False)
	img = np.ones((sorted_anns[0]['segmentation'].shape[0], sorted_anns[0]['segmentation'].shape[1], 4))
	img[:,:,3] = 0
	for ann in sorted_anns:
		m = ann['segmentation']
		color_mask = np.concatenate([np.random.random(3), [0.35]])
		img[m] = color_mask
	ax.imshow(img)


def test():
	files = os.listdir("download")
	for file in files:
		name = file.split(".")[0]
		print(name)




def main():
	print("program starts ...")
	files = os.listdir("download2")
	mask_generator_2 = SamAutomaticMaskGenerator(
		model=sam,
		points_per_side=32,
		pred_iou_thresh=0.86,
		stability_score_thresh=0.92,
		crop_n_layers=1,
		crop_n_points_downscale_factor=2,
		min_mask_region_area=100,  # Requires open-cv to run post-processing
		)

	for file in files:
		name = file.split(".")[0]
		print(name)
		oFile = open("geo_result2/" + name + "_para.csv", "w")
		image = cv2.imread("download2/" + file)
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		# masks = mask_generator.generate(image)
		result = mask_generator_2.generate(image)

		masks = [mask for mask in sorted(result, key=lambda x: x['area'], reverse=True)]
		for mask in masks:
			# print(mask['area'])
			oFile.write(str(mask['area']) + "\n")
		oFile.close()
		# plt.figure(figsize=(20,20))
		# plt.imshow(image)
		# show_anns(result)
		# plt.axis('off')
		# plt.show()


if __name__ == '__main__':
	main()
	# test()