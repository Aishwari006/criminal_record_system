-- ============================================================
-- 🌱 SEED DATA FOR CORE TABLES
-- ============================================================

-- 🔹 Criminals
INSERT INTO criminals (first_name, last_name, dob, address, city, state, status) VALUES
('Rohan', 'Patil', '1990-05-12', 'MG Road', 'Pune', 'Maharashtra', 'In Custody'),
('Sneha', 'Kulkarni', '1988-09-23', 'Civil Lines', 'Nagpur', 'Maharashtra', 'Released'),
('Vijay', 'Deshmukh', '1982-03-17', 'Marine Drive', 'Mumbai', 'Maharashtra', 'At Large'),
('Anjali', 'Rao', '1995-06-05', 'Jayanagar', 'Bangalore', 'Karnataka', 'In Custody'),
('Kiran', 'Shetty', '1991-11-11', 'Whitefield', 'Bangalore', 'Karnataka', 'Deceased'),
('Arun', 'Singh', '1987-08-09', 'Connaught Place', 'Delhi', 'Delhi', 'In Custody'),
('Rekha', 'Iyer', '1993-02-14', 'Anna Nagar', 'Chennai', 'Tamil Nadu', 'Released'),
('Ajay', 'Mehta', '1985-12-01', 'Sector 18', 'Noida', 'Uttar Pradesh', 'At Large'),
('Pooja', 'Verma', '1996-07-19', 'Park Street', 'Kolkata', 'West Bengal', 'In Custody'),
('Sanjay', 'Naidu', '1989-10-02', 'Laxmi Road', 'Pune', 'Maharashtra', 'Released');


-- 🔹 Crimes
INSERT INTO crimes (type, description, date_committed, location) VALUES
('Theft', 'Jewelry theft in local market', '2025-01-05', 'Pune'),
('Fraud', 'Bank scam reported', '2025-01-15', 'Mumbai'),
('Assault', 'Street assault case', '2025-01-25', 'Nagpur'),
('Murder', 'Homicide in residential area', '2025-02-05', 'Delhi'),
('Cybercrime', 'Online phishing reported', '2025-02-10', 'Bangalore'),
('Smuggling', 'Illegal goods trafficking', '2025-02-20', 'Chennai'),
('Drug Trafficking', 'Police busted drug ring', '2025-02-25', 'Hyderabad'),
('Robbery', 'ATM robbery incident', '2025-03-01', 'Pune'),
('Kidnapping', 'Missing person case filed', '2025-03-10', 'Kolkata'),
('Extortion', 'Business threatened for money', '2025-03-15', 'Delhi');


-- 🔹 Police Stations
INSERT INTO police_station (name, address, city, state) VALUES
('Shivaji Nagar PS', 'MG Road', 'Pune', 'Maharashtra'),
('Marine Lines PS', 'Marine Drive', 'Mumbai', 'Maharashtra'),
('Jayanagar PS', 'BTM Layout', 'Bangalore', 'Karnataka'),
('Connaught PS', 'Rajiv Chowk', 'Delhi', 'Delhi'),
('Park Street PS', 'Park Street', 'Kolkata', 'West Bengal'),
('Anna Nagar PS', 'Main Road', 'Chennai', 'Tamil Nadu'),
('Banjara Hills PS', 'Road No 10', 'Hyderabad', 'Telangana'),
('Whitefield PS', 'Tech Park Road', 'Bangalore', 'Karnataka'),
('Sector 18 PS', 'Atta Market', 'Noida', 'Uttar Pradesh'),
('Civil Lines PS', 'Residency Road', 'Nagpur', 'Maharashtra');


