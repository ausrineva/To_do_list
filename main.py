from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'tasks.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL,
            user TEXT
        );
    ''')
    conn.commit()
    conn.close()


create_tables()


@app.route('/', methods=['GET', 'POST'])
def tasks():
    conn = get_db_connection()
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        user = request.form['user']
        conn.execute('INSERT INTO tasks (title, description, status, user) VALUES (?, ?, ?, ?)',
                     (title, description, status, user))
        conn.commit()
        return redirect(url_for('tasks'))

    all_tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return render_template('tasks.html', tasks=all_tasks, task={})


@app.route('/modify/<int:task_id>', methods=['GET', 'POST'])
def modify_task(task_id):
    conn = get_db_connection()
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        conn.execute('UPDATE tasks SET title = ?, description = ? WHERE id = ?',
                     (title, description, task_id))
        conn.commit()
        return redirect(url_for('tasks'))

    task = conn.execute('SELECT * FROM tasks WHERE id = ?',
                        (task_id,)).fetchone()
    conn.close()
    return render_template('modify_task.html', task=task)


@app.route('/change_status/<int:task_id>', methods=['GET', 'POST'])
def change_status(task_id):
    conn = get_db_connection()
    if request.method == 'POST':
        status = request.form['status']
        conn.execute('UPDATE tasks SET status = ? WHERE id = ?',
                     (status, task_id))
        conn.commit()
        return redirect(url_for('tasks'))

    task = conn.execute('SELECT * FROM tasks WHERE id = ?',
                        (task_id,)).fetchone()
    conn.close()
    return render_template('change_status.html', task=task)


@app.route('/assign_user/<int:task_id>', methods=['GET', 'POST'])
def assign_user(task_id):
    conn = get_db_connection()
    if request.method == 'POST':
        user = request.form['user']
        conn.execute('UPDATE tasks SET user = ? WHERE id = ?',
                     (user, task_id))
        conn.commit()
        return redirect(url_for('tasks'))

    task = conn.execute('SELECT * FROM tasks WHERE id = ?',
                        (task_id,)).fetchone()
    conn.close()
    return render_template('assign_user.html', task=task)


if __name__ == '__main__':
    app.run(debug=True)
