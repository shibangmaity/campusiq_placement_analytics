"""
CampusIQ - Data Seeder (v3)
Loads the real CampusIQ dataset into a single Postgres `students` table.

Handles CSV variants that don't include Student_ID / Roll_No by generating
them automatically from row order, so the loader works whether or not those
two identifier columns are present in the source file.

Run: python database/seed_data.py
"""

import os
import pandas as pd
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()

CSV_PATH = os.environ.get(
    "DATASET_CSV_PATH",
    os.path.join(os.path.dirname(__file__), "CampusIQ_Final_Dataset_Presentation.csv"),
)

# ============================================
# DB CONNECTION
# ============================================
def get_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        database=os.environ.get("DB_NAME", "campusiq"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", ""),
        port=os.environ.get("DB_PORT", 5432),
    )


# ============================================
# HELPERS — the raw CSV packs status + company
# into one string ("Completed - IBM", "Placed - TCS").
# Split these out so they're queryable columns.
# ============================================
def split_status_company(value):
    """'Completed - IBM' -> ('Completed', 'IBM')   'Not Yet' -> ('Not Yet', None)"""
    if not isinstance(value, str) or " - " not in value:
        return (value, None)
    status, company = value.split(" - ", 1)
    return (status.strip(), company.strip())


def split_placement(value):
    """'Placed - TCS' -> (True, 'TCS')   'Not Placed' -> (False, None)"""
    if not isinstance(value, str):
        return (False, None)
    if value.strip() == "Not Placed":
        return (False, None)
    if value.startswith("Placed - "):
        return (True, value.split(" - ", 1)[1].strip())
    return (False, None)


CREATE_TABLE_SQL = """
DROP TABLE IF EXISTS students CASCADE;
CREATE TABLE students (
    student_id           INTEGER PRIMARY KEY,
    roll_no               INTEGER,
    student_name          TEXT,
    gender                TEXT,
    stream                TEXT,
    branch                TEXT,
    semester              INTEGER,
    tenth_percent         NUMERIC(5,2),
    tenth_board           TEXT,
    tenth_passout_year    INTEGER,
    twelfth_percent       NUMERIC(5,2),
    twelfth_education     TEXT,
    twelfth_passout_year  INTEGER,
    admission_year        INTEGER,
    cgpa                  NUMERIC(4,2),
    attendance_percent    NUMERIC(5,2),
    backlog               TEXT,
    top_certification     TEXT,
    internship_status     TEXT,
    internship_company    TEXT,
    projects_count        INTEGER,
    placed                BOOLEAN,
    placement_company     TEXT
);

CREATE INDEX idx_students_branch ON students(branch);
CREATE INDEX idx_students_semester ON students(semester);
CREATE INDEX idx_students_placed ON students(placed);
"""


def main():
    print(f"📄 Loading dataset from {CSV_PATH}")
    # utf-8-sig strips a BOM if present (harmless if there isn't one), and
    # stripping column names guards against stray whitespace from re-saves.
    df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")
    df.columns = df.columns.str.strip()
    print(f"   {len(df)} rows found")

    # Some dataset variants don't include Student_ID / Roll_No — generate
    # them from row order so the loader works either way.
    if "Student_ID" not in df.columns:
        print("   ⚠️  'Student_ID' not in CSV — generating sequential IDs (1..N)")
        df.insert(0, "Student_ID", range(1, len(df) + 1))
    if "Roll_No" not in df.columns:
        print("   ⚠️  'Roll_No' not in CSV — defaulting to Student_ID")
        df.insert(1, "Roll_No", df["Student_ID"])

    rows = []
    for _, r in df.iterrows():
        intern_status, intern_company = split_status_company(r["Internship_Status"])
        placed, placement_company = split_placement(r["Placement_Status"])
        rows.append((
            int(r["Student_ID"]),
            int(r["Roll_No"]),
            r["Student_Name"],
            r["Gender"],
            r["Stream"],
            r["Branch"],
            int(r["Semester"]),
            float(r["10th_%"]) if pd.notna(r["10th_%"]) else None,
            r["10th_Board"],
            int(r["10th_Passout_Year"]) if pd.notna(r["10th_Passout_Year"]) else None,
            float(r["12th_%"]) if pd.notna(r["12th_%"]) else None,
            r["12th_Education"] if pd.notna(r["12th_Education"]) else None,
            int(r["12th_Passout_Year"]) if pd.notna(r["12th_Passout_Year"]) else None,
            int(r["University_Admission_Year"]),
            float(r["CGPA"]),
            float(r["Attendance_%"]),
            r["Backlog"],
            r["Top_Certification"],
            intern_status,
            intern_company,
            int(r["Projects_Count"]),
            placed,
            placement_company,
        ))

    conn = get_connection()
    cur = conn.cursor()

    print("🗑️  Recreating students table...")
    cur.execute(CREATE_TABLE_SQL)
    conn.commit()

    print(f"🎓 Inserting {len(rows)} students...")
    psycopg2.extras.execute_values(
        cur,
        """
        INSERT INTO students (
            student_id, roll_no, student_name, gender, stream, branch, semester,
            tenth_percent, tenth_board, tenth_passout_year,
            twelfth_percent, twelfth_education, twelfth_passout_year,
            admission_year, cgpa, attendance_percent, backlog,
            top_certification, internship_status, internship_company,
            projects_count, placed, placement_company
        ) VALUES %s
        """,
        rows,
    )
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM students")
    count = cur.fetchone()[0]
    print(f"✅ Done. {count} students loaded into Postgres from the real dataset.")

    cur.close()
    conn.close()

    
if __name__ == "__main__":
    main()