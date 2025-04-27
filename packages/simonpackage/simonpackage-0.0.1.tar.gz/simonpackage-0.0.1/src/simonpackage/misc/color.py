import random

def generateRandomHexColor():
    """
    generate string of random hex color, i.e. #00ff00
    :return:
    """
    cc = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    hex_color_str = '#' + ''.join(random.choices(cc, k=6))
    return hex_color_str

def generateRandomTupleColor(normal=False):
    """
    generate tuple of rgb color tuple, (r,g,b)
    :param normal: if true, float [0,1] ,else [0,255]
    :return:
    """
    if normal:
        return (random.random(), random.random(), random.random())
    return (random.randint(0,255), random.randint(0,255), random.randint(0,255))

def hex2rgbColor(hex_color_string, normal=False):
    r,g,b = hex_color_string[1:3],hex_color_string[3:5],hex_color_string[5:]
    if normal:
        return (int(r,16)/256, int(g,16)/256, int(b,16)/256)
    return (int(r,16), int(g,16), int(b,16))


def rgb2hexColor(rgb):
    r,g,b = rgb
    if type(r)==float or type(g)==float or type(b)==float:
        r,g,b = int(r*256), int(g*256),int(b*256)
    hex_color_str = '#' + ('00' + hex(r).strip('0x'))[-2:] + ('00' + hex(g).strip('0x'))[-2:]\
    + ('00' + hex(b).strip('0x'))[-2:]
    return hex_color_str


if __name__ == '__main__':
    # print(generateRandomTupleColor(normal=True))
    print(rgb2hexColor((0,0,0.8)))