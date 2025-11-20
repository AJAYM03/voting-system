````markdown
# Online Voting System

A secure, web-based voting application built with Python (Flask) and MySQL. This system supports role-based access for Administrators, Candidates, and Voters, facilitating the entire election lifecycle from scheduling to reporting results.

## 🚀 Features

* **Role-Based Authentication:**
    * **Admin:** Schedule elections, update statuses (Scheduled/Ongoing/Completed), and download statistical reports.
    * **Candidate:** Register to run in specific upcoming elections.
    * **Voter:** View ongoing elections and cast secure, one-time votes.
* **Secure Voting:** Backend logic ensures one person can only vote once per election.
* **PDF Reporting:** Generate and download election results and statistics as PDF files using ReportLab.
* **Smart Validation:** Age restrictions enforced during registration (18+ for voters, 25+ for candidates).

## 🛠️ Tech Stack

* **Backend:** Python (Flask)
* **Database:** MySQL
* **Frontend:** HTML, CSS, Bootstrap 5
* **PDF Generation:** ReportLab
* **Database Driver:** mysql-connector-python

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository_url>
cd voting-system
````

### 2\. Install Dependencies

Ensure you have Python installed, then run:

```bash
pip install -r requirements.txt
```

### 3\. Database Setup

1.  Create a MySQL database named `voting_system` (or update `config.py`).
2.  Execute the following SQL commands to create the required tables:

<!-- end list -->

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

### 4\. Configuration

Update the `config.py` file with your database credentials if they differ from the defaults:

```python
class Config:
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '1234')
    DB_NAME = os.getenv('DB_NAME', 'voting_system')
```

### 5\. Run the Application

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000/`.

## 📖 Usage Guide

1.  **Admin Access:**
      * Log in using the credentials defined in `config.py` (Default: User `root`, Password `1234`) to access the Admin Dashboard.
      * Create new elections and manage their status.
2.  **Candidate Registration:**
      * Register a new account with the role **Candidate**.
      * Select an election from the dashboard to register as a candidate.
3.  **Voting:**
      * Register a new account with the role **Voter**.
      * Select an ongoing election and cast your vote for a candidate.
4.  **View Results:**
      * Admins can view real-time statistics and download PDF reports from the dashboard.

<!-- end list -->

```
```
