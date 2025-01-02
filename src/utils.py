import cv2
import tempfile
import numpy as np
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw

CHAR_LIST = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~i!lI;:,\"^`"

def convert_image_to_ascii(image):
    height, width = image.shape
    num_cols = 0
    if width > 3000:
        num_cols = 200
    elif  width > 2000:
        num_cols = 150
    else:
        num_cols = 100
    cell_width = width / num_cols
    cell_height = cell_width * 2
    num_rows = int(height/cell_height)

    font = ImageFont.truetype("./font/Roboto-Regular.ttf ", size=20)
    char_width= font.getlength("A")
    char_height = char_width * 2
    out_width = char_width * num_cols
    out_height = char_height * num_rows

    out_image  = Image.new("RGB", (int(out_width), int(out_height)), (255,255,255))
    draw = ImageDraw.Draw(out_image)
    for i in range(num_rows):
        for j in range(num_cols):
            sub_image = image[
                            int(i * cell_height ): int((i+1) * cell_height),
                            int(j * cell_width) : int((j+1) * cell_width)
                        ]
            index = int(np.mean(sub_image)/255 * len(CHAR_LIST)) #get brightness
            draw.text((j * char_width, i* char_height), CHAR_LIST[index-1], fill = (0,0,0), font = font)
    return out_image


def convert_image_to_color_ascii(image):
    height, width, _ = image.shape
    num_cols = 0
    if width > 3000:
        num_cols = 200
    elif  width > 2000:
        num_cols = 150
    else:
        num_cols = 100
    cell_width = width / num_cols
    cell_height = cell_width * 2
    num_rows = int(height/cell_height)

    font = ImageFont.truetype("./font/Roboto-Regular.ttf ", size=20)
    char_width= font.getlength("A")
    char_height = char_width * 2
    out_width = char_width * num_cols
    out_height = char_height * num_rows

    # create a black background with width and height
    out_image  = Image.new("RGB", (int(out_width), int(out_height)), (0,0,0))
    draw = ImageDraw.Draw(out_image)
    for i in range(num_rows):
        for j in range(num_cols):
            sub_image = image[
                            int(i * cell_height ): int((i+1) * cell_height),
                            int(j * cell_width) : int((j+1) * cell_width)
                        ]
            avg_color = np.mean(sub_image, axis=(0, 1)) # compute mean for each channel
            # avg_color = np.clip(avg_color, 0, 255) # increase brightness
            avg_color = tuple(map(int, avg_color[::-1])) # convert to int and reverse BGR to RGB

            draw.text((j * char_width, i* char_height), CHAR_LIST[0], fill = avg_color, font = font)
    return out_image

def convert_video_to_ascii(video):
    cap = cv2.VideoCapture(video)

    if not cap.isOpened():
        print("cannot capture video")
        return 1

    ascii_frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("reading video done")
            break

        ascii_frame = convert_image_to_ascii(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
        ascii_frames.append(ascii_frame)

    cap.release()
    cv2.destroyAllWindows()

    gif_buffer = BytesIO()
    ascii_frames[0].save(
        gif_buffer,
        format="GIF",
        save_all=True,
        append_images=ascii_frames[1:],
        duration=100,  # Duration of each frame in milliseconds
        loop=0
    )
    gif_buffer.seek(0)
    return gif_buffer

def convert_video_to_color_ascii(video):
    cap = cv2.VideoCapture(video)

    if not cap.isOpened():
        print("cannot capture video")
        return 1

    ascii_frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("reading video done")
            break

        ascii_frame = convert_image_to_color_ascii(frame)
        ascii_frames.append(ascii_frame)

    cap.release()
    cv2.destroyAllWindows()

    gif_buffer = BytesIO()
    ascii_frames[0].save(
        gif_buffer,
        format="GIF",
        save_all=True,
        append_images=ascii_frames[1:],
        duration=100,  # Duration of each frame in milliseconds
        loop=0
    )
    gif_buffer.seek(0)
    return gif_buffer


