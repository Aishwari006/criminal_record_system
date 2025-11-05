-- ============================================================
-- 📈 DATABASE VIEWS
-- ============================================================

CREATE OR REPLACE VIEW v_case_summary AS
SELECT 
  c.case_id,
  cr.type AS crime_type,
  ps.name AS police_station,
  co.name AS court_name,
  c.status,
  c.date_filed
FROM cases c
JOIN crimes cr ON c.crime_id = cr.crime_id
JOIN police_station ps ON c.station_id = ps.station_id
JOIN courts co ON c.court_id = co.court_id;
