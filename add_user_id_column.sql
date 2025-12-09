-- Add user_id column to vulnerabilities table
-- This allows users to save their own bookmarked CVEs

ALTER TABLE vulnerabilities 
ADD COLUMN user_id INT NULL AFTER notes;

-- Add index for faster queries
CREATE INDEX idx_vulnerabilities_user_id ON vulnerabilities(user_id);

-- Optional: Add foreign key constraint (if you want referential integrity)
-- ALTER TABLE vulnerabilities 
-- ADD CONSTRAINT fk_vulnerabilities_user 
-- FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

