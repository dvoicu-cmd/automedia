-- Create the tables --
CREATE TABLE accounts (account_id INT AUTO_INCREMENT PRIMARY KEY);
CREATE TABLE media_pools (media_pool_id INT AUTO_INCREMENT PRIMARY KEY);
CREATE TABLE media_files (media_file_id INT AUTO_INCREMENT PRIMARY KEY);
CREATE TABLE content_files (content_id INT AUTO_INCREMENT PRIMARY KEY);
CREATE TABLE j_accounts__content_files (id INT AUTO_INCREMENT PRIMARY KEY);
CREATE TABLE j_accounts__media_pools (id INT AUTO_INCREMENT PRIMARY KEY);
CREATE TABLE j_media_pools__media_files (id INT AUTO_INCREMENT PRIMARY KEY);

-- Alter tables and add the cols --
ALTER TABLE accounts
ADD COLUMN username VARCHAR(255),
ADD CONSTRAINT unique_username UNIQUE (username),
ADD COLUMN email BLOB(255),
ADD COLUMN password BLOB(255),
ADD COLUMN hash_2fa BLOB(255),
ADD COLUMN platform VARCHAR(255),
ADD COLUMN description TEXT;

ALTER TABLE media_pools
ADD COLUMN media_pool_name VARCHAR(255),
ADD CONSTRAINT unique_media_pool_name UNIQUE (media_pool_name),
ADD COLUMN description TEXT;

ALTER TABLE media_files
ADD COLUMN file_location VARCHAR(255),
ADD CONSTRAINT unique_media_location UNIQUE (file_location),
ADD COLUMN media_type VARCHAR(255),
ADD COLUMN title VARCHAR(255),
ADD COLUMN description TEXT,
ADD COLUMN to_archive TINYINT(1);

ALTER TABLE content_files
ADD COLUMN file_location VARCHAR(255),
ADD CONSTRAINT unique_content_location UNIQUE (file_location),
ADD COLUMN title VARCHAR(255),
ADD COLUMN description TEXT,
ADD COLUMN to_archive TINYINT(1);

ALTER TABLE j_accounts__content_files
ADD COLUMN account_id INT,
ADD COLUMN content_id INT,
ADD CONSTRAINT fk_account_a_c FOREIGN KEY (account_id) REFERENCES accounts(account_id),
ADD CONSTRAINT fk_content_a_c FOREIGN KEY (content_id) REFERENCES content_files(content_id);

ALTER TABLE j_accounts__media_pools
ADD COLUMN account_id INT,
ADD COLUMN media_pool_id INT,
ADD CONSTRAINT fk_account_a_mp FOREIGN KEY (account_id) REFERENCES accounts (account_id),
ADD CONSTRAINT fk_media_pool_a_mp FOREIGN KEY (media_pool_id) REFERENCES media_pools (media_pool_id);

ALTER TABLE j_media_pools__media_files
ADD COLUMN media_pool_id INT,
ADD COLUMN media_file_id INT,
ADD CONSTRAINT fk_media_pool_mp_mf FOREIGN KEY (media_pool_id) REFERENCES media_pools (media_pool_id),
ADD CONSTRAINT fk_media_file_mp_mf FOREIGN KEY (media_file_id) REFERENCES media_files (media_file_id);

-- Crash Course: Create users for the mariadb server
-- Replace the remote host with your subnetwork. ex: 192.168.1.% or 10.10.2.%
-- Update password to be more secure
-- When granting privileges, you want to specify the database name
-- ex
-- CREATE USER 'automedia_node'@'localhost' IDENTIFIED BY 'password';
-- GRANT SELECT, INSERT, UPDATE, DELETE ON *.* TO 'automedia_node'@'localhost';
-- FLUSH PRIVILEGES;

-- Crash Course: Deleting users for the mariadb server
-- DROP USER 'automedia_node'@'localhost';

-- Crash Course: Showing all users for mariadb server
-- SELECT User, Host FROM mysql.user;
