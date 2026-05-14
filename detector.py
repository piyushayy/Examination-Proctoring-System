import cv2
import mediapipe as mp
import numpy as np

class Detector:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=2, # Increased to detect intruders
            refine_landmarks=True,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        
        # 3D model points for a generic face mapping
        self.model_points = np.array([
            (0.0, 0.0, 0.0),             # Nose tip (landmark 1)
            (0.0, -330.0, -65.0),        # Chin (landmark 152)
            (-225.0, 170.0, -135.0),     # Left eye left corner (landmark 33)
            (225.0, 170.0, -135.0),      # Right eye right corner (landmark 263)
            (-150.0, -150.0, -125.0),    # Left mouth corner (landmark 61)
            (150.0, -150.0, -125.0)      # Right mouth corner (landmark 291)
        ])

    def detect_behavior(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.face_mesh.process(rgb)

        if not result.multi_face_landmarks:
            return "NO_FACE"
        
        # FEATURE: Multi-face detection
        if len(result.multi_face_landmarks) > 1:
            return "MULTIPLE_FACES"

        landmarks = result.multi_face_landmarks[0].landmark
        img_h, img_w, _ = frame.shape
        
        # Extract 2D image points from specific facial landmarks
        image_points = np.array([
            (landmarks[1].x * img_w, landmarks[1].y * img_h),     # Nose tip
            (landmarks[152].x * img_w, landmarks[152].y * img_h), # Chin
            (landmarks[33].x * img_w, landmarks[33].y * img_h),   # Left eye corner
            (landmarks[263].x * img_w, landmarks[263].y * img_h), # Right eye corner
            (landmarks[61].x * img_w, landmarks[61].y * img_h),   # Left mouth corner
            (landmarks[291].x * img_w, landmarks[291].y * img_h)  # Right mouth corner
        ], dtype="double")

        # Approximate camera matrix based on image dimensions
        focal_length = img_w
        center = (img_w / 2, img_h / 2)
        camera_matrix = np.array([
            [focal_length, 0, center[0]],
            [0, focal_length, center[1]],
            [0, 0, 1]
        ], dtype="double")

        dist_coeffs = np.zeros((4, 1)) # Assuming no lens distortion

        # Solve Perspective-n-Point to find head rotation
        success, rotation_vector, translation_vector = cv2.solvePnP(
            self.model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE
        )
        
        if not success:
            return "NORMAL"

        # Convert rotation vector to Euler angles (yaw, pitch, roll)
        rmat, _ = cv2.Rodrigues(rotation_vector)
        angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)
        
        pitch = angles[0] * 360 # Up/Down
        yaw = angles[1] * 360   # Left/Right
        
        # Use Euler angles to determine looking direction
        if yaw < -10:
            return "LOOKING_LEFT"
        elif yaw > 10:
            return "LOOKING_RIGHT"
        elif pitch < -10:
            return "LOOKING_DOWN"
        elif pitch > 15:
            return "LOOKING_UP"

        return "NORMAL"