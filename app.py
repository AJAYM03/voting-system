import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
from datetime import datetime
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection, get_elections, get_election_statistics, get_candidates_by_election, update_election_status, get_votes_by_election
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or 'your_default_secret_key'

@app.route('/admin/download_statistics/<string:election_title>')
def download_statistics(election_title):
    statistics = get_election_statistics()
    if election_title not in statistics:
        flash("No statistics found for this election.", "danger")
        return redirect(url_for('view_statistics'))

    output = BytesIO()
    p = canvas.Canvas(output, pagesize=letter)
    p.drawString(100, 750, f"Election Statistics for {election_title}")

    # Draw column headings with adjusted positions
    p.drawString(100, 730, "Candidate Name                     Total Votes")
    y = 710
    for candidate in statistics[election_title]:
        p.drawString(100, y, candidate['candidate_name'])
        p.drawString(350, y, str(candidate['total_votes']))  # Align votes independently
        y -= 20

    p.showPage()
    p.save()
    output.seek(0)
    return send_file(output, as_attachment=True, download_name=f"{election_title}_statistics.pdf", mimetype='application/pdf')

@app.route('/admin/download_all_statistics')
def download_all_statistics():
    statistics = get_election_statistics()
    
    output = BytesIO()
    p = canvas.Canvas(output, pagesize=letter)
    p.drawString(100, 750, "Election Statistics for All Elections")
    p.drawString(100, 730, "Election Title                     Candidate Name                     Total Votes")
    
    y = 710
    for election_title, candidates in statistics.items():
        p.drawString(100, y, election_title)  # Aligning election title
        y -= 20
        for candidate in candidates:
            p.drawString(100, y, '')  # Empty space for alignment under title
            p.drawString(130, y, candidate['candidate_name'])  # Align candidate names under header
            p.drawString(350, y, str(candidate['total_votes']))  # Align votes independently
            y -= 20
        y -= 10  # Additional space between elections

    p.showPage()
    p.save()
    output.seek(0)
    return send_file(output, as_attachment=True, download_name="all_elections_statistics.pdf", mimetype='application/pdf')


@app.route('/auth/logout')
def logout():
    session.clear()  # Clear the session
    flash("You have been logged out.", "success")
    return redirect(url_for('login'))  # Redirect to the login page

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))  # Redirect to the dashboard if logged in
    return redirect(url_for('login'))  # Redirect to login if not logged in

@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user is trying to log in as admin
        if username == Config.DB_USER and password == Config.DB_PASSWORD:
            session['user_id'] = username  # Store the username or an identifier
            session['role'] = 'admin'
            flash("Admin login successful!", "success")
            return redirect(url_for('dashboard'))

        # For regular user login
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user and check_password_hash(user[2], password):  # Updated to index 2 for password
                session['user_id'] = user[0]  # User ID
                session['role'] = user[3]      # User Role
                flash("Login successful!", "success")
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid username or password.", "danger")
        except Exception as e:
            print(f"Error: {e}")
            flash("An error occurred while logging in.", "danger")
        finally:
            cursor.close()
            connection.close()

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_role = session.get('role')
    
    if user_role == 'admin':
        statistics = get_election_statistics()
        return render_template('dashboard.html', role='admin', statistics=statistics)
    
    elif user_role == 'voter':
        elections = get_elections()
        return render_template('dashboard.html', role='voter', elections=elections)

    elif user_role == 'candidate':
        elections = get_elections()
        return render_template('dashboard.html', role='candidate', elections=elections)

    return redirect(url_for('login'))

