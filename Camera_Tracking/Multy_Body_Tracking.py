import cv2
import socket
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# UDP setup
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)

# Create the pose landmarker
base_options = python.BaseOptions(model_asset_path="pose_landmarker_full.task")
options = vision.PoseLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_poses=4  # up to 4 people
)
pose_landmarker = vision.PoseLandmarker.create_from_options(options)

# Start camera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
frame_count = 0

while True:
    success, img = cap.read()
    if not success:
        break

    # Convert to mediapipe image
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    frame_count += 1

    # Run multi-pose detection
    result = pose_landmarker.detect_for_video(mp_image, frame_count)

    if result.pose_landmarks:
        for i, pose in enumerate(result.pose_landmarks):
            # Only track up to 4 people
            if i >= 4:
                break

            # Draw landmarks on image
            for lm in pose:
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(img, (cx, cy), 4, (0, 255, 0), -1)

            # Flatten data for UDP
            flat_points = []
            for lm in pose:
                flat_points.extend([round(lm.x, 5), round(lm.y, 5), round(lm.z, 5)])

            # Convert to comma-separated string and send
            data_str = ",".join(map(str, flat_points))
            message = f"Person{i}:{data_str}"
            sock.sendto(str.encode(message), serverAddressPort)
            print(f"Sent person {i} data ({len(flat_points)//3} points)")

    cv2.imshow("Multi-Person Pose", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