-- 🔹 Police Officers
INSERT INTO police_officer (station_id, first_name, last_name, badge_number, officer_rank, hire_date) VALUES
(1, 'Amit', 'Sharma', 'B123', 'Inspector', '2020-03-15'),
(2, 'Priya', 'Desai', 'B124', 'Sub-Inspector', '2021-04-18'),
(3, 'Raj', 'Verma', 'B125', 'Constable', '2022-01-20'),
(4, 'Sunita', 'Nair', 'B126', 'Head Constable', '2019-09-25'),
(5, 'Vikram', 'Menon', 'B127', 'Inspector', '2018-02-10'),
(6, 'Deepak', 'Joshi', 'B128', 'Sub-Inspector', '2021-06-11'),
(7, 'Reena', 'Reddy', 'B129', 'Constable', '2022-07-01'),
(8, 'Nikhil', 'Patel', 'B130', 'Head Constable', '2019-11-12'),
(9, 'Arjun', 'Saxena', 'B131', 'Inspector', '2020-08-03'),
(10, 'Sneha', 'Kapoor', 'B132', 'Constable', '2023-01-09');


-- 🔹 Victims
INSERT INTO victims (first_name, last_name, dob, address, phone) VALUES
('Neha', 'Kulkarni', '1990-04-12', 'Camp Area, Pune', '9998887771'),
('Ravi', 'Shah', '1987-09-05', 'Andheri, Mumbai', '9998887772'),
('Kavita', 'Joshi', '1995-11-23', 'BTM Layout, Bangalore', '9998887773'),
('Suresh', 'Patil', '1982-03-19', 'Rajiv Chowk, Delhi', '9998887774'),
('Anita', 'Nair', '1998-07-15', 'Anna Nagar, Chennai', '9998887775'),
('Manoj', 'Verma', '1985-01-10', 'Park Street, Kolkata', '9998887776'),
('Pallavi', 'Rao', '1993-05-21', 'Whitefield, Bangalore', '9998887777'),
('Asha', 'Menon', '1992-08-08', 'Banjara Hills, Hyderabad', '9998887778'),
('Rohit', 'Gupta', '1989-02-11', 'Sector 18, Noida', '9998887779'),
('Geeta', 'Naik', '1991-10-14', 'Civil Lines, Nagpur', '9998887780');


-- 🔹 Courts
INSERT INTO courts (name, type, city, state) VALUES
('Pune District Court', 'District', 'Pune', 'Maharashtra'),
('Mumbai High Court', 'High', 'Mumbai', 'Maharashtra'),
('Bangalore Sessions Court', 'District', 'Bangalore', 'Karnataka'),
('Delhi High Court', 'High', 'Delhi', 'Delhi'),
('Chennai Magistrate Court', 'Magistrate', 'Chennai', 'Tamil Nadu'),
('Kolkata District Court', 'District', 'Kolkata', 'West Bengal'),
('Hyderabad High Court', 'High', 'Hyderabad', 'Telangana'),
('Nagpur Sessions Court', 'District', 'Nagpur', 'Maharashtra'),
('Noida District Court', 'District', 'Noida', 'Uttar Pradesh'),
('Bangalore High Court', 'High', 'Bangalore', 'Karnataka');


-- 🔹 Cases
INSERT INTO cases (crime_id, station_id, court_id, summary, status, date_filed) VALUES
(1, 1, 1, 'Jewelry theft case in Pune market', 'Open', '2025-01-06'),
(2, 2, 2, 'Bank scam involving online fraud', 'Under Investigation', '2025-01-17'),
(3, 3, 3, 'Assault incident in Nagpur', 'Closed', '2025-01-26'),
(4, 4, 4, 'Murder case near Connaught Place', 'Open', '2025-02-06'),
(5, 5, 5, 'Cybercrime targeting corporate employees', 'Open', '2025-02-11'),
(6, 6, 6, 'Smuggling case at Chennai port', 'Under Investigation', '2025-02-21'),
(7, 7, 7, 'Drug trafficking case busted in Hyderabad', 'Closed', '2025-02-26'),
(8, 8, 8, 'ATM robbery near Tech Park', 'Open', '2025-03-02'),
(9, 9, 9, 'Kidnapping of a minor in Noida', 'Under Investigation', '2025-03-11'),
(10, 10, 10, 'Extortion attempt at Nagpur business', 'Closed', '2025-03-16');
