import os
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai
 


import subprocess
import platform
import os
 
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

 
genai.configure(api_key=api_key)

 
model = genai.GenerativeModel('gemini-2.0-flash')

 
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

 
image_path = "footpat2.jpeg"   

 
image = Image.open(image_path)

 
response = model.generate_content([user_prompt, image])

response_text = response.text
print(response_text)


 
 


 
def speak_text(text, voice="en", speed=150, pitch=50, volume=750,pause_length=0.95):
    
    os.environ["PATH"] += r";C:\Program Files (x86)\eSpeak\command_line"
    
    exe = "espeak" if platform.system() == "Windows" else "espeak-ng"
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
    
    os.environ["PATH"] += r";C:\Program Files (x86)\eSpeak\command_line"
    
    exe = "espeak" if platform.system() == "Windows" else "espeak-ng"
    subprocess.run([
        exe,
        f"-v{voice}",
        f"-s{speed}",
        f"-p{pitch}",
        f"-a{volume}",
        "-w", filename,
        text
    ])
    print(f"Saved to {filename}")




speak_text(response_text)
save_to_wav(response_text, filename="output.wav")


 

 

 