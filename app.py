# ============================================
# STEP 1: IMPORTS
# ============================================
# These are the tools we need from Flask and other libraries

from flask import Flask, render_template, request, redirect, url_for, flash
# Flask: The main framework
# render_template: To display HTML pages
# request: To get data from forms
# redirect: To send users to different pages
# url_for: To generate URLs for routes
# flash: To show messages to users

from flask_sqlalchemy import SQLAlchemy
# SQLAlchemy: Makes working with databases easy

from flask_scss import Scss
# Scss: Compiles SCSS to CSS

from datetime import datetime
# datetime: To work with dates and times


# ============================================
# STEP 2: CREATE THE APP
# ============================================

app = Flask(__name__)
# This creates our Flask application

# Secret key for security (needed for flash messages)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Database configuration
# We'll use SQLite - a simple database stored in a file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Initialize SCSS compiler
Scss(app, static_dir='static', asset_dir='static')


# ============================================
# STEP 3: CREATE DATABASE MODEL
# ============================================
# A model is like a blueprint for our data
# This defines what a "Task" looks like in our database

class Task(db.Model):
    """
    Task Model - represents a task in our database
    Each task has: id, title, description, completed status, and creation date
    """
    # Primary key - unique ID for each task
    id = db.Column(db.Integer, primary_key=True)
    
    # Task title - required field (nullable=False)
    title = db.Column(db.String(100), nullable=False)
    
    # Task description - optional field
    description = db.Column(db.String(200))
    
    # Completed status - default is False (not completed)
    completed = db.Column(db.Boolean, default=False)
    
    # Creation date - automatically set when task is created
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        """
        This method defines how a Task object is displayed
        Useful for debugging
        """
        return f'<Task {self.id}: {self.title}>'


# ============================================
# STEP 4: ROUTES (URLs and their functions)
# ============================================

@app.route('/')
def index():
    """
    HOME PAGE - READ (View all tasks)
    This is the main page that shows all tasks
    """
    # Query the database to get all tasks, ordered by creation date
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    
    # Render the HTML template and pass the tasks to it
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['GET', 'POST'])
def add_task():
    """
    ADD TASK PAGE - CREATE
    GET: Show the form to add a new task
    POST: Process the form and save the task to database
    """
    if request.method == 'POST':
        # Get data from the form
        title = request.form.get('title')
        description = request.form.get('description')
        
        # Validate: make sure title is not empty
        if not title:
            flash('Title is required!', 'error')
            return redirect(url_for('add_task'))
        
        # Create a new Task object
        new_task = Task(title=title, description=description)
        
        # Add it to the database
        db.session.add(new_task)
        db.session.commit()
        
        # Show success message
        flash('Task added successfully!', 'success')
        
        # Redirect to home page
        return redirect(url_for('index'))
    
    # If GET request, show the form
    return render_template('add_task.html')


@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    """
    EDIT TASK PAGE - UPDATE
    GET: Show the form with current task data
    POST: Update the task in the database
    """
    # Get the task from database or return 404 if not found
    task = Task.query.get_or_404(task_id)
    
    if request.method == 'POST':
        # Get updated data from form
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        
        # Validate
        if not task.title:
            flash('Title is required!', 'error')
            return redirect(url_for('edit_task', task_id=task_id))
        
        # Save changes to database
        db.session.commit()
        
        flash('Task updated successfully!', 'success')
        return redirect(url_for('index'))
    
    # If GET request, show the form with current data
    return render_template('edit_task.html', task=task)


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    """
    DELETE TASK - DELETE
    Remove a task from the database
    """
    # Get the task from database or return 404 if not found
    task = Task.query.get_or_404(task_id)
    
    # Delete the task
    db.session.delete(task)
    db.session.commit()
    
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    """
    TOGGLE TASK COMPLETION
    Mark a task as completed or not completed
    """
    task = Task.query.get_or_404(task_id)
    
    # Toggle the completed status
    task.completed = not task.completed
    db.session.commit()
    
    status = 'completed' if task.completed else 'reopened'
    flash(f'Task {status}!', 'success')
    return redirect(url_for('index'))


# ============================================
# STEP 5: RUN THE APP
# ============================================

if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    # Run the app in debug mode (shows errors and auto-reloads)
    app.run(debug=True)