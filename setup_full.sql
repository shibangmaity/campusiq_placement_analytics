-- ============================================
-- CampusIQ Complete Database Setup
-- Run this file in psql after connecting to campusiq DB
-- Command: \i setup_full.sql
-- ============================================

-- Drop tables if they exist (clean start)
DROP TABLE IF EXISTS feedback CASCADE;
DROP TABLE IF EXISTS events CASCADE;
DROP TABLE IF EXISTS certifications CASCADE;
DROP TABLE IF EXISTS internships CASCADE;
DROP TABLE IF EXISTS backlogs CASCADE;
DROP TABLE IF EXISTS results CASCADE;
DROP TABLE IF EXISTS placements CASCADE;
DROP TABLE IF EXISTS marks CASCADE;
DROP TABLE IF EXISTS attendance CASCADE;
DROP TABLE IF EXISTS courses CASCADE;
DROP TABLE IF EXISTS faculty CASCADE;
DROP TABLE IF EXISTS students CASCADE;

-- ============================================
-- TABLE 1: students
-- ============================================
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    roll_number VARCHAR(20) UNIQUE NOT NULL,
    branch VARCHAR(10) NOT NULL,
    semester INTEGER NOT NULL CHECK (semester BETWEEN 1 AND 8),
    cgpa DECIMAL(4,2) CHECK (cgpa BETWEEN 0 AND 10),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15),
    gender VARCHAR(10),
    admission_year INTEGER
);

-- ============================================
-- TABLE 2: faculty
-- ============================================
CREATE TABLE faculty (
    faculty_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(20) NOT NULL,
    designation VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    experience_years INTEGER
);

-- ============================================
-- TABLE 3: courses
-- ============================================
CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    subject_code VARCHAR(20) UNIQUE NOT NULL,
    subject_name VARCHAR(100) NOT NULL,
    branch VARCHAR(10) NOT NULL,
    semester INTEGER NOT NULL,
    credits INTEGER DEFAULT 3,
    faculty_id INTEGER REFERENCES faculty(faculty_id)
);

-- ============================================
-- TABLE 4: attendance
-- ============================================
CREATE TABLE attendance (
    attendance_id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(student_id),
    course_id INTEGER REFERENCES courses(course_id),
    month VARCHAR(20) NOT NULL,
    present_days INTEGER NOT NULL,
    total_days INTEGER NOT NULL,
    CONSTRAINT valid_days CHECK (present_days <= total_days)
);

-- ============================================
-- TABLE 5: marks
-- ============================================
CREATE TABLE marks (
    marks_id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(student_id),
    course_id INTEGER REFERENCES courses(course_id),
    exam_type VARCHAR(20) NOT NULL CHECK (exam_type IN ('MID1', 'MID2', 'END_SEM', 'PRACTICAL')),
    marks_obtained DECIMAL(5,2) NOT NULL,
    max_marks DECIMAL(5,2) NOT NULL DEFAULT 100
);

-- ============================================
-- TABLE 6: results
-- ============================================
CREATE TABLE results (
    result_id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(student_id),
    semester INTEGER NOT NULL,
    sgpa DECIMAL(4,2) CHECK (sgpa BETWEEN 0 AND 10),
    cgpa DECIMAL(4,2) CHECK (cgpa BETWEEN 0 AND 10),
    total_credits INTEGER,
    year INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'PASS' CHECK (status IN ('PASS', 'FAIL', 'DETAINED'))
);

-- ============================================
-- TABLE 7: backlogs
-- ============================================
CREATE TABLE backlogs (
    backlog_id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(student_id),
    course_id INTEGER REFERENCES courses(course_id),
    semester INTEGER NOT NULL,
    attempts INTEGER DEFAULT 1,
    cleared BOOLEAN DEFAULT FALSE,
    cleared_year INTEGER
);

