import cv2
import time
from inference_sdk import InferenceHTTPClient
 
cap = cv2.VideoCapture(0)

 
client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key= os.getenv("ROBOFLOW_API_KEY")   
)

try:
    print("Press Ctrl+C to stop.")
    while True:
        # Capture frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Save frame to file
        image_path = "temp_capture.jpg"
        cv2.imwrite(image_path, frame)

        # Send image to Roboflow workflow
        result = client.run_workflow(
            workspace_name="shri-2krws",
            workflow_id="custom-workflow-3",
            images={"image": image_path},
            use_cache=True
        )

        # Print result
        print("Inference result:")
        print(result)

        # Wait 2 seconds
        time.sleep(2)

except KeyboardInterrupt:
    print("Stopping capture...")

finally:
    cap.release()
    cv2.destroyAllWindows()
