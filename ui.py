from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt

class MainUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sentinel AI Proctor")
        self.setFixedSize(900, 700)
        self.setStyleSheet("background-color: #121212; color: white; font-family: Arial;")

        layout = QVBoxLayout(self)

        # Video feed
        self.video = QLabel()
        self.video.setStyleSheet("border: 2px solid #333; border-radius: 10px; background: black;")
        self.video.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.video)

        # Bottom Bar
        info_layout = QHBoxLayout()
        
        self.status = self.create_stat_label("Status: NORMAL")
        self.score = self.create_stat_label("Score: 0.0")
        self.risk = self.create_stat_label("Risk: LOW")

        info_layout.addWidget(self.status)
        info_layout.addWidget(self.score)
        info_layout.addWidget(self.risk)
        layout.addLayout(info_layout)

    def create_stat_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px; background: #1E1E1E; border-radius: 5px;")
        return label

    def update_frame(self, frame):
        h, w, ch = frame.shape
        img = QImage(frame.data, w, h, ch * w, QImage.Format_BGR888)
        self.video.setPixmap(QPixmap.fromImage(img).scaled(860, 540, Qt.KeepAspectRatio))