from flask import Flask, request, jsonify
import cv2
import numpy as np
import os

app = Flask(__name__)

def process_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Membuat treshold untuk membedakan batu dengan wadah
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

    # Cari kontur
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Hitung total area gambar
    total_area = image.shape[0] * image.shape[1]

    batu_area = 0
    jumlah_batu = len(contours)
    for contour in contours:
        batu_area += cv2.contourArea(contour)

    # Hitung persentase area yang dipenuhi batu
    batu_percentage = (batu_area / total_area) * 100

    # Tampilkan jumlah batu dan persentase area di atas gambar
    cv2.putText(image, f"Jumlah Batu: {jumlah_batu}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(image, f"Batu Area: {batu_percentage:.2f}%", (10, 60), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Gambar kontur (area batu) pada gambar
    cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

    return image, jumlah_batu, batu_percentage

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "Tidak ada file yang diunggah"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nama file kosong"}), 400
    
    # Membaca gambar dari file upload
    image = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        return jsonify({"error": "Format gambar tidak didukung atau gambar tidak valid"}), 400
    
    # Proses gambar
    processed_image, jumlah_batu, batu_percentage = process_image(image)
    
    # Encode gambar kembali ke format jpeg
    _, buffer = cv2.imencode('.jpg', processed_image)
    image_data = buffer.tobytes()
    
    # Return hasil dalam JSON dan gambar dalam bentuk base64
    response = {
        "jumlah_batu": jumlah_batu,
        "batu_percentage": batu_percentage,
        "processed_image": image_data.hex()  # Gambar dikembalikan sebagai hexadecimal string
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
