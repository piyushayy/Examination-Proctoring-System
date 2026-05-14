import time

class CheatScorer:
    def __init__(self):
        self.score = 0.0
        self.last_update = time.time()
        self.high_risk_start_time = None # Tracks when we entered the HIGH zone
        
        self.rates = {
            "NO_FACE": 5.0, "MULTIPLE_FACES": 15.0, "LOOKING_LEFT": 3.0,
            "LOOKING_RIGHT": 3.0, "NORMAL": -1.5, "LOOKING_DOWN": 3.0,
            "LOOKING_UP": 2.0
        }

    def update(self, state):
        now = time.time()
        dt = now - self.last_update
        self.last_update = now

        # Standard score update
        change = self.rates.get(state, 0) * dt
        self.score = max(0, self.score + change)

        # Monitor HIGH risk duration
        if self.score >= 25: # Threshold for HIGH
            if self.high_risk_start_time is None:
                self.high_risk_start_time = now
        else:
            self.high_risk_start_time = None

    def get_high_risk_duration(self):
        if self.high_risk_start_time:
            return time.time() - self.high_risk_start_time
        return 0

    def trigger_violation(self, penalty=30):
        self.score += penalty

    def risk_level(self):
        if self.score < 10: return "LOW", "#4CAF50"
        if self.score < 25: return "MEDIUM", "#FFC107"
        return "HIGH", "#F44336"