-- ============================================
-- TABLE 8: placements
-- ============================================
CREATE TABLE placements (
    placement_id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(student_id),
    company VARCHAR(100) NOT NULL,
    role VARCHAR(100),
    package_lpa DECIMAL(5,2),
    offer_type VARCHAR(20) DEFAULT 'FTE' CHECK (offer_type IN ('FTE', 'PPO', 'Internship')),
    status VARCHAR(20) DEFAULT 'Selected' CHECK (status IN ('Selected', 'Rejected', 'Applied', 'Waiting')),
    year INTEGER NOT NULL
);

-- ============================================
-- TABLE 9: internships
-- ============================================
CREATE TABLE internships (
    internship_id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(student_id),
    company VARCHAR(100) NOT NULL,
    role VARCHAR(100),
    duration_months INTEGER,
    stipend_monthly INTEGER,
    ppo_offered BOOLEAN DEFAULT FALSE,
    year INTEGER NOT NULL
);

-- ============================================
-- TABLE 10: certifications
-- ============================================
CREATE TABLE certifications (
    cert_id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(student_id),
    platform VARCHAR(50) NOT NULL,
    course_name VARCHAR(200) NOT NULL,
    issued_date DATE,
    credential_id VARCHAR(100)
);

-- ============================================
-- TABLE 11: feedback
-- ============================================
CREATE TABLE feedback (
    feedback_id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(student_id),
    faculty_id INTEGER REFERENCES faculty(faculty_id),
    course_id INTEGER REFERENCES courses(course_id),
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    semester INTEGER,
    year INTEGER
);

-- ============================================
-- TABLE 12: events
-- ============================================
CREATE TABLE events (
    event_id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(student_id),
    event_name VARCHAR(200) NOT NULL,
    category VARCHAR(50) CHECK (category IN ('Hackathon', 'Cultural', 'Sports', 'Technical', 'Seminar')),
    position VARCHAR(20),
    date DATE,
    organized_by VARCHAR(100)
);

-- ============================================
-- SEED DATA
-- ============================================

-- Faculty (10 faculty members)
INSERT INTO faculty (name, department, designation, email, experience_years) VALUES
('Dr. Rajesh Kumar', 'CSE', 'Professor', 'rajesh.kumar@kiit.ac.in', 15),
('Dr. Priya Sharma', 'CSE', 'Associate Professor', 'priya.sharma@kiit.ac.in', 10),
('Dr. Amit Patel', 'CSE', 'Assistant Professor', 'amit.patel@kiit.ac.in', 7),
('Dr. Sunita Rath', 'ECE', 'Professor', 'sunita.rath@kiit.ac.in', 18),
('Dr. Mohan Das', 'ECE', 'Associate Professor', 'mohan.das@kiit.ac.in', 12),
('Dr. Ananya Singh', 'CSE', 'Assistant Professor', 'ananya.singh@kiit.ac.in', 5),
('Dr. Vikram Nair', 'CSE', 'Professor', 'vikram.nair@kiit.ac.in', 20),
('Dr. Deepa Mishra', 'EEE', 'Associate Professor', 'deepa.mishra@kiit.ac.in', 9),
('Dr. Ravi Shankar', 'CSE', 'Assistant Professor', 'ravi.shankar@kiit.ac.in', 4),
('Dr. Kavita Joshi', 'ECE', 'Assistant Professor', 'kavita.joshi@kiit.ac.in', 6);

-- Courses (12 courses)
INSERT INTO courses (subject_code, subject_name, branch, semester, credits, faculty_id) VALUES
('CS501', 'Machine Learning', 'CSE', 5, 4, 1),
('CS502', 'Database Management Systems', 'CSE', 5, 4, 2),
('CS503', 'Operating Systems', 'CSE', 5, 3, 3),
('CS601', 'Deep Learning', 'CSE', 6, 4, 1),
('CS602', 'Cloud Computing', 'CSE', 6, 3, 6),
('CS701', 'Natural Language Processing', 'CSE', 7, 4, 7),
('CS702', 'Software Engineering', 'CSE', 7, 3, 9),
('EC501', 'Digital Signal Processing', 'ECE', 5, 4, 4),
('EC502', 'VLSI Design', 'ECE', 5, 3, 5),
('EC601', 'Wireless Communication', 'ECE', 6, 4, 10),
('EE501', 'Power Systems', 'EEE', 5, 4, 8),
('CS504', 'Computer Networks', 'CSE', 5, 3, 2);

