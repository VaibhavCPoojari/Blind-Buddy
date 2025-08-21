from picamera2 import Picamera2
import time
from inference_sdk import InferenceHTTPClient
 

 
client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key= os.getenv("ROBOFLOW_API_KEY")
)

picam2 = Picamera2()
config = picam2.create_still_configuration()
picam2.configure(config)
picam2.start()

 
try:
    while True:
        print("Capturing image...")
        image_path = "/tmp/image.jpg"
        picam2.capture_file(image_path)
        print(f"Captured image: {image_path}")

        
        result = client.run_workflow(
            workspace_name="shri-2krws",
            workflow_id="custom-workflow-3",
            images={"image": image_path},
            use_cache=True
        )

        
        print("Inference result:")
        print(result)

         
        time.sleep(5)

except KeyboardInterrupt:
    print("Stopped by user.")
    picam2.stop()
