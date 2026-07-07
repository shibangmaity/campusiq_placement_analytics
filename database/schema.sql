-- CampusIQ Database Schema
-- Run this file to set up the PostgreSQL database
-- Owner: P3 (Database + Data Pipeline)

CREATE DATABASE campusiq;
\c campusiq;

-- Students table
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    roll_number VARCHAR(20) UNIQUE NOT NULL,
    branch VARCHAR(10) NOT NULL,  -- CSE, ECE, EEE, MECH, CIVIL
    semester INTEGER NOT NULL CHECK (semester BETWEEN 1 AND 8),
    cgpa DECIMAL(4,2) CHECK (cgpa BETWEEN 0 AND 10),
    email VARCHAR(100) UNIQUE
);

-- Attendance table
CREATE TABLE attendance (
    attendance_id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(student_id),
    subject VARCHAR(50) NOT NULL,
    month VARCHAR(20) NOT NULL,
    present_days INTEGER NOT NULL,
    total_days INTEGER NOT NULL,
    CONSTRAINT valid_days CHECK (present_days <= total_days)
);

-- Marks table
CREATE TABLE marks (
    marks_id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(student_id),
    subject VARCHAR(50) NOT NULL,
    exam_type VARCHAR(20) NOT NULL,  -- MID1, MID2, END_SEM
    marks_obtained DECIMAL(5,2) NOT NULL,
    max_marks DECIMAL(5,2) NOT NULL DEFAULT 100
);

-- Placements table
CREATE TABLE placements (
    placement_id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(student_id),
    company VARCHAR(100) NOT NULL,
    package_lpa DECIMAL(5,2),
    status VARCHAR(20) DEFAULT 'Applied',  -- Applied, Selected, Rejected
    year INTEGER NOT NULL
);

-- Courses table
CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    subject_name VARCHAR(50) NOT NULL,
    branch VARCHAR(10) NOT NULL,
    semester INTEGER NOT NULL,
    faculty VARCHAR(100)
);

-- Sample data (add more as needed)
INSERT INTO students (name, roll_number, branch, semester, cgpa, email) VALUES
('Shibang Maity', '21CS001', 'CSE', 7, 7.44, 'shibangmaity@gmail.com'),
('Student Two', '21CS002', 'CSE', 7, 8.20, 'student2@kiit.ac.in'),
('Student Three', '21CS003', 'CSE', 6, 6.80, 'student3@kiit.ac.in'),
('Student Four', '21ECE001', 'ECE', 5, 7.90, 'student4@kiit.ac.in'),
('Student Five', '21CS004', 'CSE', 8, 9.10, 'student5@kiit.ac.in');

-- Indexes for performance
CREATE INDEX idx_students_branch ON students(branch);
CREATE INDEX idx_attendance_student ON attendance(student_id);
CREATE INDEX idx_marks_student ON marks(student_id);
