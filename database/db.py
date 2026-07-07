import os
import psycopg2
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# --------------------------------------------------
# Dataset Path
# --------------------------------------------------
CSV_PATH = os.environ.get(
    "DATASET_CSV_PATH",
    os.path.join(
        os.path.dirname(__file__),
        "CampusIQ_Final_Dataset_Presentation.csv"
    ),
)

# --------------------------------------------------
# Column normalization
# --------------------------------------------------
# The source CSV / Postgres table uses TitleCase / mixed headers
# (e.g. "Attendance_%", "Branch", "Placement_Status"). All page code
# in this app is written against lower_snake_case names. Normalize
# once here so every page can rely on a consistent schema.
COLUMN_RENAME_MAP = {
    "Student_ID": "student_id",
    "Roll_No": "roll_no",
    "Student_Name": "name",
    "Gender": "gender",
    "Stream": "stream",
    "Branch": "branch",
    "Semester": "semester",
    "10th_%": "tenth_percent",
    "10th_Board": "tenth_board",
    "10th_Passout_Year": "tenth_passout_year",
    "12th_%": "twelfth_percent",
    "12th_Education": "twelfth_education",
    "12th_Passout_Year": "twelfth_passout_year",
    "University_Admission_Year": "university_admission_year",
    "CGPA": "cgpa",
    "Attendance_%": "attendance_percent",
    "Backlog": "backlog",
    "Top_Certification": "top_certification",
    "Internship_Status": "internship_status",
    "Projects_Count": "projects_count",
    "Placement_Status": "placement_status",
}


def normalize_students_df(df: pd.DataFrame) -> pd.DataFrame:
    """Rename raw source columns to the lower_snake_case names the
    rest of the app expects, and derive a boolean `placed` column
    from `placement_status` (there is no separate boolean column
    in the source data).
    """
    df = df.rename(columns=COLUMN_RENAME_MAP)

    if "placement_status" in df.columns:
        df["placement_status"] = df["placement_status"].fillna("").astype(str).str.strip()

        # Real values look like "Placed - Accenture" or "Not Placed" —
        # not a plain "Placed"/"Not Placed" flag. Derive both a boolean
        # and the company name from this single field.
        df["placed"] = df["placement_status"].str.lower().str.startswith("placed -")
        df["placement_company"] = (
            df["placement_status"]
            .str.split(" - ", n=1)
            .str[1]
            .fillna("")
            .str.strip()
        )

    if "internship_status" in df.columns:
        df["internship_status"] = df["internship_status"].fillna("").astype(str).str.strip()

        # Same compound-string issue as placement: real values look like
        # "Completed - IBM" or "Ongoing - Amazon", not a bare status. Split
        # into a clean status ("Completed"/"Ongoing"/"Not Yet") and company,
        # so anything doing internship_status.map({"Completed": ..., ...})
        # actually matches instead of silently falling through to a default.
        df["internship_company"] = (
            df["internship_status"]
            .str.split(" - ", n=1)
            .str[1]
            .fillna("")
            .str.strip()
        )
        df["internship_status"] = (
            df["internship_status"]
            .str.split(" - ", n=1)
            .str[0]
            .str.strip()
        )

    return df


# --------------------------------------------------
# PostgreSQL Connection
# --------------------------------------------------
def get_connection():
    """Create PostgreSQL connection."""
    try:
        return psycopg2.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            database=os.environ.get("DB_NAME", "campusiq"),
            user=os.environ.get("DB_USER", "postgres"),
            password=os.environ.get("DB_PASSWORD", ""),
            port=os.environ.get("DB_PORT", 5432),
        )
    except Exception as e:
        try:
            st.error(f"Database connection failed: {e}")
        except Exception:
            pass
        return None


# --------------------------------------------------
# Execute SQL
# --------------------------------------------------
def run_query(sql: str) -> pd.DataFrame:
    """Execute SQL on PostgreSQL and return DataFrame.

    If the query targets the `students` table, the result columns
    are normalized to the lower_snake_case names the app expects.
    """

    conn = get_connection()

    if conn is None:
        raise Exception(
            "Database connection failed. Check your .env configuration."
        )

    try:
        df = pd.read_sql_query(sql, conn)
        conn.close()

        if "students" in sql.lower():
            df = normalize_students_df(df)

        return df

    except Exception as e:
        conn.close()
        raise Exception(f"Query failed:\n{e}")


# --------------------------------------------------
# Sample Data (Used by Ask Anything, Placement Predictor, etc.)
# --------------------------------------------------
@st.cache_data
def get_sample_data():
    """
    Load the CampusIQ dataset from CSV, then normalize column names
    to lower_snake_case for use by the rest of the app.
    """

    # utf-8-sig strips a BOM if present (harmless if there isn't one).
    df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")

    # Remove accidental leading/trailing spaces
    df.columns = df.columns.str.strip()

    # Some dataset variants don't include Student_ID / Roll_No — generate
    # them from row order so this works whether or not they're present,
    # same as database/seed_data.py.
    if "Student_ID" not in df.columns:
        df.insert(0, "Student_ID", range(1, len(df) + 1))
    if "Roll_No" not in df.columns:
        df.insert(1, "Roll_No", df["Student_ID"])

    # Convert numeric columns (still using original CSV header names,
    # since this happens before renaming)
    numeric_cols = [
        "Student_ID",
        "Roll_No",
        "Semester",
        "10th_%",
        "10th_Passout_Year",
        "12th_%",
        "12th_Passout_Year",
        "University_Admission_Year",
        "CGPA",
        "Attendance_%",
        "Projects_Count",
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Clean text columns
    text_cols = [
        "Student_Name",
        "Gender",
        "Stream",
        "Branch",
        "10th_Board",
        "12th_Education",
        "Backlog",
        "Top_Certification",
        "Internship_Status",
        "Placement_Status",
    ]

    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].fillna("").astype(str).str.strip()

    df = normalize_students_df(df)

    return {
        "students": df
    }