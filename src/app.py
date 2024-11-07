from flask import Flask, request, jsonify
from image_processing import detect_rocks_in_image
from dotenv import load_dotenv

import os
import cv2
import numpy as np

load_dotenv()

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def handle_image_upload():
    """
    Handle image upload via a POST request, process the image to detect rocks,
    and return the result as JSON.
    
    Returns:
        JSON response containing rock detection details and the processed image.
    """
    # Check if the request contains a file
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return jsonify({"error": "Empty filename"}), 400
    
    # Decode the uploaded image from the file
    image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        return jsonify({"error": "Invalid image format"}), 400
    
    # Process the image to detect rocks
    rock_count, rock_area_percentage, processed_image = detect_rocks_in_image(image)
    
    # Encode the processed image as JPEG
    _, image_buffer = cv2.imencode('.jpg', processed_image)
    encoded_image = image_buffer.tobytes()
    
    # Construct the response with detection results and the processed image
    response_data = {
        "rock_count": rock_count,
        "rock_area_percentage": rock_area_percentage,
        "processed_image": encoded_image.hex()  # Return image as hexadecimal string
    }
    
    return jsonify(response_data)

if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))

    app.run(host=host, port=port)
