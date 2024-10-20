import cv2

def detect_rocks_in_image(image):
    """
    Process the input image to detect rocks and calculate their area percentage.
    
    Parameters:
        image (np.ndarray): Input image in BGR format.
    
    Returns:
        processed_image (np.ndarray): Image with rock contours and annotations.
        rock_count (int): Number of rocks detected.
        rock_area_percentage (float): Percentage of the image area covered by rocks.
    """
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply binary thresholding to separate rocks from the background
    _, binary_thresh = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY_INV)

    # Find contours representing the rocks
    contours, _ = cv2.findContours(binary_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Calculate total image area
    total_image_area = image.shape[0] * image.shape[1]

    # Calculate the total area occupied by rocks and count the number of rocks
    total_rock_area = 0
    rock_count = len(contours)
    for contour in contours:
        total_rock_area += cv2.contourArea(contour)

    # Calculate the percentage of the image area covered by rocks
    rock_area_percentage = (total_rock_area / total_image_area) * 100

    # Annotate the image with the rock count and area percentage
    cv2.putText(image, f"Rocks Detected: {rock_count}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(image, f"Rock Area: {rock_area_percentage:.2f}%", (10, 60), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Draw contours around detected rocks
    cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

    return image, rock_count, rock_area_percentage
