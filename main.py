import cv2
import math
from cvzone.HandTrackingModule import HandDetector
from pynput.mouse import Controller
import time

mouse = Controller()
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Camera cannot be opened.")
    exit()

detector = HandDetector(detectionCon=0.3, maxHands=1)

previous_scroll = 0

def main():
    global previous_scroll
    while True:
        ret, frame = camera.read()
        frame = cv2.flip(frame, 1)

        if not ret:
            print("Failed to read frame.")
            break

        hands, image = detector.findHands(frame)

        if hands:
            first_hand = hands[0]
            landmark_list = first_hand["lmList"]

            if len(landmark_list) != 0:
                x1, y1 = landmark_list[4][0], landmark_list[4][1]
                x2, y2 = landmark_list[8][0], landmark_list[8][1]
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

                cv2.circle(image, (x1, y1), 5, (0, 0, 255), cv2.FILLED)
                cv2.circle(image, (x2, y2), 5, (0, 0, 255), cv2.FILLED)
                cv2.line(image, (x1, y1), (x2, y2), (0, 0, 0), 3)

                length = math.hypot(x2 - x1, y2 - y1)
                scroll_amount = 0

                if length < 50:  
                    scroll_amount = 1
                elif length > 100:  
                    scroll_amount = -1

                if scroll_amount != 0:
                    previous_scroll += scroll_amount * 0.1
                    mouse.scroll(0, previous_scroll)
                    previous_scroll = max(min(previous_scroll, 1), -1)

                if length < 50:
                    cv2.circle(image, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
                elif length > 100:
                    cv2.circle(image, (cx, cy), 5, (0, 0, 0), cv2.FILLED)
                else:
                    cv2.circle(image, (cx, cy), 5, (0, 0, 255), cv2.FILLED)

        cv2.imshow("Hand Scroll Control", image)
        cv2.resizeWindow("Hand Scroll Control", 700, 500)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()