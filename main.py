import cv2
import math
from cvzone.HandTrackingModule import HandDetector
from pynput.mouse import Controller
import time

mouse = Controller()
kamera = cv2.VideoCapture(0)

if not kamera.isOpened():
    print("Kamera tidak dapat dibuka.")
    exit()

detektor = HandDetector(detectionCon=0.3, maxHands=1)

scroll_sebelumnya = 0

def main():
    global scroll_sebelumnya
    while True:
        ret, frame = kamera.read()
        frame = cv2.flip(frame, 1)

        if not ret:
            print("Gagal membaca frame.")
            break

        tangan, gambar = detektor.findHands(frame)

        if tangan:
            tangan_pertama = tangan[0]
            daftar_landmark = tangan_pertama["lmList"]

            if len(daftar_landmark) != 0:
                x1, y1 = daftar_landmark[4][0], daftar_landmark[4][1]
                x2, y2 = daftar_landmark[8][0], daftar_landmark[8][1]
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

                cv2.circle(gambar, (x1, y1), 5, (0, 0, 255), cv2.FILLED)
                cv2.circle(gambar, (x2, y2), 5, (0, 0, 255), cv2.FILLED)
                cv2.line(gambar, (x1, y1), (x2, y2), (0, 0, 0), 3)

                panjang = math.hypot(x2 - x1, y2 - y1)
                jumlah_scroll = 0

                if panjang < 50:  
                    jumlah_scroll = 1
                elif panjang > 100:  
                    jumlah_scroll = -1

                if jumlah_scroll != 0:
                    scroll_sebelumnya += jumlah_scroll * 0.1
                    mouse.scroll(0, scroll_sebelumnya)
                    scroll_sebelumnya = max(min(scroll_sebelumnya, 1), -1)

                if panjang < 50:
                    cv2.circle(gambar, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
                elif panjang > 100:
                    cv2.circle(gambar, (cx, cy), 5, (0, 0, 0), cv2.FILLED)
                else:
                    cv2.circle(gambar, (cx, cy), 5, (0, 0, 255), cv2.FILLED)

        cv2.imshow("Kontrol Scroll dengan Tangan", gambar)
        cv2.resizeWindow("Kontrol Scroll dengan Tangan", 700, 500)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    kamera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
 