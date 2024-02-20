import cv2
import numpy as np
import time

# Tanımlamak istediğiniz QR kodu metni
target_qr_text = "https://www.teknofest.org/tr/"

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

detector = cv2.QRCodeDetector()

while cap.isOpened():
    success, img = cap.read()

    start = time.perf_counter()

    # QR kodlarını tespit et
    value, points, qrcode = detector.detectAndDecode(img)

    if value != "" and value == target_qr_text:
        x1, y1, x2, y2 = points[0][0], points[0][1], points[2][0], points[2][1]

        x_center = (x2 - x1) / 2 + x1
        y_center = (y2 - y1) / 2 + y1

        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 5)
        cv2.circle(img, (int(x_center), int(y_center)), 3, (0, 255, 0), 3)
        cv2.putText(img, str(value), (30, 120), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255))

    else:
        # Tanımlanmamış QR kodları için ekranda "Tanımlanmamış" yazısı görüntülenir
        cv2.putText(img, "Tanımlanmamış", (30, 120), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255))

    end = time.perf_counter()
    totalTime = end - start
    fps = 1 / totalTime

    cv2.putText(img, f'FPS: {int(fps)}', (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255))

    cv2.imshow('img', img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
