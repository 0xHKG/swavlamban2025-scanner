-- Create Scanner User Account for Testing
-- Password: scanner123
-- This SQL can be run on SQLite or PostgreSQL

-- Create scanner user (password is bcrypt hash of "scanner123")
INSERT INTO users (
    username,
    password_hash,
    organization,
    max_entries,
    role,
    quota_ex_day1,
    quota_ex_day2,
    quota_interactive,
    quota_plenary,
    allowed_passes,
    is_active,
    created_at
) VALUES (
    'scanner1',
    '$2b$12$LKaGPj7QQYHJvZ9X1.vvnO8wYc3YqN6yJxH0vP6eJ5X7.aKZ5YH2m',
    'Gate Operations',
    0,
    'scanner',
    0,
    0,
    0,
    0,
    '{}',
    1,
    datetime('now')
);

-- Verify the user was created
SELECT username, organization, role, is_active FROM users WHERE username = 'scanner1';
