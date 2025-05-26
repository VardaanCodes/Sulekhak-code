import svgwrite
import os
import cv2

input_directory = "cropped_test2_characters"
output_directory = "svg"
os.makedirs(output_directory, exist_ok=True)


def process_image(filepath):
    img = cv2.imread(filepath, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=1)
    contours, _ = cv2.findContours(cleaned, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
    filename = os.path.splitext(os.path.basename(filepath))[0]
    svgpath = os.path.join(output_directory, f"{filename}.svg")
    dwg = svgwrite.Drawing(svgpath, profile="tiny")
    for contour in contours:
        epsilon = 0.004 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        points = [(float(point[0][0]), float(point[0][1])) for point in approx]
        if len(points) > 2:
            dwg.add(dwg.polygon(points, fill="black"))
    dwg.save()
    return True


for filename in os.listdir(input_directory):
    if filename.lower().endswith(".png"):
        process_image(os.path.join(input_directory, filename))

print("SVGs created with thin, clean outlines in 'svg' directory.")
