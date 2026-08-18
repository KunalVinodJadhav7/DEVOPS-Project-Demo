-- Create Database (if not exists)
CREATE DATABASE IF NOT EXISTS leave_approval_db;
USE leave_approval_db;

-- 1. Roles Table (Stores the 5-Tier Organizational Hierarchy)
CREATE TABLE IF NOT EXISTS roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL, -- 'employee', 'hr', 'manager', 'admin', 'super_admin'
    description VARCHAR(255)
);

-- Seed Initial Roles
INSERT INTO roles (role_name, description) VALUES 
('employee', 'Standard user who submits and tracks leave requests'),
('hr', 'Tier 2 reviewer for initial HR policy verification'),
('manager', 'Tier 3 reviewer for direct team lead/manager approval'),
('admin', 'Tier 4 department head or admin oversight and final decision'),
('super_admin', 'Tier 5 system infrastructure and notification dispatch control');

-- 2. Users Table (Linked to Roles)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
);

-- 3. Leave Requests Table (Tracks the State Machine Workflow)
CREATE TABLE IF NOT EXISTS leave_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    reason VARCHAR(250) NOT NULL,
    status ENUM('PENDING_HR', 'PENDING_MANAGER', 'PENDING_ADMIN', 'APPROVED', 'REJECTED') DEFAULT 'PENDING_HR',
    document_name VARCHAR(255) DEFAULT NULL,
    hr_comments TEXT DEFAULT NULL,
    manager_comments TEXT DEFAULT NULL,
    admin_notes TEXT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 4. Audit Logs Table (Tracks Multi-Tier Actions for Accountability)
CREATE TABLE IF NOT EXISTS audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    leave_request_id INT NOT NULL,
    actor_id INT NOT NULL,
    action_performed VARCHAR(100) NOT NULL,
    comments TEXT DEFAULT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (leave_request_id) REFERENCES leave_requests(id) ON DELETE CASCADE,
    FOREIGN KEY (actor_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 5. AUTOMATED TRIGGER: Log Status Updates Automatically
DELIMITER //

CREATE TRIGGER after_leave_status_update
AFTER UPDATE ON leave_requests
FOR EACH ROW
BEGIN
    -- Check if the status column has actually changed
    IF OLD.status <> NEW.status THEN
        INSERT INTO audit_logs (leave_request_id, actor_id, action_performed, comments)
        VALUES (
            NEW.id, 
            NEW.employee_id, -- Can be mapped to the specific reviewer ID dynamically in backend if preferred
            CONCAT('STATUS_CHANGE_TO_', NEW.status),
            COALESCE(NEW.admin_notes, NEW.manager_comments, NEW.hr_comments, 'Automated status progression')
        );
    END IF;
END//

DELIMITER ;