-- Create the restaurant database
CREATE DATABASE IF NOT EXISTS restaurant;

-- admin: full privileges on restaurant
CREATE USER IF NOT EXISTS 'admin' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON restaurant.* TO 'admin';

-- ds2022: read-only
-- SELECT covers SHOW TABLES / SHOW FULL TABLES and JOINs on restaurant
-- SHOW DATABASES lets the account list DBs it can access
CREATE USER IF NOT EXISTS 'ds2022' IDENTIFIED BY 'password';
GRANT SELECT ON restaurant.* TO 'ds2022';
GRANT SHOW DATABASES ON *.* TO 'ds2022';

FLUSH PRIVILEGES;
