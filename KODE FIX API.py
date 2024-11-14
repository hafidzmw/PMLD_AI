from flask import Flask, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)

# Function to process the image
def process_image(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use Canny edge detection to find edges
    edges = cv2.Canny(gray, 50, 150)

    # Use morphological operations to thicken edge areas
    kernel = np.ones((5, 5), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=2)
    edges = cv2.erode(edges, kernel, iterations=1)

    # Find contours from the edge-detected image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter out small contours (likely noise) based on area
    min_contour_area = 100  # Adjust this for the smallest stone size
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]

    # Calculate the number of stones
    number_of_stones = len(filtered_contours)

    # Calculate the percentage area covered by stones
    total_pixels = edges.size
    white_pixels = cv2.countNonZero(edges)
    percentage_area = (white_pixels / total_pixels) * 100

    # Draw contours and convex hulls on the original image
    for contour in filtered_contours:
        # Draw the original contour in green
        cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)

        # Calculate and draw the convex hull of the contour in red
        hull = cv2.convexHull(contour)
        cv2.drawContours(image, [hull], -1, (0, 0, 255), 2)

    # Add info text to the image
    info_text = f'Jumlah Batu: {number_of_stones}, Luas Batu: {percentage_area:.2f}%'
    (text_width, text_height), _ = cv2.getTextSize(info_text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
    cv2.rectangle(image, (10, 10), (10 + text_width + 10, 10 + text_height + 10), (0, 0, 0), -1)
    cv2.putText(image, info_text, (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    return number_of_stones, percentage_area, image

# Route for uploading and processing an image
@app.route('/process_image', methods=['POST'])
def upload_image():
    # Check if an image file was uploaded
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    # Read the file as an image using OpenCV
    npimg = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # Process the image
    number_of_stones, percentage_area, processed_image = process_image(image)

    # Encode the processed image to PNG format
    _, buffer = cv2.imencode('.png', processed_image)
    image_data = buffer.tobytes()

    # Return the results in JSON format, with image data in hex
    response = {
        "jumlah_batu": number_of_stones,
        "batu_percentage": percentage_area,
        "processed_image": image_data.hex()
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
