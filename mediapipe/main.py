import cv2
import mediapipe as mp
import time
import numpy as np

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands(False, 2, 1, 0.5, 0.5)
mpDraw = mp.solutions.drawing_utils
handLmsStyle = mpDraw.DrawingSpec(color=(255, 0, 255), thickness=3)
handConStyle = mpDraw.DrawingSpec(color=(155, 0, 0), thickness=5)

pTime = 0
cTime = 0

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

while True:
    ret, img = cap.read()
    if ret == 1:
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(imgRGB)

        imgHeight = img.shape[0]
        imgWidth = img.shape[1]

        origin = (imgWidth // 2, imgHeight // 2)
        a = int(np.sqrt((imgWidth ** 2) / 16))//2
        b = int(np.sqrt((imgHeight ** 2) / 4))//2
        ellipse_center = (imgWidth // 2, imgHeight // 2)

        cv2.ellipse(img, ellipse_center, (a, b), 0, 0, 360, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.line(img, (0, origin[1]), (imgWidth, origin[1]), (255, 255, 255), 2)
        cv2.line(img, (origin[0], 0), (origin[0], imgHeight), (255, 255, 255), 2)

        if result.multi_hand_landmarks:
            for handIdx, handLms in enumerate(result.multi_hand_landmarks):
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS, handLmsStyle, handConStyle)
                handConStyle = mpDraw.DrawingSpec(color=(155, 0, 0), thickness=2)

                for i, lm in enumerate(handLms.landmark):
                    xPosition = int(lm.x * imgWidth)
                    yPosition = int(lm.y * imgHeight)

                    relative_x = xPosition - origin[0]
                    relative_y = yPosition - origin[1]

                    cv2.putText(img, f"({relative_x}, {relative_y})", (xPosition-25, yPosition+5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 2)

                    if i % 4 == 0:
                        cv2.circle(img, (xPosition, yPosition), 5, (255, 255, 255), cv2.FILLED)

                    if handIdx == 0:
                        print("First hand - Point", i, ": (", xPosition, ",", yPosition, ")")
                    else:
                        print("Second hand - Point", i, ": (", xPosition, ",", yPosition, ")")

                    if ((relative_y / (height/4))**2 + (relative_x / (height/8))**2) <= 1:
                        print("WARNING: Point", i, "inside the ellipse!")
                        cv2.putText(img, "WARNING", (xPosition, yPosition), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f"FPS: {int(fps)}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

        cv2.imshow('img', img)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
