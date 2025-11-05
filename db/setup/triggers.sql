-- ============================================================
-- 🔥 TRIGGERS FOR DELETED RECORD LOGGING
-- ============================================================

CREATE TABLE IF NOT EXISTS deleted_records_log (
  log_id INT AUTO_INCREMENT PRIMARY KEY,
  table_name VARCHAR(100),
  record_id INT,
  record_data JSON,
  deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER $$

-- Criminals
CREATE TRIGGER trg_after_criminal_delete
AFTER DELETE ON criminals
FOR EACH ROW
BEGIN
  INSERT INTO deleted_records_log (table_name, record_id, record_data)
  VALUES ('criminals', OLD.criminal_id,
    JSON_OBJECT('first_name', OLD.first_name, 'last_name', OLD.last_name,
                'dob', OLD.dob, 'address', OLD.address,
                'city', OLD.city, 'state', OLD.state, 'status', OLD.status));
END$$

-- Crimes
CREATE TRIGGER trg_after_crime_delete
AFTER DELETE ON crimes
FOR EACH ROW
BEGIN
  INSERT INTO deleted_records_log (table_name, record_id, record_data)
  VALUES ('crimes', OLD.crime_id,
    JSON_OBJECT('type', OLD.type, 'description', OLD.description,
                'date_committed', OLD.date_committed, 'location', OLD.location));
END$$

-- Cases
CREATE TRIGGER trg_after_case_delete
AFTER DELETE ON cases
FOR EACH ROW
BEGIN
  INSERT INTO deleted_records_log (table_name, record_id, record_data)
  VALUES ('cases', OLD.case_id,
    JSON_OBJECT('crime_id', OLD.crime_id, 'station_id', OLD.station_id,
                'court_id', OLD.court_id, 'summary', OLD.summary,
                'status', OLD.status, 'date_filed', OLD.date_filed));
END$$

-- Victims
CREATE TRIGGER trg_after_victim_delete
AFTER DELETE ON victims
FOR EACH ROW
BEGIN
  INSERT INTO deleted_records_log (table_name, record_id, record_data)
  VALUES ('victims', OLD.victim_id,
    JSON_OBJECT('first_name', OLD.first_name, 'last_name', OLD.last_name,
                'dob', OLD.dob, 'address', OLD.address, 'phone', OLD.phone));
END$$

-- Police Officer
CREATE TRIGGER trg_after_officer_delete
AFTER DELETE ON police_officer
FOR EACH ROW
BEGIN
  INSERT INTO deleted_records_log (table_name, record_id, record_data)
  VALUES ('police_officer', OLD.officer_id,
    JSON_OBJECT('station_id', OLD.station_id, 'first_name', OLD.first_name,
                'last_name', OLD.last_name, 'badge_number', OLD.badge_number,
                'officer_rank', OLD.officer_rank, 'hire_date', OLD.hire_date));
END$$

-- Police Station
CREATE TRIGGER trg_after_station_delete
AFTER DELETE ON police_station
FOR EACH ROW
BEGIN
  INSERT INTO deleted_records_log (table_name, record_id, record_data)
  VALUES ('police_station', OLD.station_id,
    JSON_OBJECT('name', OLD.name, 'address', OLD.address,
                'city', OLD.city, 'state', OLD.state));
END$$

-- Courts
CREATE TRIGGER trg_after_court_delete
AFTER DELETE ON courts
FOR EACH ROW
BEGIN
  INSERT INTO deleted_records_log (table_name, record_id, record_data)
  VALUES ('courts', OLD.court_id,
    JSON_OBJECT('name', OLD.name, 'type', OLD.type,
                'city', OLD.city, 'state', OLD.state));
END$$

DELIMITER ;