@app.route('/auth/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        email = request.form['email']
        dob = request.form['dob']  # Get the date of birth

        # Calculate age
        birth_date = datetime.strptime(dob, '%Y-%m-%d')
        age = (datetime.now() - birth_date).days // 365

        if (role == 'voter' and age < 18) or (role == 'candidate' and age < 25):
            flash(f"You must be at least {18 if role == 'voter' else 25} years old to register as a {role}.", "danger")
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, role, email, dob) VALUES (%s, %s, %s, %s, %s)", 
                           (username, hashed_password, role, email, dob))
            connection.commit()
            flash("Registration successful! You can log in now.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            print(f"Error: {e}")
            flash("An error occurred while registering.", "danger")
        finally:
            cursor.close()
            connection.close()

    return render_template('register.html')


@app.route('/admin/create_election', methods=['GET', 'POST'])
def create_election():
    if request.method == 'POST':
        election_name = request.form['name']
        election_date = request.form['date']

        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO elections (title, date, status) VALUES (%s, %s, 'scheduled')", 
                           (election_name, election_date))
            connection.commit()
            flash("Election created successfully!", "success")
            return redirect(url_for('dashboard'))
        except Exception as e:
            print(f"Error: {e}")
            flash("An error occurred while creating the election.", "danger")
        finally:
            cursor.close()
            connection.close()

    return render_template('create_election.html')

@app.route('/candidates/<int:election_id>', methods=['GET'])
def fetch_candidates(election_id):  # Renamed to avoid endpoint conflicts
    candidates = get_candidates_by_election(election_id)
    election_title = None
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT title FROM elections WHERE id = %s", (election_id,))
        election_title = cursor.fetchone()[0]
    except Exception as e:
        print(f"Error fetching election title: {e}")
    finally:
        cursor.close()
        connection.close()

    return jsonify({'candidates': [{'id': c[0], 'name': c[1]} for c in candidates], 'election_title': election_title})

@app.route('/admin/update_election_status', methods=['GET', 'POST'])
def update_election_status_route():
    if request.method == 'POST':
        election_id = request.form['election_id']
        new_status = request.form['new_status']

        update_election_status(election_id, new_status)
        flash("Election status updated successfully!", "success")
        return redirect(url_for('dashboard'))

    elections = get_elections()
    return render_template('update_election_status.html', elections=elections)


@app.route('/candidate/register', methods=['GET', 'POST'])
def register_candidate():
    if request.method == 'POST':
        user_id = session.get('user_id')
        election_id = request.form['election_id']

        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            # Check if the user is already a candidate for this election
            cursor.execute("SELECT * FROM candidates WHERE election_id = %s AND user_id = %s", (election_id, user_id))
            if cursor.fetchone():
                flash("You are already registered as a candidate for this election.", "danger")
                return redirect(url_for('dashboard'))

            # Proceed to register the candidate
            cursor.execute("INSERT INTO candidates (election_id, user_id) VALUES (%s, %s)", 
                           (election_id, user_id))
            connection.commit()
            flash("Candidate registered successfully!", "success")
            return redirect(url_for('dashboard'))
        except Exception as e:
            print(f"Error: {e}")
            flash("An error occurred while registering the candidate.", "danger")
        finally:
            cursor.close()
            connection.close()

    elections = get_elections()
    return render_template('register_candidate.html', elections=elections)


@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        election_id = request.form['election_id']
        candidate_id = request.form['candidate_id']
        user_id = session.get('user_id')

        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            # Check if the user has already voted in this election
            cursor.execute("SELECT * FROM votes WHERE election_id = %s AND user_id = %s", (election_id, user_id))
            if cursor.fetchone():
                flash("You have already voted in this election.", "danger")
                return redirect(url_for('dashboard'))

            # Proceed to cast the vote
            cursor.execute("INSERT INTO votes (election_id, user_id, candidate_id) VALUES (%s, %s, %s)", 
                           (election_id, user_id, candidate_id))
            connection.commit()
            flash("Vote cast successfully!", "success")
            return redirect(url_for('dashboard'))
        except Exception as e:
            print(f"Error: {e}")
            flash("An error occurred while casting your vote.", "danger")
        finally:
            cursor.close()
            connection.close()

    # Retrieve elections for voters to select from
    elections = get_elections()
    return render_template('vote.html', elections=elections)


@app.route('/admin/view_elections')
def view_elections():
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM elections")
        elections = cursor.fetchall()
        return render_template('view_elections.html', elections=elections)
    except Exception as e:
        print(f"Error: {e}")
        flash("An error occurred while retrieving elections.", "danger")
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