-- Students (50 KIIT students)
INSERT INTO students (name, roll_number, branch, semester, cgpa, email, phone, gender, admission_year) VALUES
('Aarav Sharma', '22CS001', 'CSE', 5, 8.75, 'aarav.sharma@kiit.ac.in', '9876543201', 'Male', 2022),
('Priya Patel', '22CS002', 'CSE', 5, 9.10, 'priya.patel@kiit.ac.in', '9876543202', 'Female', 2022),
('Rohan Mehta', '22CS003', 'CSE', 5, 7.40, 'rohan.mehta@kiit.ac.in', '9876543203', 'Male', 2022),
('Sneha Reddy', '22CS004', 'CSE', 5, 8.20, 'sneha.reddy@kiit.ac.in', '9876543204', 'Female', 2022),
('Arjun Singh', '22CS005', 'CSE', 5, 6.80, 'arjun.singh@kiit.ac.in', '9876543205', 'Male', 2022),
('Ananya Das', '22CS006', 'CSE', 5, 9.30, 'ananya.das@kiit.ac.in', '9876543206', 'Female', 2022),
('Vikram Nair', '22CS007', 'CSE', 5, 7.90, 'vikram.nair@kiit.ac.in', '9876543207', 'Male', 2022),
('Kavya Iyer', '22CS008', 'CSE', 5, 8.50, 'kavya.iyer@kiit.ac.in', '9876543208', 'Female', 2022),
('Rahul Gupta', '22CS009', 'CSE', 5, 6.20, 'rahul.gupta@kiit.ac.in', '9876543209', 'Male', 2022),
('Pooja Mishra', '22CS010', 'CSE', 5, 7.70, 'pooja.mishra@kiit.ac.in', '9876543210', 'Female', 2022),
('Kiran Kumar', '22CS011', 'CSE', 6, 8.90, 'kiran.kumar@kiit.ac.in', '9876543211', 'Male', 2022),
('Deepa Rao', '22CS012', 'CSE', 6, 7.30, 'deepa.rao@kiit.ac.in', '9876543212', 'Female', 2022),
('Saurav Jha', '22CS013', 'CSE', 6, 6.50, 'saurav.jha@kiit.ac.in', '9876543213', 'Male', 2022),
('Riya Banerjee', '22CS014', 'CSE', 6, 9.00, 'riya.banerjee@kiit.ac.in', '9876543214', 'Female', 2022),
('Aditya Verma', '22CS015', 'CSE', 6, 8.10, 'aditya.verma@kiit.ac.in', '9876543215', 'Male', 2022),
('Shreya Pillai', '22CS016', 'CSE', 6, 7.60, 'shreya.pillai@kiit.ac.in', '9876543216', 'Female', 2022),
('Nikhil Tiwari', '22CS017', 'CSE', 6, 6.90, 'nikhil.tiwari@kiit.ac.in', '9876543217', 'Male', 2022),
('Meera Krishnan', '22CS018', 'CSE', 6, 8.40, 'meera.krishnan@kiit.ac.in', '9876543218', 'Female', 2022),
('Siddharth Roy', '22CS019', 'CSE', 7, 7.10, 'siddharth.roy@kiit.ac.in', '9876543219', 'Male', 2022),
('Tanvi Shah', '22CS020', 'CSE', 7, 8.80, 'tanvi.shah@kiit.ac.in', '9876543220', 'Female', 2022),
('Harsh Agarwal', '22CS021', 'CSE', 7, 6.40, 'harsh.agarwal@kiit.ac.in', '9876543221', 'Male', 2022),
('Divya Nair', '22CS022', 'CSE', 7, 9.20, 'divya.nair@kiit.ac.in', '9876543222', 'Female', 2022),
('Pranav Joshi', '22CS023', 'CSE', 7, 7.50, 'pranav.joshi@kiit.ac.in', '9876543223', 'Male', 2022),
('Swati Kulkarni', '22CS024', 'CSE', 7, 8.30, 'swati.kulkarni@kiit.ac.in', '9876543224', 'Female', 2022),
('Rohit Pandey', '22CS025', 'CSE', 7, 5.90, 'rohit.pandey@kiit.ac.in', '9876543225', 'Male', 2022),
('Nidhi Saxena', '22CS026', 'CSE', 8, 8.60, 'nidhi.saxena@kiit.ac.in', '9876543226', 'Female', 2022),
('Abhishek Yadav', '22CS027', 'CSE', 8, 7.20, 'abhishek.yadav@kiit.ac.in', '9876543227', 'Male', 2022),
('Pallavi Ghosh', '22CS028', 'CSE', 8, 9.40, 'pallavi.ghosh@kiit.ac.in', '9876543228', 'Female', 2022),
('Suresh Babu', '22CS029', 'CSE', 8, 6.70, 'suresh.babu@kiit.ac.in', '9876543229', 'Male', 2022),
('Akanksha Dubey', '22CS030', 'CSE', 8, 8.00, 'akanksha.dubey@kiit.ac.in', '9876543230', 'Female', 2022),
('Gaurav Chauhan', '22EC001', 'ECE', 5, 7.80, 'gaurav.chauhan@kiit.ac.in', '9876543231', 'Male', 2022),
('Roshni Menon', '22EC002', 'ECE', 5, 8.90, 'roshni.menon@kiit.ac.in', '9876543232', 'Female', 2022),
('Ajay Srivastava', '22EC003', 'ECE', 5, 6.60, 'ajay.srivastava@kiit.ac.in', '9876543233', 'Male', 2022),
('Namrata Bose', '22EC004', 'ECE', 5, 7.40, 'namrata.bose@kiit.ac.in', '9876543234', 'Female', 2022),
('Vishal Thakur', '22EC005', 'ECE', 6, 8.20, 'vishal.thakur@kiit.ac.in', '9876543235', 'Male', 2022),
('Preeti Dutta', '22EC006', 'ECE', 6, 7.70, 'preeti.dutta@kiit.ac.in', '9876543236', 'Female', 2022),
('Manish Tripathi', '22EC007', 'ECE', 6, 6.30, 'manish.tripathi@kiit.ac.in', '9876543237', 'Male', 2022),
('Sunaina Kapoor', '22EC008', 'ECE', 6, 9.10, 'sunaina.kapoor@kiit.ac.in', '9876543238', 'Female', 2022),
('Kartik Malhotra', '22EC009', 'ECE', 7, 7.90, 'kartik.malhotra@kiit.ac.in', '9876543239', 'Male', 2022),
('Ishita Chatterjee', '22EC010', 'ECE', 7, 8.50, 'ishita.chatterjee@kiit.ac.in', '9876543240', 'Female', 2022),
('Rakesh Mohan', '22EE001', 'EEE', 5, 7.10, 'rakesh.mohan@kiit.ac.in', '9876543241', 'Male', 2022),
('Shruti Acharya', '22EE002', 'EEE', 5, 8.30, 'shruti.acharya@kiit.ac.in', '9876543242', 'Female', 2022),
('Deepak Rajan', '22EE003', 'EEE', 5, 6.90, 'deepak.rajan@kiit.ac.in', '9876543243', 'Male', 2022),
('Poornima Hegde', '22EE004', 'EEE', 6, 7.60, 'poornima.hegde@kiit.ac.in', '9876543244', 'Female', 2022),
('Sanjay Patil', '22EE005', 'EEE', 6, 8.70, 'sanjay.patil@kiit.ac.in', '9876543245', 'Male', 2022),
('Lavanya Subramanian', '22EE006', 'EEE', 6, 7.30, 'lavanya.subramanian@kiit.ac.in', '9876543246', 'Female', 2022),
('Nitin Bhatt', '22EE007', 'EEE', 7, 6.50, 'nitin.bhatt@kiit.ac.in', '9876543247', 'Male', 2022),
('Rashmi Desai', '22EE008', 'EEE', 7, 9.00, 'rashmi.desai@kiit.ac.in', '9876543248', 'Female', 2022),
('Tarun Mathur', '22EE009', 'EEE', 7, 7.80, 'tarun.mathur@kiit.ac.in', '9876543249', 'Male', 2022),
('Usha Pillai', '22EE010', 'EEE', 8, 8.40, 'usha.pillai@kiit.ac.in', '9876543250', 'Female', 2022);

