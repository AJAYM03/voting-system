# Online Voting System  
A secure and scalable web-based voting platform built using **Flask** and **MySQL**, offering role-based access for Administrators, Candidates, and Voters. The system handles the entire election lifecycle from scheduling to vote counting and PDF report generation.

---

## Badges

![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Framework-black.svg)
![MySQL](https://img.shields.io/badge/Database-MySQL-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

---

## Features

### Role-Based Access
- **Admin**
  - Create and schedule elections
  - Manage election statuses (Scheduled, Ongoing, Completed)
  - View dashboards and download statistical PDF reports
- **Candidate**
  - Register and apply to contest in available elections
- **Voter**
  - View ongoing elections
  - Cast a secure, single vote per election

### Core Functionalities
- **One-Time Secure Voting:** Backend validation prevents duplicate voting.
- **PDF Generation:** Election results & stats exported using ReportLab.
- **Age Validation:** 
  - Voter: 18 years minimum  
  - Candidate: 25 years minimum

---

## Tech Stack

| Layer       | Technology |
|-------------|------------|
| Backend     | Python (Flask) |
| Database    | MySQL |
| Frontend    | HTML, CSS, Bootstrap 5 |
| PDF Engine  | ReportLab |
| Driver      | mysql-connector-python |

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository_url>
cd voting-system
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Setup

1. Create a MySQL database named **voting_system**.  
2. Run the SQL schema:

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    email VARCHAR(255),
    dob DATE
);

CREATE TABLE elections (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    status VARCHAR(50) DEFAULT 'scheduled'
);

CREATE TABLE candidates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    election_id INT,
    user_id INT,
    FOREIGN KEY (election_id) REFERENCES elections(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE votes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    election_id INT,
    user_id INT,
    candidate_id INT,
    FOREIGN KEY (election_id) REFERENCES elections(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (candidate_id) REFERENCES candidates(id)
);
```

---

## Configuration

Modify `config.py` as needed:

```python
class Config:
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '1234')
    DB_NAME = os.getenv('DB_NAME', 'voting_system')
```

---

## Running the Application
```bash
python app.py
```

Open in browser:
```
http://127.0.0.1:5000/
```

---

## Usage Guide

### Admin
- Log in with the default admin credentials (in config).
- Create/manage elections and statuses.
- View stats and download PDF reports.

### Candidate
- Register with **Candidate** role.
- Select upcoming election and register as a contestant.

### Voter
- Register with **Voter** role.
- View ongoing elections and vote once per election.

---

## Folder Structure (Recommended)

```
voting-system/
│── app.py
│── config.py
│── requirements.txt
│── static/
│── templates/
│── routes/
│── models/
│── utils/
│── reports/
└── README.md
```

---

## License
This project is released under the **MIT License**.

---

## Contributions
Pull requests are welcome. For major changes, please open an issue first to discuss your ideas.

---

