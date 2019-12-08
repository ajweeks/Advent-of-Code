
def get_input_str():
    return open("day08.in").readlines()[0]


def get_inputs(input_str):
    return [int(y) for y in input_str]


def part1():
    inputs = get_inputs(get_input_str())
    # inputs = get_inputs("123456789012")
    min_count_0 = 99999
    min_count_0_layer = -1
    w = 25
    h = 6
    layer_count = int(len(inputs) / (w * h))
    for layer_idx in range(layer_count):
        count_0 = 0
        for y in range(h):
            for x in range(w):
                if inputs[layer_idx * (w * h) + y * w + x] == 0:
                    count_0 += 1
        if count_0 < min_count_0:
            min_count_0 = count_0
            min_count_0_layer = layer_idx

    one_count = 0
    two_count = 0
    for y in range(h):
        for x in range(w):
            if inputs[min_count_0_layer * (w * h) + y * w + x] == 1:
                one_count += 1
            if inputs[min_count_0_layer * (w * h) + y * w + x] == 2:
                two_count += 1

    return one_count * two_count


#    ##  ####  ##  #  #  ##
#   #  # #    #  # #  # #  #
#   #    ###  #    #  # #
#   #    #    #    #  # # ##
#   #  # #    #  # #  # #  #
#    ##  #     ##   ##   ###

def print_image(pixels, w, h):
    for y in range(h):
        for x in range(w):
            print("#" if pixels[y * w + x] else ' ', end='')
        print()


def part2():
    # 0 = black, 1 = white, 2 = transparent #
    inputs = get_inputs(get_input_str())
    w = 25
    h = 6
    layer_count = int(len(inputs) / (w * h))
    pixel_data = [-1] * (w * h)
    for layer_idx in range(layer_count):
        for y in range(h):
            for x in range(w):
                pixel = inputs[layer_idx * (w * h) + y * w + x]
                if pixel != 2 and pixel_data[y * w + x] == -1:
                    pixel_data[y * w + x] = pixel

    # print_image(pixel_data, w, h)
    return "CFCUG"
