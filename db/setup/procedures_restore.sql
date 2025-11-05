-- ============================================================
-- ♻️ RESTORE PROCEDURES FOR DELETED RECORDS
-- ============================================================

DELIMITER $$

CREATE PROCEDURE sp_restore_criminal(IN p_log_id INT)
BEGIN
  DECLARE v_data JSON;
  SET v_data = (SELECT record_data FROM deleted_records_log WHERE log_id = p_log_id AND table_name = 'criminals');
  INSERT INTO criminals (first_name, last_name, dob, address, city, state, status)
  VALUES (
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.first_name')),
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.last_name')),
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.dob')),
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.address')),
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.city')),
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.state')),
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.status'))
  );
  DELETE FROM deleted_records_log WHERE log_id = p_log_id;
END$$

CREATE PROCEDURE sp_restore_crime(IN p_log_id INT)
BEGIN
  DECLARE v_data JSON;
  SET v_data = (SELECT record_data FROM deleted_records_log WHERE log_id = p_log_id AND table_name = 'crimes');
  INSERT INTO crimes (type, description, date_committed, location)
  VALUES (
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.type')),
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.description')),
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.date_committed')),
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.location'))
  );
  DELETE FROM deleted_records_log WHERE log_id = p_log_id;
END$$

CREATE PROCEDURE sp_restore_case(IN p_log_id INT)
BEGIN
  DECLARE v_data JSON;
  SET v_data = (SELECT record_data FROM deleted_records_log WHERE log_id = p_log_id AND table_name = 'cases');
  INSERT INTO cases (crime_id, station_id, court_id, summary, status, date_filed)
  VALUES (
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.crime_id')),
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.station_id')),
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.court_id')),
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.summary')),
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.status')),
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.date_filed'))
  );
  DELETE FROM deleted_records_log WHERE log_id = p_log_id;
END$$

CREATE PROCEDURE sp_restore_victim(IN p_log_id INT)
BEGIN
  DECLARE v_data JSON;
  SET v_data = (SELECT record_data FROM deleted_records_log WHERE log_id = p_log_id AND table_name = 'victims');
  INSERT INTO victims (first_name, last_name, dob, address, phone)
  VALUES (
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.first_name')),
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.last_name')),
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.dob')),
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.address')),
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.phone'))
  );
  DELETE FROM deleted_records_log WHERE log_id = p_log_id;
END$$

CREATE PROCEDURE sp_restore_officer(IN p_log_id INT)
BEGIN
  DECLARE v_data JSON;
  SET v_data = (SELECT record_data FROM deleted_records_log WHERE log_id = p_log_id AND table_name = 'police_officer');
  INSERT INTO police_officer (station_id, first_name, last_name, badge_number, officer_rank, hire_date)
  VALUES (
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.station_id')),
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.first_name')),
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.last_name')),
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.badge_number')),
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.officer_rank')),
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.hire_date'))
  );
  DELETE FROM deleted_records_log WHERE log_id = p_log_id;
END$$

CREATE PROCEDURE sp_restore_station(IN p_log_id INT)
BEGIN
  DECLARE v_data JSON;
  SET v_data = (SELECT record_data FROM deleted_records_log WHERE log_id = p_log_id AND table_name = 'police_station');
  INSERT INTO police_station (name, address, city, state)
  VALUES (
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.name')),
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.address')),
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.city')),
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.state'))
  );
  DELETE FROM deleted_records_log WHERE log_id = p_log_id;
END$$

CREATE PROCEDURE sp_restore_court(IN p_log_id INT)
BEGIN
  DECLARE v_data JSON;
  SET v_data = (SELECT record_data FROM deleted_records_log WHERE log_id = p_log_id AND table_name = 'courts');
  INSERT INTO courts (name, type, city, state)
  VALUES (
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.name')),
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.type')),
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.city')),
    JSON_UNQUOTE(JSON_EXTRACT(v_data, '$.state'))
  );
  DELETE FROM deleted_records_log WHERE log_id = p_log_id;
END$$

DELIMITER ;
