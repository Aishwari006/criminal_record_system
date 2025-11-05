-- ============================================================
-- 📦 LINKING DATA (10 rows each for 7 linking tables)
-- ============================================================


-- 🔹 1️⃣ crime_involvement (Criminals ↔ Crimes)
INSERT INTO crime_involvement (criminal_id, crime_id, role) VALUES
(1, 1, 'Suspect'),
(2, 2, 'Convicted'),
(3, 3, 'Suspect'),
(4, 4, 'Accomplice'),
(5, 5, 'Witness'),
(6, 6, 'Convicted'),
(7, 7, 'Suspect'),
(8, 8, 'Convicted'),
(9, 9, 'Suspect'),
(10, 10, 'Accomplice');


-- 🔹 2️⃣ crime_victims (Crimes ↔ Victims)
INSERT INTO crime_victims (victim_id, crime_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10);


-- 🔹 3️⃣ case_assignment (Cases ↔ Officers)
INSERT INTO case_assignment (case_id, officer_id, role) VALUES
(1, 1, 'Lead'),
(2, 2, 'Investigator'),
(3, 3, 'Support'),
(4, 4, 'Lead'),
(5, 5, 'Investigator'),
(6, 6, 'Support'),
(7, 7, 'Lead'),
(8, 8, 'Investigator'),
(9, 9, 'Support'),
(10, 10, 'Lead');


-- 🔹 4️⃣ registrations (Police Stations ↔ Cases)
INSERT INTO registrations (station_id, case_id, registration_date) VALUES
(1, 1, '2025-01-10'),
(2, 2, '2025-02-15'),
(1, 3, '2025-03-05'),
(2, 4, '2025-03-10'),
(3, 5, '2025-03-12'),
(4, 6, '2025-03-14'),
(1, 7, '2025-03-17'),
(2, 8, '2025-03-20'),
(3, 9, '2025-03-22'),
(4, 10, '2025-03-25');


-- 🔹 5️⃣ case_trial (Cases ↔ Courts)
INSERT INTO case_trial (case_id, court_id, hearing_date, status) VALUES
(1, 1, '2025-03-01', 'Scheduled'),
(2, 2, '2025-03-15', 'Ongoing'),
(3, 1, '2025-04-01', 'Scheduled'),
(4, 2, '2025-04-05', 'Ongoing'),
(5, 3, '2025-04-09', 'Closed'),
(6, 4, '2025-04-12', 'Scheduled'),
(7, 1, '2025-04-14', 'Ongoing'),
(8, 2, '2025-04-17', 'Closed'),
(9, 3, '2025-04-20', 'Scheduled'),
(10, 4, '2025-04-25', 'Ongoing');


-- 🔹 6️⃣ case_crimes (Cases ↔ Crimes)
INSERT INTO case_crimes (case_id, crime_id, details) VALUES
(1, 1, 'Main offense'),
(2, 2, 'Connected crime'),
(3, 3, 'Secondary offense'),
(4, 4, 'Primary crime related to theft'),
(5, 5, 'Fraud-related case'),
(6, 6, 'Cybercrime involvement'),
(7, 7, 'Connected homicide'),
(8, 8, 'Drug trafficking link'),
(9, 9, 'Smuggling case'),
(10, 10, 'Assault and robbery case');


-- 🔹 7️⃣ employees (Police Stations ↔ Officers)
INSERT INTO employees (station_id, officer_id, assigned_date) VALUES
(1, 1, '2024-12-20'),
(2, 2, '2025-01-10'),
(1, 3, '2025-02-01'),
(2, 4, '2025-02-03'),
(3, 5, '2025-02-06'),
(4, 6, '2025-02-09'),
(1, 7, '2025-02-12'),
(2, 8, '2025-02-15'),
(3, 9, '2025-02-18'),
(4, 10, '2025-02-21');
