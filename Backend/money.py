from picamera2 import Picamera2
import cv2
from roboflow import Roboflow
import os
 
picam2 = Picamera2()
 
picam2.configure(picam2.create_video_configuration())
 
picam2.start()
 
rf = Roboflow(api_key=os.getenv("ROBOFLOW_API_KEY"))
 
workspace = rf.workspace("Shri")
project = workspace.project("indian-currency-detection-elfyf-mwqmr")
model = project.version(1).model

 
cv2.namedWindow("Money identification", cv2.WINDOW_NORMAL)
while True:
     
    frame = picam2.capture_array()
    
    if frame is not None:
         
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
         
        predictions = model.predict(frame_bgr, confidence=40, overlap=30).json()
         
        print(predictions)
         
        for prediction in predictions["predictions"]:
            print(prediction)  
            
             
            if "x" in prediction and "y" in prediction and "width" in prediction and "height" in prediction:
                x1, y1 = prediction["x"], prediction["y"]
                width, height = prediction["width"], prediction["height"]
                x2, y2 = x1 + width, y1 + height
            else:
                
                x1, y1, x2, y2 = prediction["xmin"], prediction["ymin"], prediction["xmax"], prediction["ymax"]
             
            print(f"Bounding Box: x1={x1}, y1={y1}, x2={x2}, y2={y2}")
            
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            label = prediction["class"]
            confidence = prediction["confidence"]
            
            cv2.rectangle(frame_bgr, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame_bgr, f"{label} ({confidence*100:.2f}%)", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        cv2.imshow("Webcam Feed--- Money", frame_bgr)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
picam2.stop()
cv2.destroyAllWindows()