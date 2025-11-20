# Online Voting System

A web-based voting application built with Python (Flask) and MySQL. This system supports role-based access for Administrators, Candidates, and Voters, allowing for secure election management, candidate registration, and voting.

## Features

* **Role-Based Authentication:**
    * **Admin:** Create elections, update election status (Scheduled/Ongoing/Completed), and view/download election statistics.
    * **Candidate:** Register to run in specific elections.
    * **Voter:** View ongoing elections and cast a secure vote (one vote per election per user).
* **Election Management:** Create elections with specific titles and dates.
* **PDF Reporting:** Generate and download election results and statistics as PDF files using ReportLab.
* **Security:** Password hashing using `werkzeug.security`.
* **Validation:** Age restrictions for registration (18+ for voters, 25+ for candidates).

## Tech Stack

* **Backend:** Python (Flask)
* **Database:** MySQL
* **Frontend:** HTML, CSS, Bootstrap 5
* **PDF Generation:** ReportLab
* **Database Driver:** mysql-connector-python

## Installation

### 1. Clone the Repository
```bash
git clone <repository_url>
cd voting-system
