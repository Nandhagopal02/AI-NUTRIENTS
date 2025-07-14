import mediapipe as mp
import cv2
import exercise as ex

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def mp_stream(cap, exercise, counter, phase, return_count=False):
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                func = getattr(ex, exercise)
                counter, phase = func(image, landmarks, counter, phase)

            if not return_count:
                cv2.imshow("Exercise", image)
                if cv2.waitKey(10) & 0xFF == 27:
                    break

        return counter
