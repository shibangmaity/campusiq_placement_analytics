import os
from groq import Groq

# -----------------------------
# Initialize Groq Client
# -----------------------------
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# -----------------------------
# Database Schema
# -----------------------------
# IMPORTANT: Ask Anything runs the generated SQL via DuckDB against the
# dataframe returned by database.db.get_sample_data() — NOT against the raw
# CSV/Postgres TitleCase columns. That dataframe has already been normalized
# by normalize_students_df() in db.py, so this schema must describe THOSE
# column names, or every generated query fails with "column not found".
DB_SCHEMA = """
Table: students  (queried as an in-memory DuckDB table, one row per student)

Columns:

student_id            INTEGER
roll_no               INTEGER
name                  TEXT      -- student's name
gender                TEXT
stream                TEXT
branch                TEXT
semester              INTEGER
tenth_percent         NUMERIC
tenth_board           TEXT
tenth_passout_year    INTEGER
twelfth_percent       NUMERIC
twelfth_education     TEXT
twelfth_passout_year  INTEGER
university_admission_year  INTEGER
cgpa                  NUMERIC
attendance_percent    NUMERIC
backlog               TEXT      -- 'No' | 'Yes' | 'Yes (Cleared)'
top_certification     TEXT      -- certification name, or 'No Certification'
internship_status     TEXT      -- 'Not Yet' | 'Ongoing' | 'Completed'
internship_company    TEXT      -- '' if internship_status = 'Not Yet'
projects_count        INTEGER
placement_status      TEXT      -- raw original value, e.g. 'Placed - TCS' or 'Not Placed'
placed                BOOLEAN   -- TRUE if the student was placed, FALSE otherwise
placement_company     TEXT      -- '' if placed = FALSE

There is ONLY ONE table: students.
"""

# -----------------------------
# LLM System Prompt
# -----------------------------
SYSTEM_PROMPT = f"""
You are an expert SQL generator for CampusIQ. The SQL you write runs against
an in-memory DuckDB table, so use standard ANSI SQL (DuckDB understands
PostgreSQL syntax closely enough — ROUND, CASE, boolean TRUE/FALSE all work).

Your job is to convert natural language questions into SQL queries.

{DB_SCHEMA}

Rules:

1. Return ONLY the SQL query.
2. No markdown.
3. No explanation.
4. No backticks.
5. Query ONLY the students table.
6. Never invent column names — use exactly the names listed above, all
   lowercase, no quoting needed (none of them contain spaces or symbols).
7. Limit output to 100 rows unless the user explicitly requests more.

Definitions:

Placed student:
placed = TRUE
(Do NOT use placement_status = 'Placed' — the raw column holds compound
values like 'Placed - TCS', which never equals the bare word 'Placed'.
Always filter on the boolean `placed` column instead.)

Not Placed:
placed = FALSE

Average CGPA:
ROUND(AVG(cgpa), 2)

Average Attendance:
ROUND(AVG(attendance_percent), 2)

Placement Rate:
ROUND(100.0 * SUM(CASE WHEN placed THEN 1 ELSE 0 END) / COUNT(*), 2)

Placed at a specific company (e.g. "students placed at TCS"):
placed = TRUE AND placement_company ILIKE '%TCS%'

Examples:

Question:
Show top 10 students by CGPA.

SQL:
SELECT name, cgpa
FROM students
ORDER BY cgpa DESC
LIMIT 10;

Question:
How many students are placed?

SQL:
SELECT COUNT(*) AS placed_students
FROM students
WHERE placed = TRUE;

Question:
Average attendance of CSE students.

SQL:
SELECT ROUND(AVG(attendance_percent), 2) AS average_attendance
FROM students
WHERE branch = 'CSE';

Question:
Students having more than 8 CGPA.

SQL:
SELECT name, cgpa
FROM students
WHERE cgpa > 8
LIMIT 100;

Question:
Students placed at TCS.

SQL:
SELECT name, branch, placement_company
FROM students
WHERE placed = TRUE AND placement_company ILIKE '%TCS%'
LIMIT 100;
"""


# -----------------------------
# Natural Language -> SQL
# -----------------------------
def nl_to_sql(user_question: str) -> str:
    """
    Convert natural language to SQL for the normalized students table.
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_question
                }
            ],
            temperature=0.1,
            max_tokens=400
        )

        sql = response.choices[0].message.content.strip()

        sql = sql.replace("```sql", "")
        sql = sql.replace("```", "")
        sql = sql.strip()

        return sql

    except Exception as e:
        return f"ERROR: {e}"


# -----------------------------
# Explain SQL Result
# -----------------------------
def explain_result(question: str, sql: str, result_summary: str) -> str:
    """
    Explain SQL results in plain English.
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """
You are a helpful data analyst.

Given:
- User Question
- SQL Query
- SQL Result

Provide a concise explanation in 2-3 sentences.

Do not mention SQL.

Highlight any important insights.
"""
                },
                {
                    "role": "user",
                    "content": f"""
Question:
{question}

SQL:
{sql}

Result:
{result_summary}
"""
                }
            ],
            temperature=0.4,
            max_tokens=180
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Could not generate explanation: {e}"