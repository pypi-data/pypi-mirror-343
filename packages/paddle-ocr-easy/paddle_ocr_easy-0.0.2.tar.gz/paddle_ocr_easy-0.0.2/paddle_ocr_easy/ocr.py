import cv2
import matplotlib.pyplot as plt
from paddleocr import PaddleOCR, draw_ocr
import numpy as np

# Initialize the OCR model
ocr_model = PaddleOCR(use_angle_cls=True, lang='en')

def recognize_and_plot(image_path_or_array):
    """
    Run OCR on the given image and plot the result.
    Args:
        image_path_or_array (str or np.ndarray): Path to image or image array.
    """

    # Read image
    if isinstance(image_path_or_array, str):
        image = cv2.imread(image_path_or_array)
        if image is None:
            raise FileNotFoundError(f"Image at {image_path_or_array} not found.")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    elif isinstance(image_path_or_array, np.ndarray):
        image = image_path_or_array
    else:
        raise ValueError("Input must be a file path or an image array.")

    # Run OCR
    result = ocr_model.ocr(image, cls=True)

    # Extract boxes and texts
    boxes = [line[0] for line in result[0]]
    txts = [line[1][0] for line in result[0]]
    scores = [line[1][1] for line in result[0]]
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    # Draw OCR results
    image_with_ocr = draw_ocr(image, boxes, txts, scores, font_path = font_path)  # Replace with a real TTF if needed
    plt.figure(figsize=(10, 10))
    plt.imshow(image_with_ocr)
    plt.axis('off')
    plt.show()

    # Print detected text
    print("Detected Texts:")
    for text in txts:
        print(text)
