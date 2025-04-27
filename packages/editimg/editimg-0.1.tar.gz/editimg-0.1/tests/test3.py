from editimg.imagekit import Image
import time

image = Image("tests/white.png")

start = time.time()
selection = image.square_select((0, 0), (767, 767))
image.fill(selection, (114, 170, 80, 127))
selection = image.square_select((255, 255), (1023, 1023))
image.fill(selection, (92, 67, 46, 127))
end = time.time()
print(end - start)

image.save_as("tests/test3.png")