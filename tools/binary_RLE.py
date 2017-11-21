# coding=utf-8
import numpy as np
import cv2
# import image_reader
# import naive_LZ77
# import LZ77

class Binary_RLE_Compressor(object):
	""" RLE compressor for binary image"""
	def __init__(self):
		super(Binary_RLE_Compressor, self).__init__()

	def image2string(self,img,dim_1_size,dim_2_size):
		"""
		change a two-dim image into one-dim string
		"""
		ans = []
		ans.append(dim_1_size)
		ans.append(dim_2_size)

		for i in range(dim_1_size):
			for j in range(dim_2_size):
				ans.append(img[i,j])
		return ans

	def compression(self, img):
		for i in range(img.shape[0]):
			for j in range(img.shape[1]):
				if img[i,j] == 255:
					img[i,j] = 0
				else:
					img[i,j] = 1


		compressed_data = [img.shape[0],img.shape[1]]
		data_flow = self.image2string(img,img.shape[0],img.shape[1])
		
		# initialization params
		count = 1
		curr_color = 1
		if data_flow[2] == 0:
			curr_color = 0
		else:
			compressed_data.append(0)

		for i in range(3,len(data_flow)):
			# same color
			if curr_color == data_flow[i]:
				count+=1
			# different color
			else:
				compressed_data.append(count)
				curr_color = data_flow[i]
				count = 1

		return compressed_data

	def decompression(self, compressed_data):
		dim_1_size = compressed_data[0]
		dim_2_size = compressed_data[1]
		curr_index = [0,0]
		curr_color = 0
		origin_image = np.zeros([dim_1_size,dim_2_size],dtype=np.uint8)

		for i in range(2,len(compressed_data)):
			curr_count = compressed_data[i]
			next_index = [
				curr_index[0]+(curr_index[1] + curr_count - 1) / dim_2_size,
				(curr_index[1] + curr_count - 1) % dim_2_size
			]
			
			if curr_color == 1:
				curr_index = next_index
			else:
				while curr_index[0] <= next_index[0]:
					if curr_index[0] < next_index[0]:
						while curr_index[1] < dim_2_size:
							origin_image[curr_index[0],curr_index[1]] = 255
							curr_index[1]+=1
					else:
						while curr_index[1] <= next_index[1]:
							origin_image[curr_index[0],curr_index[1]] = 255
							curr_index[1]+=1
					curr_index[1] = 0
					curr_index[0] += 1

			if next_index[1] + 1 == dim_2_size:
				next_index[1] = 0
				next_index[0] += 1
			else:
				next_index[1] += 1
			curr_index = next_index
			curr_color = 1 - curr_color

		return origin_image

# for test

# VALUE = 125
# IMG_NAME = 'test.PNG'

# if __name__ == '__main__':
# 	test_img = cv2.imread(IMG_NAME,cv2.IMREAD_GRAYSCALE)
# 	cv2.threshold(test_img,VALUE,255,cv2.THRESH_BINARY,test_img)
# 	cv2.imshow('origin_image',test_img)
# 	cv2.waitKey(0)

# 	img_for_compress = np.copy(test_img)
# 	compressor = Binary_RLE_Compressor()
# 	pack = compressor.compression(img_for_compress)
# 	print len(pack) - 2
# 	unpack = compressor.decompression(pack)

# 	cv2.imshow('compressed_img', unpack)
# 	cv2.waitKey(0)

# if __name__ == '__main__':
# 	im_reader = image_reader.image_reader(IMG_NAME)
# 	test_image = im_reader.read_image()

# 	img_for_compress = np.copy(test_image)
# 	RLE_compressor = Binary_RLE_Compressor()
# 	pack = RLE_compressor.compression(img_for_compress)
# 	print len(pack) - 2
# 	LZ77_compressor = LZ77.LZ77(50)
# 	LZ77_pack = LZ77_compressor.compress(pack,verbose=False)
# 	LZ77_unpack = LZ77_compressor.decompress(fromFile=False,data_flow=LZ77_pack)
# 	unpack_image = RLE_compressor.decompression(LZ77_unpack)
# 	cv2.imshow('test',unpack_image)
# 	cv2.waitKey(0)
# 	LZ77_compressor = naive_LZ77.naive_LZ77({
# 	'buffer_size' : 80,	# size of lookahead buffer
# 	'window_size' : 160,	# size of dictionary
# 	'auto' : False		# Whether decide the size of buffer and dictionary automatically
# })
# 	LZ77_pack = LZ77_compressor.compress_string(pack)
# 	print len(LZ77_pack) - 2
# 	print LZ77_pack






