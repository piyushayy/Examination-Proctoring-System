# pyrefly: ignore [missing-import]
import numpy as np
import threading
from config import Config

try:
    import pyaudio
except ImportError:
    pyaudio = None
    print("Warning: pyaudio not installed. Audio monitoring will be disabled. Install with: pip install pyaudio")

class AudioMonitor:
    def __init__(self):
        self.is_running = False
        self.audio = None
        self.stream = None
        self.suspicious_noise_detected = False
        self.thread = None

    def start(self):
        """Starts the background audio monitoring thread."""
        if pyaudio is None:
            return
            
        self.audio = pyaudio.PyAudio()
        try:
            self.stream = self.audio.open(
                format=Config.AUDIO_FORMAT,
                channels=Config.AUDIO_CHANNELS,
                rate=Config.AUDIO_RATE,
                input=True,
                frames_per_buffer=Config.AUDIO_CHUNK
            )
            self.is_running = True
            self.thread = threading.Thread(target=self._monitor_loop)
            self.thread.daemon = True
            self.thread.start()
            print("[AUDIO] Background audio monitoring started.")
        except Exception as e:
            print(f"[AUDIO ERROR] Failed to start audio stream: {e}")

    def _monitor_loop(self):
        """Continuous loop running in a thread to check volume levels."""
        while self.is_running:
            try:
                data = np.frombuffer(self.stream.read(Config.AUDIO_CHUNK, exception_on_overflow=False), dtype=np.int16)
                # Calculate the volume as root mean square
                volume = np.linalg.norm(data) / len(data)
                
                if volume > Config.AUDIO_THRESHOLD:
                    self.suspicious_noise_detected = True
            except Exception as e:
                pass

    def check_noise(self):
        """Returns True if a noise threshold violation occurred since last check."""
        if self.suspicious_noise_detected:
            self.suspicious_noise_detected = False
            return True
        return False

    def stop(self):
        """Stops the audio monitor gracefully."""
        self.is_running = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.audio:
            self.audio.terminate()
        print("[AUDIO] Audio monitoring stopped.")
