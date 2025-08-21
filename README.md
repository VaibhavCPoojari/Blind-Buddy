# AI-Enhanced Smart Device for Assisting the Visually Challenged

This project presents the **design and implementation of a smart assistive device** that enhances autonomy and safety for visually challenged individuals. The device integrates **computer vision, ultrasonic sensing, and AI-powered speech feedback** to provide real-time navigation assistance, text recognition, and currency detection.  

Developed as an **interdisciplinary engineering project** at **RV College of Engineering®**, this system demonstrates the use of AI and embedded systems in improving accessibility and inclusivity.  

---

## 🚀 Features
- **Real-time Obstacle Detection & Navigation**  
  - Ultrasonic sensors + camera vision  
  - Reliable navigation in indoor/outdoor environments  

- **Currency Detection**  
  - Indian currency recognition using deep learning models  
  - Achieved mAP@50 of **93.4%** (Precision 90.8%, Recall 90.1%)  

- **Text Recognition**  
  - Optical Character Recognition (OCR) with **Tesseract + OpenCV**  
  - Reads public signboards and printed text  

- **Voice Feedback System**  
  - Text-to-Speech for natural and intuitive user interaction  
  - Eliminates dependency on visual displays  

---

## 🛠️ Tech Stack
- **Hardware:** Raspberry Pi 4B, Ultrasonic Sensors, Pi Camera Module  
- **Software & Libraries:**  
  - Python  
  - OpenCV (Image Processing)  
  - Tesseract OCR  
  - YOLOv10 (Object Detection)  
  - LLaMA/Groq Interface (Language Processing)  
  - Text-to-Speech (TTS)  

---

## 📐 System Design
The device follows a **multi-sensor, AI-assisted pipeline**:
1. **Ultrasonic sensors** detect nearby obstacles  
2. **Camera + YOLOv10** performs real-time object and currency detection  
3. **OCR** reads text from signboards  
4. **LLM integration** provides contextual navigation guidance  
5. **TTS engine** delivers audio feedback to the user  

---

## 📊 Results
- **Indian Currency Detection:** mAP@50 = **93.4%**  
- **Real-time Navigation Module:** Precision = **89.6%**, Recall = **88.2%**, Latency ≈ 2s  
- **User Testing:** High reliability and usability across indoor and outdoor environments  

---

## 🎯 Objectives
- Develop a **portable AI-powered assistive device**  
- Provide **real-time obstacle detection** for safe mobility  
- Enable **independent financial transactions** via currency recognition  
- Implement **OCR + TTS** for reading text aloud  
- Deliver **voice-based feedback** for intuitive interaction  

---

## 📦 Future Scope
- Reduce latency further for smoother real-time interaction  
- Expand object recognition (traffic signals, crosswalks, landmarks)  
- Enhance robustness in varied environmental conditions  
- Improve form factor for everyday usability  

---

## 👨‍💻 Contributors
- **M Barath** (1RV22ET023)  
- **Sreesha K R** (1RV22ET049)  
- **Shrivarsha** (1RV22CS195)  
- **K Keerthan Kini** (1RV22IS028)  
- **Vaibhav C Poojari** (1RV22ME119)  

Guided by **Prof. Sujata Priyambada Mishra**  
RV College of Engineering®, Department of ECE  

---

## 📄 License
This project is developed under **RV College of Engineering®**.  
All Intellectual Property Rights belong to the institution and authors.  
