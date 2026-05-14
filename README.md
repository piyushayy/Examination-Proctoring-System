## Examination Proctoring System

A desktop-based AI proctoring application that monitors examinee behavior in real time using **face presence and eye movement analysis**. The system assigns a **time-aware cheating score**, classifies risk levels, and **automatically captures screenshots** when suspicious behavior persists.

Built with a focus on fairness, explainability, and real-world usability.

---

## 🚀 Features

- Real-time webcam monitoring
- Face detection and eye movement tracking
- Time-based cheating score (reduces false positives)
- Risk classification: Low / Medium / High
- Automatic screenshot capture on suspicious behavior
- Native desktop application (no browser required)

---

## 🧠 How It Works

1. Captures live video feed using OpenCV  
2. Detects face and eye landmarks using MediaPipe  
3. Analyzes gaze direction and face presence over time  
4. Increases cheating score only if behavior persists  
5. Captures screenshots when high-risk behavior is detected  

Short, natural movements are ignored to avoid unfair penalties.

---

## 🛠 Tech Stack

- Python 3.10
- OpenCV
- MediaPipe
- PySide6 (Desktop UI)
- NumPy

---
