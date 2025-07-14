DROP DATABASE IF EXISTS flask_app;
CREATE DATABASE flask_app;
USE flask_app;

CREATE TABLE IF NOT EXISTS user (
    email VARCHAR(255) PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    password VARCHAR(255),
    contact VARCHAR(20),
    upwork_profile TEXT,
    connects_balance INT,
    title VARCHAR(255),
    hourly_rate DECIMAL(10, 2),
    milestone_rate DECIMAL(10, 2)
    is_active TINYINT(1) DEFAULT 1
);


CREATE TABLE IF NOT EXISTS skills_directory (
    skill_version VARCHAR(100) PRIMARY KEY,
    category VARCHAR(100),
    sub_category VARCHAR(100)
);


CREATE TABLE IF NOT EXISTS user_skills (
    email VARCHAR(255),
    skill_version VARCHAR(100),
    proficiency VARCHAR(50),
    PRIMARY KEY (email, skill_version),
    FOREIGN KEY (email) REFERENCES user(email),
    FOREIGN KEY (skill_version) REFERENCES skills_directory(skill_version)
);


CREATE TABLE IF NOT EXISTS relationships (
    user_email VARCHAR(255),
    manager_email VARCHAR(255),
    role VARCHAR(50),
    status VARCHAR(50),
    PRIMARY KEY (user_email, manager_email),
    FOREIGN KEY (user_email) REFERENCES user(email),
    FOREIGN KEY (manager_email) REFERENCES user(email)
);


CREATE TABLE IF NOT EXISTS jobs (
    job_id VARCHAR(100) PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    connects_required INT,
    category VARCHAR(100),
    skills_requested TEXT,
    date_posted DATE,
    deadline DATE,
    stage VARCHAR(100),
    expected_cost DECIMAL(10, 2),
    expected_earning DECIMAL(10, 2),
    client_rating DECIMAL(3, 2),
    feasibility_score DECIMAL(4, 2),
    link VARCHAR(255)
);


CREATE TABLE IF NOT EXISTS proposal (
    owner_email VARCHAR(255),
    job_id VARCHAR(100),
    date DATE,
    status VARCHAR(50) DEFAULT 'pending',  -- e.g., 'pending', 'accepted', 'rejected'
    PRIMARY KEY (owner_email, job_id),
    FOREIGN KEY (owner_email) REFERENCES user(email),
    FOREIGN KEY (job_id) REFERENCES jobs(job_id)
);


CREATE TABLE IF NOT EXISTS project (
    owner_email VARCHAR(255),    
    job_id VARCHAR(100),
    title VARCHAR(255),
    description TEXT,
    created_at DATE,
    PRIMARY KEY (owner_email, job_id),
    FOREIGN KEY (job_id) REFERENCES proposal(job_id),
    FOREIGN KEY (owner_email) REFERENCES proposal(owner_email)
);


CREATE TABLE IF NOT EXISTS tasks (
    owner_email VARCHAR(255),    
    job_id VARCHAR(100),
    assigned_to_email VARCHAR(255),
    created_datetime DATETIME,
    deadline_datetime DATETIME,
    completed_datetime DATETIME,
    priority VARCHAR(50),
    description TEXT,
    PRIMARY KEY (owner_email, job_id, created_datetime),
    FOREIGN KEY (job_id) REFERENCES project(job_id),
    FOREIGN KEY (owner_email) REFERENCES project(owner_email),
    FOREIGN KEY (assigned_to_email) REFERENCES user(email)
);

CREATE TABLE IF NOT EXISTS notification (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_email VARCHAR(255),
    message VARCHAR(255),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_email) REFERENCES user(email)
);

CREATE TABLE IF NOT EXISTS message (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender_email VARCHAR(255),
    receiver_email VARCHAR(255),
    content TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (sender_email) REFERENCES user(email),
    FOREIGN KEY (receiver_email) REFERENCES user(email)
);

SHOW TABLES;

