from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory, abort
import os
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database path
DATABASE = 'users.db'

# Initialize the database
def initialize_database():
    init_db()


def init_db():
    """Initialize the SQLite database and create necessary tables."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )''')
    
    # Create employee directory table
    cursor.execute('''CREATE TABLE IF NOT EXISTS employee_directory (
        employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        department TEXT,
        job_title TEXT,
        phone_number TEXT,
        address TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')

    # Create uploads table
    cursor.execute('''CREATE TABLE IF NOT EXISTS uploads (
        upload_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        filename TEXT,
        upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')

    # Check if the payroll table exists with the old schema
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='payroll'")
    if cursor.fetchone():
        # Get the current schema
        cursor.execute("PRAGMA table_info(payroll)")
        columns = [row[1] for row in cursor.fetchall()]
        
        # If the old columns exist, perform schema migration
        if 'deductions' in columns or 'bonus' in columns or 'pay_date' in columns:
            # Rename old table
            cursor.execute("ALTER TABLE payroll RENAME TO payroll_old")

            # Create new table without the unwanted columns
            cursor.execute('''CREATE TABLE payroll (
                payroll_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                salary REAL NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )''')

            # Copy relevant data from old table to new table
            cursor.execute('''INSERT INTO payroll (user_id, salary)
                               SELECT user_id, salary FROM payroll_old''')

            # Drop the old table
            cursor.execute("DROP TABLE payroll_old")
    else:
        # If the payroll table doesn't exist, create it directly with the new schema
        cursor.execute('''CREATE TABLE payroll (
            payroll_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            salary REAL NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )''')

    # Create leave management table
    cursor.execute('''CREATE TABLE IF NOT EXISTS leave_management (
        leave_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        leave_type TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        status TEXT CHECK(status IN ('Pending', 'Approved', 'Rejected')) DEFAULT 'Pending',
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS uploads (
        upload_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        filename TEXT,
        upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('UserProfile'))
    return render_template('homePage.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['user_pwd']
        confirm_password = request.form['user_pwd1']
        
        if password != confirm_password:
            return "Passwords do not match.", 400

        hashed_password = generate_password_hash(password)
        
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed_password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return "Email already registered.", 400
    
    return render_template('Register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('UserProfile'))
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['user_pwd0']
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user[3], password):  # user[3] is the hashed password
            session['user_id'] = user[0]  # Store user_id in session
            session['username'] = user[1]  # Store the name in the session
            return redirect(url_for('UserProfile'))
        else:
            return "Invalid email or password.", 401
    
    return render_template('Login.html')

@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    email = request.form.get('email')
    
    # Add logic for password recovery here (e.g., sending an email)
    print(f"Password recovery for: {email}")
    return redirect(url_for('login'))


# File Upload Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if the uploaded file is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/UserProfile')
def UserProfile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('UserProfile.html', username=session['username'])

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload."""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'No file selected for uploading', 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # To ensure unique filenames, prepend user_id and timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"user_{user_id}_{timestamp}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Save file info to the database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO uploads (user_id, filename)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                filename=excluded.filename,
                upload_time=excluded.upload_time
        ''', (user_id, filename))
        conn.commit()
        conn.close()
        
        return 'CV uploaded successfully.', 200
    else:
        return 'Invalid file type. Please upload a valid file.', 400

@app.route('/save_employee_details', methods=['POST'])
def save_employee_details():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    department = request.form['department']
    job_title = request.form['job_title']
    phone_number = request.form['phone_number']
    address = request.form['address']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO employee_directory (user_id, department, job_title, phone_number, address)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            department=excluded.department,
            job_title=excluded.job_title,
            phone_number=excluded.phone_number,
            address=excluded.address
    ''', (user_id, department, job_title, phone_number, address))
    conn.commit()
    conn.close()

    return 'Employee details saved successfully.', 200

@app.route('/save_payroll', methods=['POST'])
def save_payroll():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    salary = request.form['salary']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO payroll (user_id, salary)
        VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            salary=excluded.salary
    ''', (user_id, salary))
    conn.commit()
    conn.close()

    return 'Payroll details saved successfully.', 200

@app.route('/display_info', methods=['GET'])
def display_info():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Fetch CV filename
    cursor.execute("SELECT filename FROM uploads WHERE user_id = ?", (user_id,))
    cv = cursor.fetchone()

    # Fetch employee details
    cursor.execute('''
        SELECT department, job_title, phone_number, address
        FROM employee_directory WHERE user_id = ?
    ''', (user_id,))
    employee_details = cursor.fetchone()

    # Fetch payroll details
    cursor.execute('SELECT salary FROM payroll WHERE user_id = ?', (user_id,))
    payroll = cursor.fetchone()

    conn.close()

    # Generate CV URL if exists
    cv_url = url_for('uploaded_file', filename=cv[0]) if cv else None

    return jsonify({
        'cv': cv_url,
        'department': employee_details[0] if employee_details else "N/A",
        'job_title': employee_details[1] if employee_details else "N/A",
        'phone_number': employee_details[2] if employee_details else "N/A",
        'address': employee_details[3] if employee_details else "N/A",
        'salary': payroll[0] if payroll else "N/A"
    })

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    if 'user_id' not in session:
        abort(403)
    
    user_id = session['user_id']
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT filename FROM uploads WHERE user_id = ?", (user_id,))
    cv = cursor.fetchone()
    conn.close()
    
    if cv and cv[0] == filename:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    else:
        abort(403)

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)  # Remove the username from session to log out
    return redirect(url_for('login')) 

if __name__ == '__main__':
    app.run(debug=True)
