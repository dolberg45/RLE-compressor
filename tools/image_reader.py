# coding=utf-8
import numpy as np
import cv2

class image_reader(object):
	"""Reader of the image"""
	def __init__(self, filename, threshold=127, mode=0):
		super(image_reader, self).__init__()
		self.img_name = filename
		self.threshold = threshold
		self.mode = mode

	def read_image(self):
		#if self.mode == 0:
		image = cv2.imread(self.img_name,cv2.IMREAD_GRAYSCALE)
		cv2.threshold(image,self.threshold,255,cv2.THRESH_BINARY,image)
		return image

# for test
# if __name__ == '__main__':
# 	img_reader = image_reader('test.PNG')
# 	image = img_reader.read_image()
# 	cv2.imshow('test',image)
# 	cv2.waitKey(0)