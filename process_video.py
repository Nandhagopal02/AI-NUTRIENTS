import cv2
import videoStream as vs

def count_reps_from_video(video_path, exercise):
    exercise = exercise.strip().lower()
    if exercise not in ["pushup", "squat", "pullup"]:
        raise ValueError(f"Unsupported exercise: {exercise}")

    counter = 0
    phase = None

    if exercise == "pushup":
        counter = -1
        phase = "UP"
    elif exercise == "squat":
        phase = "DOWN"
    elif exercise == "pullup":
        phase = None

    cap = cv2.VideoCapture(video_path)
    reps = vs.mp_stream(cap, exercise, counter, phase, return_count=True)
    cap.release()
    cv2.destroyAllWindows()
    return reps
