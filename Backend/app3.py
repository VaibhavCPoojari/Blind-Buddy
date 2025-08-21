import os
import time
from picamera2 import Picamera2
from PIL import Image
import google.generativeai as genai
import subprocess
import platform
 
 
api_key =  os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

 
folder_path = "/home/pi/Desktop/x"
os.makedirs(folder_path, exist_ok=True)

 
capture_interval = 5  # seconds
total_duration = 120  # seconds
end_time = time.time() + total_duration

# Voice feedback settings
def speak_text(text, voice="en", speed=150, pitch=50, volume=750, pause_length=0.95):
    exe = "espeak" if platform.system() == "Linux" else "espeak-ng"
    subprocess.run([
        exe,
        f"-v{voice}",
        f"-s{speed}",
        f"-p{pitch}",
        f"-a{volume}",
        f"-g{pause_length}",
        text
    ])

def save_to_wav(text, filename="output.wav", voice="en", speed=150, pitch=86, volume=750):
    exe = "espeak" if platform.system() == "Linux" else "espeak-ng"
    subprocess.run([
        exe,
        f"-v{voice}",
        f"-s{speed}",
        f"-p{pitch}",
        f"-a{volume}",
        "-w", filename,
        text
    ])
 
user_prompt = """
You are a real-time navigation assistant guiding a visually impaired person outdoors using images from smart glasses. Your task is to analyze the image and provide **clear, safe movement instructions** based on the visible surroundings.

Instructions:
1. Identify obstacles: poles, vehicles, people, animals, pits, ditches, stairs, walls, etc.
2. Detect hazards: rivers, drains, open construction zones, traffic, drop-offs.
3. Evaluate safe walkable space—left, right, forward.
4. If there is no safe path, instruct to stop and seek help.
5. Use simple, spoken phrases for audio feedback. Avoid visual or technical terms.

Examples:
- “Stop. Obstacle ahead.”
- “Pole in front. Move slightly left and go forward.”
- “Danger: river on the right. Stay left.”
- “Vehicle ahead. Wait or turn back.”
- “Footpath clear. Walk forward slowly.”
- “Edge on the left. Keep to the right.”
"""

 

 
camera = Picamera2()
camera.start()

while time.time() < end_time:
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    image_path = os.path.join(folder_path, f"image_{timestamp}.jpg")
 
    camera.capture_file(image_path)
    print(f"Captured: {image_path}")

    try:
         
        image = Image.open(image_path)
        response = model.generate_content([user_prompt, image])
        response_text = response.text.strip()
        print("Gemini Response:", response_text)

        
        speak_text(response_text)
        audio_filename = os.path.join(folder_path, f"response_{timestamp}.wav")
        save_to_wav(response_text, filename=audio_filename)

    except Exception as e:
        print(f"Error processing image {image_path}: {e}")

    time.sleep(capture_interval)

camera.stop()
print("Done capturing and processing images.")
