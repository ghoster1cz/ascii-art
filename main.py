import json
import sys

import canvas_lib
import image_lib


def check_args():
    if len(sys.argv) < 2:
        raise ValueError("Too few arguments! Need image path")

    kwargs = {}
    for arg in sys.argv[2:]:
        kwargs[arg.split("=")[0]] = arg.split("=")[1]

    output_resolution = []
    character_set = {}
    verbose = False
    output_path = kwargs.get("out")

    if kwargs.get("verbose") == "True":
        verbose = True

    input_path = sys.argv[1]
    if verbose: print("Taking image from", input_path)

    if kwargs.get("chars") is None:
        if verbose: print("Setting default character set")
        character_set = {
            0: " ",
            10: ".",
            20: "-",
            30: ",",
            40: ":",
            50: ";",
            60: "!",
            70: "|",
            80: "/",
            90: "=",
            100: "+",
            110: "*",
            120: "o",
            130: "O",
            140: "0",
            150: "Q",
            160: "%",
            170: "&",
            180: "#",
            190: "@"
        }
    else:
        if verbose: print("Loading character set from", kwargs.get("chars"))
        with open(kwargs.get("chars"), "r") as f:
            json_set = json.loads(f.read())
        for k, v in json_set.items():
            if not k.isdigit:
                raise ValueError("Bad format of character set file! (should be in format \"00\": \"@\")")

            k = int(k)

            if not 0 <= k <= 255:
                raise ValueError("Bad key in character set file! Keys must be numbers from 0 to 255 (included)!")

            if len(v) != 1:
                raise ValueError("Bad value in character set file! value of key must be only 1 character!")

            character_set[k] = v

    if kwargs.get("res") is None:
        if verbose: print("Setting output resolution to image resolution")
        output_resolution = [-1, -1]
    else:
        resolution = kwargs.get("res")
        resolution_list = resolution.split("x")
        if len(resolution_list) != 2:
            raise ValueError("Bad arguments for flag res! (should be in format 0000x0000)")

        if not resolution_list[0].isdigit() or not resolution_list[1].isdigit():
            raise ValueError("Bad arguments for flag res! (should be in format 0000x0000)")

        resolution_list = [int(x) for x in resolution_list]

        if (resolution_list[0] < 3 or resolution_list[1] < 3) and (
                resolution_list[0] != -1 or resolution_list[1] != -1):
            raise ValueError("Bad arguments for flag res! Resolution must be minimally 3x3")

        if verbose: print("Setting output resolution to {0}x{1}".format(*resolution_list))

        output_resolution = resolution_list

    return input_path, output_path, character_set, output_resolution


def init():
    input_path, output_path, character_set, output_resolution = check_args()
    image = image_lib.image_to_array(input_path)

    if image.shape[1] < output_resolution[0] or image.shape[0] < output_resolution[1]:
        raise ValueError("Bad arguments for flag res! Output resolution cant be bigger than image resolution!")

    if output_resolution[0] == -1:
        output_resolution[0] = image.shape[1]
        output_resolution[1] = image.shape[0]

    canvas = canvas_lib.Canvas(*output_resolution, character_set)

    output = image_lib.generate_uniart(canvas, image)

    if output_path:
        image_lib.save_image(output, output_path)
    else:
        for row in output:
            for char in row:
                print(char, end="")
            print()


if __name__ == "__main__":
    init()
