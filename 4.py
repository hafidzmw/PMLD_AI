from flask import Flask, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)

# Fungsi untuk memproses gambar
def process_image(image):
    # mengubah gambar menjadi grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # threshold
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # menghitung total pixel
    total_pixels = thresh.size
    white_pixels = cv2.countNonZero(thresh)

    # hitung persentase luas batu
    percentage_area = (white_pixels / total_pixels) * 100

    # menemukan kontur dalam gambar
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # hitung jumlah batu
    number_of_stones = len(contours)

    # gambarkan kontur pada gambar asli
    for contour in contours:
        cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)

    return number_of_stones, percentage_area, image

# Route untuk mengupload gambar dan memprosesnya
@app.route('/process_image', methods=['POST'])
def upload_image():
    # Mengecek apakah ada file gambar yang diupload
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    # Membaca file sebagai gambar menggunakan OpenCV
    npimg = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # Proses gambar
    number_of_stones, percentage_area, processed_image = process_image(image)

    # Menyimpan gambar yang diproses (opsional, jika ingin melihat hasilnya)
    cv2.imwrite('processed_image.png', processed_image)

    # Encode gambar kembali ke format jpeg
    _, buffer = cv2.imencode('.png', processed_image)
    image_data = buffer.tobytes()

     # Return hasil dalam JSON dan gambar dalam bentuk base64
    response = {
        "jumlah_batu": number_of_stones,
        "batu_percentage": percentage_area,
        "processed_image": image_data.hex()
    }

if __name__ == '__main__':
    app.run(debug=True)
