from flask import Flask, render_template, redirect, url_for, flash, session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from forms import LoginForm, RegistrationForm, RecordHoursForm  # Adjust as needed
from models import Base , Teacher , Record # Adjust as needed
from models import Teacher  

app = Flask(__name__)
app.config.from_object("config.Config")

# Database setup
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Base.metadata.create_all(engine)

# Create a scoped session
Session = scoped_session(sessionmaker(bind=engine))

app.secret_key = 'your_secret_key'  # Change this to a secure key

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/record_hours', methods=['GET', 'POST'])
def record_hours():
    form = RecordHoursForm()
    if form.validate_on_submit():
        with Session() as session:
            # Handle form submission and save data
            # Example: session.add(new_record) for your model
            session.commit()  # Commit your changes to the database
            flash('Hours recorded successfully!', 'success')
            return redirect(url_for('view_hours'))
    return render_template('record_hours.html', form=form)

@app.route('/view_hours', methods=['GET'])
def view_hours():
    with Session() as session:
        # Fetch data to display
        hours_data = session.query(Record).all()  # Replace Record with your actual model class
    return render_template('view_hours.html', hours=hours_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data.strip()
        
        if username == 'admin' and password == 'password':
            flash('Login successful!', 'success')
            return redirect(url_for('app_dashboard', teacher_name=username))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/app')
def app_dashboard():
    teacher_name = "Teacher Name"  # Replace with logic to get the teacher's name
    return render_template('app.html', teacher_name=teacher_name)

@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

# Cleanup session on shutdown
@app.teardown_appcontext
def cleanup_session(exception=None):
    Session.remove()

if __name__ == '__main__':
    app.run(debug=True)