-- Create default admin user for CVE Dashboard
-- Run this once after setting up the application

INSERT INTO users (username, email, pw_hash, role, verified, created_at)
VALUES ('admin', 'admin@cisa.gov', 'admin123', 'ADMIN', 1, NOW())
ON DUPLICATE KEY UPDATE
  pw_hash = 'admin123',
  role = 'ADMIN',
  verified = 1;

-- Verify user was created
SELECT id, username, email, role, verified, created_at FROM users WHERE email = 'admin@cisa.gov';

