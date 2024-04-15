from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)  # Sukuria Flask aplikacijos instanciją.
DATABASE = 'tasks.db'  # Duomenų bazės failo pavadinimas.


def get_db_connection():
    # Sukuria prisijungimą prie duomenų bazės.
    conn = sqlite3.connect(DATABASE)
    # Nustato eilučių gamybos metodą, kuris leidžia naudoti stulpelių pavadinimus.
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
    ''')  # Sukuria lentelę 'tasks', jei ji neegzistuoja.
    conn.commit()  # Įvykdo užklausą.
    conn.close()  # Uždaromas prisijungimas prie duomenų bazės.


# Iškviečiama funkcija, kuri sukuria lentelę pradėjus aplikaciją.
create_tables()


@app.route('/', methods=['GET', 'POST'])
def tasks():
    conn = get_db_connection()
    if request.method == 'POST':
        # Gaunami duomenys iš POST užklausos ir įrašomi į duomenų bazę.
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        user = request.form['user']
        conn.execute('INSERT INTO tasks (title, description, status, user) VALUES (?, ?, ?, ?)',
                     (title, description, status, user))
        conn.commit()
        # Nukreipia vartotoją atgal į užduočių sąrašo puslapį.
        return redirect(url_for('tasks'))

    # Gaunami visi užduočių įrašai.
    all_tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return render_template('tasks.html', tasks=all_tasks, task={})


@app.route('/modify/<int:task_id>', methods=['GET', 'POST'])
def modify_task(task_id):
    conn = get_db_connection()
    if request.method == 'POST':
        # Iš formos gaunami nauji duomenys, kurie bus įrašyti į duomenų bazę.
        title = request.form['title']
        description = request.form['description']
        conn.execute('UPDATE tasks SET title = ?, description = ? WHERE id = ?',
                     (title, description, task_id))
        conn.commit()
        # Vartotojas nukreipiamas atgal į pradinį puslapį.
        return redirect(url_for('tasks'))

    # Užduotis gaunama iš duomenų bazės, kad būtų galima ją redaguoti.
    task = conn.execute('SELECT * FROM tasks WHERE id = ?',
                        (task_id,)).fetchone()
    conn.close()
    return render_template('modify_task.html', task=task)


@app.route('/change_status/<int:task_id>', methods=['GET', 'POST'])
def change_status(task_id):
    conn = get_db_connection()
    if request.method == 'POST':
        # Užduoties statusas atnaujinamas duomenų bazėje.
        status = request.form['status']
        conn.execute('UPDATE tasks SET status = ? WHERE id = ?',
                     (status, task_id))
        conn.commit()
        return redirect(url_for('tasks'))

    # Gaunami užduoties duomenys, kad būtų galima keisti jos statusą.
    task = conn.execute('SELECT * FROM tasks WHERE id = ?',
                        (task_id,)).fetchone()
    conn.close()
    return render_template('change_status.html', task=task)


@app.route('/assign_user/<int:task_id>', methods=['GET', 'POST'])
def assign_user(task_id):
    conn = get_db_connection()
    if request.method == 'POST':
        # Užduotis priskiriama vartotojui.
        user = request.form['user']
        conn.execute('UPDATE tasks SET user = ? WHERE id = ?',
                     (user, task_id))
        conn.commit()
        return redirect(url_for('tasks'))

    # Gaunami užduoties duomenys, kad galėtumėte priskirti vartotoją.
    task = conn.execute('SELECT * FROM tasks WHERE id = ?',
                        (task_id,)).fetchone()
    conn.close()
    return render_template('assign_user.html', task=task)


# Aplikacijos pradžios taškas. Jei šis failas paleidžiamas kaip pagrindinis, aplikacija bus paleista.
if __name__ == '__main__':
    # Debug režimas leidžia matyti klaidas naršyklėje ir automatiškai perkrauna serverį, kai atliekami pakeitimai kode.
    app.run(debug=True)
