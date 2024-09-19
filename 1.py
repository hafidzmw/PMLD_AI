import cv2
import numpy as np

#membaca gambar
image = cv2.imread('ss2.png')

#mengubah gambar menjadi grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#threshold
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

#menghitung total pixel
total_pixels = thresh.size
white_pixels = cv2.countNonZero(thresh)

#hitung peresentase luas batu
percentage_area = (white_pixels / total_pixels) * 100

#menemukan kontur dalam gambar
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#hitung jumlah batu
number_of_stones = len(contours)

#gambarkan kontur pada gambar asli
for contour in contours:
    cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)
    
#tampilkan informasi pada gambar
info_text = f'Jumlah Batu: {number_of_stones}, Luas Batu: {percentage_area:.2f}%'
cv2.putText(image, info_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

#menampilkan hasil
print(f'Jumlah Batu: {number_of_stones}')
print (f'Luas batu adalah: {percentage_area:.2f}%')

#menampilkan gambar asli dan gambar hasil thresholding
cv2.imshow('Gambar Asli dengan Kontur', image)
cv2.imshow('Gambar Threshold', thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()
