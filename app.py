import mediapipe as mp
import cv2
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a,b,c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1]-b[1],c[0]-b[0]) - np.arctan2(a[1]-b[1],a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle> 180.0:
        angle = 360-angle

    return angle 

cap = cv2.VideoCapture(0)
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret,frame = cap.read()
        
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        try:
            landmarks = results.pose_landmarks.landmark
            # landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            # landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
            # landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]

            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            angle = calculate_angle(shoulder,elbow,wrist)


            cv2.putText(image,str(angle),
                        tuple(np.multiply(elbow,[640,480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX,0.5, (255,255,255),2,cv2.LINE_AA
                        )
        except:
            pass
        mp_drawing.draw_landmarks(image, results.pose_landmarks, 
                                         mp_pose.POSE_CONNECTIONS,
                                         mp_drawing.DrawingSpec(color=(245,117,66),thickness=2,circle_radius=2),
                                         mp_drawing.DrawingSpec(color=(245,66,236),thickness=2,circle_radius=2)
            )

        cv2.imshow("MediaPipe Feed",image)
        if cv2.waitKey(10) & 0xff == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()