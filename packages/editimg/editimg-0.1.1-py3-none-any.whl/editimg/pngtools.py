# editimg
# Copyright (c) 2025 Gustavo de Melo Timbó
# Licensed under the MIT License

import struct
import zlib

def decode(file_path, return_chunks = False, image_data_type = "list"):
    # Get the file content
    try:
        with open(file_path, "rb") as file:
            file_content = file.read()
    except:
        raise FileNotFoundError(f"{file_path} does not exist.")

    # Get the file type
    if file_content[:8] == b'\211PNG\r\n\032\n':
        file_type = "png"
    else:
        raise ValueError("Expected PNG file.")

    if file_type == "png":
        # Read chunks
        tRNS = None
        cHRM = None
        chunks = []
        compressed_data = b''
        i = 8
        while True:
            chunk_length = int.from_bytes(file_content[i:i+4], byteorder='big')
            i += 4
            chunk_type = file_content[i:i+4]
            i += 4
            _check_corrupted_chunk(i + chunk_length + 4, len(file_content))
            chunk_data = file_content[i:i+chunk_length]
            i += chunk_length
            chunk_crc = file_content[i:i+4]
            i += 4

            # Check chunk's CRC
            if int.from_bytes(chunk_crc, byteorder='big') != zlib.crc32(chunk_type + chunk_data) & 0xffffffff:
                raise ValueError("CRC mismatch: possible corruption.")

            # [0]=length, [1]=type, [2]=data, [3]=crc
            chunk = [chunk_length, chunk_type, chunk_data, chunk_crc]

            if chunk_type == b'IHDR':
                width = int.from_bytes(chunk_data[0:4], byteorder='big')
                height = int.from_bytes(chunk_data[4:8], byteorder='big')
                bit_depth = chunk_data[8]
                color_type = chunk_data[9]
                compression_method = chunk_data[10]
                filter_method = chunk_data[11]
                interlace_method = chunk_data[12]
                if compression_method != 0:
                    raise ValueError("This PNG file uses an invalid compression method.")
                if filter_method != 0:
                    raise ValueError("This PNG file uses an invalid filter method.")
                if not color_type in [0, 2, 3, 4, 6]:
                    raise ValueError("This PNG file uses an invalid color type.")
                if not bit_depth in [1, 2, 4, 8, 16]:
                    raise ValueError("This PNG file uses an invalid bit depth.")
                if color_type == 2 and not bit_depth in [8, 16]:
                    raise ValueError("This PNG file uses an invalid bit depth.")
                if color_type == 3 and not bit_depth in [1, 2, 4, 8]:
                    raise ValueError("This PNG file uses an invalid bit depth.")
                if color_type == 4 and not bit_depth in [8, 16]:
                    raise ValueError("This PNG file uses an invalid bit depth.")
                if color_type == 6 and not bit_depth in [8, 16]:
                    raise ValueError("This PNG file uses an invalid bit depth.")
                if interlace_method not in [0, 1]:
                    raise ValueError("This PNG file uses an invalid interlace method.")

            elif chunk_type == b'IDAT':
                compressed_data += chunk_data

            elif chunk_type == b'PLTE':
                palette = list(chunk_data)

            elif chunk_type == b'tRNS': # Not checked if it works
                tRNS = list(chunk_data)

            elif chunk_type == b'cHRM': # Not checked if it works
                if len(chunk_data) != 32:
                    raise ValueError("This PNG file has an invalid cHRM chunk.")

                chromaticities = [] # ["white_x", "white_y", "red_x", "red_y", "green_x", "green_y", "blue_x", "blue_y"]

                for index in range(8):
                    chromaticities.append(int.from_bytes(chunk_data[index * 4:(index + 1) * 4], byteorder='big') / 100000)

            elif chunk_type == b'IEND':
                break

            else:
                chunks.append(chunk)

        if color_type == 0: # color_type = "grayscale"
            num_channels = 1
        elif color_type == 2: # color_type = "RGB"
            num_channels = 3
        elif color_type == 3: # color_type = "palette"
            num_channels = 1
        elif color_type == 4: # color_type = "grayscale + alpha"
            num_channels = 2
        elif color_type == 6: # color_type = "RGBA"
            num_channels = 4

        decompressed_data = zlib.decompress(compressed_data)
        bpp = bit_depth * num_channels / 8
        # No interlace
        if interlace_method == 0:
            # Filtering
            bpf = 1 if int(bpp) == 0 else int(bpp) # bytes per filter
            previous_row = None
            unfiltered_image_data = []
            for row_index in range(height):
                row_length = 1 + int(width * bpp)
                row_length = 2 if row_length == 1 else row_length
                filter_byte = decompressed_data[row_index * row_length]
                row = list(decompressed_data[row_index * row_length + 1:(row_index + 1) * row_length])
                row = _remove_filter(filter_byte, bpf, row, previous_row)
                # Correct for different bit depths
                if bit_depth < 8:
                    new_row = []
                    index = 0
                    while index != len(row):
                        byte = format(row[index], '08b')
                        for j in range(int(8 / bit_depth)):
                            new_row.append(int(byte[bit_depth * j:bit_depth * (j + 1)], 2))
                        index += 1
                    row = new_row
                elif bit_depth == 16:
                    index = 0
                    while index != len(row):
                        row[index] *= row[index + num_channels]
                        row.pop(index + num_channels)
                        index += 1
                unfiltered_image_data.append(row)
                previous_row = row
        else:
            raise NotImplementedError("Adam7 algorithm not implemented yet.")

        # Separate into channels
        image_data = []
        for channel in range(num_channels):
            image_data.append([])
            for row_index in range(height):
                row = []
                for index in range(channel, width * num_channels, num_channels):
                    row.append(unfiltered_image_data[row_index][index])
                image_data[channel].append(row)

        # Transform data into RGBA
        if color_type == 0:
            red = image_data[0]
            green = image_data[0]
            blue = image_data[0]
            alpha = []
            grayscale_transparent = None
            if tRNS != None:
                grayscale_transparent = (tRNS[0] << 8) + tRNS[1]
            for row in range(height):
                alpha.append([])
                for column in range(width):
                    pixel_val = red[row][column]
                    if grayscale_transparent != None and pixel_val == grayscale_transparent:
                        alpha[row].append(0)
                    else:
                        alpha[row].append(255)
        elif color_type == 2:
            red = image_data[0]
            green = image_data[1]
            blue = image_data[2]
            alpha = []
            r_tRNS = g_tRNS = b_tRNS = None
            if tRNS != None and len(tRNS) >= 6:
                r_tRNS = (tRNS[0] << 8) + tRNS[1]
                g_tRNS = (tRNS[2] << 8) + tRNS[3]
                b_tRNS = (tRNS[4] << 8) + tRNS[5]
            for row in range(height):
                alpha.append([])
                for column in range(width):
                    r = red[row][column]
                    g = green[row][column]
                    b = blue[row][column]
                    if r_tRNS != None and r == r_tRNS and g == g_tRNS and b == b_tRNS:
                        alpha[row].append(0)
                    else:
                        alpha[row].append(255)
        elif color_type == 3:
            red = []
            green = []
            blue = []
            alpha = []
            for row in range(height):
                red.append([])
                green.append([])
                blue.append([])
                alpha.append([])
                for column in range(width):
                    index = image_data[0][row][column]
                    red[row].append(palette[index * 3])
                    green[row].append(palette[index * 3 + 1])
                    blue[row].append(palette[index * 3 + 2])
                    if tRNS != None and index < len(tRNS):
                        alpha[row].append(tRNS[index])
                    else:
                        alpha[row].append(255)
        elif color_type == 4:
            red = image_data[0]
            green = image_data[0]
            blue = image_data[0]
            alpha = image_data[1]
        elif color_type == 6:
            red = image_data[0]
            green = image_data[1]
            blue = image_data[2]
            alpha = image_data[3]
            if tRNS != None and len(tRNS) >= 3:
                tRNS_r = tRNS[0]
                tRNS_g = tRNS[1]
                tRNS_b = tRNS[2]
                for row in range(height):
                    for column in range(width):
                        if (red[row][column] == tRNS_r and
                            green[row][column] == tRNS_g and
                            blue[row][column] == tRNS_b and
                            alpha[row][column] == 255):
                            alpha[row][column] = 0
        if image_data_type == "list":
            image_data = [red, green, blue, alpha]
        elif image_data_type == "dict":
            image_data = {"red": red, "green": green, "blue": blue, "alpha": alpha}
        
        """ if color_type == 0:
            color_type = "grayscale"
        elif color_type == 2:
            color_type = "RGB"
        elif color_type == 3:
            color_type = "palette"
        elif color_type == 4:
            color_type = "grayscale + alpha"
        elif color_type == 6:
            color_type = "RGBA"
        print("color type: " + color_type) """

        if return_chunks:
            return image_data, chunks
        else:
            return image_data

