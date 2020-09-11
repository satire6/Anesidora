--
-- Create database
--
create database switchboard;

-- 
-- Create login
--
GRANT SELECT, INSERT, UPDATE, DELETE 
  ON switchboard.*
  TO 'switchboard_user'@'localhost'
  IDENTIFIED BY '0bhctiws';

GRANT SELECT, INSERT, UPDATE, DELETE 
  ON switchboard.* 
  TO 'switchboard_user'@'%'
  IDENTIFIED BY '0bhctiws';