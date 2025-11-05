-- ============================================================
-- 📦 DATABASE SCHEMA FOR CRIMINAL RECORD SYSTEM
-- ============================================================

CREATE TABLE IF NOT EXISTS police_station (
  station_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255),
  address TEXT,
  city VARCHAR(100),
  state VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS police_officer (
  officer_id INT AUTO_INCREMENT PRIMARY KEY,
  station_id INT,
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  badge_number VARCHAR(50),
  officer_rank VARCHAR(100),
  hire_date DATE,
  FOREIGN KEY (station_id) REFERENCES police_station(station_id)
);

CREATE TABLE IF NOT EXISTS criminals (
  criminal_id INT AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  dob DATE,
  address TEXT,
  city VARCHAR(100),
  state VARCHAR(100),
  status ENUM('At Large', 'In Custody', 'Released', 'Deceased')
);

CREATE TABLE IF NOT EXISTS crimes (
  crime_id INT AUTO_INCREMENT PRIMARY KEY,
  type VARCHAR(100),
  description TEXT,
  date_committed DATE,
  location VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS courts (
  court_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255),
  type ENUM('District', 'High', 'Supreme', 'Magistrate'),
  city VARCHAR(100),
  state VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS cases (
  case_id INT AUTO_INCREMENT PRIMARY KEY,
  crime_id INT,
  station_id INT,
  court_id INT,
  summary TEXT,
  status ENUM('Open', 'Closed', 'Under Investigation'),
  date_filed DATE,
  FOREIGN KEY (crime_id) REFERENCES crimes(crime_id),
  FOREIGN KEY (station_id) REFERENCES police_station(station_id),
  FOREIGN KEY (court_id) REFERENCES courts(court_id)
);

CREATE TABLE IF NOT EXISTS victims (
  victim_id INT AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  dob DATE,
  address TEXT,
  phone VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS crime_involvement (
  involvement_id INT AUTO_INCREMENT PRIMARY KEY,
  criminal_id INT,
  crime_id INT,
  role ENUM('Suspect', 'Convicted', 'Accomplice', 'Witness'),
  FOREIGN KEY (criminal_id) REFERENCES criminals(criminal_id),
  FOREIGN KEY (crime_id) REFERENCES crimes(crime_id)
);

CREATE TABLE IF NOT EXISTS crime_victims (
  crime_victim_id INT AUTO_INCREMENT PRIMARY KEY,
  victim_id INT,
  crime_id INT,
  FOREIGN KEY (victim_id) REFERENCES victims(victim_id),
  FOREIGN KEY (crime_id) REFERENCES crimes(crime_id)
);

CREATE TABLE IF NOT EXISTS case_assignment (
  assignment_id INT AUTO_INCREMENT PRIMARY KEY,
  case_id INT,
  officer_id INT,
  role ENUM('Lead', 'Support', 'Investigator'),
  FOREIGN KEY (case_id) REFERENCES cases(case_id),
  FOREIGN KEY (officer_id) REFERENCES police_officer(officer_id)
);
