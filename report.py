import json
import os
from config import Config
from database import Database

class ReportGenerator:
    def __init__(self):
        self.db = Database()

    def generate_json_report(self, session_id, student_name, student_id):
        """Generates a structured JSON report of all violations in a session."""
        events = self.db.get_session_events(session_id)
        
        report_data = {
            "session_id": session_id,
            "student_name": student_name,
            "student_id": student_id,
            "total_violations": len(events),
            "events": []
        }
        
        for event in events:
            report_data["events"].append({
                "timestamp": event[0],
                "type": event[1],
                "description": event[2],
                "evidence_path": event[3]
            })
            
        filepath = os.path.join(Config.REPORTS_DIR, f"report_{student_id}_session_{session_id}.json")
        
        with open(filepath, 'w') as f:
            json.dump(report_data, f, indent=4)
            
        print(f"[REPORT] JSON Report generated at: {filepath}")
        return filepath
