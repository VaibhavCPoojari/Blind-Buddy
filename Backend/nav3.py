from picamera2 import Picamera2
import cv2
import numpy as np
import requests
import time

api_url = "https://detect.roboflow.com/custom-workflow-2"
api_key = os.getenv("ROBOFLOW_API_KEY")

picam2 = Picamera2()
picam2.start()
time.sleep(2)  # Camera warm-up

while True:
    # Capture frame as OpenCV image (numpy array)
    frame = picam2.capture_array()

    # Encode frame as JPEG
    retval, buffer = cv2.imencode('.jpg', frame)
    if not retval:
        continue

    # Send frame to Roboflow Workflow
    response = requests.post(
        api_url,
        files={"image": buffer.tobytes()},
        params={"api_key": api_key}
    )
    result = response.json()

    # Print or handle the output (your workflow returns 'gemini_instruction')
    print(result.get("gemini_instruction", "No instruction"))
    
    # Display the frame (press 'q' to quit)
    cv2.imshow("Picamera2 Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

picam2.close()
cv2.destroyAllWindows()