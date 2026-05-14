from database import Database

class SessionManager:
    def __init__(self):
        self.db = Database()
        self.current_session_id = None
        self.student_name = None
        self.student_id = None

    def start_session(self, name, student_id):
        """Registers the student and starts a new examination session."""
        self.student_name = name
        self.student_id = student_id
        
        internal_id = self.db.register_student(name, student_id)
        self.current_session_id = self.db.create_session(internal_id)
        
        print(f"[SESSION START] {name} (ID: {student_id}). Session ID: {self.current_session_id}")
        return self.current_session_id

    def end_session(self):
        """Ends the current examination session."""
        if self.current_session_id:
            self.db.end_session(self.current_session_id)
            print(f"[SESSION END] Session {self.current_session_id} ended.")
            
    def log_violation(self, event_type, description, evidence_path=None):
        """Logs a violation event to the active session."""
        if self.current_session_id:
            self.db.log_event(self.current_session_id, event_type, description, evidence_path)
            print(f"[VIOLATION LOGGED] {event_type} - {description}")
