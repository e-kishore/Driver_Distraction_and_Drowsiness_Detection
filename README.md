# Driver Distraction and Drowsiness Detection 🚗😴
### Real-Time Monitoring Using YOLO and Deep Learning

This project presents a real-time **Driver Distraction and Drowsiness Detection System** using **YOLO (You Only Look Once)** and **Deep Learning** techniques.  
The system continuously monitors driver behavior through a camera feed to detect distraction and fatigue, triggering alerts to prevent road accidents.

---

## 📌 Project Overview

Driver distraction and drowsiness are major causes of road accidents worldwide.  
This project aims to improve road safety by detecting unsafe driver behaviors such as:
- Mobile phone usage
- Eye closure and prolonged blinking
- Inattentive head movement
- Lack of focus while driving

The system uses **YOLO-based object detection** combined with facial and eye analysis to identify risky behavior in real time.

---

## 🎯 Objectives

- Detect driver distraction using object detection
- Identify drowsiness using eye and facial behavior analysis
- Provide real-time alerts to drivers and vehicle owners
- Reduce accident risks through early warning mechanisms
- Enable integration with Advanced Driver Assistance Systems (ADAS)

---

## 🧠 Technologies Used

- **Programming Language:** Python
- **Deep Learning Models:** YOLO (YOLOv5 / YOLOv8)
- **Libraries & Frameworks:**
  - OpenCV
  - TensorFlow / PyTorch
  - Ultralytics YOLO
  - NumPy
  - Flask (for web interface)
- **Database:** MySQL
- **IDE:** PyCharm / VS Code

---

## ⚙️ System Architecture

1. Camera captures real-time video feed  
2. YOLO detects driver face, eyes, and distraction objects  
3. Drowsiness detected using eye closure and blink analysis  
4. Distraction level calculated  
5. Alert system triggered based on severity  

---

## 📂 Dataset

- Custom dataset of driver images and videos
- Includes distracted and non-distracted scenarios
- Objects detected:
  - Mobile phone
  - Driver face
  - Eye state (open/closed)
- Data augmented for robustness

---

## 🔍 Methodology

### 1. Data Prep
