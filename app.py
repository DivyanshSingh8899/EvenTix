from flask import Flask, render_template, request, redirect, url_for, flash, send_file  # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user  # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash  # type: ignore
import qrcode  # type: ignore
from datetime import datetime, timezone
import uuid
import io
import os

app = Flask(__name__)
# Secure secret key
app.config['SECRET_KEY'] = 'event-booking-secret-key-123'
# Configure SQLite DB
basedir = os.path.abspath(os.path.dirname(__file__))

# On Vercel (serverless), the filesystem is read-only, so we use /tmp for the SQLite db
if os.environ.get('VERCEL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/database.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# --- Models ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    bookings = db.relationship('Booking', backref='user', lazy=True)

    def __init__(self, username=None, email=None, password=None, is_admin=False, **kwargs):
        super().__init__(**kwargs)
        if username: self.username = username
        if email: self.email = email
        if password: self.password = password
        self.is_admin = is_admin

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    total_tickets = db.Column(db.Integer, nullable=False)
    available_tickets = db.Column(db.Integer, nullable=False)
    ticket_price = db.Column(db.Float, nullable=False)
    bookings = db.relationship('Booking', backref='event', lazy='dynamic', cascade="all, delete-orphan")

    def __init__(self, title=None, description=None, date_time=None, location=None, total_tickets=None, available_tickets=None, ticket_price=None, **kwargs):
        super().__init__(**kwargs)
        if title: self.title = title
        if description: self.description = description
        if date_time: self.date_time = date_time
        if location: self.location = location
        if total_tickets is not None: self.total_tickets = total_tickets
        if available_tickets is not None: self.available_tickets = available_tickets
        if ticket_price is not None: self.ticket_price = ticket_price

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    num_tickets = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    booking_reference = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    booking_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    def __init__(self, user_id=None, event_id=None, num_tickets=None, total_price=None, **kwargs):
        super().__init__(**kwargs)
        if user_id is not None: self.user_id = user_id
        if event_id is not None: self.event_id = event_id
        if num_tickets is not None: self.num_tickets = num_tickets
        if total_price is not None: self.total_price = total_price

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Routes ---

@app.route('/')
def index():
    # Show recently added events (limit to 3 for the homepage)
    recent_events = Event.query.order_by(Event.date_time.asc()).limit(3).all()
    return render_template('index.html', events=recent_events)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user_exists = User.query.filter_by(username=username).first()
        email_exists = User.query.filter_by(email=email).first()
        
        if user_exists:
            flash('Username already exists.', 'danger')
        elif email_exists:
            flash('Email already registered.', 'danger')
        else:
            # Use default pbkdf2:sha256
            hashed_pw = generate_password_hash(password)
            new_user = User(username=username, email=email, password=hashed_pw)
            
            # Make the first registered user an admin automatically
            if User.query.count() == 0:
                new_user.is_admin = True
                
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash(f'Welcome back, {user.username}!', 'success')
            
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/events')
def events():
    all_events = Event.query.order_by(Event.date_time.asc()).all()
    return render_template('events.html', events=all_events)

@app.route('/event/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event_detail.html', event=event)

@app.route('/book/<int:event_id>', methods=['GET', 'POST'])
@login_required
def book_ticket(event_id):
    event = Event.query.get_or_404(event_id)
    
    # If a booking reference or id is passed dynamically through template
    # we just show the confirmation (handled in the template rendering below)
    
    if request.method == 'POST':
        num_tickets = int(request.form.get('num_tickets', 1))
        
        if num_tickets <= 0:
            flash('Please select at least 1 ticket.', 'danger')
        elif num_tickets > event.available_tickets:
            flash(f'Only {event.available_tickets} tickets available.', 'danger')
        else:
            total_price = num_tickets * event.ticket_price
            booking = Booking(
                user_id=current_user.id,
                event_id=event.id,
                num_tickets=num_tickets,
                total_price=total_price
            )
            event.available_tickets -= num_tickets
            
            db.session.add(booking)
            db.session.commit()
            
            flash('Booking successful!', 'success')
            # Re-render booking template but this time with a booking object
            # to display confirmation & QR code details
            return render_template('booking.html', event=event, booking=booking)
            
    return render_template('booking.html', event=event)

@app.route('/qr_code/<string:booking_reference>')
@login_required
def qr_code(booking_reference):
    booking = Booking.query.filter_by(booking_reference=booking_reference).first_or_404()
    
    # Check permissions
    if booking.user_id != current_user.id and not current_user.is_admin:
        return 'Unauthorized', 403
        
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f"Booking Ref: {booking.booking_reference}\nEvent: {booking.event.title}\nTickets: {booking.num_tickets}\nUser: {booking.user.username}")
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')


@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied. Administrator privileges required.', 'danger')
        return redirect(url_for('index'))
        
    events = Event.query.order_by(Event.date_time.desc()).all()
    bookings = Booking.query.order_by(Booking.booking_date.desc()).all()
    
    return render_template('admin_dashboard.html', events=events, bookings=bookings)

@app.route('/admin/event/new', methods=['POST'])
@login_required
def admin_create_event():
    if not current_user.is_admin:
        return redirect(url_for('index'))
        
    title = request.form.get('title')
    description = request.form.get('description')
    date_time_str = request.form.get('date_time') # Format: YYYY-MM-DDTHH:MM
    date_time = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M')
    location = request.form.get('location')
    total_tickets = int(request.form.get('total_tickets'))
    ticket_price = float(request.form.get('ticket_price'))
    
    new_event = Event(
        title=title,
        description=description,
        date_time=date_time,
        location=location,
        total_tickets=total_tickets,
        available_tickets=total_tickets,
        ticket_price=ticket_price
    )
    
    db.session.add(new_event)
    db.session.commit()
    flash('Event created successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/event/delete/<int:event_id>', methods=['POST'])
@login_required
def admin_delete_event(event_id):
    if not current_user.is_admin:
        return redirect(url_for('index'))
        
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/event/edit/<int:event_id>', methods=['POST'])
@login_required
def admin_edit_event(event_id):
    if not current_user.is_admin:
        return redirect(url_for('index'))
        
    event = Event.query.get_or_404(event_id)
    event.title = request.form.get('title')
    event.description = request.form.get('description')
    
    date_time_str = request.form.get('date_time')
    event.date_time = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M')
    
    event.location = request.form.get('location')
    
    new_total = int(request.form.get('total_tickets'))
    diff = new_total - event.total_tickets
    event.total_tickets = new_total
    event.available_tickets += diff
    
    event.ticket_price = float(request.form.get('ticket_price'))
    
    db.session.commit()
    flash('Event updated successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

# Create database tables globally so Vercel Serverless triggers it
with app.app_context():
    try:
        db.create_all()
        
        # Create default admin user if it doesn't exist
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            default_admin = User(
                username='admin',
                email='admin@eventix.com',
                password=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(default_admin)
            db.session.commit()
            print("✓ Default admin user created: username='admin', password='admin123'")
    except Exception as e:
        print(f"Error initializing DB: {e}")

# Application initialization
if __name__ == '__main__':
    app.run(debug=True)
