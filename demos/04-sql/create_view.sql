USE restaurant;

-- Create the employees_states view
CREATE VIEW employees_states AS
SELECT e.name, s.home_state
FROM employees e
JOIN states s ON e.state_id = s.state_code;

-- Show all tables
SHOW FULL TABLES;

-- Show the employees_states view
SELECT * FROM employees_states;
