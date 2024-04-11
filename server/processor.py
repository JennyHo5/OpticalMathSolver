import cv2
import numpy as np
import matplotlib.pyplot as plt
# import pytesseract
from recognizer import recognize_math

# For draw locally
gray_global = None
thresh_global = None
dilated_global = None
contour_image_global = None
# to use pytesseract in Windows https://stackoverflow.com/questions/50951955/pytesseract-tesseractnotfound-error-tesseract-is-not-installed-or-its-not-i
# pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' 
# equation_text = pytesseract.image_to_string(equation_region, config='--psm 10')
# print(equation_text)
"""
    Identify the region of each equatoin from the image that may contain multiple equations
    return: equation_regions, a list of regions
"""

def parse_equation(image):
    global gray_global, dilated_global
    # Convert image in grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_global = gray
    dilated, contours = process_image(gray)
    
    """
        To parse the image to identify regions of equations
            - find bounding box of contours (thresholding 200)
            - if the bounding boxes are deemed to be on the same horizontal line (similar y-coords), they belong to the same math equation
            - then, they should be formed as one larger bounding box
    """

    max_height = 0
    bounding_boxes = []
    
    # find bounding box for contours
    for contour in contours:
        if cv2.contourArea(contour) > 175:
            x, y, w, h = cv2.boundingRect(contour)
            max_height = max(max_height, h)
            equation_region = image[y:y+h, x:x+w]
            # cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 2)
            bounding_boxes.append((x, y, w, h))

    # use the height of the largest bounding box as a reference to determine if bounding boxes have similar y-coords
    y_threshold = max_height        
    def on_same_line(box1, box2, threshold):
        return abs(box1[1] - box2[1]) < threshold

    # group the bounding boxes 
    lines = []
    for box in bounding_boxes:
        added = False
        for line in lines:
            if any(on_same_line(box, other_box, y_threshold) for other_box in line):
                line.append(box)
                added = True
                break
        if not added:
            lines.append([box])

    # find the bounding box for each equation
    equation_regions = []
    for line in lines:
        # Calculate the min x, min y, max x, and max y for the boxes in the line, box = (x, y, w, h)
        x_coords = [box[0] for box in line]
        y_coords = [box[1] for box in line]
        w_coords = [box[2] for box in line]
        h_coords = [box[3] for box in line]
        min_x = min(x_coords)
        min_y = min(y_coords)
        max_x = max(x_coords[i] + w_coords[i] for i in range(len(line)))
        max_y = max(y_coords[i] + h_coords[i] for i in range(len(line)))
        rows, cols = dilated.shape
        # Append the merged bounding box for the line, add padding 25 pixels if not out of bound
        min_x = max(min_x-25, 0)
        min_y = max(min_y-25, 0)
        h = min (max_y + 25, rows) - min_y
        w = min (max_x + 25, cols) - min_x
        equation_regions.append((min_x, min_y, w, h))
        
        # Draw merged bounding boxes on the image (for demo and test)
        cv2.rectangle(dilated, (min_x, min_y), (min_x + w, min_y + h), (255, 255, 255), 3)
    
    dilated_global = dilated
    # draw(gray_global, thresh_global, dilated_global, contour_image_global)

    return dilated, equation_regions


        


def process_image(image):
    global thresh_global, contour_image_global
    """
        TODO: Play around with the parameters of image processing functions to optimaize the quality of output image
    """

    # Noise Reduction
    # applying a very small median and Gaussian blur ((3,3) kernel) before the bilateral filter can help in reducing noise without significantly impacting the edge details
    # bilateralFilter is highly effective in noise removal while keeping edges sharp
    image = cv2.medianBlur(image, 3)
    image = cv2.GaussianBlur(image, (3, 3), 0)
    image = cv2.bilateralFilter(src=image, d=23, sigmaColor=75, sigmaSpace=75)
    
    # Adaptive threshold, binarized the image
    thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 13, 1)
    # remove implusive noise after thresholding
    thresh = cv2.medianBlur(thresh, 5)

    thresh_global = thresh

    # Morphology - dilation
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))  # Adjust the kernel size if needed
    dilated = cv2.dilate(thresh, kernel, iterations=1)
    
    # Reduce implusive noise caused by dilation
    dilated = cv2.medianBlur(dilated, 11)
    
    # Find contours to identify the region of interest
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours on the original image(for test and demo)
    contour_image = cv2.drawContours(image.copy(), contours, -1, (0, 255, 0), 3)
    contour_image_global = contour_image
    
    return dilated, contours
    

"""
    FOR LOCAL TESTING

"""
def draw(gray, thresh, dilated, contour_image):
    plt.figure(figsize=(12,12))

    plt.subplot(221)
    plt.imshow(gray, cmap = 'gray')
    plt.title('gray')

    plt.subplot(222)
    plt.imshow(thresh, cmap = 'gray')
    plt.title('Binarized Adaptive Threshold')

    plt.subplot(223)
    plt.imshow(dilated, cmap = 'gray')
    plt.title('dilated')

    contour_img_rgb = cv2.cvtColor(contour_image, cv2.COLOR_BGR2RGB)
    plt.subplot(224)
    plt.imshow(contour_img_rgb)
    plt.title('Contour_img after Binarized AdaptiveThreshold')

    plt.savefig('bilateralFilter.png')
    plt.show()