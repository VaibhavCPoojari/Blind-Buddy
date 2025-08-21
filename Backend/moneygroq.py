import cv2
import time
import base64
from groq import Groq

# Initialize webcam
cap = cv2.VideoCapture(0)

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def image_to_data_url(image_path):
    """Convert image to base64 data URL for Groq API."""
    with open(image_path, "rb") as img_file:
        b64_image = base64.b64encode(img_file.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{b64_image}"

try:
    print("Press Ctrl+C to stop.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            continue

        # Save current frame to file
        image_path = "current_currency.jpg"
        cv2.imwrite(image_path, frame)

        # Convert to base64 data URL
        image_data_url = image_to_data_url(image_path)

        # Send to Groq
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
                            "image_url": {"url": image_data_url}
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

        # Print formatted response
        print("Groq API response:")
        print(completion.choices[0].message.content)

        # Wait for 2 seconds
        time.sleep(2)

except KeyboardInterrupt:
    print("Stopped by user.")

finally:
    cap.release()
    cv2.destroyAllWindows()
