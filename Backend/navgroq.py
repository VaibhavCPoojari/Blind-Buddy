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
                                """ You are a real-time navigation assistant guiding a visually impaired person through outdoor environments. The person wears a camera that continuously captures images of their surroundings.

Each incoming image has bounding boxes and labels already drawn on detected objects — including but not limited to: person, vehicle, bike, pothole, stair, pole, wall, tree, door, barrier, etc.

Your task is to analyze the entire scene holistically and provide:

✅ One clear, safe, adaptive navigation instruction in plain text (single sentence, suitable for converting to speech)
✅ One clear reason explaining why this instruction is necessary (single sentence, plain text)

Instructions you provide must follow these rules:
Evaluate all detected objects: their positions (left, center, right), sizes, and proximity to the user.

Understand scene layout: is the area open, narrow, crowded, or partially blocked? Is there space to walk forward safely?

Detect hazards: vehicles moving or too close, potholes or uneven terrain ahead, objects blocking the path, stairs or ledges, narrow clearances, people or bikes crossing, confusing or busy areas.

Provide relative, context-aware instructions — do not assume fixed distances or count steps (e.g., avoid “walk 5 steps forward”). Use flexible, adaptive language like:

“Walk forward carefully” (if open and clear)

“Proceed slowly” (if partially open with some caution)

“Move slightly left” or “Take one step to the right” (if needing small adjustments)

“Stop and wait” (if hazard is near or imminent)

“Stand still and wait” (if something is approaching or crossing)

Always prioritize safety over speed — if there’s any uncertainty or danger, instruct to stop or wait.

Avoid unnecessary details, numbers, or over-explanation — provide only what is needed in that moment.

Output format:
Return two lines only (plain text, no extra explanation or headers):

Instruction: (one sentence, clear, adaptive, actionable)

Reason: (one sentence, why this instruction is necessary)

Example outputs:
Instruction: Stop and wait.
Reason: A pothole is just ahead in front of you.

Instruction: Move slightly left and proceed slowly.
Reason: A bike is on your right side.

Instruction: Walk forward carefully.
Reason: The path in front is open and clear.

Instruction: Take one step to the right and wait.
Reason: To adjust away from a wall on your left.

Instruction: Stand still and wait.
Reason: A vehicle is approaching from your left.

Additional Clarifications for the Model:
Carefully interpret depth and spacing: how much free space exists?

Resolve crowded or busy scenes by favoring conservative, safe instructions.

Adapt to moving hazards: predict risk based on their motion and direction.

Never skip hazards just because there’s a partial opening — always account for both static and dynamic risks.

Response Should follow this json structure:

  {
        instruction:<instruction based on analysis of the scene>,
        reason:<reason for the instruction>
  }

"""


   
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