-- Attendance data (for CSE students, 3 subjects, 3 months)
INSERT INTO attendance (student_id, course_id, month, present_days, total_days) VALUES
(1, 1, 'January', 22, 25), (1, 2, 'January', 24, 25), (1, 3, 'January', 20, 25),
(2, 1, 'January', 25, 25), (2, 2, 'January', 25, 25), (2, 3, 'January', 24, 25),
(3, 1, 'January', 18, 25), (3, 2, 'January', 20, 25), (3, 3, 'January', 17, 25),
(4, 1, 'January', 23, 25), (4, 2, 'January', 22, 25), (4, 3, 'January', 21, 25),
(5, 1, 'January', 15, 25), (5, 2, 'January', 16, 25), (5, 3, 'January', 14, 25),
(6, 1, 'January', 25, 25), (6, 2, 'January', 24, 25), (6, 3, 'January', 25, 25),
(7, 1, 'January', 20, 25), (7, 2, 'January', 21, 25), (7, 3, 'January', 19, 25),
(8, 1, 'January', 24, 25), (8, 2, 'January', 23, 25), (8, 3, 'January', 22, 25),
(9, 1, 'January', 12, 25), (9, 2, 'January', 14, 25), (9, 3, 'January', 11, 25),
(10, 1, 'January', 21, 25), (10, 2, 'January', 20, 25), (10, 3, 'January', 19, 25),
(1, 1, 'February', 20, 22), (1, 2, 'February', 21, 22), (1, 3, 'February', 18, 22),
(2, 1, 'February', 22, 22), (2, 2, 'February', 22, 22), (2, 3, 'February', 21, 22),
(3, 1, 'February', 16, 22), (3, 2, 'February', 17, 22), (3, 3, 'February', 15, 22),
(4, 1, 'February', 20, 22), (4, 2, 'February', 19, 22), (4, 3, 'February', 18, 22),
(5, 1, 'February', 13, 22), (5, 2, 'February', 14, 22), (5, 3, 'February', 12, 22);

