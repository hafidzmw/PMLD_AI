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
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Thresholding
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Menghitung total pixel
    total_pixels = thresh.size
    white_pixels = cv2.countNonZero(thresh)

    # Hitung persentase luas batu (area putih)
    percentage_area = (white_pixels / total_pixels) * 100

    # Menemukan kontur dalam gambar
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Hitung jumlah batu (kontur yang ditemukan)
    number_of_stones = len(contours)

    # Gambar kontur pada gambar asli
    for contour in contours:
        cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)

    return number_of_stones, percentage_area, image