def encode(image_data, chunks = None, bit_depth = None, color_type = None):
    file_content = b'\211PNG\r\n\032\n'

    if type(image_data) == list:
        red = 0
        green = 1
        blue = 2
        alpha = 3
    elif type(image_data) == dict:
        red = "red"
        green = "green"
        blue = "blue"
        alpha = "alpha"

    # Create IHDR chunk
    width = len(image_data[red][0])
    height = len(image_data[red])
    bit_depth = 8
    color_type = 6
    compression = 0
    filter_method = 0
    interlace = 0

    chunk_length = struct.pack(">I", 13)
    chunk_type = b'IHDR'
    chunk_data = struct.pack(">IIBBBBB", width, height, bit_depth, color_type, compression, filter_method, interlace) # chunk data
    chunk_crc = _get_chunk_crc(chunk_type, chunk_data)

    file_content += chunk_length + chunk_type + chunk_data + chunk_crc

    # Create other chunks
    if chunks != None:
        for chunk in chunks:
            chunk_type = chunk[1]
            chunk_data = chunk[2]
            chunk_length = struct.pack(">I", len(chunk_data))
            chunk_crc = chunk[3]

            if int.from_bytes(chunk_crc, byteorder='big') != zlib.crc32(chunk_type + chunk_data) & 0xffffffff:
                raise ValueError("CRC mismatch: possible corruption.")

            file_content += chunk_length + chunk_type + chunk_data + chunk_crc

    # Create IDAT chunks
    # Currently only creating one IDAT chunk, may implement more in the future
    scanlines = bytearray()
    for row in range(height):
        filter_byte = _choose_filter()
        scanlines.append(filter_byte)
        for column in range(width):
            scanlines.append(image_data[red][row][column])
            scanlines.append(image_data[green][row][column])
            scanlines.append(image_data[blue][row][column])
            scanlines.append(image_data[alpha][row][column])

    chunk_type = b'IDAT'
    chunk_data = zlib.compress(bytes(scanlines))
    chunk_length = struct.pack(">I", len(chunk_data))
    chunk_crc = _get_chunk_crc(chunk_type, chunk_data)

    file_content += chunk_length + chunk_type + chunk_data + chunk_crc

    # Create IEND chunk
    chunk_length = struct.pack(">I", 0)
    chunk_type = b'IEND'
    chunk_data = b''
    chunk_crc = _get_chunk_crc(chunk_type, chunk_data)

    file_content += chunk_length + chunk_type + chunk_data + chunk_crc

    return file_content

