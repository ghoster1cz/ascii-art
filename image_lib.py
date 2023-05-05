from PIL import Image
import numpy as np


def get_area(image, top_left, bottom_right):
    area_y = image[top_left[0]:bottom_right[0]]
    area_x = np.array([x[top_left[1]:bottom_right[1]] for x in area_y])
    return area_x


def image_to_array(image_path):
    return np.array(Image.open(image_path))


def average_area_brightness(area):
    return np.average(area)


def generate_uniart(canvas, image):
    character_width = image.shape[1] / canvas.width
    character_height = image.shape[0] / canvas.height

    progress = (canvas.height * canvas.width) / 10

    output_image = []

    for y in range(canvas.height-1):
        output_image.append([])
        for x in range(canvas.width-1):
            area = get_area(
                image,
                (int(character_height * y), int(character_width * x)),
                (int(character_height * (y + 1)), int(character_width * (x + 1)))
            )
            brightness = average_area_brightness(area)
            character = canvas.get_character_from_brightness(brightness)

            output_image[y].append(character)

            if (y * canvas.width + x) % progress == 0:
                print("Generating text: {0}%".format(((y * canvas.width + x)/progress) * 10))

    print("Done!")
    return np.array(output_image)


def save_image(image, output):
    print("Saving text to", output)
    with open(output, "w+") as f:
        for row in image:
            for char in row:
                f.write(char)
            f.write("\n")

    print("Done!")