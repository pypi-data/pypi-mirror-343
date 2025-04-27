from editimg.pngtools import decode, encode, save_file

image_data = [[], [], [], []]

for i1 in range(4096):
    image_data[0].append([])
    image_data[1].append([])
    image_data[2].append([])
    image_data[3].append([])
    for i2 in range(4096):
        image_data[0][i1].append(0)
        image_data[1][i1].append(0)
        image_data[2][i1].append(0)
        image_data[3][i1].append(255)

i1 = 0
i2 = 0
for red in range(256):
    for green in range(256):
        for blue in range(256):
            image_data[0][i1][i2] = red
            image_data[1][i1][i2] = green
            image_data[2][i1][i2] = blue
            i2 += 1
            if i2 == 4096:
                i2 = 0
                i1 += 1

image_data = encode(image_data)
save_file("tests/test2.png", image_data)