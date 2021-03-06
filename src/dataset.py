import numpy as np
import os

from PIL import Image

from torch.utils.data import Dataset

EXTENSIONS = ['.jpg', '.png']

def load_image(file):
	return Image.open(file)

def is_image(filename):
	return any(filename.endswith(ext) for ext in EXTENSIONS)

def image_path(root, basename, extension):
	return os.path.join(root, '{basename}{extension}')

def image_basename(filename):
	return os.path.basename(os.path.splitext(filename)[0])

class VOC12(Dataset):

	def __init__(self, root, input_transform=None, target_transform=None):
		self.images_root = os.path.join(root, 'JPEGImages')
		self.labels_root = os.path.join(root, 'twentyClassData')

		self.filenames = [image_basename(f)
			for f in os.listdir(self.labels_root) if is_image(f)]
		self.filenames.sort()
		self.filenames=self.filenames[0:2600]

		self.input_transform = input_transform
		self.target_transform = target_transform

	def __getitem__(self, index):
		filename = self.filenames[index]

		with open(self.images_root+"/"+str(filename)+'.jpg', 'rb') as f:
			
			image = load_image(f).convert('RGB')
		with open(self.labels_root+"/"+str(filename)+'.png', 'rb') as f:
			
			label = load_image(f).convert('P')

		if self.input_transform is not None:
			image = self.input_transform(image)
		if self.target_transform is not None:
			label = self.target_transform(label)

		return image, label

	def __len__(self):
		return len(self.filenames)