import os
import sys
import tkinter as tk    
from tkinter import filedialog

import cv2


def get_image_path_from_dialog():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select an Image File",
        filetypes=(("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff"), ("All files", "*.*")),
    )
    return file_path


input_image_path = get_image_path_from_dialog()

if not input_image_path:
    print("No image selected. Exiting.")
    sys.exit(1)

image = cv2.imread(input_image_path)

if image is None:
    print(f"Error: Could not read image from {input_image_path}. Exiting.")
    sys.exit(1)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr))

input_file_basename = os.path.basename(input_image_path)
input_filename_without_ext = os.path.splitext(input_file_basename)[0]
output_char_dir = f"cropped_{input_filename_without_ext}_characters"

if not os.path.exists(output_char_dir):
    os.makedirs(output_char_dir)

processed_contours = set()
char_count = 0

for i, contour in enumerate(contours):
    if i in processed_contours:
        continue

    x, y, w, h = cv2.boundingRect(contour)
    area = cv2.contourArea(contour)  # Note: 'area' is calculated but not used.

    if w < 5 or h < 5:
        continue

    merged_box = [x, y, w, h]
    for j, other_contour in enumerate(contours):
        if j == i or j in processed_contours:
            continue
        ox, oy, ow, oh = cv2.boundingRect(other_contour)
        main_cx = x + w / 2
        dot_cx = ox + ow / 2
        horizontal_center_distance = abs(dot_cx - main_cx)
        max_center_distance = max(w, ow) * 1.2
        vertical_gap = min(abs((oy + oh) - y), abs((y + h) - oy))
        if (
            horizontal_center_distance < max_center_distance
            and vertical_gap < max(h, oh) * 0.5
            and (ow * oh) < (w * h * 0.5)
        ):
            merged_box[0] = min(x, ox)
            merged_box[1] = min(y, oy)
            merged_box[2] = max(x + w, ox + ow) - merged_box[0]
            merged_box[3] = max(y + h, oy + oh) - merged_box[1]
            processed_contours.add(j)
            break  # Exit inner loop once a merge occurs

    x, y, w, h = merged_box
    pad = 2
    y_start = max(0, y - pad)
    y_end = min(image.shape[0], y + h + pad)
    x_start = max(0, x - pad)
    x_end = min(image.shape[1], x + w + pad)

    cropped = image[y_start:y_end, x_start:x_end]
    cv2.imwrite(f"{output_char_dir}/char_{char_count}.png", cropped)
    char_count += 1
    processed_contours.add(i)

print(f"Cropped {char_count} characters saved in '{output_char_dir}' directory.")
