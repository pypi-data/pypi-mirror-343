from editimg.pngtools import decode, encode, save_file
from sugar import clear

""" file_path = "bit2x2-1bpp.png"
file_path = "bit9x9-1bpp.png"
file_path = "idx2x2-8bpp.png"
file_path = "idx9x9-8bpp.png"
file_path = "rgb2x2-8bpp.png"
file_path = "rgb2x2-16bpp.png"
file_path = "rgb2x2-32bpp.png"
file_path = "rgba32x32-2layers.png"
file_path = "test_images/png/" + file_path """

file_path = "tests/testimage.png"

clear()
image_data, chunks = decode(file_path, return_chunks=True)
file_content = encode(image_data, chunks=chunks)
save_file("tests/test.png", file_content)