# editimg
# Copyright (c) 2025 Gustavo de Melo Timbó
# Licensed under the MIT License

from .pngtools import encode, decode, save_file

class Image():
    def __init__(self, file_path = None):
        if file_path != None:
            self.file_path = file_path
            self.image_data, self.chunks = decode(file_path, return_chunks=True)

            if type(self.image_data) == list:
                self.red = 0
                self.green = 1
                self.blue = 2
                self.alpha = 3
            elif type(self.image_data) == dict:
                self.red = "red"
                self.green = "green"
                self.blue = "blue"
                self.alpha = "alpha"

            self.width = len(self.image_data[self.red][0])
            self.height = len(self.image_data[self.red])

    def create_new_image(self, width, height, image_data_type = "list"):
        if image_data_type == "list":
            self.image_data = [[], [], [], []]
            self.red = 0
            self.green = 1
            self.blue = 2
            self.alpha = 3
        elif image_data_type == "dict":
            self.image_data = {"red": [], "green": [], "blue": [], "alpha": []}
            self.red = "red"
            self.green = "green"
            self.blue = "blue"
            self.alpha = "alpha"

        for row in range(height):
            self.image_data[self.red].append([])
            self.image_data[self.green].append([])
            self.image_data[self.blue].append([])
            self.image_data[self.alpha].append([])
            for column in range(width):
                self.image_data[self.red][row].append(0)
                self.image_data[self.green][row].append(0)
                self.image_data[self.blue][row].append(0)
                self.image_data[self.alpha][row].append(255)

    def square_select(self, start: tuple, finish: tuple):
        selection = set()
        for x in range(start[0], finish[0] + 1):
            for y in range(start[1], finish[1] + 1):
                selection.add((x, y))
        return selection

    def fill(self, selection, color_fg: tuple):
        input_memory = []
        output_memory = []
        for pixel in selection:
            row = pixel[1]
            column = pixel[0]

            color_bg = (self.image_data[self.red][row][column],
                           self.image_data[self.green][row][column],
                           self.image_data[self.blue][row][column],
                           self.image_data[self.alpha][row][column])
            input_colors = [color_bg, color_fg]
            if input_colors in input_memory:
                color_result = output_memory[input_memory.index(input_colors)]
            else:
                color_result = blend_rgba(color_bg, color_fg)
                input_memory.append(input_colors)
                output_memory.append(color_result)

            self.image_data[self.red][row][column] = color_result[0]
            self.image_data[self.green][row][column] = color_result[1]
            self.image_data[self.blue][row][column] = color_result[2]
            self.image_data[self.alpha][row][column] = color_result[3]

    def save(self):
        file_content = encode(self.image_data, self.chunks)
        save_file(self.file_path, file_content)

    def save_as(self, file_path):
        file_content = encode(self.image_data, self.chunks)
        save_file(file_path, file_content)

def blend_rgba(color_bg: tuple[int,int,int,int], color_fg: tuple[int,int,int,int]) -> tuple[int,int,int,int]:
    if color_fg[3] == 255:
        return color_fg

    alpha_bg = color_bg[3] / 255
    red_bg = color_bg[0] * alpha_bg
    green_bg = color_bg[1] * alpha_bg
    blue_bg = color_bg[2] * alpha_bg

    alpha_fg = color_fg[3] / 255
    red_fg = color_fg[0] * alpha_fg
    green_fg = color_fg[1] * alpha_fg
    blue_fg = color_fg[2] * alpha_fg

    alpha_result = alpha_fg + alpha_bg * (1 - alpha_fg)
    red_result = red_fg + red_bg * (1 - alpha_fg)
    green_result = green_fg + green_bg * (1 - alpha_fg)
    blue_result = blue_fg + blue_bg * (1 - alpha_fg)

    if alpha_result != 0:
        red_result = int(round(red_result / alpha_result))
        green_result = int(round(green_result / alpha_result))
        blue_result = int(round(blue_result / alpha_result))
    else:
        red_result = green_result = blue_result = 0

    alpha_result = int(round(alpha_result * 255))

    return (red_result, green_result, blue_result, alpha_result)