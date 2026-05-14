import os

class Config:
    # Database
    DB_NAME = "proctoring.db"
    
    # Directories
    EVIDENCE_DIR = "evidence"
    REPORTS_DIR = "reports"
    
    # Audio Thresholds (PyAudio)
    AUDIO_CHUNK = 1024
    AUDIO_FORMAT = 8 # pyaudio.paInt16
    AUDIO_CHANNELS = 1
    AUDIO_RATE = 44100
    AUDIO_THRESHOLD = 800 # Adjust based on microphone sensitivity

    @classmethod
    def setup_dirs(cls):
        """Creates necessary directories if they don't exist."""
        os.makedirs(cls.EVIDENCE_DIR, exist_ok=True)
        os.makedirs(cls.REPORTS_DIR, exist_ok=True)
