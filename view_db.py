import sqlite3

def view_database():
    print("="*50)
    print("EXAMINATION PROCTORING DATABASE VIEWER")
    print("="*50 + "\n")
    
    try:
        conn = sqlite3.connect("proctoring.db")
        cursor = conn.cursor()
        
        # View Students
        print("--- STUDENTS TABLE ---")
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        if not students:
            print("No students found.")
        else:
            print(f"{'ID':<5} | {'Name':<20} | {'Student ID':<15}")
            print("-" * 45)
            for student in students:
                print(f"{student[0]:<5} | {student[1]:<20} | {student[2]:<15}")
        print("\n")
        
        # View Sessions
        print("--- SESSIONS TABLE ---")
        cursor.execute("SELECT * FROM sessions")
        sessions = cursor.fetchall()
        if not sessions:
            print("No sessions found.")
        else:
            print(f"{'ID':<5} | {'Student DB ID':<15} | {'Start Time':<20} | {'End Time':<20}")
            print("-" * 68)
            for session in sessions:
                end_time = session[3] if session[3] else "In Progress"
                print(f"{session[0]:<5} | {session[1]:<15} | {session[2]:<20} | {end_time:<20}")
        print("\n")
        
        # View Events
        print("--- EVENTS TABLE ---")
        cursor.execute("SELECT * FROM events")
        events = cursor.fetchall()
        if not events:
            print("No events found.")
        else:
            print(f"{'ID':<5} | {'Session ID':<10} | {'Timestamp':<20} | {'Type':<15} | {'Description':<30} | {'Evidence'}")
            print("-" * 105)
            for event in events:
                evidence = event[5] if event[5] else "None"
                # Truncate description if too long
                desc = event[4]
                if len(desc) > 28:
                    desc = desc[:25] + "..."
                print(f"{event[0]:<5} | {event[1]:<10} | {event[2]:<20} | {event[3]:<15} | {desc:<30} | {evidence}")
        print("\n")
                
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    view_database()
