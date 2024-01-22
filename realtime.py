import time
import cv2
import numpy as np
from utils import upload_image

# print(cv2.__file__)
# upload_image("car.jpg")


# Colors and Constants
RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (176, 130, 39)
ORANGE = (0, 127, 255)

# Create Car Classifier
FONT = cv2.FONT_HERSHEY_COMPLEX

# Configuration
offset = 6
fps = 60
min_width = 80
min_height = 80
linePos = 550

ground_truth1 = 62
ground_truth2 = 36


def center_position(x, y, w, h):
    center_x = x + (w // 2)
    center_y = y + (h // 2)
    return center_x, center_y


def count_using_bg_sub():
    ans = input("Enter 'yes' for realtime and 'no' for demo:  ")
    CAP = None

    if ans.lower() == "yes":
        CAP = cv2.VideoCapture(0)
    elif ans.lower() == "no":
        CAP = cv2.VideoCapture('video.mp4')
    else:
        print("Invalid input")
        return
    # CAP = cv2.VideoCapture(0)
    # Initialize Background Subtractor
    subtract = cv2.createBackgroundSubtractorMOG2()
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    # Configuration for detection
    detect_vehicle = []
    vehicle_counts = 0

    while CAP.isOpened():
        duration = 1 / fps
        time.sleep(duration)

        # Read each frame of the video
        ret, frame = CAP.read()
        if frame is None:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 5)

        # Subtract background, fill up object area, and clear noise
        img_sub = subtract.apply(blur)
        dilation = cv2.dilate(img_sub, np.ones((5, 5)))
        opening = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel)
        contours = cv2.findContours(
            opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

        # Count if the car passes this line
        cv2.line(frame, (25, linePos), (1200, linePos), BLUE, 1)

        for contour in contours:
            x1, y1, w1, h1 = cv2.boundingRect(contour)
            valid_contour = (w1 >= min_width) and (h1 >= min_height)
            if not valid_contour:
                continue

            cv2.rectangle(frame, (x1, y1), (x1 + w1, y1 + h1), GREEN, 1)
            center_vehicle = center_position(x1, y1, w1, h1)
            detect_vehicle.append(center_vehicle)
            # cv2.circle(frame, center_vehicle, 4, RED, -1)

            # if the center of the car passes the counting line
            for x, y in detect_vehicle:
                if y < linePos + offset and y > linePos - offset:
                    # cv2.line(frame, (25, linePos), (1200, linePos), ORANGE, 3)
                    detect_vehicle.remove((x, y))
                    vehicle_counts += 1

                    # Save the cropped image
                    vehicle_roi = frame[y1:y1+h1, x1:x1+w1]
                    image_name = f'vehicle_{time.time()}.png'
                    cv2.imwrite(image_name, vehicle_roi)
                    # upload to server
                    # upload_image(image_name)

        cv2.putText(
            frame, f"Car Detected: {vehicle_counts}", (50, 70), FONT, 2, RED, 3, cv2.LINE_AA)
        cv2.imshow('Vehicles Detection', frame)

        # Press 'ESC' Key to Quit
        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()
    CAP.release()

    return vehicle_counts


count_using_bg_sub()
# if __name__ == "__main__":
