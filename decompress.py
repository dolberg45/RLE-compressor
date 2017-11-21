#coding=utf-8
from tools import *
import cv2
import numpy as np
import argparse


def main():
	compressed = ''
	arg_parser = argparse.ArgumentParser()
	arg_parser.add_argument("--compressed",help="The path of compressed file")
	arg_parser.add_argument("--window",help="size of compress window")
	#arg_parser.add_argument("--output_path",help="path of output compressed file")
	args = arg_parser.parse_args()
	if args.compressed:
		compressed = args.compressed
	else:
		print "no compressed file input"
		
	if args.window:
		window_size = args.window
	else:
		window_size = 50

	RLE_decompressor = binary_RLE.Binary_RLE_Compressor()
	LZ77_decompressor = LZ77.LZ77(window_size)
	LZ77_unpack = LZ77_decompressor.decompress(fromFile=True,input_file_path=compressed)
	RLE_unpack = RLE_decompressor.decompression(LZ77_unpack)
	cv2.imshow('result', RLE_unpack)
	cv2.waitKey(0)
	save_img_path = compressed[:compressed.find('.')] + '.png'
	cv2.imwrite(save_img_path, RLE_unpack)

if __name__ == '__main__':
	main()
