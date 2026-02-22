import sqlite3
from datetime import datetime, timezone

DATABASE = "tickets_enhanced.db"

def db():
    return sqlite3.connect(DATABASE)

def initialize_schema():
    with db() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            severity TEXT NOT NULL CHECK(severity IN ('Low','Medium','High','Critical')),
            resolution_minutes INTEGER NOT NULL CHECK(resolution_minutes >= 0),
            resolved INTEGER NOT NULL CHECK(resolved IN (0, 1)),
            created_on TEXT NOT NULL
        )
        """)

        conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_category_severity
        ON tickets(category, severity)
        """)

def log_ticket(category, severity, resolution_minutes, resolved=True):
    category = (category or "").strip()
    if not category:
        raise ValueError("Category cannot be blank")

    allowed = {"Low", "Medium", "High", "Critical"}
    if severity not in allowed:
        raise ValueError("Severity must be Low/Medium/High/Critical")

    if resolution_minutes < 0:
        raise ValueError("Resolution minutes must be >= 0")

    with db() as conn:
        conn.execute("""
        INSERT INTO tickets(category, severity, resolution_minutes, resolved, created_on)
        VALUES (?, ?, ?, ?, ?)
        """, (
            category,
            severity,
            int(resolution_minutes),
            1 if resolved else 0,
            datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00","Z")
        ))

def list_open_tickets():
    with db() as conn:
        rows = conn.execute("""
        SELECT ticket_id, category, severity, resolution_minutes, created_on
        FROM tickets
        WHERE resolved = 0
        ORDER BY created_on DESC
        """).fetchall()

    print("\nOpen Tickets:")
    if not rows:
        print("(none)")
    for r in rows:
        print(r)

def resolution_stats():
    with db() as conn:
        rows = conn.execute("""
        SELECT category,
               COUNT(*) AS total,
               ROUND(AVG(resolution_minutes), 1) AS avg_minutes
        FROM tickets
        GROUP BY category
        ORDER BY avg_minutes DESC
        """).fetchall()

    print("\nResolution Stats (by category):")
    for r in rows:
        print(r)

def severity_distribution():
    with db() as conn:
        rows = conn.execute("""
        SELECT severity, COUNT(*) AS count
        FROM tickets
        GROUP BY severity
        ORDER BY count DESC
        """).fetchall()

    print("\nSeverity Distribution:")
    for r in rows:
        print(r)

if __name__ == "__main__":
    initialize_schema()

    log_ticket("Network", "High", 45, True)
    log_ticket("Account Access", "Medium", 20, True)
    log_ticket("Printer", "Low", 15, False)
    log_ticket("VPN", "Critical", 90, True)

    list_open_tickets()
    resolution_stats()
    severity_distribution()

