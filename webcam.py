import cv2

# Test webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam")
else:
    print("Webcam opened successfully")
    ret, frame = cap.read()
    if ret:
        print("Webcam can capture images")
        cv2.imwrite('test_photo.jpg', frame)
        print("Test photo saved as 'test_photo.jpg'")
    else:
        print("Error: Could not capture image")

    cap.release()
    cv2.destroyAllWindows()