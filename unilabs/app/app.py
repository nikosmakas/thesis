from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import os
from dotenv import load_dotenv
from models import db, Coursename, Coursetoprof, CourseLab, LabGroup, Professor, RelCourseLab, RelGroupProf, RelGroupStudent, RelLabGroup, RelLabStudent, Student, StudentMissesPerGroup
import re

# Φόρτωση μεταβλητών περιβάλλοντος
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-123')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///labregister.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        am = request.form.get('am')
        password = request.form.get('password')
        user = Student.query.filter_by(am=am).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Επιτυχής σύνδεση!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Λάθος στοιχεία. Προσπαθήστε ξανά.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Αποσυνδεθήκατε.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    lab_groups = LabGroup.query.all()
    professors = Professor.query.all()
    labs = CourseLab.query.all()
    groups = LabGroup.query.all()
    students = Student.query.all()
    registrations = RelLabStudent.query.all()
    absences = StudentMissesPerGroup.query.all()
    # Υπολογισμός πληρότητας για κάθε τμήμα
    for group in groups:
        if hasattr(group, 'capacity') and group.capacity:
            group.occupancy_percentage = (getattr(group, 'enrolled', 0) / group.capacity) * 100
        else:
            group.occupancy_percentage = 0
    return render_template('dashboard.html', 
                         lab_groups=lab_groups,
                         professors=professors,
                         labs=labs,
                         groups=groups,
                         students=students,
                         registrations=registrations,
                         absences=absences)

@app.route('/test-db')
def test_db():
    from models import Student
    students = Student.query.all()
    return '<br>'.join([f"{s.am} - {s.name}" for s in students])

@app.route('/init-db')
def init_db():
    from models import db
    db.create_all()
    sql_path = os.path.join(os.path.dirname(__file__), 'data_labregister.sql')
    with open(sql_path, encoding='utf-8') as f:
        sql = f.read()
    # Βελτιωμένο parsing: split με βάση το ';' αλλά κρατάμε τα multi-line INSERTS
    statements = re.findall(r'(INSERT INTO [^;]+;)', sql, re.DOTALL | re.IGNORECASE)
    conn = db.engine.raw_connection()
    cursor = conn.cursor()
    count_misses = 0
    for stmt in statements:
        try:
            if 'INSERT INTO student_misses_pergroup' in stmt:
                # Σπάσε το multi-row insert σε μεμονωμένα inserts
                prefix = 'INSERT INTO student_misses_pergroup (am, group_id, misses) VALUES'
                values_part = stmt[len(prefix):].strip().rstrip(';')
                rows = [row.strip() for row in values_part.split('),')]
                for row in rows:
                    if not row.endswith(')'):
                        row = row + ')'
                    single_insert = f"{prefix} {row};"
                    try:
                        cursor.execute(single_insert)
                        count_misses += 1
                    except Exception as e:
                        print('SQL error (single-row):', e, '\nStatement:', single_insert)
            else:
                cursor.execute(stmt)
        except Exception as e:
            print('SQL error:', e, '\nStatement:', stmt)
    conn.commit()
    cursor.close()
    conn.close()
    # Debug: εκτύπωσε όλα τα statements που περιέχουν student_misses_pergroup
    debug_misses = [stmt for stmt in statements if 'student_misses_pergroup' in stmt]
    print('DEBUG: Found statements for student_misses_pergroup:', debug_misses)
    return f'Database initialized with all data! INSERTS for student_misses_pergroup: {count_misses}'

@app.route('/labs')
def labs():
    labs = CourseLab.query.all()
    return render_template('labs.html', labs=labs)

@app.route('/groups')
def groups():
    groups = LabGroup.query.all()
    return render_template('groups.html', groups=groups)

@app.route('/students')
def students():
    students = Student.query.all()
    return render_template('students.html', students=students)

@app.route('/professors')
def professors():
    professors = Professor.query.all()
    return render_template('professors.html', professors=professors)

@app.route('/registrations')
def registrations():
    registrations = RelLabStudent.query.all()
    return render_template('registrations.html', registrations=registrations)

@app.route('/absences')
def absences():
    absences = StudentMissesPerGroup.query.all()
    return render_template('absences.html', absences=absences)

@app.route('/test-misses')
def test_misses():
    from models import StudentMissesPerGroup
    misses = StudentMissesPerGroup.query.all()
    return '<br>'.join([f'{m.am} - {m.group_id} - {m.misses}' for m in misses])

if __name__ == '__main__':
    app.run(debug=True) 