-- Marks data
INSERT INTO marks (student_id, course_id, exam_type, marks_obtained, max_marks) VALUES
(1, 1, 'MID1', 42, 50), (1, 1, 'MID2', 44, 50), (1, 1, 'END_SEM', 78, 100),
(2, 1, 'MID1', 48, 50), (2, 1, 'MID2', 47, 50), (2, 1, 'END_SEM', 92, 100),
(3, 1, 'MID1', 35, 50), (3, 1, 'MID2', 33, 50), (3, 1, 'END_SEM', 65, 100),
(4, 1, 'MID1', 40, 50), (4, 1, 'MID2', 42, 50), (4, 1, 'END_SEM', 80, 100),
(5, 1, 'MID1', 28, 50), (5, 1, 'MID2', 30, 50), (5, 1, 'END_SEM', 58, 100),
(6, 1, 'MID1', 49, 50), (6, 1, 'MID2', 50, 50), (6, 1, 'END_SEM', 95, 100),
(7, 1, 'MID1', 38, 50), (7, 1, 'MID2', 40, 50), (7, 1, 'END_SEM', 74, 100),
(8, 1, 'MID1', 44, 50), (8, 1, 'MID2', 43, 50), (8, 1, 'END_SEM', 85, 100),
(9, 1, 'MID1', 22, 50), (9, 1, 'MID2', 25, 50), (9, 1, 'END_SEM', 48, 100),
(10, 1, 'MID1', 37, 50), (10, 1, 'MID2', 38, 50), (10, 1, 'END_SEM', 72, 100);

