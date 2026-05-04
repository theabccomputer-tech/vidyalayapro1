from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, date, timedelta
from functools import wraps
import json, os, random, uuid
# License system integrated below

app = Flask(__name__)
app.secret_key = 'SchoolERP@2025SecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school_erp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# School classes by edition type
CLASSES_PRIMARY = ['Nursery', 'LKG', 'UKG', '1', '2', '3', '4', '5']
CLASSES_MIDDLE  = ['Nursery', 'LKG', 'UKG', '1', '2', '3', '4', '5', '6', '7', '8']
CLASSES_SENIOR  = ['Nursery', 'LKG', 'UKG', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

def get_classes():
    try:
        s = SchoolSettings.query.first()
        t = s.school_type if s else 'senior'
        if t == 'primary': return CLASSES_PRIMARY
        elif t == 'middle': return CLASSES_MIDDLE
        else: return CLASSES_SENIOR
    except:
        return CLASSES_SENIOR
db = SQLAlchemy(app)

# ══════════════════════════════════════════════
# MODELS
# ══════════════════════════════════════════════

class SchoolSettings(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    school_name   = db.Column(db.String(200), default='Vidyalaya Pro School')
    school_address= db.Column(db.Text,        default='')
    school_phone  = db.Column(db.String(20),  default='')
    school_email  = db.Column(db.String(100), default='')
    affiliation   = db.Column(db.String(100), default='CBSE')
    academic_year = db.Column(db.String(20),  default='2024-25')
    school_logo   = db.Column(db.String(200), default='')
    school_photo  = db.Column(db.String(200), default='')
    school_name_hindi = db.Column(db.String(200), default='')
    school_code   = db.Column(db.String(50),  default='')
    school_city   = db.Column(db.String(50),  default='')
    school_state  = db.Column(db.String(50),  default='')
    school_pincode= db.Column(db.String(10),  default='')
    established_year = db.Column(db.String(10), default='')
    principal_phone  = db.Column(db.String(20), default='')
    working_days  = db.Column(db.String(5),   default='6')
    school_start_time = db.Column(db.String(10), default='08:00')
    school_end_time   = db.Column(db.String(10), default='14:30')
    year_start    = db.Column(db.String(20),  default='')
    year_end      = db.Column(db.String(20),  default='')
    school_banner = db.Column(db.String(200), default='')
    principal_name= db.Column(db.String(100), default='')
    principal_photo=db.Column(db.String(200), default='')
    school_tagline= db.Column(db.String(200), default='')
    facebook_url  = db.Column(db.String(200), default='')
    website_url   = db.Column(db.String(200), default='')
    license_key   = db.Column(db.Text,        default='')
    license_status= db.Column(db.String(20),  default='inactive')
    theme         = db.Column(db.String(10),  default='dark')
    dashboard_layout = db.Column(db.Text,     default='')
    school_type      = db.Column(db.String(20), default='senior')
    accent_color     = db.Column(db.String(20),  default='#6c63ff')
    theme_preset     = db.Column(db.String(20),  default='dark')

class User(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    username   = db.Column(db.String(50),  unique=True, nullable=False)
    password   = db.Column(db.String(256), nullable=False)
    role       = db.Column(db.String(20),  nullable=False)
    name       = db.Column(db.String(100))
    email      = db.Column(db.String(100))
    phone      = db.Column(db.String(20))
    photo      = db.Column(db.String(200), default='')
    created_at = db.Column(db.DateTime,   default=datetime.utcnow)
    is_active  = db.Column(db.Boolean,    default=True)

class Student(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'))
    admission_no    = db.Column(db.String(20), unique=True)
    name            = db.Column(db.String(100), nullable=False)
    name_hindi      = db.Column(db.String(100), default='')
    class_name      = db.Column(db.String(20))
    section         = db.Column(db.String(5))
    roll_no         = db.Column(db.Integer)
    dob             = db.Column(db.String(20))
    gender          = db.Column(db.String(10))
    blood_group     = db.Column(db.String(5),  default='')
    religion        = db.Column(db.String(30), default='')
    caste           = db.Column(db.String(30), default='')
    category        = db.Column(db.String(10), default='General')
    nationality     = db.Column(db.String(30), default='Indian')
    aadhaar_no      = db.Column(db.String(20), default='')
    address         = db.Column(db.Text)
    city            = db.Column(db.String(50), default='')
    state           = db.Column(db.String(50), default='')
    pincode         = db.Column(db.String(10), default='')
    father_name     = db.Column(db.String(100), default='')
    father_phone    = db.Column(db.String(20),  default='')
    father_occupation=db.Column(db.String(100), default='')
    father_email    = db.Column(db.String(100), default='')
    mother_name     = db.Column(db.String(100), default='')
    mother_phone    = db.Column(db.String(20),  default='')
    mother_occupation=db.Column(db.String(100), default='')
    guardian_name   = db.Column(db.String(100), default='')
    guardian_phone  = db.Column(db.String(20),  default='')
    guardian_relation=db.Column(db.String(50),  default='')
    parent_name     = db.Column(db.String(100), default='')
    parent_phone    = db.Column(db.String(20),  default='')
    parent_email    = db.Column(db.String(100), default='')
    previous_school = db.Column(db.String(200), default='')
    admission_date  = db.Column(db.String(20),  default='')
    fee_status      = db.Column(db.String(20),  default='pending')
    photo           = db.Column(db.String(200), default='')
    transport_route = db.Column(db.String(100), default='')
    medical_condition=db.Column(db.Text,        default='')
    emergency_contact=db.Column(db.String(20),  default='')
    house           = db.Column(db.String(30),  default='')
    created_at      = db.Column(db.DateTime,   default=datetime.utcnow)
    is_active       = db.Column(db.Boolean,    default=True)

class Teacher(db.Model):
    id               = db.Column(db.Integer, primary_key=True)
    user_id          = db.Column(db.Integer, db.ForeignKey('user.id'))
    employee_id      = db.Column(db.String(20), unique=True)
    name             = db.Column(db.String(100), nullable=False)
    name_hindi       = db.Column(db.String(100), default='')
    subject          = db.Column(db.String(50))
    subjects_taught  = db.Column(db.String(200), default='')
    class_assigned   = db.Column(db.String(20))
    classes_taught   = db.Column(db.String(200), default='')
    designation      = db.Column(db.String(100), default='Teacher')
    department       = db.Column(db.String(50),  default='')
    qualification    = db.Column(db.String(200))
    specialization   = db.Column(db.String(100), default='')
    experience_years = db.Column(db.Integer,     default=0)
    phone            = db.Column(db.String(20))
    alt_phone        = db.Column(db.String(20),  default='')
    email            = db.Column(db.String(100))
    aadhaar_no       = db.Column(db.String(20),  default='')
    pan_no           = db.Column(db.String(15),  default='')
    dob              = db.Column(db.String(20),  default='')
    gender           = db.Column(db.String(10),  default='')
    blood_group      = db.Column(db.String(5),   default='')
    address          = db.Column(db.Text,        default='')
    city             = db.Column(db.String(50),  default='')
    state            = db.Column(db.String(50),  default='')
    salary           = db.Column(db.Float,       default=0)
    bank_name        = db.Column(db.String(100), default='')
    account_no       = db.Column(db.String(30),  default='')
    ifsc             = db.Column(db.String(15),  default='')
    join_date        = db.Column(db.String(20))
    photo            = db.Column(db.String(200), default='')
    is_active        = db.Column(db.Boolean,     default=True)

class Attendance(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    date       = db.Column(db.String(20))
    status     = db.Column(db.String(20))
    marked_by  = db.Column(db.Integer)
    note       = db.Column(db.String(100), default='')

class Fee(db.Model):
    id             = db.Column(db.Integer, primary_key=True)
    student_id     = db.Column(db.Integer, db.ForeignKey('student.id'))
    fee_type       = db.Column(db.String(50))
    amount         = db.Column(db.Float)
    paid_amount    = db.Column(db.Float, default=0)
    discount       = db.Column(db.Float, default=0)
    due_date       = db.Column(db.String(20))
    paid_date      = db.Column(db.String(20))
    payment_mode   = db.Column(db.String(30), default='Cash')
    transaction_id = db.Column(db.String(50), default='')
    status         = db.Column(db.String(20), default='pending')
    receipt_no     = db.Column(db.String(20))
    remarks        = db.Column(db.String(200), default='')

class Exam(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(100))
    class_name    = db.Column(db.String(20))
    subject       = db.Column(db.String(50))
    date          = db.Column(db.String(20))
    time          = db.Column(db.String(20), default='')
    room          = db.Column(db.String(30), default='')
    max_marks     = db.Column(db.Integer)
    passing_marks = db.Column(db.Integer, default=33)
    created_by    = db.Column(db.Integer)

class Result(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    exam_id    = db.Column(db.Integer, db.ForeignKey('exam.id'))
    marks      = db.Column(db.Float)
    grade      = db.Column(db.String(5))
    remarks    = db.Column(db.String(100), default='')

class Notice(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    title      = db.Column(db.String(200))
    content    = db.Column(db.Text)
    target     = db.Column(db.String(20), default='all')
    priority   = db.Column(db.String(10), default='normal')
    created_by = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active  = db.Column(db.Boolean,  default=True)

class Timetable(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(20))
    section    = db.Column(db.String(5))
    day        = db.Column(db.String(15))
    period     = db.Column(db.Integer)
    subject    = db.Column(db.String(50))
    teacher_id = db.Column(db.Integer)
    start_time = db.Column(db.String(10))
    end_time   = db.Column(db.String(10))

class Book(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    title        = db.Column(db.String(200))
    author       = db.Column(db.String(100))
    isbn         = db.Column(db.String(20))
    category     = db.Column(db.String(50))
    publisher    = db.Column(db.String(100), default='')
    edition      = db.Column(db.String(20),  default='')
    year         = db.Column(db.String(10),  default='')
    total_copies = db.Column(db.Integer, default=1)
    available    = db.Column(db.Integer, default=1)

class BookIssue(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    book_id     = db.Column(db.Integer, db.ForeignKey('book.id'))
    student_id  = db.Column(db.Integer, db.ForeignKey('student.id'))
    issue_date  = db.Column(db.String(20))
    due_date    = db.Column(db.String(20))
    return_date = db.Column(db.String(20))
    fine        = db.Column(db.Float, default=0)
    status      = db.Column(db.String(20), default='issued')

class Transport(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    route_name   = db.Column(db.String(100))
    driver_name  = db.Column(db.String(100))
    driver_phone = db.Column(db.String(20),  default='')
    helper_name  = db.Column(db.String(100), default='')
    vehicle_no   = db.Column(db.String(20))
    vehicle_type = db.Column(db.String(30),  default='Bus')
    capacity     = db.Column(db.Integer)
    fee          = db.Column(db.Float)
    stops        = db.Column(db.Text,        default='')
    morning_time = db.Column(db.String(10),  default='')
    evening_time = db.Column(db.String(10),  default='')

class Homework(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer)
    class_name = db.Column(db.String(20))
    subject    = db.Column(db.String(50))
    title      = db.Column(db.String(200))
    description= db.Column(db.Text)
    due_date   = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Enquiry(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    student_name    = db.Column(db.String(100))
    class_applying  = db.Column(db.String(20))
    dob             = db.Column(db.String(20),  default='')
    gender          = db.Column(db.String(10),  default='')
    parent_name     = db.Column(db.String(100))
    relation        = db.Column(db.String(20),  default='Father')
    phone           = db.Column(db.String(20))
    alt_phone       = db.Column(db.String(20),  default='')
    email           = db.Column(db.String(100))
    address         = db.Column(db.Text,        default='')
    previous_school = db.Column(db.String(200), default='')
    reference       = db.Column(db.String(100), default='')
    status          = db.Column(db.String(20),  default='new')
    follow_up_date  = db.Column(db.String(20),  default='')
    notes           = db.Column(db.Text)
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)

class StaffLeave(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer)
    leave_type = db.Column(db.String(30))
    from_date  = db.Column(db.String(20))
    to_date    = db.Column(db.String(20))
    reason     = db.Column(db.Text)
    status     = db.Column(db.String(20), default='pending')
    applied_on = db.Column(db.DateTime,  default=datetime.utcnow)

class Event(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    title      = db.Column(db.String(200))
    description= db.Column(db.Text,        default='')
    event_date = db.Column(db.String(20))
    event_type = db.Column(db.String(30),  default='General')
    venue      = db.Column(db.String(100), default='')
    photo      = db.Column(db.String(200), default='')
    created_by = db.Column(db.Integer)
    created_at = db.Column(db.DateTime,   default=datetime.utcnow)

class AuditLog(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer)
    action     = db.Column(db.String(200))
    module     = db.Column(db.String(50))
    timestamp  = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(50))

# ══════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════

def allowed_file(f):
    return '.' in f and f.rsplit('.', 1)[1].lower() in ALLOWED_EXT

def save_photo(file, folder='students'):
    if file and file.filename and allowed_file(file.filename):
        ext  = file.filename.rsplit('.', 1)[1].lower()
        fname = str(uuid.uuid4()) + '.' + ext
        path = os.path.join(app.config['UPLOAD_FOLDER'], folder)
        os.makedirs(path, exist_ok=True)
        file.save(os.path.join(path, fname))
        return f'uploads/{folder}/{fname}'
    return ''

def login_required(f):
    @wraps(f)
    def w(*a, **k):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*a, **k)
    return w

def admin_required(f):
    @wraps(f)
    def w(*a, **k):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if session.get('role') not in ['admin','superadmin']:
            flash('Admin access required.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*a, **k)
    return w

def super_required(f):
    @wraps(f)
    def w(*a, **k):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if session.get('role') != 'superadmin':
            flash('Super Admin access required.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*a, **k)
    return w

def log_action(action, module):
    try:
        db.session.add(AuditLog(user_id=session.get('user_id'), action=action,
                                module=module, ip_address=request.remote_addr))
        db.session.commit()
    except: pass

def get_grade(marks, max_marks):
    p = (marks / max_marks * 100) if max_marks else 0
    return 'A+' if p>=90 else 'A' if p>=80 else 'B+' if p>=70 else 'B' if p>=60 else 'C' if p>=50 else 'D' if p>=33 else 'F'

def get_settings():
    s = SchoolSettings.query.first()
    if not s:
        s = SchoolSettings()
        db.session.add(s); db.session.commit()
    return s

@app.context_processor
def inject_globals():
    try:
        s = get_settings()
        classes = get_classes()
        is_super = session.get('role') == 'superadmin'
        accent   = s.accent_color or '#6c63ff'
        preset   = s.theme_preset or 'dark'
        return dict(gs=s, theme=s.theme, all_classes=classes,
                    is_super=is_super, accent_color=accent, theme_preset=preset)
    except:
        return dict(gs=None, theme='dark', all_classes=CLASSES_SENIOR,
                    is_super=False, accent_color='#6c63ff', theme_preset='dark')

# ══════════════════════════════════════════════
# AUTH
# ══════════════════════════════════════════════

@app.route('/')
def index():
    return redirect(url_for('dashboard') if 'user_id' in session else url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = User.query.filter_by(username=request.form['username'], is_active=True).first()
        if u and check_password_hash(u.password, request.form['password']):
            session.update({'user_id':u.id,'username':u.username,'role':u.role,'name':u.name,'photo':u.photo})
            log_action(f'Login: {u.username}', 'Auth')
            return redirect(url_for('dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    log_action('Logout', 'Auth'); session.clear()
    return redirect(url_for('login'))

# ══════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════

@app.route('/dashboard')
@login_required
def dashboard():
    today = date.today().strftime('%Y-%m-%d')
    stats = {
        'total_students': Student.query.filter_by(is_active=True).count(),
        'total_teachers': Teacher.query.filter_by(is_active=True).count(),
        'total_fees': float(db.session.query(db.func.sum(Fee.paid_amount)).scalar() or 0),
        'pending_fees': Fee.query.filter_by(status='pending').count(),
        'today_present': Attendance.query.filter_by(date=today, status='present').count(),
        'today_absent': Attendance.query.filter_by(date=today, status='absent').count(),
        'upcoming_exams': Exam.query.filter(Exam.date >= today).count(),
        'new_enquiries': Enquiry.query.filter_by(status='new').count(),
        'library_books': Book.query.count(),
        'total_events': Event.query.count(),
    }
    notices         = Notice.query.filter_by(is_active=True).order_by(Notice.created_at.desc()).limit(5).all()
    recent_students = Student.query.filter_by(is_active=True).order_by(Student.created_at.desc()).limit(5).all()
    upcoming_exams  = Exam.query.filter(Exam.date >= today).order_by(Exam.date).limit(5).all()
    recent_fees     = db.session.query(Fee, Student).join(Student, Fee.student_id==Student.id).order_by(Fee.id.desc()).limit(5).all()
    upcoming_events = Event.query.filter(Event.event_date >= today).order_by(Event.event_date).limit(4).all()
    s               = get_settings()
    layout          = json.loads(s.dashboard_layout) if s.dashboard_layout else \
                      ['stats','att_chart','fee_chart','recent_students','notices','upcoming_exams','recent_fees','events']
    return render_template('dashboard.html', stats=stats, notices=notices,
                           recent_students=recent_students, upcoming_exams=upcoming_exams,
                           recent_fees=recent_fees, upcoming_events=upcoming_events,
                           layout=layout, today=today)

@app.route('/dashboard/save-layout', methods=['POST'])
@login_required
def save_dashboard_layout():
    s = get_settings(); s.dashboard_layout = json.dumps(request.json.get('layout',[])); db.session.commit()
    return jsonify({'ok':True})

@app.route('/dashboard/toggle-theme', methods=['POST'])
@login_required
def toggle_theme():
    s = get_settings(); s.theme = 'light' if s.theme=='dark' else 'dark'; db.session.commit()
    return jsonify({'theme': s.theme})

@app.route('/settings/theme', methods=['POST'])
@login_required
def update_theme():
    s = get_settings()
    data = request.get_json() or {}
    preset = data.get('theme_preset','dark')
    valid_presets = ['dark','light','dark-blue','light-blue','dark-green','light-green','dark-red','light-saffron']
    if preset in valid_presets:
        s.theme_preset = preset
        s.theme = 'light' if 'light' in preset else 'dark'
        db.session.commit()
    return jsonify({'ok': True, 'theme_preset': s.theme_preset})

# ══════════════════════════════════════════════
# STUDENTS
# ══════════════════════════════════════════════

@app.route('/students')
@login_required
def students():
    search  = request.args.get('search','')
    cls     = request.args.get('class','')
    sec     = request.args.get('section','')
    q = Student.query.filter_by(is_active=True)
    if search: q = q.filter(Student.name.ilike(f'%{search}%')|Student.admission_no.ilike(f'%{search}%')|Student.father_phone.ilike(f'%{search}%'))
    if cls:    q = q.filter_by(class_name=cls)
    if sec:    q = q.filter_by(section=sec)
    students = q.order_by(Student.class_name, Student.roll_no).all()
    classes  = db.session.query(Student.class_name).filter_by(is_active=True).distinct().all()
    return render_template('students.html', students=students, classes=classes,
                           search=search, class_filter=cls, section_filter=sec)

@app.route('/students/add', methods=['GET','POST'])
@login_required
def add_student():
    if request.method == 'POST':
        photo = save_photo(request.files.get('photo'), 'students')
        adm   = 'ADM' + str(Student.query.count() + 1001)
        f     = request.form
        s = Student(
            admission_no=adm, photo=photo,
            name=f.get('name',''), name_hindi=f.get('name_hindi',''),
            class_name=f.get('class_name',''), section=f.get('section','A'),
            roll_no=f.get('roll_no',0) or 0, dob=f.get('dob',''), gender=f.get('gender',''),
            blood_group=f.get('blood_group',''), religion=f.get('religion',''),
            caste=f.get('caste',''), category=f.get('category','General'),
            nationality=f.get('nationality','Indian'), aadhaar_no=f.get('aadhaar_no',''),
            address=f.get('address',''), city=f.get('city',''),
            state=f.get('state',''), pincode=f.get('pincode',''),
            father_name=f.get('father_name',''), father_phone=f.get('father_phone',''),
            father_occupation=f.get('father_occupation',''), father_email=f.get('father_email',''),
            mother_name=f.get('mother_name',''), mother_phone=f.get('mother_phone',''),
            mother_occupation=f.get('mother_occupation',''),
            guardian_name=f.get('guardian_name',''), guardian_phone=f.get('guardian_phone',''),
            guardian_relation=f.get('guardian_relation',''),
            previous_school=f.get('previous_school',''), admission_date=f.get('admission_date',''),
            transport_route=f.get('transport_route',''),
            medical_condition=f.get('medical_condition',''),
            emergency_contact=f.get('emergency_contact',''), house=f.get('house',''),
            parent_name=f.get('father_name',''), parent_phone=f.get('father_phone',''),
            parent_email=f.get('father_email','')
        )
        db.session.add(s); db.session.commit()
        # Auto-create pending fee record for new student
        auto_fee = Fee(
            student_id=s.id,
            fee_type='Tuition Fee',
            amount=float(f.get('tuition_fee', 5000) or 5000),
            paid_amount=0,
            discount=0,
            status='pending',
            due_date=(date.today().replace(day=1) + timedelta(days=32)).replace(day=1).strftime('%Y-%m-%d'),
            receipt_no='PENDING-' + s.admission_no,
            payment_mode='Cash',
            remarks='Auto-created on admission'
        )
        db.session.add(auto_fee)
        # If transport route selected, add transport fee too
        if s.transport_route:
            route = Transport.query.filter_by(route_name=s.transport_route).first()
            if route and route.fee > 0:
                transport_fee = Fee(
                    student_id=s.id,
                    fee_type='Transport Fee',
                    amount=route.fee,
                    paid_amount=0,
                    status='pending',
                    due_date=auto_fee.due_date,
                    receipt_no='PENDING-T-' + s.admission_no,
                    payment_mode='Cash',
                    remarks='Auto-created for ' + s.transport_route
                )
                db.session.add(transport_fee)
        db.session.commit()
        log_action(f'Student added: {s.name}', 'Student')
        flash(f'Student {s.name} added! Admission No: {adm} | Fee record auto-created.', 'success')
        return redirect(url_for('view_student', id=s.id))
    return render_template('add_student.html', transport_routes=Transport.query.all())

@app.route('/students/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit_student(id):
    s = Student.query.get_or_404(id)
    if request.method == 'POST':
        if request.files.get('photo') and request.files['photo'].filename:
            s.photo = save_photo(request.files['photo'], 'students')
        f = request.form
        for field in ['name','name_hindi','class_name','section','roll_no','dob','gender',
                      'blood_group','religion','caste','category','nationality','aadhaar_no',
                      'address','city','state','pincode','father_name','father_phone',
                      'father_occupation','father_email','mother_name','mother_phone',
                      'mother_occupation','guardian_name','guardian_phone','guardian_relation',
                      'previous_school','transport_route','medical_condition','emergency_contact','house']:
            if f.get(field) is not None:
                setattr(s, field, f.get(field))
        s.parent_name = s.father_name; s.parent_phone = s.father_phone; s.parent_email = s.father_email
        db.session.commit()
        flash('Student updated!', 'success')
        return redirect(url_for('view_student', id=id))
    return render_template('edit_student.html', student=s, transport_routes=Transport.query.all())

@app.route('/students/view/<int:id>')
@login_required
def view_student(id):
    s    = Student.query.get_or_404(id)
    att  = Attendance.query.filter_by(student_id=id).order_by(Attendance.date.desc()).limit(30).all()
    fees = Fee.query.filter_by(student_id=id).all()
    results = db.session.query(Result,Exam).join(Exam,Result.exam_id==Exam.id).filter(Result.student_id==id).all()
    issued  = db.session.query(BookIssue,Book).join(Book,BookIssue.book_id==Book.id).filter(BookIssue.student_id==id).all()
    present = sum(1 for a in att if a.status=='present')
    total   = len(att)
    pct     = round(present/total*100,1) if total else 0
    return render_template('view_student.html', student=s, attendance=att,
                           fees=fees, results=results, issued_books=issued,
                           att_pct=pct, att_present=present, att_total=total)

@app.route('/students/delete/<int:id>')
@login_required
def delete_student(id):
    s = Student.query.get_or_404(id); s.is_active = False; db.session.commit()
    flash(f'{s.name} removed.', 'warning')
    return redirect(url_for('students'))

@app.route('/students/promote', methods=['POST'])
@admin_required
def promote_students():
    cf = request.form.get('class_from'); ct = request.form.get('class_to')
    students = Student.query.filter_by(class_name=cf, is_active=True).all()
    for s in students: s.class_name = ct
    db.session.commit()
    flash(f'{len(students)} students promoted to Class {ct}!', 'success')
    return redirect(url_for('students'))

# ══════════════════════════════════════════════
# TEACHERS
# ══════════════════════════════════════════════

@app.route('/teachers')
@login_required
def teachers():
    return render_template('teachers.html', teachers=Teacher.query.filter_by(is_active=True).all())

@app.route('/teachers/add', methods=['GET','POST'])
@login_required
def add_teacher():
    if request.method == 'POST':
        photo  = save_photo(request.files.get('photo'), 'teachers')
        emp_id = 'EMP' + str(Teacher.query.count() + 101)
        f      = request.form
        t = Teacher(
            employee_id=emp_id, photo=photo,
            name=f.get('name',''), name_hindi=f.get('name_hindi',''),
            subject=f.get('subject',''), subjects_taught=f.get('subjects_taught',''),
            class_assigned=f.get('class_assigned',''), classes_taught=f.get('classes_taught',''),
            designation=f.get('designation','Teacher'), department=f.get('department',''),
            qualification=f.get('qualification',''), specialization=f.get('specialization',''),
            experience_years=int(f.get('experience_years',0) or 0),
            phone=f.get('phone',''), alt_phone=f.get('alt_phone',''),
            email=f.get('email',''), aadhaar_no=f.get('aadhaar_no',''),
            pan_no=f.get('pan_no',''), dob=f.get('dob',''), gender=f.get('gender',''),
            blood_group=f.get('blood_group',''), address=f.get('address',''),
            city=f.get('city',''), state=f.get('state',''),
            salary=float(f.get('salary',0) or 0),
            bank_name=f.get('bank_name',''), account_no=f.get('account_no',''),
            ifsc=f.get('ifsc',''), join_date=f.get('join_date','')
        )
        db.session.add(t); db.session.flush()
        uname = 'teacher_' + emp_id.lower()
        u = User(username=uname, password=generate_password_hash('Teacher@123'),
                 role='teacher', name=t.name, email=t.email, phone=t.phone, photo=photo)
        db.session.add(u); db.session.flush()
        t.user_id = u.id; db.session.commit()
        flash(f'Teacher added! Login: {uname} / Password: Teacher@123', 'success')
        return redirect(url_for('view_teacher', id=t.id))
    return render_template('add_teacher.html')

@app.route('/teachers/view/<int:id>')
@login_required
def view_teacher(id):
    t = Teacher.query.get_or_404(id)
    leaves = StaffLeave.query.filter_by(teacher_id=id).order_by(StaffLeave.applied_on.desc()).all()
    return render_template('view_teacher.html', teacher=t, leaves=leaves)

@app.route('/teachers/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit_teacher(id):
    t = Teacher.query.get_or_404(id)
    if request.method == 'POST':
        if request.files.get('photo') and request.files['photo'].filename:
            t.photo = save_photo(request.files['photo'], 'teachers')
        f = request.form
        for field in ['name','name_hindi','designation','department','subject','subjects_taught',
                      'class_assigned','classes_taught','qualification','specialization',
                      'phone','alt_phone','email','aadhaar_no','pan_no','dob','gender',
                      'blood_group','address','city','state','bank_name','account_no','ifsc']:
            if f.get(field) is not None: setattr(t, field, f.get(field))
        t.salary = float(f.get('salary', t.salary) or t.salary)
        t.experience_years = int(f.get('experience_years', t.experience_years) or t.experience_years)
        db.session.commit()
        flash('Teacher updated!', 'success')
        return redirect(url_for('view_teacher', id=id))
    return render_template('edit_teacher.html', teacher=t)

# ══════════════════════════════════════════════
# ATTENDANCE
# ══════════════════════════════════════════════

@app.route('/attendance', methods=['GET','POST'])
@login_required
def attendance():
    today  = date.today().strftime('%Y-%m-%d')
    sel_dt = request.args.get('date', today)
    sel_cl = request.args.get('class_name','')
    classes = db.session.query(Student.class_name).filter_by(is_active=True).distinct().all()
    students, att_map = [], {}
    if sel_cl:
        students = Student.query.filter_by(class_name=sel_cl, is_active=True).order_by(Student.roll_no).all()
        att_map  = {a.student_id: a.status for a in Attendance.query.filter_by(date=sel_dt).all()}
    if request.method == 'POST':
        cls = request.form['class_name']; dt = request.form['date']
        for s in Student.query.filter_by(class_name=cls, is_active=True).all():
            status = request.form.get(f'att_{s.id}','absent')
            ex = Attendance.query.filter_by(student_id=s.id, date=dt).first()
            if ex: ex.status = status
            else:  db.session.add(Attendance(student_id=s.id, date=dt, status=status, marked_by=session['user_id']))
        db.session.commit()
        flash(f'Attendance saved for Class {cls} — {dt}', 'success')
        return redirect(url_for('attendance', date=dt, class_name=cls))
    return render_template('attendance.html', students=students, classes=classes,
                           selected_class=sel_cl, selected_date=sel_dt, attendance_map=att_map, today=today)

@app.route('/attendance/report')
@login_required
def attendance_report():
    cls   = request.args.get('class','')
    month = request.args.get('month', date.today().strftime('%Y-%m'))
    data  = []
    if cls:
        for s in Student.query.filter_by(class_name=cls, is_active=True).all():
            recs = Attendance.query.filter_by(student_id=s.id).filter(Attendance.date.startswith(month)).all()
            pr = sum(1 for r in recs if r.status=='present')
            ab = sum(1 for r in recs if r.status=='absent')
            lt = sum(1 for r in recs if r.status=='late')
            tot= len(recs)
            pct= round(pr/tot*100,1) if tot else 0
            data.append({'student':s,'present':pr,'absent':ab,'late':lt,'total':tot,'pct':pct})
    classes = db.session.query(Student.class_name).distinct().all()
    return render_template('attendance_report.html', report_data=data,
                           classes=classes, selected_class=cls, month=month)

# ══════════════════════════════════════════════
# FEES
# ══════════════════════════════════════════════

@app.route('/fees')
@login_required
def fees():
    search = request.args.get('search','')
    sf     = request.args.get('status','')
    q = db.session.query(Fee,Student).join(Student, Fee.student_id==Student.id)
    if search: q = q.filter(Student.name.ilike(f'%{search}%')|Student.admission_no.ilike(f'%{search}%'))
    if sf:     q = q.filter(Fee.status==sf)
    fees       = q.order_by(Fee.id.desc()).all()
    collected  = float(db.session.query(db.func.sum(Fee.paid_amount)).scalar() or 0)
    pending    = float(db.session.query(db.func.sum(Fee.amount-Fee.paid_amount)).filter(Fee.status=='pending').scalar() or 0)
    all_students = Student.query.filter_by(is_active=True).all()
    return render_template('fees.html', fees=fees, total_collected=collected,
                           total_pending=pending, students_list=all_students,
                           search=search, status_filter=sf)

@app.route('/fees/add', methods=['POST'])
@login_required
def add_fee():
    f  = request.form
    net= float(f.get('amount',0)) - float(f.get('discount',0))
    pd = float(f.get('paid_amount',0))
    status = 'paid' if pd>=net else ('partial' if pd>0 else 'pending')
    fee = Fee(student_id=int(f['student_id']), fee_type=f['fee_type'],
              amount=float(f.get('amount',0)), discount=float(f.get('discount',0)),
              paid_amount=pd, due_date=f.get('due_date',''),
              payment_mode=f.get('payment_mode','Cash'),
              transaction_id=f.get('transaction_id',''),
              remarks=f.get('remarks',''), status=status,
              receipt_no='RCP'+str(Fee.query.count()+1001),
              paid_date=date.today().strftime('%Y-%m-%d') if status=='paid' else '')
    db.session.add(fee); db.session.commit()
    flash('Fee record added!', 'success')
    return redirect(url_for('fees'))

@app.route('/fees/collect/<int:id>', methods=['POST'])
@login_required
def collect_fee(id):
    fee = Fee.query.get_or_404(id)
    fee.paid_amount += float(request.form.get('amount',0))
    fee.payment_mode = request.form.get('payment_mode','Cash')
    fee.transaction_id= request.form.get('transaction_id','')
    net = fee.amount - fee.discount
    if fee.paid_amount >= net:
        fee.status='paid'; fee.paid_date=date.today().strftime('%Y-%m-%d')
    else:
        fee.status='partial'
    db.session.commit()
    flash(f'₹{request.form.get("amount")} collected!', 'success')
    return redirect(url_for('fees'))

# ══════════════════════════════════════════════
# EXAMS & RESULTS
# ══════════════════════════════════════════════

@app.route('/exams')
@login_required
def exams():
    return render_template('exams.html', exams=Exam.query.order_by(Exam.date.desc()).all())

@app.route('/exams/add', methods=['POST'])
@login_required
def add_exam():
    f = request.form
    db.session.add(Exam(name=f['name'], class_name=f['class_name'], subject=f['subject'],
                        date=f['date'], time=f.get('time',''), room=f.get('room',''),
                        max_marks=int(f['max_marks']), passing_marks=int(f.get('passing_marks',33)),
                        created_by=session['user_id']))
    db.session.commit(); flash('Exam scheduled!', 'success')
    return redirect(url_for('exams'))

@app.route('/exams/marks/<int:exam_id>', methods=['GET','POST'])
@login_required
def enter_marks(exam_id):
    exam     = Exam.query.get_or_404(exam_id)
    # Match both '10' and '10A' style class names
    cls = exam.class_name.rstrip('ABCDE')  # '10A' -> '10', 'Nursery' stays 'Nursery'
    if cls != exam.class_name and len(cls) < len(exam.class_name):
        students = Student.query.filter(
            (Student.class_name == exam.class_name) | (Student.class_name == cls),
            Student.is_active == True
        ).order_by(Student.roll_no).all()
    else:
        students = Student.query.filter_by(class_name=exam.class_name, is_active=True).order_by(Student.roll_no).all()
    existing = {r.student_id: r for r in Result.query.filter_by(exam_id=exam_id).all()}
    if request.method == 'POST':
        for s in students:
            mv = request.form.get(f'marks_{s.id}')
            if mv and mv.strip():
                marks = float(mv); grade = get_grade(marks, exam.max_marks)
                if s.id in existing:
                    existing[s.id].marks=marks; existing[s.id].grade=grade
                    existing[s.id].remarks=request.form.get(f'remarks_{s.id}','')
                else:
                    db.session.add(Result(student_id=s.id, exam_id=exam_id, marks=marks,
                                         grade=grade, remarks=request.form.get(f'remarks_{s.id}','')))
        db.session.commit()
        flash(f'Marks saved for {len(students)} students!', 'success')
        return redirect(url_for('exams'))
    return render_template('enter_marks.html', exam=exam, students=students,
                           existing=existing, existing_map=existing)

@app.route('/results/report-card/<int:student_id>')
@login_required
def report_card(student_id):
    student = Student.query.get_or_404(student_id)
    results = db.session.query(Result,Exam).join(Exam,Result.exam_id==Exam.id).filter(Result.student_id==student_id).all()
    tm  = sum(r.marks for r,e in results)
    tmx = sum(e.max_marks for r,e in results)
    pct = round(tm/tmx*100,1) if tmx else 0
    att = Attendance.query.filter_by(student_id=student_id).all()
    ap  = sum(1 for a in att if a.status=='present')
    att_pct = round(ap/len(att)*100,1) if att else 0
    return render_template('report_card.html', student=student, results=results,
                           total_marks=tm, total_max=tmx, overall_pct=pct,
                           overall_grade=get_grade(tm,tmx), att_pct=att_pct)

# ══════════════════════════════════════════════
# TIMETABLE
# ══════════════════════════════════════════════

@app.route('/timetable')
@login_required
def timetable():
    cls  = request.args.get('class','')
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    sch  = {d:{} for d in days}
    if cls:
        for e in Timetable.query.filter_by(class_name=cls).all():
            sch[e.day][e.period] = e
    return render_template('timetable.html', schedule=sch, days=days,
                           class_name=cls, classes=db.session.query(Student.class_name).distinct().all())

@app.route('/timetable/add', methods=['POST'])
@login_required
def add_timetable():
    f  = request.form
    ex = Timetable.query.filter_by(class_name=f['class_name'],day=f['day'],period=int(f['period'])).first()
    if ex:
        ex.subject=f['subject']; ex.start_time=f.get('start_time',''); ex.end_time=f.get('end_time','')
    else:
        db.session.add(Timetable(class_name=f['class_name'], section=f.get('section','A'),
                                 day=f['day'], period=int(f['period']), subject=f['subject'],
                                 start_time=f.get('start_time',''), end_time=f.get('end_time','')))
    db.session.commit(); flash('Timetable updated!', 'success')
    return redirect(url_for('timetable', **{'class': f['class_name']}))

# ══════════════════════════════════════════════
# LIBRARY
# ══════════════════════════════════════════════

@app.route('/library')
@login_required
def library():
    books    = Book.query.all()
    all_stu  = Student.query.filter_by(is_active=True).all()
    issued   = db.session.query(BookIssue,Book,Student).join(Book,BookIssue.book_id==Book.id).join(Student,BookIssue.student_id==Student.id).filter(BookIssue.status=='issued').all()
    return render_template('library.html', books=books, issued=issued, students_list=all_stu)

@app.route('/library/add-book', methods=['POST'])
@login_required
def add_book():
    f = request.form; c = int(f.get('copies',1))
    db.session.add(Book(title=f['title'], author=f.get('author',''), isbn=f.get('isbn',''),
                        category=f.get('category',''), publisher=f.get('publisher',''),
                        edition=f.get('edition',''), year=f.get('year',''),
                        total_copies=c, available=c))
    db.session.commit(); flash('Book added!', 'success')
    return redirect(url_for('library'))

@app.route('/library/issue', methods=['POST'])
@login_required
def issue_book():
    book = Book.query.get(int(request.form['book_id']))
    if book.available<=0:
        flash('No copies available!','danger'); return redirect(url_for('library'))
    due = (date.today()+timedelta(days=15)).strftime('%Y-%m-%d')
    db.session.add(BookIssue(book_id=book.id, student_id=int(request.form['student_id']),
                             issue_date=date.today().strftime('%Y-%m-%d'), due_date=due))
    book.available -= 1; db.session.commit()
    flash(f'Book issued! Due: {due}', 'success')
    return redirect(url_for('library'))

@app.route('/library/return/<int:id>')
@login_required
def return_book(id):
    bi = BookIssue.query.get_or_404(id)
    bi.return_date=date.today().strftime('%Y-%m-%d'); bi.status='returned'
    due = datetime.strptime(bi.due_date,'%Y-%m-%d').date()
    if date.today()>due:
        bi.fine=(date.today()-due).days*2
        flash(f'Returned. Fine: ₹{bi.fine}','warning')
    else: flash('Book returned!','success')
    Book.query.get(bi.book_id).available += 1; db.session.commit()
    return redirect(url_for('library'))

# ══════════════════════════════════════════════
# NOTICES
# ══════════════════════════════════════════════

@app.route('/notices')
@login_required
def notices():
    return render_template('notices.html', notices=Notice.query.filter_by(is_active=True).order_by(Notice.created_at.desc()).all())

@app.route('/notices/add', methods=['POST'])
@login_required
def add_notice():
    f = request.form
    db.session.add(Notice(title=f['title'], content=f['content'],
                          target=f.get('target','all'), priority=f.get('priority','normal'),
                          created_by=session['user_id']))
    db.session.commit(); flash('Notice published!', 'success')
    return redirect(url_for('notices'))

@app.route('/notices/delete/<int:id>')
@login_required
def delete_notice(id):
    n=Notice.query.get_or_404(id); n.is_active=False; db.session.commit()
    flash('Notice removed.','warning'); return redirect(url_for('notices'))

# ══════════════════════════════════════════════
# ADMISSIONS
# ══════════════════════════════════════════════

@app.route('/admissions')
@login_required
def admissions():
    sf = request.args.get('status','')
    q  = Enquiry.query
    if sf: q = q.filter_by(status=sf)
    return render_template('admissions.html', enquiries=q.order_by(Enquiry.created_at.desc()).all(), status_filter=sf)

@app.route('/admissions/add', methods=['POST'])
@login_required
def add_enquiry():
    f = request.form
    db.session.add(Enquiry(student_name=f['student_name'], class_applying=f['class_applying'],
                           dob=f.get('dob',''), gender=f.get('gender',''),
                           parent_name=f['parent_name'], relation=f.get('relation','Father'),
                           phone=f['phone'], alt_phone=f.get('alt_phone',''),
                           email=f.get('email',''), address=f.get('address',''),
                           previous_school=f.get('previous_school',''), reference=f.get('reference',''),
                           follow_up_date=f.get('follow_up_date',''), notes=f.get('notes','')))
    db.session.commit(); flash('Enquiry saved!','success')
    return redirect(url_for('admissions'))

@app.route('/admissions/update-status/<int:id>', methods=['POST'])
@login_required
def update_enquiry_status(id):
    e=Enquiry.query.get_or_404(id); e.status=request.form['status']
    e.notes=request.form.get('notes',e.notes); db.session.commit()
    flash('Status updated!','success'); return redirect(url_for('admissions'))

# ══════════════════════════════════════════════
# TRANSPORT
# ══════════════════════════════════════════════

@app.route('/transport')
@login_required
def transport():
    routes = Transport.query.all()
    on_bus = Student.query.filter(Student.transport_route!='', Student.is_active==True).all()
    return render_template('transport.html', routes=routes, students_on_bus=on_bus)

@app.route('/transport/add', methods=['POST'])
@login_required
def add_transport():
    f = request.form
    db.session.add(Transport(route_name=f['route_name'], driver_name=f['driver_name'],
                             driver_phone=f.get('driver_phone',''), helper_name=f.get('helper_name',''),
                             vehicle_no=f['vehicle_no'], vehicle_type=f.get('vehicle_type','Bus'),
                             capacity=int(f.get('capacity',40)), fee=float(f.get('fee',0)),
                             stops=f.get('stops',''), morning_time=f.get('morning_time',''),
                             evening_time=f.get('evening_time','')))
    db.session.commit(); flash('Route added!','success')
    return redirect(url_for('transport'))

# ══════════════════════════════════════════════
# HOMEWORK
# ══════════════════════════════════════════════

@app.route('/homework')
@login_required
def homework():
    role = session.get('role')
    q    = Homework.query.filter_by(teacher_id=session['user_id']) if role=='teacher' else Homework.query
    return render_template('homework.html', hw_list=q.order_by(Homework.created_at.desc()).all())

@app.route('/homework/add', methods=['POST'])
@login_required
def add_homework():
    f = request.form
    db.session.add(Homework(teacher_id=session['user_id'], class_name=f['class_name'],
                            subject=f['subject'], title=f['title'],
                            description=f.get('description',''), due_date=f['due_date']))
    db.session.commit(); flash('Homework assigned!','success')
    return redirect(url_for('homework'))

# ══════════════════════════════════════════════
# EVENTS
# ══════════════════════════════════════════════

@app.route('/events')
@login_required
def events():
    return render_template('events.html', events=Event.query.order_by(Event.event_date).all())

@app.route('/events/add', methods=['POST'])
@login_required
def add_event():
    f = request.form
    db.session.add(Event(title=f['title'], description=f.get('description',''),
                         event_date=f['event_date'], event_type=f.get('event_type','General'),
                         venue=f.get('venue',''), created_by=session['user_id']))
    db.session.commit(); flash('Event added!','success')
    return redirect(url_for('events'))

@app.route('/events/delete/<int:id>')
@login_required
def delete_event(id):
    db.session.delete(Event.query.get_or_404(id)); db.session.commit()
    flash('Event deleted.','warning'); return redirect(url_for('events'))

# ══════════════════════════════════════════════
# LEAVE
# ══════════════════════════════════════════════

@app.route('/leave/apply', methods=['POST'])
@login_required
def apply_leave():
    t = Teacher.query.filter_by(user_id=session['user_id']).first()
    if not t: flash('Only teachers can apply leave.','danger'); return redirect(url_for('dashboard'))
    f = request.form
    db.session.add(StaffLeave(teacher_id=t.id, leave_type=f['leave_type'],
                              from_date=f['from_date'], to_date=f['to_date'],
                              reason=f.get('reason','')))
    db.session.commit(); flash('Leave applied!','success')
    return redirect(url_for('teacher_portal'))

@app.route('/leave/process/<int:id>/<action>')
@admin_required
def process_leave(id, action):
    l=StaffLeave.query.get_or_404(id)
    l.status='approved' if action=='approve' else 'rejected'; db.session.commit()
    flash(f'Leave {l.status}!','success'); return redirect(url_for('teachers'))

# ══════════════════════════════════════════════
# REPORTS
# ══════════════════════════════════════════════

@app.route('/reports')
@login_required
def reports():
    today   = date.today().strftime('%Y-%m-%d')
    fbt     = db.session.query(Fee.fee_type, db.func.sum(Fee.paid_amount)).group_by(Fee.fee_type).all()
    att     = Attendance.query.filter_by(date=today).all()
    present = sum(1 for a in att if a.status=='present')
    absent  = sum(1 for a in att if a.status=='absent')
    ccounts = db.session.query(Student.class_name, db.func.count(Student.id)).filter_by(is_active=True).group_by(Student.class_name).all()
    gcounts = db.session.query(Student.gender, db.func.count(Student.id)).filter_by(is_active=True).group_by(Student.gender).all()
    return render_template('reports.html', fee_by_type=fbt, present=present, absent=absent,
                           class_counts=ccounts, gender_counts=gcounts, today=today)

# ══════════════════════════════════════════════
# SETTINGS & PROFILE
# ══════════════════════════════════════════════

@app.route('/settings', methods=['GET','POST'])
@login_required
def settings():
    s = get_settings()
    if request.method == 'POST':
        for field in ['school_name','school_name_hindi','school_address','school_phone','school_type','accent_color','theme_preset',
                      'school_email','school_website','school_code','school_city','school_state',
                      'school_pincode','affiliation','academic_year','established_year',
                      'principal_name','principal_phone','working_days',
                      'school_start_time','school_end_time','year_start','year_end']:
            val = request.form.get(field)
            if val is not None and hasattr(s, field):
                setattr(s, field, val)
        for fld, folder in [('school_logo','school'),('school_photo','school'),('principal_photo','school')]:
            if request.files.get(fld) and request.files[fld].filename:
                setattr(s, fld, save_photo(request.files[fld], folder))
        db.session.commit()
        flash('Settings saved!', 'success')
        return redirect(url_for('settings'))
    license_info = None
    try:
        import json as _json
        if os.path.exists('license.json'):
            with open('license.json') as f:
                ld = _json.load(f)
            from license_generator import validate_license
            license_info = validate_license(ld.get('license_key',''), ld.get('full_token',''))
    except:
        license_info = {'valid': False, 'message': 'No license file'}
    return render_template('settings.html', settings=s, license_info=license_info)

@app.route('/license/update', methods=['POST'])
@login_required
def update_license():
    import json as _j
    lk    = request.form.get('license_key','').strip()
    token = request.form.get('full_token','').strip()
    try:
        from license_generator import validate_license
        result = validate_license(lk, token)
        if result['valid']:
            with open('license.json', 'w') as f:
                _j.dump({'license_key':lk,'full_token':token,
                         'school_name':result.get('school_name',''),
                         'expiry_date':result.get('expiry_date','')}, f, indent=2)
            flash(f"License updated! Valid till {result.get('expiry_date','')}", 'success')
        else:
            flash(f"Invalid license: {result['message']}", 'danger')
    except Exception as e:
        flash(f'Error: {e}', 'danger')
    return redirect(url_for('settings'))

@app.route('/backup/download')
@admin_required
def backup_download():
    import shutil
    from flask import send_file
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'school_erp.db')
    if os.path.exists(db_path):
        bname = f"backup_{date.today().strftime('%Y%m%d')}_school_erp.db"
        bpath = os.path.join('/tmp', bname)
        shutil.copy2(db_path, bpath)
        return send_file(bpath, as_attachment=True, download_name=bname)
    flash('Database not found!', 'danger')
    return redirect(url_for('settings'))

@app.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    u = User.query.get(session['user_id'])
    if request.method=='POST':
        if request.files.get('photo') and request.files['photo'].filename:
            u.photo=save_photo(request.files['photo'],'staff'); session['photo']=u.photo
        u.name=request.form.get('name',u.name)
        u.email=request.form.get('email',u.email)
        u.phone=request.form.get('phone',u.phone)
        if request.form.get('new_password'):
            if check_password_hash(u.password, request.form.get('current_password','')):
                u.password=generate_password_hash(request.form['new_password']); flash('Password changed!','success')
            else:
                flash('Wrong current password!','danger'); return redirect(url_for('profile'))
        db.session.commit(); session['name']=u.name; flash('Profile updated!','success')
        return redirect(url_for('profile'))
    return render_template('profile.html', user=u)

# ══════════════════════════════════════════════
# USERS & AUDIT
# ══════════════════════════════════════════════

@app.route('/users')
@admin_required
def users():
    return render_template('users.html', users=User.query.all())

@app.route('/users/add', methods=['POST'])
@admin_required
def add_user():
    if User.query.filter_by(username=request.form['username']).first():
        flash('Username exists!','danger'); return redirect(url_for('users'))
    photo=save_photo(request.files.get('photo'),'staff')
    db.session.add(User(username=request.form['username'],
                        password=generate_password_hash(request.form['password']),
                        role=request.form['role'], name=request.form['name'],
                        email=request.form.get('email',''), phone=request.form.get('phone',''),
                        photo=photo))
    db.session.commit(); flash('User created!','success')
    return redirect(url_for('users'))

@app.route('/users/toggle/<int:id>')
@admin_required
def toggle_user(id):
    u=User.query.get_or_404(id); u.is_active=not u.is_active; db.session.commit()
    flash(f'User {"activated" if u.is_active else "deactivated"}.','success')
    return redirect(url_for('users'))

@app.route('/audit-logs')
@admin_required
def audit_logs():
    logs  = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(300).all()
    umap  = {u.id:u.name for u in User.query.all()}
    return render_template('audit_logs.html', logs=logs, users=umap)

# ══════════════════════════════════════════════
# PORTALS
# ══════════════════════════════════════════════

@app.route('/portal/student')
@login_required
def student_portal():
    if session.get('role') not in ['student','admin']: return redirect(url_for('dashboard'))
    u  = User.query.get(session['user_id'])
    st = Student.query.filter_by(user_id=u.id).first()
    att_pct=fees=hw=books=results=0
    notices = Notice.query.filter(Notice.target.in_(['all','student']), Notice.is_active==True).order_by(Notice.created_at.desc()).limit(5).all()
    if st:
        att = Attendance.query.filter_by(student_id=st.id).all()
        pr  = sum(1 for a in att if a.status=='present')
        att_pct = round(pr/len(att)*100,1) if att else 0
        fees    = Fee.query.filter_by(student_id=st.id).all()
        hw      = Homework.query.filter_by(class_name=st.class_name).order_by(Homework.created_at.desc()).limit(5).all()
        books   = db.session.query(BookIssue,Book).join(Book).filter(BookIssue.student_id==st.id, BookIssue.status=='issued').all()
        results = db.session.query(Result,Exam).join(Exam).filter(Result.student_id==st.id).all()
    return render_template('student_portal.html', student=st, att_pct=att_pct,
                           fees=fees, hw=hw, books=books, results=results, notices=notices)

@app.route('/portal/teacher')
@login_required
def teacher_portal():
    if session.get('role') not in ['teacher','admin']: return redirect(url_for('dashboard'))
    u  = User.query.get(session['user_id'])
    t  = Teacher.query.filter_by(user_id=u.id).first()
    notices    = Notice.query.filter(Notice.target.in_(['all','teacher']), Notice.is_active==True).order_by(Notice.created_at.desc()).limit(5).all()
    my_classes = pending_hw = leaves = []
    if t:
        my_classes = Student.query.filter_by(class_name=t.class_assigned, is_active=True).all()
        pending_hw = Homework.query.filter_by(teacher_id=session['user_id']).order_by(Homework.created_at.desc()).limit(5).all()
        leaves     = StaffLeave.query.filter_by(teacher_id=t.id).order_by(StaffLeave.applied_on.desc()).limit(5).all()
    return render_template('teacher_portal.html', teacher=t, notices=notices,
                           my_classes=my_classes, pending_hw=pending_hw, leaves=leaves)

# ══════════════════════════════════════════════
# API
# ══════════════════════════════════════════════

@app.route('/api/attendance-chart')
@login_required
def api_attendance_chart():
    today = date.today()
    labels,pres,abs_ = [],[],[]
    for i in range(6,-1,-1):
        d = (today-timedelta(days=i)).strftime('%Y-%m-%d')
        labels.append(d)
        pres.append(Attendance.query.filter_by(date=d,status='present').count())
        abs_.append(Attendance.query.filter_by(date=d,status='absent').count())
    return jsonify({'labels':labels,'present':pres,'absent':abs_})

@app.route('/api/fee-chart')
@login_required
def api_fee_chart():
    data = db.session.query(Fee.fee_type, db.func.sum(Fee.paid_amount)).group_by(Fee.fee_type).all()
    return jsonify({'labels':[d[0] for d in data],'amounts':[float(d[1] or 0) for d in data]})

@app.route('/api/stats')
@login_required
def api_stats():
    today = date.today().strftime('%Y-%m-%d')
    return jsonify({'students':Student.query.filter_by(is_active=True).count(),
                    'teachers':Teacher.query.filter_by(is_active=True).count(),
                    'present':Attendance.query.filter_by(date=today,status='present').count(),
                    'fees':float(db.session.query(db.func.sum(Fee.paid_amount)).scalar() or 0)})

# ══════════════════════════════════════════════
# LICENSE ROUTES
# ══════════════════════════════════════════════

@app.route('/license/activate', methods=['POST'])
@login_required
def activate_license():
    key    = request.form.get('license_key','').strip()
    result = verify_license(key)
    s      = get_settings()
    if result['valid']:
        s.license_key    = key
        s.license_status = 'active'
        db.session.commit()
        save_license(key)
        flash(f"License activated! {result['message']}", 'success')
    else:
        flash(result['message'], 'danger')
    return redirect(url_for('settings'))

@app.route('/license/check')
@login_required
def license_check():
    s      = get_settings()
    key    = s.license_key or load_license()
    if not key:
        return jsonify({'valid': False, 'message': 'No license'})
    result = verify_license(key)
    return jsonify(result)

# ══════════════════════════════════════════════
# EVENTS WITH PHOTO
# ══════════════════════════════════════════════

@app.route('/events/add-with-photo', methods=['POST'])
@login_required
def add_event_photo():
    photo = save_photo(request.files.get('photo'), 'events')
    f     = request.form
    db.session.add(Event(
        title=f['title'], description=f.get('description',''),
        event_date=f['event_date'], event_type=f.get('event_type','General'),
        venue=f.get('venue',''), photo=photo, created_by=session['user_id']
    ))
    db.session.commit()
    flash('Event added!','success')
    return redirect(url_for('events'))

# ══════════════════════════════════════════════
# ══════════════════════════════════════════════
# SUPER ADMIN PANEL
# ══════════════════════════════════════════════

@app.route('/super')
def super_panel():
    if 'user_id' not in session: return redirect(url_for('login'))
    if session.get('role') != 'superadmin':
        return redirect(url_for('login'))
    schools = SchoolSettings.query.all()
    all_users = User.query.all()
    total_students = Student.query.filter_by(is_active=True).count()
    total_teachers = Teacher.query.filter_by(is_active=True).count()
    total_fees = float(db.session.query(db.func.sum(Fee.paid_amount)).scalar() or 0)
    license_info = None
    try:
        import json as _j
        if os.path.exists('license.json'):
            with open('license.json') as f: ld = _j.load(f)
            from license_generator import validate_license
            license_info = validate_license(ld.get('license_key',''), ld.get('full_token',''))
    except: pass
    return render_template('super_panel.html',
        schools=schools, all_users=all_users,
        total_students=total_students, total_teachers=total_teachers,
        total_fees=total_fees, license_info=license_info)

@app.route('/super/reset-admin', methods=['POST'])
def super_reset_admin():
    if session.get('role') != 'superadmin':
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    new_pwd = request.form.get('new_password','')
    if len(new_pwd) < 6:
        flash('Password minimum 6 characters!', 'danger')
        return redirect(url_for('super_panel'))
    admin = User.query.filter_by(role='admin').first()
    if admin:
        admin.password = generate_password_hash(new_pwd)
        db.session.commit()
        log_action(f'Super Admin reset admin password', 'SuperAdmin')
        flash('Admin password reset successfully!', 'success')
    return redirect(url_for('super_panel'))

@app.route('/super/update-school', methods=['POST'])
def super_update_school():
    if session.get('role') != 'superadmin':
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    s = get_settings()
    s.school_name    = request.form.get('school_name', s.school_name)
    s.school_type    = request.form.get('school_type', s.school_type)
    s.academic_year  = request.form.get('academic_year', s.academic_year)
    s.affiliation    = request.form.get('affiliation', s.affiliation)
    if request.files.get('school_logo') and request.files['school_logo'].filename:
        s.school_logo = save_photo(request.files['school_logo'], 'school')
    db.session.commit()
    log_action('Super Admin updated school settings', 'SuperAdmin')
    flash('School settings updated!', 'success')
    return redirect(url_for('super_panel'))

@app.route('/super/wipe-data', methods=['POST'])
def super_wipe_data():
    if session.get('role') != 'superadmin':
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    confirm = request.form.get('confirm_text','')
    if confirm != 'RESET CONFIRM':
        flash('Confirmation text galat hai!', 'danger')
        return redirect(url_for('super_panel'))
    # Keep only super admin and settings
    super_user = User.query.get(session['user_id'])
    s = get_settings()
    # Delete all data
    Result.query.delete()
    Attendance.query.delete()
    Fee.query.delete()
    BookIssue.query.delete()
    Homework.query.delete()
    StaffLeave.query.delete()
    Enquiry.query.delete()
    Exam.query.delete()
    Student.query.delete()
    Teacher.query.delete()
    Notice.query.delete()
    Event.query.delete()
    Transport.query.delete()
    Book.query.delete()
    Timetable.query.delete()
    # Delete non-super users
    User.query.filter(User.id != super_user.id).delete()
    db.session.commit()
    log_action('Super Admin wiped all data', 'SuperAdmin')
    flash('All data wiped. Fresh installation ready!', 'warning')
    return redirect(url_for('super_panel'))

# ══════════════════════════════════════════════
# SEED DATA
# ══════════════════════════════════════════════

def seed_database():
    if User.query.count() > 0: return
    s = SchoolSettings(school_name='Vidyalaya Pro School',
                       school_address='123, School Road, Model Town, Bareilly',
                       school_phone='0581-2456789', school_email='principal@vidyalaya.edu.in',
                       affiliation='CBSE', academic_year='2024-25',
                       theme='dark', theme_preset='dark', accent_color='#6c63ff',
                       school_type='senior')
    db.session.add(s)
    # Super Admin (Developer - Saadat)
    super_admin = User(username='superadmin', password=generate_password_hash('SuperAdmin@2025'),
                       role='superadmin', name='Super Administrator', email='saadat@vidyalayapro.com')
    db.session.add(super_admin)
    
    # School Admin / Principal
    admin = User(username='admin', password=generate_password_hash('Admin@123'),
                 role='admin', name='Principal Admin', email='admin@school.com', phone='9999000001')
    db.session.add(admin)
    tu = User(username='teacher1', password=generate_password_hash('Teacher@123'),
              role='teacher', name='Mrs. Sunita Sharma', email='sunita@school.com', phone='9876543210')
    db.session.add(tu); db.session.flush()
    teacher = Teacher(user_id=tu.id, employee_id='EMP101', name='Mrs. Sunita Sharma',
                      subject='Mathematics', subjects_taught='Math,Science',
                      class_assigned='10A', classes_taught='10A,9B',
                      designation='Senior Teacher', department='Science',
                      qualification='M.Sc B.Ed', specialization='Applied Mathematics',
                      experience_years=8, phone='9876543210', email='sunita@school.com',
                      dob='1985-06-15', gender='Female', blood_group='B+',
                      address='45, Teacher Colony', city='Bareilly', state='UP',
                      salary=42000, bank_name='SBI', account_no='1234567890',
                      ifsc='SBIN0001234', join_date='2022-06-01')
    db.session.add(teacher)
    students_data = [
        # Nursery / LKG / UKG
        ('Aarav Gupta',  'आरव गुप्ता',  'Nursery','A',1,'Male',  'A+','Hinduism','General','Rakesh Gupta',  '9012341001','Business','Pooja Gupta',   '9012341002'),
        ('Diya Sharma',  'दिया शर्मा',  'Nursery','A',2,'Female','O+','Hinduism','OBC',    'Sunil Sharma',  '9012341003','Service', 'Rekha Sharma',  '9012341004'),
        ('Vihan Singh',  'विहान सिंह',  'LKG',    'A',1,'Male',  'B+','Hinduism','General','Amar Singh',    '9012341005','Farmer',  'Kiran Singh',   '9012341006'),
        ('Ananya Tiwari','अनन्या तिवारी','LKG',    'A',2,'Female','AB+','Hinduism','General','Deepak Tiwari', '9012341007','Doctor',  'Sita Tiwari',   '9012341008'),
        ('Aryan Verma',  'आर्यन वर्मा', 'UKG',    'A',1,'Male',  'O-','Hinduism','OBC',    'Rohit Verma',   '9012341009','Teacher', 'Geeta Verma',   '9012341010'),
        ('Kavya Yadav',  'काव्या यादव', 'UKG',    'A',2,'Female','A-','Hinduism','OBC',    'Mohan Yadav',   '9012341011','Labour',  'Champa Devi',   '9012341012'),
        # Class 1-5
        ('Rahul Kumar',  'राहुल कुमार', '1',      'A',1,'Male',  'A+','Hinduism','General','Vikram Kumar',  '9012345001','Business','Sunita Devi',   '9012345002'),
        ('Priya Singh',  'प्रिया सिंह', '3',      'A',1,'Female','O+','Hinduism','OBC',    'Rajesh Singh',  '9012345003','Service', 'Meena Singh',   '9012345004'),
        ('Rohan Sharma', 'रोहन शर्मा',  '5',      'A',1,'Male',  'O-','Hinduism','General','Dinesh Sharma', '9012345009','Teacher', 'Geeta Sharma',  '9012345010'),
        # Class 6-8
        ('Anjali Patel', 'अंजली पटेल',  '6',      'A',1,'Female','A-','Hinduism','OBC',    'Ramesh Patel',  '9012345011','Farmer',  'Sushila Patel', '9012345012'),
        ('Amit Verma',   'अमित वर्मा',  '8',      'B',1,'Male',  'B+','Hinduism','General','Suresh Verma',  '9012345005','Farmer',  'Kamla Verma',   '9012345006'),
        ('Neha Gupta',   'नेहा गुप्ता', '8',      'B',2,'Female','AB+','Hinduism','General','Mahesh Gupta', '9012345007','Shopkeeper','Rani Gupta',  '9012345008'),
        # Class 9-12
        ('Vikash Yadav', 'विकाश यादव',  '10',     'A',1,'Male',  'B-','Hinduism','OBC',    'Mohan Yadav',   '9012345013','Labour',  'Champa Devi',   '9012345014'),
        ('Pooja Mishra', 'पूजा मिश्रा', '10',     'A',2,'Female','O+','Hinduism','General','Anil Mishra',   '9012345015','Service', 'Poonam Mishra', '9012345016'),
        ('Arjun Tiwari', 'अर्जुन तिवारी','12',    'A',1,'Male',  'A+','Hinduism','General','Prem Tiwari',   '9012345017','Doctor',  'Anita Tiwari',  '9012345018'),
        ('Sita Devi',    'सीता देवी',   '12',     'A',2,'Female','B+','Hinduism','SC',     'Ram Prasad',    '9012345019','Labour',  'Savitri Devi',  '9012345020'),
    ]
    cities = ['Bareilly','Lucknow','Agra','Kanpur','Varanasi']
    houses = ['Red House','Blue House','Green House','Yellow House']
    for i,(name,nh,cls,sec,roll,gen,bg,rel,cat,fn,fp,fo,mn,mp) in enumerate(students_data):
        su = User(username=f'student{i+1}', password=generate_password_hash('Student@123'), role='student', name=name)
        db.session.add(su); db.session.flush()
        st = Student(
            user_id=su.id, admission_no=f'ADM{1001+i}', name=name, name_hindi=nh,
            class_name=cls, section=sec, roll_no=roll,
            dob=f'200{4+i%6}-{(i%9)+1:02d}-{10+i}', gender=gen, blood_group=bg,
            religion=rel, caste=cat, category=cat, nationality='Indian',
            aadhaar_no=f'12345678{9001+i}',
            address=f'{i+1}/A, Street {i+1}, Model Nagar',
            city=cities[i%5], state='Uttar Pradesh', pincode=f'2430{10+i}',
            father_name=fn, father_phone=fp, father_occupation=fo, father_email=f'parent{i+1}@mail.com',
            mother_name=mn, mother_phone=mp,
            parent_name=fn, parent_phone=fp, parent_email=f'parent{i+1}@mail.com',
            previous_school=f'ABC Primary School, {cities[i%5]}',
            admission_date='2024-04-01', emergency_contact=fp,
            house=houses[i%4], transport_route='Route A - City Center' if i%2==0 else ''
        )
        db.session.add(st); db.session.flush()
        db.session.add(Fee(student_id=st.id, fee_type='Tuition Fee', amount=5000,
                           paid_amount=5000 if i%3!=0 else 0,
                           status='paid' if i%3!=0 else 'pending',
                           due_date='2025-04-30', receipt_no=f'RCP{1001+i}',
                           payment_mode='Online' if i%2==0 else 'Cash',
                           paid_date='2025-04-01' if i%3!=0 else ''))
        if i%2==0:
            db.session.add(Fee(student_id=st.id, fee_type='Transport Fee', amount=1500,
                               paid_amount=1500, status='paid', due_date='2025-04-30',
                               paid_date='2025-04-01', receipt_no=f'RCP{2001+i}', payment_mode='Cash'))
    for title,content,target,priority in [
        ('Annual Sports Day','Annual Sports Day on 15th May.','all','high'),
        ('Fee Last Date','Due: 30 April. Late fee ₹50/day.','all','urgent'),
        ('Staff Meeting','All teachers — Monday 9 AM.','teacher','normal'),
        ('Summer Vacation','School closed 1 June–30 June.','all','normal'),
    ]:
        db.session.add(Notice(title=title,content=content,target=target,priority=priority,created_by=1))
    for name,cls,subj,dt,mm in [
        ('Unit Test 1','10','Mathematics','2025-04-20',50),
        ('Unit Test 1','10','Science','2025-04-22',50),
        ('Unit Test 1','12','English','2025-04-23',50),
        ('Mid Term','10','Mathematics','2025-05-12',100),
        ('Mid Term','12','English','2025-05-14',100),
        ('Mid Term','8','Science','2025-05-15',100),
        ('Mid Term','6','Hindi','2025-05-16',100),
        ('Nursery Annual','Nursery','General','2025-05-20',50),
        ('LKG Annual','LKG','General','2025-05-21',50),
        ('UKG Annual','UKG','General','2025-05-22',50),
    ]:
        db.session.add(Exam(name=name,class_name=cls,subject=subj,date=dt,max_marks=mm,passing_marks=int(mm*.33),created_by=1))
    for title,author,isbn,cat,pub,copies in [
        ('Mathematics Class 10','NCERT','978-81-7450-1','Textbook','NCERT',5),
        ('Science Class 10','NCERT','978-81-7450-2','Textbook','NCERT',5),
        ('Wings of Fire','A.P.J. Abdul Kalam','978-81-7371-1','Biography','Universities Press',3),
        ('The Alchemist','Paulo Coelho','978-0-06-112241','Fiction','HarperOne',2),
        ('English Grammar','Wren & Martin','978-93-5100-2','Reference','S.Chand',4),
    ]:
        db.session.add(Book(title=title,author=author,isbn=isbn,category=cat,publisher=pub,total_copies=copies,available=copies))
    for rn,dn,dp,vn,cap,fee,stops,mt,et in [
        ('Route A - City Center','Ram Singh','9876500001','UP32 AB 1234',40,800,'Clock Tower,Civil Lines,Station','07:30','14:30'),
        ('Route B - Sector 5','Shyam Lal','9876500002','UP32 CD 5678',35,700,'Sector 5,Park Chowk,Hospital','07:45','14:45'),
        ('Route C - Railway Colony','Mohan Das','9876500003','UP32 EF 9012',30,600,'Railway Gate,Colony Main,Market','07:15','14:15'),
    ]:
        db.session.add(Transport(route_name=rn,driver_name=dn,driver_phone=dp,vehicle_no=vn,capacity=cap,fee=fee,stops=stops,morning_time=mt,evening_time=et))
    today = date.today()
    for title,desc,etype,dd,venue in [
        ('Annual Sports Day','Inter-house competition','Sports',str(today+timedelta(days=15)),'School Ground'),
        ('Independence Day','78th Independence Day','National','2025-08-15','Assembly'),
        ('Parent Teacher Meeting','PTM all classes','Academic',str(today+timedelta(days=7)),'Classrooms'),
        ('Science Exhibition','Class 8-12 projects','Academic',str(today+timedelta(days=20)),'Hall A'),
    ]:
        db.session.add(Event(title=title,description=desc,event_type=etype,event_date=dd,venue=venue,created_by=1))
    days=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    subs=['Mathematics','Science','English','Hindi','Social Studies','Computer','P.T.','Sanskrit']
    times=[('08:00','08:45'),('08:45','09:30'),('09:30','10:15'),('10:30','11:15'),
           ('11:15','12:00'),('12:00','12:45'),('13:30','14:15'),('14:15','15:00')]
    for day in days:
        for period in range(1,8):
            st,et=times[period-1]
            db.session.add(Timetable(class_name='10A',section='A',day=day,period=period,
                                     subject=subs[(period+days.index(day))%len(subs)],
                                     start_time=st,end_time=et))
    for subj,title,desc,due in [
        ('Mathematics','Ch-3 Exercise','Complete Q1-20 from Ex 3.4',str(today+timedelta(days=3))),
        ('Science','Lab Report','Write lab report on photosynthesis',str(today+timedelta(days=2))),
        ('English','Essay Writing','300 word essay on Environment',str(today+timedelta(days=4))),
    ]:
        db.session.add(Homework(teacher_id=2,class_name='10A',subject=subj,title=title,description=desc,due_date=due))
    all_students = Student.query.all()
    for i in range(7):
        d=(today-timedelta(days=i)).strftime('%Y-%m-%d')
        for st in all_students:
            db.session.add(Attendance(student_id=st.id,date=d,status='present' if random.random()>.12 else 'absent',marked_by=1))
    db.session.flush()
    db.session.flush()
    exams_all = Exam.query.all()
    for exam in exams_all:
        cls_base = exam.class_name.rstrip('ABCDE')
        matching_students = Student.query.filter(
            (Student.class_name == exam.class_name) | (Student.class_name == cls_base),
            Student.is_active == True
        ).all()
        for st in matching_students:
            m = round(random.uniform(exam.passing_marks, exam.max_marks), 1)
            db.session.add(Result(student_id=st.id, exam_id=exam.id,
                                  marks=m, grade=get_grade(m, exam.max_marks)))
    db.session.commit()
    print('✅ Database seeded!')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_database()
    app.run(debug=True, host='0.0.0.0', port=5000)