def save_file(file_path: str, file_content):
    with open(file_path, "wb") as file:
        file.write(file_content)

def _choose_filter():
    return 0 # Temporary solution

def _get_chunk_crc(chunk_type, chunk_data):
    return struct.pack(">I", zlib.crc32(chunk_type + chunk_data) & 0xffffffff)

def _remove_filter(filter_byte, bpf, row: list, previous_row):
    if filter_byte == 0:
        return row
    if filter_byte == 1:
        for index in range(len(row)):
            if index >= bpf:
                row[index] = (row[index] + row[index - bpf]) % 256
    elif filter_byte == 2:
        for index in range(len(row)):
            if previous_row != None:
                row[index] = (row[index] + previous_row[index]) % 256
    elif filter_byte == 3:
        for index in range(len(row)):
            if index >= bpf and previous_row != None:
                row[index] = (row[index] + (row[index - bpf] + previous_row[index]) // 2) % 256
    elif filter_byte == 4:
        for index in range(len(row)):
            row[index] = (row[index] + _paeth_predictor(row, index, bpf, previous_row)) % 256
    return row

def _paeth_predictor(row, index, bpf, previous_row):
    a = row[index - bpf] if index >= bpf else 0
    b = previous_row[index] if previous_row != None else 0
    c = previous_row[index - bpf] if index >= bpf and previous_row != None else 0

    p = a + b - c
    pa = abs(p - a)
    pb = abs(p - b)
    pc = abs(p - c)

    if pa <= pb and pa <= pc:
        return a
    elif pb <= pc:
        return b
    else:
        return c

def _check_corrupted_chunk(chunk_end, content_length):
    if chunk_end > content_length:
        raise ValueError("Corrupted PNG: chunk extends beyond file end.")