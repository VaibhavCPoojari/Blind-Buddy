import time
import base64
from groq import Groq
from picamera2 import Picamera2

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Initialize Picamera2
picam2 = Picamera2()
config = picam2.create_still_configuration()
picam2.configure(config)
picam2.start()

def image_to_data_url(image_path):
    """Convert image to base64 data URL for Groq image_url format."""
    with open(image_path, "rb") as img_file:
        b64_image = base64.b64encode(img_file.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{b64_image}"

try:
    while True:
        image_path = "/tmp/image.jpg"
        
        # Capture image from PiCamera
        picam2.capture_file(image_path)
        print(f"Captured image: {image_path}")

        # Convert to base64 data URL
        image_data_url = image_to_data_url(image_path)

        # Run Groq inference
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "recognise the indian currency given and tell what is its denomination\n"
                                "you must give json in the form {\n"
                                "\"currency\": \"It is <currency_detected> rupees\"\n"
                                "}\n"
                                "strictly follow the json format given"
                            )
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_data_url
                            }
                        }
                    ]
                }
            ],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=False,
            response_format={"type": "json_object"},
            stop=None,
        )

        # Print result
        print("Groq Inference Result:")
        print(completion.choices[0].message.content)

        # Wait 2 seconds before next capture
        time.sleep(2)

except KeyboardInterrupt:
    print("Stopped by user.")
    picam2.stop()