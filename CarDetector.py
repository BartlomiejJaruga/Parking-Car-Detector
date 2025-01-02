import numpy as np
import matplotlib.pyplot as plt
from skimage import io, color, filters, feature, morphology, measure
from skimage.morphology import erosion, reconstruction, disk, square, dilation
from skimage.transform import rescale, resize
import cv2
import time
import pandas as pd
from PIL import Image, ImageDraw, ImageFont


def convert_hsv_to_opencv(h, s, v):
    # h (Hue) w stopniach [0-360] -> [0-179]
    h_opencv = h / 2
    # s, v (Saturation, Value) w % [0-100] -> [0-255]
    s_opencv = s * 2.55
    v_opencv = v * 2.55
    return np.array([round(h_opencv), round(s_opencv), round(v_opencv)])


def convert_opencv_to_hsv(h, s, v):
    # h (Hue) w [0-179] -> stopnie [0-360]
    h_internet = h * 2
    # s, v (Saturation, Value) w [0-255] -> %
    s_internet = s / 2.55
    v_internet = v / 2.55
    return np.array([round(h_internet), round(s_internet), round(v_internet)])


def drawAllLicencePlateNumbers(image: np.array, cars_licence_plates: list | tuple, cars_rectangles_positions: list[list] | tuple[tuple]):
    img = Image.fromarray(image)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except IOError:
        font = ImageFont.load_default()

    for idx, licence_plate in enumerate(cars_licence_plates):
        if idx > len(cars_rectangles_positions):
            break
        x, y = cars_rectangles_positions[idx]
        text_bbox = draw.textbbox((x, y), licence_plate, font=font)
        draw.rectangle(text_bbox, fill="blue")
        draw.text((x, y), licence_plate, fill="white", font=font)

    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


def findCars(frame, show_steps=False, show_end_product=False):
    image = frame.copy()
    resized_image = cv2.resize(image, (600, 600))

    hsv_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)

    if show_steps:
        _, axes = plt.subplots(1, 2, figsize=(12, 6))
        axes[0].imshow(resized_image, cmap="gray")
        axes[0].set_title("Resized image")
        axes[1].imshow(hsv_image, cmap="gray")
        axes[1].set_title("hsv from BGR")
        plt.show()

    # ======================= MASKOWANIE AUTEK I WYSWIETLANIE TYLKO ICH NA OBRAZIE =============================

    # sampled_hsv_values = hsv_image[310:320, 590:600].reshape(-1, 3)
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #     print(pd.DataFrame(sampled_hsv_values, columns=["H", "S", "V"]))

    # thresholdy dla linii
    # lower_threshold = np.array([20, 10, 200])
    # upper_threshold = np.array([26, 50, 255])

    # thresholdy dla autek (minimalne wartości: [..., 74-75, 74-75])
    lower_threshold = np.array([0, 74, 74])  # węższe prostokąty dla +-85
    upper_threshold = np.array([179, 255, 255])

    # print(str(lower_threshold) + " " + str(upper_threshold))
    # print(str(convert_opencv_to_hsv(0, 85, 85)) + " " + str(convert_opencv_to_hsv(179, 255, 255)))

    mask = cv2.inRange(hsv_image, lower_threshold, upper_threshold)
    mask = dilation(mask, disk(4))  # większe wartości (powyżej 10 może łączyć auta) dają większe prostokąty

    # counter = np.count_nonzero(mask)
    # print(counter)

    result = cv2.bitwise_and(resized_image, resized_image, mask=mask)

    if show_steps:
        _, axes = plt.subplots(1, 3, figsize=(12, 6))
        axes[0].imshow(resized_image)
        axes[0].set_title("Resized image")
        axes[1].imshow(mask, cmap="gray")
        axes[1].set_title("result")
        axes[2].imshow(result)
        axes[2].set_title("result")
        plt.show()

    # ============================= RYSOWANIE PROSTOKĄTÓW DOOKOŁA AUTEK =================================

    labeled_image = measure.label(mask, connectivity=2)
    labeled_image = morphology.remove_small_objects(labeled_image, connectivity=2, min_size=3000)

    regions = measure.regionprops(labeled_image)

    image_with_boxes = resized_image.copy()

    car_positions = []
    for region in regions:
        min_row, min_col, max_row, max_col = region.bbox
        car_positions.append([min_col, min_row])
        cv2.rectangle(image_with_boxes, (min_col, min_row), (max_col, max_row), (255, 0, 0), 2)

    image_with_boxes = cv2.cvtColor(image_with_boxes, cv2.COLOR_BGR2RGB)

    if show_end_product:
        _, axes = plt.subplots(1, 2, figsize=(12, 6))
        axes[0].imshow(resized_image)
        axes[0].set_title("Original footage")
        axes[1].imshow(image_with_boxes)
        axes[1].set_title("Detected cars")
        plt.show()

    return [image_with_boxes, car_positions]


if __name__ == "__main__":
    image = cv2.imread("parking.jpg")
    found_cars, car_pos = findCars(image)
    plates = ['EL 123456', 'EKU 111222', 'EZD 023023', 'PL 6969']
    image_with_licence_plates = drawAllLicencePlateNumbers(found_cars, plates, car_pos)
    cv2.imshow("cars", image_with_licence_plates)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
