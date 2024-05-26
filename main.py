import sqlite3
from flask import Flask, render_template, redirect, request, url_for
from task import Task

# Connect to database.
todo_db = sqlite3.connect("todo.db", check_same_thread=False)
cursor = todo_db.cursor()
todo_data = cursor.execute("SELECT * from todo")

# Translate database contents to a list of Task objects.
todo_list = []
for SQL_task in todo_data:
    new_task = Task(SQL_task[0], (SQL_task[1] == "Yes"))
    new_task.update()
    todo_list.append(new_task)

# Flask.
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template("todo_list.html", todo_list=todo_list)

# Add a new task to the list and database. Then redirect back to the main page.
@app.route('/add', methods=['GET', 'POST'])
def add():
    description = request.form['description_entry']
    todo_list.append(Task(description, False))
    cursor.execute('''
    INSERT INTO todo (description, completed)
    VALUES (?,?)
    ''', (description, "No"))
    todo_db.commit()

    return redirect(url_for('main'))


# Update list and database to reflect that a task has been completed. Then redirect back to the main page.
@app.route("/complete_task", methods=['POST'])
def finish():
    completed_task = request.form.get("complete")
    for task in todo_list:
        if task.description == completed_task:
            task.completed = True
            task.update()
            cursor.execute('''
            UPDATE todo
            SET completed = ?
            WHERE description = ?
            ''', ("Yes", task.description))
            todo_db.commit()
    return redirect(url_for('main'))


if __name__ == "__main__":
    app.run(debug=True)

todo_db.close()