-- Results (semester wise SGPA)
INSERT INTO results (student_id, semester, sgpa, cgpa, total_credits, year, status) VALUES
(1, 3, 8.50, 8.60, 22, 2023, 'PASS'), (1, 4, 8.90, 8.75, 22, 2024, 'PASS'),
(2, 3, 9.00, 9.05, 22, 2023, 'PASS'), (2, 4, 9.20, 9.10, 22, 2024, 'PASS'),
(3, 3, 7.20, 7.35, 22, 2023, 'PASS'), (3, 4, 7.50, 7.40, 22, 2024, 'PASS'),
(4, 3, 8.10, 8.15, 22, 2023, 'PASS'), (4, 4, 8.30, 8.20, 22, 2024, 'PASS'),
(5, 3, 6.50, 6.70, 22, 2023, 'PASS'), (5, 4, 6.90, 6.80, 22, 2024, 'PASS'),
(6, 3, 9.40, 9.35, 22, 2023, 'PASS'), (6, 4, 9.20, 9.30, 22, 2024, 'PASS'),
(7, 3, 7.80, 7.85, 22, 2023, 'PASS'), (7, 4, 8.00, 7.90, 22, 2024, 'PASS'),
(8, 3, 8.40, 8.45, 22, 2023, 'PASS'), (8, 4, 8.60, 8.50, 22, 2024, 'PASS'),
(9, 3, 5.80, 6.10, 22, 2023, 'PASS'), (9, 4, 6.40, 6.20, 22, 2024, 'PASS'),
(10, 3, 7.60, 7.65, 22, 2023, 'PASS'), (10, 4, 7.80, 7.70, 22, 2024, 'PASS');

-- Backlogs (only low performing students)
INSERT INTO backlogs (student_id, course_id, semester, attempts, cleared, cleared_year) VALUES
(5, 3, 4, 2, TRUE, 2024),
(9, 1, 3, 1, FALSE, NULL),
(9, 3, 4, 2, TRUE, 2024),
(25, 2, 5, 1, FALSE, NULL),
(21, 1, 5, 1, FALSE, NULL);

-- Placements (final year students)
INSERT INTO placements (student_id, company, role, package_lpa, offer_type, status, year) VALUES
(26, 'TCS', 'Software Engineer', 7.00, 'FTE', 'Selected', 2026),
(27, 'Infosys', 'Systems Engineer', 6.50, 'FTE', 'Selected', 2026),
(28, 'Google', 'SDE', 45.00, 'FTE', 'Selected', 2026),
(29, 'Wipro', 'Project Engineer', 6.00, 'FTE', 'Selected', 2026),
(30, 'Capgemini', 'Analyst', 8.00, 'FTE', 'Selected', 2026),
(26, 'Accenture', 'Associate', 9.50, 'FTE', 'Rejected', 2026),
(28, 'Microsoft', 'SDE', 50.00, 'FTE', 'Rejected', 2026);

-- Internships
INSERT INTO internships (student_id, company, role, duration_months, stipend_monthly, ppo_offered, year) VALUES
(1, 'Amazon', 'SDE Intern', 2, 80000, TRUE, 2025),
(2, 'Google', 'ML Intern', 3, 100000, TRUE, 2025),
(3, 'TCS', 'Developer Intern', 2, 15000, FALSE, 2025),
(4, 'Wipro', 'Data Analyst Intern', 2, 20000, FALSE, 2025),
(6, 'Microsoft', 'SDE Intern', 3, 95000, TRUE, 2025),
(8, 'Flipkart', 'Backend Intern', 2, 60000, FALSE, 2025),
(10, 'Infosys', 'Developer Intern', 2, 15000, FALSE, 2025);

