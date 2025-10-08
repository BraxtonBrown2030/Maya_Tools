import cv2
from cvzone.PoseModule import PoseDetector
import socket
"""
pyinstaller --onefile --windowed --add-data "D:\Pyinstall\.venv\Lib\site-packages\mediapipe\modules\pose_landmark;mediapipe\modules\pose_landmark" --add-data "D:\Pyinstall\.venv\Lib\site-packages\mediapipe\modules\pose_detection;mediapipe\modules\pose_detection" --add-data "D:\Pyinstall\.venv\Lib\site-packages;site-packages" BodyTracking.py
"""
video_source = 0
server_address = "127.0.0.1"
server_port = 5052
detection_conf = 0.8

# Initialize webcam
cap = cv2.VideoCapture(video_source)
cap.set(3, 1280)
cap.set(4, 720)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = (server_address, server_port)

# Initialize Pose Detector
detector = PoseDetector(detectionCon=detection_conf)

while True:
    success, img = cap.read()
    if not success:
        break

    # Detect pose
    img = detector.findPose(img)

    # Extract landmark list
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=True)

    if lmList and len(lmList) > 28:
        point11 = (lmList[11][0], lmList[11][1])  # Left Shoulder
        point12 = (lmList[12][0], lmList[12][1])  # Right Shoulder
        point13 = (lmList[13][0], lmList[13][1])  # Left Elbow
        point14 = (lmList[14][0], lmList[14][1])  # Right Elbow
        point15 = (lmList[15][0], lmList[15][1])  # Left Wrist
        point16 = (lmList[16][0], lmList[16][1])  # Right Wrist
        point23 = (lmList[23][0], lmList[23][1])  # Left Hip
        point24 = (lmList[24][0], lmList[24][1])  # Right Hip
        point25 = (lmList[25][0], lmList[25][1])  # Left knee
        point26 = (lmList[26][0], lmList[26][1])  # Right knee
        point27 = (lmList[27][0], lmList[27][1])  # Left ankle
        point28 = (lmList[28][0], lmList[28][1])  # Right ankle
        # Torso midpoint = average of 4 points
        torso_x = (point11[0] + point12[0] + point23[0] + point24[0]) // 4
        torso_y = (point11[1] + point12[1] + point23[1] + point24[1]) // 4
        mid_point = (torso_x, torso_y)

        # Draw torso midpoint
        cv2.circle(img, mid_point, 10, (0, 0, 255), cv2.FILLED)

        data_list = [point11[0],
                     -point11[1],
                     point13[0],
                     -point13[1],
                     point15[0],
                     -point15[1],
                     point12[0],
                     -point12[1],
                     point14[0],
                     -point14[1],
                     point16[0],
                     -point16[1],
                     point23[0],
                     -point23[1],
                     point25[0],
                     -point25[1],
                     point27[0],
                     -point27[1],
                     point24[0],
                     -point24[1],
                     point26[0],
                     -point26[1],
                     point28[0],
                     -point28[1],
                     mid_point[0],
                     -mid_point[1]]


        data = ",".join(map(str, data_list))

        sock.sendto(str.encode(data), serverAddressPort)
        # print(data)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()