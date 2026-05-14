import sys
import cv2
import os
import time
from datetime import datetime
# pyrefly: ignore [missing-import]
from PySide6.QtWidgets import QApplication, QInputDialog
# pyrefly: ignore [missing-import]
from PySide6.QtCore import QTimer
from ui import MainUI
from detector import Detector
from scoring import CheatScorer

# New imports for production system
from config import Config
from session import SessionManager
from audio_monitor import AudioMonitor
from report import ReportGenerator

def main():
    Config.setup_dirs()

    app = QApplication(sys.argv)
    window = MainUI()
    
    # Get Student Info
    name, ok1 = QInputDialog.getText(None, "Registration", "Enter Student Name:")
    if not ok1 or not name: name = "Unknown"
    
    student_id, ok2 = QInputDialog.getText(None, "Registration", "Enter Student ID:")
    if not ok2 or not student_id: student_id = "0000"

    window.show()

    # Initialize Modules
    session_manager = SessionManager()
    session_id = session_manager.start_session(name, student_id)

    audio_monitor = AudioMonitor()
    audio_monitor.start()

    cap = cv2.VideoCapture(0)
    detector = Detector()
    scorer = CheatScorer()
    
    last_screenshot_time = 0

    def update():
        nonlocal last_screenshot_time
        ret, frame = cap.read()
        if not ret: return

        state = detector.detect_behavior(frame)
        scorer.update(state)
        
        # Audio check
        if audio_monitor.check_noise():
            scorer.trigger_violation(penalty=10)
            session_manager.log_violation("AUDIO_ALERT", "Loud noise detected")
            
        risk_text, risk_color = scorer.risk_level()
        
        # SCREENSHOT LOGIC: If HIGH for > 10 seconds
        duration = scorer.get_high_risk_duration()
        if duration > 10:
            now = time.time()
            # Only save one image every 5 seconds of sustained high risk
            if now - last_screenshot_time > 5:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{Config.EVIDENCE_DIR}/violation_{timestamp}.jpg"
                
                # Add a red border to the saved evidence image
                cv2.rectangle(frame, (0,0), (frame.shape[1], frame.shape[0]), (0,0,255), 20)
                cv2.imwrite(filename, frame)
                
                print(f"EVIDENCE SAVED: {filename}")
                session_manager.log_violation("HIGH_RISK_SUSTAINED", f"State: {state}", filename)
                last_screenshot_time = now

        # Update UI
        window.status.setText(f"Status: {state}")
        window.score.setText(f"Score: {round(scorer.score, 1)}")
        window.risk.setText(f"Risk: {risk_text}")
        window.risk.setStyleSheet(f"color: {risk_color}; font-size: 18px; font-weight: bold;")
        window.update_frame(frame)

    timer = QTimer()
    timer.timeout.connect(update)
    timer.start(30)
    
    # Run application blockingly
    app.exec()

    # --- Teardown & Reporting ---
    print("\n--- Ending Session ---")
    audio_monitor.stop()
    session_manager.end_session()
    cap.release()
    cv2.destroyAllWindows()
    
    report_gen = ReportGenerator()
    report_gen.generate_json_report(session_id, name, student_id)

if __name__ == "__main__":
    main()