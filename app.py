from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "YOUR_OWN_API_KEY"

# Set admin_logged_in to False initially
admin_logged_in = False

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'evs_db'

mysql = MySQL(app)

from flask import session

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if username and password match with records in database
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (username, password))
        admin = cur.fetchone()
        cur.close()
        if admin:
            # Set admin_logged_in to True in the session upon successful login
            session['admin_logged_in'] = True
            # Redirect to admin dashboard
            return redirect(url_for('admin_dashboard'))
        else:
            # If login unsuccessful, display error message
            error = 'Invalid credentials. Please try again.'
    return render_template('admin_login.html', error=error)

# Route for admin dashboard
@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('admin_dashboard.html')


@app.route('/admin/add_election', methods=['GET', 'POST'])
def add_election():
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        election_name = request.form['election_name']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        status = request.form['status']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO elections (election_name, start_date, end_date, status) VALUES (%s, %s, %s, %s)',
                    (election_name, start_date, end_date, status))
        mysql.connection.commit()
        cur.close()

        flash('Election added successfully', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('add_election.html')
 

@app.route('/admin/view_elections')
def view_elections():
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM elections')
    elections = cur.fetchall()
    cur.close()

    return render_template('view_elections.html', elections=elections)

@app.route('/admin/edit_election/<int:election_id>', methods=['GET', 'POST'])
def edit_election(election_id):
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Retrieve form data
        election_name = request.form['election_name']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        status = request.form['status']

        # Update election in the database
        cur = mysql.connection.cursor()
        cur.execute('UPDATE elections SET election_name=%s, start_date=%s, end_date=%s, status=%s WHERE election_id=%s',
                    (election_name, start_date, end_date, status, election_id))
        mysql.connection.commit()
        cur.close()

        flash('Election updated successfully', 'success')
        return redirect(url_for('view_elections'))

    # Fetch the election details from the database to pre-fill the form
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM elections WHERE election_id = %s', (election_id,))
    election = cur.fetchone()
    cur.close()

    return render_template('edit_election.html', election=election)


@app.route('/admin/delete_election/<int:election_id>', methods=['GET', 'POST'])
def delete_election(election_id):
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Delete election from the database
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM elections WHERE election_id = %s', (election_id,))
        mysql.connection.commit()
        cur.close()

        flash('Election deleted successfully', 'success')
        return redirect(url_for('view_elections'))

    # Fetch the election details from the database to display confirmation message
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM elections WHERE election_id = %s', (election_id,))
    election = cur.fetchone()
    cur.close()

    return render_template('delete_election.html', election=election)

import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/candidate_pictures'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/admin/add_candidate', methods=['GET', 'POST'])
def add_candidate():
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    # Fetch all elections for dropdown menu
    cur = mysql.connection.cursor()
    cur.execute('SELECT election_id, election_name FROM elections')
    elections = cur.fetchall()
    cur.close()

    if request.method == 'POST':
        # Check if the post request has the file part
        if 'candidate_picture' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        
        file = request.files['candidate_picture']
        
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            candidate_name = request.form['candidate_name']
            candidate_party = request.form['candidate_party']
            motive = request.form['motive']
            election_id = request.form['election_id']

            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO candidates (candidate_picture, candidate_name, candidate_party, motive, election_id) VALUES (%s, %s, %s, %s, %s)',
                        (filename, candidate_name, candidate_party, motive, election_id))
            mysql.connection.commit()
            cur.close()

            flash('Candidate added successfully', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid file format. Only JPEG, JPG, or PNG files are allowed', 'error')
            return redirect(request.url)

    return render_template('add_candidate.html', elections=elections)

@app.route('/admin/view_candidates')
def view_candidates():
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute('SELECT candidates.*, elections.election_name FROM candidates INNER JOIN elections ON candidates.election_id = elections.election_id')
    candidates = cur.fetchall()
    cur.close()

    return render_template('view_candidates.html', candidates=candidates)

@app.route('/admin/edit_candidate/<int:candidate_id>', methods=['GET', 'POST'])
def edit_candidate(candidate_id):
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    # Fetch all elections for dropdown menu
    cur = mysql.connection.cursor()
    cur.execute('SELECT election_id, election_name FROM elections')
    elections = cur.fetchall()
    cur.close()

    if request.method == 'POST':
        # Retrieve form data
        candidate_name = request.form['candidate_name']
        candidate_party = request.form['candidate_party']
        motive = request.form['motive']
        election_id = request.form['election_id']

        # Update candidate in the database
        cur = mysql.connection.cursor()
        cur.execute('UPDATE candidates SET candidate_name=%s, candidate_party=%s, motive=%s, election_id=%s WHERE candidate_id=%s',
                    (candidate_name, candidate_party, motive, election_id, candidate_id))
        mysql.connection.commit()
        cur.close()

        flash('Candidate updated successfully', 'success')
        return redirect(url_for('view_candidates'))

    # Fetch the candidate details from the database to pre-fill the form
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM candidates WHERE candidate_id = %s', (candidate_id,))
    candidate = cur.fetchone()
    cur.close()

    return render_template('edit_candidate.html', candidate=candidate, elections=elections)


from werkzeug.security import generate_password_hash

@app.route('/admin/add_voter', methods=['GET', 'POST'])
def add_voter():
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Retrieve form data
        voter_name = request.form['voter_name']
        username = request.form['username']
        password = generate_password_hash(request.form['password'])  # Hash the password for security

        # Insert voter into the database
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO voters (voter_name, username, password) VALUES (%s, %s, %s)',
                    (voter_name, username, password))
        mysql.connection.commit()
        cur.close()

        flash('Voter added successfully', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('add_voter.html')


@app.route('/admin/delete_candidate/<int:candidate_id>', methods=['GET', 'POST'])
def delete_candidate(candidate_id):
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Delete candidate from the database
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM candidates WHERE candidate_id = %s', (candidate_id,))
        mysql.connection.commit()
        cur.close()

        flash('Candidate deleted successfully', 'success')
        return redirect(url_for('view_candidates'))

    # Fetch the candidate details from the database to display confirmation message
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM candidates WHERE candidate_id = %s', (candidate_id,))
    candidate = cur.fetchone()
    cur.close()

    return render_template('delete_candidate.html', candidate=candidate)

@app.route('/admin/view_voters')
def view_voters():
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM voters')
    voters = cur.fetchall()
    cur.close()

    return render_template('view_voters.html', voters=voters)

@app.route('/admin/edit_voter/<int:voter_id>', methods=['GET', 'POST'])
def edit_voter(voter_id):
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Retrieve form data
        voter_name = request.form['voter_name']
        username = request.form['username']

        # Update voter in the database
        cur = mysql.connection.cursor()
        cur.execute('UPDATE voters SET voter_name=%s, username=%s WHERE voter_id=%s',
                    (voter_name, username, voter_id))
        mysql.connection.commit()
        cur.close()

        flash('Voter updated successfully', 'success')
        return redirect(url_for('view_voters'))

    # Fetch the voter details from the database to pre-fill the form
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM voters WHERE voter_id = %s', (voter_id,))
    voter = cur.fetchone()
    cur.close()

    return render_template('edit_voter.html', voter=voter)

@app.route('/admin/delete_voter/<int:voter_id>', methods=['GET', 'POST'])
def delete_voter(voter_id):
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Delete voter from the database
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM voters WHERE voter_id = %s', (voter_id,))
        mysql.connection.commit()
        cur.close()

        flash('Voter deleted successfully', 'success')
        return redirect(url_for('view_voters'))

    # Fetch the voter details from the database to display confirmation message
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM voters WHERE voter_id = %s', (voter_id,))
    voter = cur.fetchone()
    cur.close()

    return render_template('delete_voter.html', voter=voter)

from werkzeug.security import generate_password_hash

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Retrieve form data
        voter_name = request.form['voter_name']
        username = request.form['username']
        password = generate_password_hash(request.form['password'])  # Hash the password for security

        # Check if the username is already taken
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM voters WHERE username = %s', (username,))
        existing_user = cur.fetchone()
        cur.close()

        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('register'))

        # Insert voter into the database
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO voters (voter_name, username, password) VALUES (%s, %s, %s)',
                    (voter_name, username, password))
        mysql.connection.commit()
        cur.close()

        flash('Registration successful. You can now login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

from werkzeug.security import check_password_hash

@app.route('/voter_login', methods=['GET', 'POST'])
def voter_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username exists in the database
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM voters WHERE username = %s', (username,))
        voter = cur.fetchone()
        cur.close()

        if voter and check_password_hash(voter[3], password):  # Check if password matches
            session['voter_id'] = voter[0]  # Store voter ID in session
            flash('Login successful. Welcome, {}!'.format(voter[1]), 'success')
            return redirect(url_for('voter_dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
            return redirect(url_for('voter_login'))

    return render_template('voter_login.html')


@app.route('/voter_dashboard')
def voter_dashboard():
    if 'voter_id' not in session:
        flash('You must login first.', 'error')
        return redirect(url_for('voter_login'))

    # Retrieve all elections from the database
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM elections')
    elections = cur.fetchall()
    cur.close()

    return render_template('voter_dashboard.html', elections=elections)

from werkzeug.security import generate_password_hash

@app.route('/voter_profile', methods=['GET', 'POST'])
def voter_profile():
    if 'voter_id' not in session:
        flash('You must login first.', 'error')
        return redirect(url_for('voter_login'))

    if request.method == 'POST':
        voter_name = request.form['voter_name']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            flash('Password and confirm password do not match.', 'error')
            return redirect(url_for('voter_profile'))

        # Hash the new password
        hashed_password = generate_password_hash(new_password)

        # Update voter's name and password in the database
        cur = mysql.connection.cursor()
        cur.execute('UPDATE voters SET voter_name=%s, password=%s WHERE voter_id=%s',
                    (voter_name, hashed_password, session['voter_id']))
        mysql.connection.commit()
        cur.close()

        flash('Profile updated successfully.', 'success')
        return redirect(url_for('voter_dashboard'))

    # Retrieve voter information from the database based on the session voter_id
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM voters WHERE voter_id = %s', (session['voter_id'],))
    voter = cur.fetchone()
    cur.close()

    return render_template('voter_profile.html', voter=voter)



from flask import request
import time
from blockchain import Block, Blockchain  # Importing Block and Blockchain classes from blockchain.py

# Assuming you have already initialized the Blockchain instance somewhere in your code
blockchain = Blockchain()
from datetime import datetime
from flask import flash

@app.route('/voter_view_candidates/<int:election_id>', methods=['GET', 'POST'])
def voter_view_candidates(election_id):
    if 'voter_id' not in session:
        flash('You must log in first.', 'error')
        return redirect(url_for('voter_login'))

    # Retrieve election details from the database
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM elections WHERE election_id = %s', (election_id,))
    election = cur.fetchone()
    cur.close()

    if not election:
        flash('This election does not exist.', 'error')
        return redirect(url_for('voter_dashboard'))

    # Check if the election is ongoing
    if election[2] != 'ongoing':
        flash('You cannot vote in this election.', 'error')

    # Check if the voter has already cast a vote in this election
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM votes WHERE voter_id = %s AND election_id = %s', (session['voter_id'], election_id))
    existing_vote = cur.fetchone()
    cur.close()

    if request.method == 'POST':
        if existing_vote:
            flash('You have already casted your vote in this election. You cannot vote again.', 'error')
            return redirect(url_for('voter_dashboard'))

        candidate_id = request.form['candidate_id']
        current_timestamp = datetime.now()
        # Generate block for blockchain
        new_block = Block(len(blockchain.chain), {'voter_id': session['voter_id'], 'candidate_id': candidate_id, 'timestamp': current_timestamp}, current_timestamp, blockchain.get_last_block().hash)
        blockchain.add_block(new_block)
        # Save vote details in the database
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO votes (voter_id, candidate_id, election_id, timestamp, block_id, block_hash, previous_block_hash) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    (session['voter_id'], candidate_id, election_id, current_timestamp, new_block.index, new_block.hash, new_block.previous_hash))
        mysql.connection.commit()
        cur.close()
        flash('Your vote has been casted successfully.', 'success')
        return redirect(url_for('voter_dashboard'))

    # Retrieve all candidates for the election from the database
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM candidates WHERE election_id = %s', (election_id,))
    candidates = cur.fetchall()
    cur.close()

    return render_template('voter_view_candidates.html', election=election, candidates=candidates, existing_vote=existing_vote)

from flask import render_template

@app.route('/voter_view_results')
def voter_view_results():
    if 'voter_id' not in session:
        flash('You must log in first.', 'error')
        return redirect(url_for('voter_login'))

    # Retrieve completed elections from the database
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM elections WHERE status = "completed"')
    completed_elections = cur.fetchall()

    election_results = []

    for election in completed_elections:
        # Retrieve candidates and their votes for each completed election
        cur.execute('SELECT candidates.candidate_name, COUNT(votes.candidate_id) as votes_taken FROM candidates LEFT JOIN votes ON candidates.candidate_id = votes.candidate_id WHERE candidates.election_id = %s GROUP BY candidates.candidate_id', (election[0],))
        results = cur.fetchall()
        election_results.append({'election': election, 'results': results})

    cur.close()

    return render_template('voter_view_results.html', election_results=election_results)

from flask import render_template

@app.route('/admin/view_votes')
def admin_view_votes():
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    # Retrieve all votes with related names from the database
    cur = mysql.connection.cursor()
    cur.execute('SELECT votes.*, voters.voter_name, candidates.candidate_name, elections.election_name FROM votes JOIN voters ON votes.voter_id = voters.voter_id JOIN candidates ON votes.candidate_id = candidates.candidate_id JOIN elections ON votes.election_id = elections.election_id')
    votes = cur.fetchall()
    cur.close()

    return render_template('view_votes.html', votes=votes)



@app.route('/admin/admin_view_results')
def admin_view_results():
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))

    # Retrieve completed elections from the database
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM elections WHERE status = "completed"')
    completed_elections = cur.fetchall()

    election_results = []

    for election in completed_elections:
        # Retrieve candidates and their votes for each completed election
        cur.execute('SELECT candidates.candidate_name, COUNT(votes.candidate_id) as votes_taken FROM candidates LEFT JOIN votes ON candidates.candidate_id = votes.candidate_id WHERE candidates.election_id = %s GROUP BY candidates.candidate_id', (election[0],))
        results = cur.fetchall()
        election_results.append({'election': election, 'results': results})

    cur.close()

    return render_template('admin_view_results.html', election_results=election_results)


@app.route('/voter_logout')
def voter_logout():
    # Remove voter_id from the session upon logout
    session.pop('voter_id', None)
    # Redirect to the login page after logging out
    return redirect(url_for('voter_login'))


# Route for logout
@app.route('/logout')
def logout():
    # Remove admin_logged_in from the session upon logout
    session.pop('admin_logged_in', None)
    # Redirect to the login page after logging out
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

    