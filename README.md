# RLE-compressor

### What's this?
- - -

This is a simple RLE compressor for binary(Black&White) image. We use LZ77 and RLE algorithm to compress binary png images. It has a good result in regular binary png image.

  
  


### package needed ###

- - -

**opencv for python 2.7**: You can get it from [https://opencv.org/releases.html](https://opencv.org/releases.html)

**numpy**: You can get it by "pip install numpy"

**bitarray for python 2**:  You can get it from [https://pypi.python.org/pypi/bitarray/](https://pypi.python.org/pypi/bitarray/)




### Compression
- - -

`python compress.py [--img] [local_img_path] [--window] [window_size] `

The compressed file will be saved as 'xx.bin'



### Decompression
- - -
`python decompress.py [--compressed] [compressed_file_path] [--window] [window_size]`

The size of the window should be equal to the one in compress.py




