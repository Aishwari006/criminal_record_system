-- ============================================================
-- ⚙️ STORED PROCEDURES FOR REPORTING AND OPERATIONS
-- ============================================================

DELIMITER $$

-- Get all cases handled by a specific officer
CREATE PROCEDURE sp_get_cases_by_officer(IN officerId INT)
BEGIN
  SELECT c.case_id, c.summary, c.status, ca.role
  FROM cases c
  JOIN case_assignment ca ON c.case_id = ca.case_id
  WHERE ca.officer_id = officerId;
END$$

-- Count of open cases
CREATE FUNCTION fn_open_cases()
RETURNS INT
DETERMINISTIC
BEGIN
  DECLARE count_open INT;
  SELECT COUNT(*) INTO count_open FROM cases WHERE status = 'Open';
  RETURN count_open;
END$$

DELIMITER ;
