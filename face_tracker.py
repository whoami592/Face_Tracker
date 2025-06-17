import cv2
import face_recognition
import numpy as np
import asyncio
import platform

# Banner text
BANNER_TEXT = "Coded by Pakistani Ethical Hacker Mr Sabaz Ali Khan"

async def main():
    # Initialize webcam (index 0 for default camera)
    cap = cv2.VideoCapture(0)
    
    # Check if webcam opened successfully
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    # Set frame rate
    FPS = 30
    
    while True:
        # Read frame from webcam
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame")
            break
        
        # Convert frame to RGB (face_recognition uses RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Find all face locations in the frame
        face_locations = face_recognition.face_locations(rgb_frame)
        
        # Draw rectangles around detected faces
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        
        # Create stylish banner
        banner_height = 50
        banner = np.zeros((banner_height, frame.shape[1], 3), dtype=np.uint8)
        banner[:] = (40, 40, 40)  # Dark gray background
        
        # Add text to banner
        font = cv2.FONT_HERSHEY_DUPLEX
        font_scale = 1
        font_color = (255, 255, 255)  # White text
        font_thickness = 2
        text_size = cv2.getTextSize(BANNER_TEXT, font, font_scale, font_thickness)[0]
        text_x = (frame.shape[1] - text_size[0]) // 2  # Center text
        text_y = (banner_height + text_size[1]) // 2
        cv2.putText(banner, BANNER_TEXT, (text_x, text_y), font, font_scale, font_color, font_thickness)
        
        # Combine banner with frame
        frame = np.vstack((frame, banner))
        
        # Display the frame (in a real environment, this would be shown in a window)
        # For Pyodide, we assume the output is handled by the environment
        cv2.imshow('Face Recognition Tracker', frame)
        
        # Control frame rate
        await asyncio.sleep(1.0 / FPS)
        
        # Break loop on 'q' key (for non-Pyodide environments)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())