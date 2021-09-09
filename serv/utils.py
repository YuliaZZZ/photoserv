from PIL import Image


def mode_photo_size(path_file, mean_width, mean_height):
    im = Image.open(path_file, mode="r")
    imResize = im.resize((mean_width, mean_height), Image.ANTIALIAS)
    imResize.save(path_file, "JPEG", quality=95)  # настройка качества


def calculate_photo_size(width, height):
    mean_width, mean_height = width, height
    ratio = width / height

    if mean_width <= mean_height:
        mean_height = 150
        mean_width = int(mean_height * ratio)
    else:
        mean_width = 150
        mean_height = int(mean_width * ratio)
    return mean_width, mean_height
