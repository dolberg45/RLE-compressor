#coding=utf-8
from tools import *
import argparse

def main():
	img_name = ''
	arg_parser = argparse.ArgumentParser()
	arg_parser.add_argument("--img",help="The path of image to compress")
	arg_parser.add_argument("--window",help="size of compress window")
	#arg_parser.add_argument("--output_path",help="path of output compressed file")
	args = arg_parser.parse_args()
	if args.img:
		img_name = args.img
	else:
		print "no image input"
		
	if args.window:
		window_size = args.window
	else:
		window_size = 50

	try:
		imReader = image_reader.image_reader(img_name)
		to_compress_img = imReader.read_image()
	except IOError:
		print "could not open this image, please check..."
		raise

	RLE_compressor = binary_RLE.Binary_RLE_Compressor()
	LZ77_compressor = LZ77.LZ77(window_size)
	name_of_output = img_name[:img_name.find('.')] + '.bin'
	RLE_pack = RLE_compressor.compression(to_compress_img)
	LZ77_pack = LZ77_compressor.compress(RLE_pack,name_of_output)



if __name__ == '__main__':
	main()