-- Certifications
INSERT INTO certifications (student_id, platform, course_name, issued_date, credential_id) VALUES
(1, 'Coursera', 'Machine Learning Specialization', '2024-06-15', 'CRS-ML-001'),
(2, 'Google', 'TensorFlow Developer Certificate', '2024-08-20', 'GGL-TF-002'),
(3, 'Udemy', 'Python for Data Science', '2024-03-10', 'UDM-PY-003'),
(4, 'Microsoft', 'Azure Data Fundamentals', '2024-07-05', 'MS-AZ-004'),
(6, 'AWS', 'Cloud Practitioner', '2024-09-12', 'AWS-CP-006'),
(8, 'Coursera', 'Deep Learning Specialization', '2024-11-01', 'CRS-DL-008'),
(1, 'SAP', 'SAP Data Analytics Engineer', '2025-01-15', 'SAP-DA-001'),
(2, 'Kaggle', 'Data Science Certificate', '2024-05-20', 'KGL-DS-002');

-- Feedback
INSERT INTO feedback (student_id, faculty_id, course_id, rating, comment, semester, year) VALUES
(1, 1, 1, 5, 'Excellent teaching, very clear explanations', 5, 2025),
(2, 1, 1, 5, 'Best ML professor, highly recommend', 5, 2025),
(3, 1, 1, 3, 'Average, could improve practical sessions', 5, 2025),
(4, 2, 2, 4, 'Good teaching style, helpful during doubt sessions', 5, 2025),
(5, 2, 2, 2, 'Goes too fast, hard to follow', 5, 2025),
(6, 3, 3, 4, 'Very knowledgeable, good examples', 5, 2025),
(7, 3, 3, 3, 'Decent professor, average notes', 5, 2025),
(8, 1, 1, 5, 'Fantastic professor, very engaging', 5, 2025),
(9, 2, 2, 1, 'Very poor, never explains doubts properly', 5, 2025),
(10, 3, 3, 4, 'Good professor overall', 5, 2025);

-- Events
INSERT INTO events (student_id, event_name, category, position, date, organized_by) VALUES
(1, 'HackKIIT 2025', 'Hackathon', 'Winner', '2025-02-15', 'KIIT'),
(2, 'Google Hackathon', 'Hackathon', 'Runner Up', '2025-03-20', 'Google'),
(3, 'Kalinga Utsav', 'Cultural', 'Participant', '2025-01-10', 'KIIT'),
(4, 'Tech Tatva', 'Technical', '2nd Place', '2025-04-05', 'KIIT'),
(6, 'Smart India Hackathon', 'Hackathon', 'Winner', '2024-12-01', 'Govt of India'),
(7, 'KIIT Sports Meet', 'Sports', '1st Place', '2025-01-25', 'KIIT'),
(8, 'CodeChef Starters', 'Technical', 'Top 100', '2025-02-28', 'CodeChef'),
(10, 'Seminar on AI Trends', 'Seminar', 'Participant', '2025-03-15', 'KIIT');

-- Indexes for performance
CREATE INDEX idx_students_branch ON students(branch);
CREATE INDEX idx_students_semester ON students(semester);
CREATE INDEX idx_attendance_student ON attendance(student_id);
CREATE INDEX idx_marks_student ON marks(student_id);
CREATE INDEX idx_results_student ON results(student_id);
CREATE INDEX idx_backlogs_student ON backlogs(student_id);
CREATE INDEX idx_placements_student ON placements(student_id);

-- Done!
SELECT 'CampusIQ Database Setup Complete!' AS status;
SELECT COUNT(*) AS total_students FROM students;
SELECT COUNT(*) AS total_faculty FROM faculty;
SELECT COUNT(*) AS total_courses FROM courses;
