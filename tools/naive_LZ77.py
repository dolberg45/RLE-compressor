# coding=utf-8

import numpy as np
import cv2

algorithm_para = {
	'buffer_size' : 3,	# size of lookahead buffer
	'window_size' : 6,	# size of dictionary
	'auto' : True		# Whether decide the size of buffer and dictionary automatically
}


class naive_LZ77(object):
	"""a naive implementation of LZ77"""
	def __init__(self, arg=algorithm_para):
		super(naive_LZ77, self).__init__()
		self.arg = arg

	def image2string(self,img,dim_1_size,dim_2_size):
		"""
		change a two-dim image into one-dim string
		"""
		ans = []

		for i in range(dim_1_size):
			for j in range(dim_2_size):
				if img[i,j] == 255:
					ans.append('0')
				else:
					ans.append('1')
		return ans


	def longest_match(self, data, cursor):
		""" 
			find the longest match in dictionary 
			and lookahead-buffer 
		"""
		# The tail index of the buffer
		end_buffer = min(cursor + self.arg['buffer_size'], len(data)-1)

		p = -1
		l = -1
		c = ''

		for j in range(cursor+1, end_buffer+1):
			# start index of dictionary
			start_index = max(0, cursor - self.arg['window_size'] + 1)
			# substring is cursor+1 to j, and j range from cursor+1 to end_buffer
			# which means for all fore-substring in buffer
			substring = data[cursor + 1:j + 1]

			for i in range(start_index, cursor+1):
				repetition = len(substring) / (cursor + 1 - i)
				last = len(substring) % (cursor + 1 - i)
				matchedstring = data[i:cursor+1] * repetition + data[i:i+last-1]

				if matchedstring == substring and len(substring) > 1:
					# print cursor,substring,data[i:cursor+1],repetition,last, data[i:i+last]
					p = cursor + 1 - i
					l = len(substring)
					try:
						c = data[j+1]
					except: # if arrive at the end of string
						c = ''

		# unmatched strinf between the two
		if p == -1 and l == -1:
			# print data[cursor+1]
			return 0, 0, data[cursor+1]
		return p, l, c

	def compress_img(self, img):
		"""
		compress img
		:return: tuples (p,l,c)
		"""
		data_flow = self.image2string(img,img.shape[0],img.shape[1])
		i = -1
		out = [img.shape[0],img.shape[1]]

		if self.arg['auto']:
			self.arg['buffer_size'] = out[1] / 8
			self.arg['window_size'] = out[1] / 6

		# the cursor move until it reaches the end of the flow
		while i < len(data_flow)-1:
			[p,l,c] = self.longest_match(data_flow, i)
			out.append([p,l,c])
			i += (l+1)
		return out

	def decompress_img(self, compressed_data):
		"""
		decompress the compressed date
		:param compressed: [p,l,c]
		:return: decompressed data
		"""

		cursor = -1
		out = ''

		dim_1_size = compressed_data[0]
		dim_2_size = compressed_data[1]

		for [p,l,c] in compressed_data[2:]:
			# the initialization
			if p == 0 and l == 0:
				out+=c
			# if overlaped, the repetition of dictionary 
			elif p<l:
				repetition = l/p
				last = l%p
				out += (out[cursor-p+1:cursor+1] * repetition + out[cursor+1-p:last] + c)
			elif p>=l:
				out+= (out[cursor+1-p:cursor+1] + c)
			cursor += (l+1)
			#print out
		
		output_img = np.zeros([dim_1_size,dim_2_size],dtype=np.uint8) + 255
		count = 0
		for i in range(dim_1_size):
			for j in range(dim_2_size):
				# if out[count]=='1': print out[count],
				# else: print ' ',
				if out[count] == '1':
					output_img[i,j] = 0
				count += 1
			# print '\n'

		return output_img

	def compress_string(self, data_flow):
		"""
		compress data_flow
		:return: tuples (p,l,c)
		"""
		i = -1
		out = []

		if self.arg['auto']:
			self.arg['buffer_size'] = len(data_flow) / 8
			self.arg['window_size'] = len(data_flow) / 6

		# the cursor move until it reaches the end of the flow
		while i < len(data_flow)-1:
			[p,l,c] = self.longest_match(data_flow, i)
			out.append([p,l,c])
			i += (l+1)
		return out

	def decompress_string(self, compressed):
		"""
		decompress the compressed date
		:param compressed: [p,l,c]
		:return: decompressed data
		"""

		cursor = -1
		out = ''

		for [p,l,c] in compressed:
			# the initialization
			if p == 0 and l == 0:
				out+=c
			# if overlaped, the repetition of dictionary 
			elif p<l:
				repetition = l/p
				last = l%p
				out += (out[cursor-p+1:cursor+1] * repetition + out[cursor+1-p:last] + c)
			elif p>=l:
				out+= (out[cursor+1-p:cursor+1] + c)
			cursor += (l+1)

		return list(out)