# 📝 Flask CRUD Task Manager - Learning Guide

## 🎯 What You'll Learn

This is a complete **CRUD application** (Create, Read, Update, Delete) built with Flask. It's designed to teach you Flask fundamentals step by step.

---

## 📚 What is CRUD?

**CRUD** stands for the four basic operations you can perform on data:

- **C**reate - Add new data (Add a task)
- **R**ead - View existing data (See all tasks)
- **U**pdate - Modify existing data (Edit a task)
- **D**elete - Remove data (Delete a task)

---

## 🗂️ Project Structure

```
Flask_App/
├── app.py                  # Main application file (backend logic)
├── requirements.txt        # Python dependencies
├── tasks.db               # SQLite database (created automatically)
├── templates/             # HTML templates (frontend)
│   ├── base.html         # Base template (inherited by others)
│   ├── index.html        # Home page (shows all tasks)
│   ├── add_task.html     # Form to add new task
│   └── edit_task.html    # Form to edit existing task
└── static/               # Static files (CSS, images, etc.)
    ├── style.css         # Compiled CSS
    ├── style.scss        # SCSS source file
    └── style.css.map     # Source map for debugging
```

---

## 🚀 How to Run the App

### Step 1: Create a Virtual Environment

A virtual environment keeps your project dependencies isolated from other Python projects.

#### **Windows**

1. **Create the virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment:**
   ```bash
   venv\Scripts\activate
   ```
   
   You'll see `(venv)` appear in your terminal prompt when activated.

3. **If you encounter "Access is denied" error with pip:**
   ```bash
   python -m pip install -r requirements.txt
   ```

4. **Deactivate when done:**
   ```bash
   deactivate
   ```

#### **macOS/Linux**

1. **Create the virtual environment:**
   ```bash
   python3 -m venv venv
   ```

2. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```
   
   You'll see `(venv)` appear in your terminal prompt when activated.

3. **Deactivate when done:**
   ```bash
   deactivate
   ```

> **Note:** The `venv` folder is already in `.gitignore`, so it won't be committed to version control.

---

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- **Flask** - The web framework
- **Flask-SQLAlchemy** - Database management
- **Flask-SCSS** - SCSS compilation

### Step 3: Run the Application

```bash
python app.py
```

### Step 4: Open in Browser

Go to: **http://localhost:5000**

---

## 🔍 Understanding the Code

### 1. **app.py** - The Brain of Your App

#### Imports Section
```python
from flask import Flask, render_template, request, redirect, url_for, flash
```
- `Flask` - Creates the web application
- `render_template` - Displays HTML pages
- `request` - Gets data from forms
- `redirect` - Sends users to different pages
- `url_for` - Generates URLs safely
- `flash` - Shows messages to users

#### Database Model
```python
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

This defines what a "Task" looks like:
- **id** - Unique number for each task
- **title** - The task name (required)
- **description** - Extra details (optional)
- **completed** - Is it done? (True/False)
- **created_at** - When was it created?

#### Routes (URLs)

| Route | Method | Purpose | CRUD Operation |
|-------|--------|---------|----------------|
| `/` | GET | Show all tasks | **READ** |
| `/add` | GET, POST | Add new task | **CREATE** |
| `/edit/<id>` | GET, POST | Edit task | **UPDATE** |
| `/delete/<id>` | GET | Delete task | **DELETE** |
| `/toggle/<id>` | GET | Mark complete/incomplete | **UPDATE** |

---

## 🎓 Key Concepts Explained

### 1. **Routes and Views**

```python
@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)
```

- `@app.route('/')` - This URL triggers this function
- `Task.query.all()` - Get all tasks from database
- `render_template()` - Show HTML page with data

### 2. **Forms and POST Requests**

```python
@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form.get('title')
        # Create and save task
```

- **GET** - Show the form
- **POST** - Process the form data
- `request.form.get('title')` - Get data from form field

### 3. **Database Operations**

```python
# CREATE
new_task = Task(title="Learn Flask")
db.session.add(new_task)
db.session.commit()

# READ
all_tasks = Task.query.all()
one_task = Task.query.get(1)

# UPDATE
task = Task.query.get(1)
task.title = "New Title"
db.session.commit()

# DELETE
task = Task.query.get(1)
db.session.delete(task)
db.session.commit()
```

### 4. **Template Inheritance**

```html
<!-- base.html -->
<html>
  <body>
    {% block content %}{% endblock %}
  </body>
</html>

<!-- index.html -->
{% extends 'base.html' %}
{% block content %}
  <h1>My Content</h1>
{% endblock %}
```

This avoids repeating HTML code!

### 5. **Jinja2 Templating**

```html
<!-- Loop through tasks -->
{% for task in tasks %}
  <h3>{{ task.title }}</h3>
{% endfor %}

<!-- Conditional -->
{% if task.completed %}
  <span>Done!</span>
{% else %}
  <span>Pending</span>
{% endif %}
```

---

## 🧪 Testing Your App

### Test CREATE (Add Task)
1. Click "Add Task"
2. Fill in title: "Learn Python"
3. Add description: "Complete Flask tutorial"
4. Click "Add Task"
5. ✅ Task appears on home page!

### Test READ (View Tasks)
1. Go to home page
2. ✅ See all your tasks listed

### Test UPDATE (Edit Task)
1. Click "Edit" on a task
2. Change the title
3. Click "Save Changes"
4. ✅ Task is updated!

### Test DELETE (Remove Task)
1. Click "Delete" on a task
2. Confirm deletion
3. ✅ Task is removed!

---

## 💡 Common Beginner Questions

### Q: What is SQLAlchemy?
**A:** It's an ORM (Object-Relational Mapping) that lets you work with databases using Python objects instead of SQL queries.

### Q: What is a route?
**A:** A route is a URL pattern that triggers a specific function. Example: `/add` triggers `add_task()` function.

### Q: What's the difference between GET and POST?
**A:** 
- **GET** - Request data (show a page)
- **POST** - Send data (submit a form)

### Q: What is db.session.commit()?
**A:** It saves your changes to the database. Without it, changes are lost!

### Q: Why use templates?
**A:** Templates separate HTML (frontend) from Python (backend), making code cleaner and reusable.

---

## 🎯 Next Steps to Learn More

1. **Add user authentication** - Let users log in
2. **Add categories** - Organize tasks by category
3. **Add due dates** - Set deadlines for tasks
4. **Add search** - Find tasks by keyword
5. **Deploy online** - Share your app with others

---

## 🐛 Troubleshooting

### Database not found?
Run the app once - it creates `tasks.db` automatically.

### CSS not loading?
1. Hard refresh: `Ctrl + Shift + R` (Windows) or `Cmd + Shift + R` (Mac)
2. Check that `static/style.css` exists

### Port already in use?
Change port in `app.py`:
```python
app.run(debug=True, port=5001)
```

---

## 📖 Resources to Learn More

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/en/14/tutorial/)
- [Jinja2 Templates](https://jinja.palletsprojects.com/)
- [Python Official Tutorial](https://docs.python.org/3/tutorial/)

---

## ✨ You Did It!

Congratulations! You've built a complete CRUD application with Flask. You now understand:

✅ Flask routes and views  
✅ Database models and queries  
✅ Forms and user input  
✅ Template inheritance  
✅ CRUD operations  

Keep practicing and building more features! 🚀