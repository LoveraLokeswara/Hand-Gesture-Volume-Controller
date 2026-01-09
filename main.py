import cv2
import mediapipe as mp
import numpy as np
import math
import platform
import subprocess

class HandGestureVolumeController:
    def __init__(self):
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Volume range
        self.min_vol = 0
        self.max_vol = 100
        self.vol = 0
        self.vol_bar = 400
        self.vol_percentage = 0
        
        # Get system platform
        self.system = platform.system()
        
    def get_distance(self, p1, p2):
        """Calculate Euclidean distance between two points"""
        return math.hypot(p2[0] - p1[0], p2[1] - p1[1])
    
    def set_volume(self, volume):
        """Set system volume based on platform"""
        volume = max(0, min(100, volume))  # Clamp between 0-100
        
        if self.system == "Darwin":  # macOS
            subprocess.run(['osascript', '-e', f'set volume output volume {volume}'])
        elif self.system == "Windows":
            # For Windows, using pycaw library
            try:
                from ctypes import cast, POINTER
                from comtypes import CLSCTX_ALL
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume_interface = cast(interface, POINTER(IAudioEndpointVolume))
                volume_interface.SetMasterVolumeLevelScalar(volume / 100, None)
            except Exception as e:
                print(f"Error setting volume on Windows: {e}")
        elif self.system == "Linux":
            subprocess.run(['amixer', '-D', 'pulse', 'sset', 'Master', f'{volume}%'])
    
    def draw_ui(self, img, length, vol_percentage):
        """Draw UI elements on the frame"""
        h, w, c = img.shape
        
        # Draw volume bar
        cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
        vol_bar = np.interp(length, [30, 200], [400, 150])
        cv2.rectangle(img, (50, int(vol_bar)), (85, 400), (0, 255, 0), cv2.FILLED)
        
        # Draw volume percentage
        cv2.putText(img, f'{int(vol_percentage)}%', (40, 450), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
        
        # Draw instructions
        cv2.putText(img, "Pinch to Control Volume", (w - 400, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(img, "Press 'q' to quit", (w - 400, 80), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        return img
    
    def run(self):
        """Main loop for hand gesture volume control"""
        cap = cv2.VideoCapture(0)
        cap.set(3, 1280)  # Width
        cap.set(4, 720)   # Height
        
        print("Hand Gesture Volume Controller Started!")
        print("Instructions:")
        print("- Show your hand to the camera")
        print("- Pinch thumb and index finger together to decrease volume")
        print("- Move them apart to increase volume")
        print("- Press 'q' to quit")
        
        while True:
            success, img = cap.read()
            if not success:
                print("Failed to read from camera")
                break
            
            # Flip image for mirror effect
            img = cv2.flip(img, 1)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Process the image and detect hands
            results = self.hands.process(img_rgb)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw hand landmarks
                    self.mp_draw.draw_landmarks(
                        img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                    )
                    
                    # Get landmark positions
                    lm_list = []
                    for id, lm in enumerate(hand_landmarks.landmark):
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        lm_list.append([id, cx, cy])
                    
                    if len(lm_list) >= 21:
                        # Get thumb tip (4) and index finger tip (8)
                        thumb_tip = lm_list[4][1:]
                        index_tip = lm_list[8][1:]
                        
                        # Draw circles on thumb and index finger tips
                        cv2.circle(img, tuple(thumb_tip), 15, (255, 0, 255), cv2.FILLED)
                        cv2.circle(img, tuple(index_tip), 15, (255, 0, 255), cv2.FILLED)
                        
                        # Draw line between thumb and index finger
                        cv2.line(img, tuple(thumb_tip), tuple(index_tip), (255, 0, 255), 3)
                        
                        # Calculate midpoint
                        mid_x = (thumb_tip[0] + index_tip[0]) // 2
                        mid_y = (thumb_tip[1] + index_tip[1]) // 2
                        cv2.circle(img, (mid_x, mid_y), 10, (0, 255, 0), cv2.FILLED)
                        
                        # Calculate distance between thumb and index finger
                        length = self.get_distance(thumb_tip, index_tip)
                        
                        # Convert distance to volume (30-200 pixels -> 0-100%)
                        vol_percentage = np.interp(length, [30, 200], [0, 100])
                        
                        # Set system volume
                        self.set_volume(vol_percentage)
                        
                        # Visual feedback when fingers are very close
                        if length < 40:
                            cv2.circle(img, (mid_x, mid_y), 10, (0, 0, 255), cv2.FILLED)
                        
                        # Draw UI
                        img = self.draw_ui(img, length, vol_percentage)
            else:
                # No hand detected message
                h, w, c = img.shape
                cv2.putText(img, "No hand detected", (w // 2 - 150, h // 2), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            # Display FPS
            cv2.putText(img, "Hand Gesture Volume Control", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
            
            # Show the image
            cv2.imshow("Hand Gesture Volume Controller", img)
            
            # Break loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        self.hands.close()
        print("Application closed successfully!")

if __name__ == "__main__":
    controller = HandGestureVolumeController()
    controller.run()

