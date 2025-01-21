from flask import Flask, request, render_template_string, jsonify
import sqlite3

app = Flask(__name__)

# Database setup
DATABASE = 'test.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # Create a table for users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    # Insert some test data
    cursor.execute('INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)', ('admin', 'password123'))
    cursor.execute('INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)', ('test', 'test123'))
    conn.commit()
    conn.close()

@app.route('/')
def home():
    login_form = '''
    <h1>Login Page</h1>
    <form action="/login" method="post">
        <label>Username:</label>
        <input type="text" name="username" /><br>
        <label>Password:</label>
        <input type="password" name="password" /><br>
        <button type="submit">Login</button>
    </form>
    '''
    return render_template_string(login_form)

@app.route('/login', methods=['POST'])

def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')

    # Connect to the database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # SQL query vulnerable to injection
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    try:
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()

        if user:
            return f"<h2>Welcome {user[1]}!</h2>"
        else:
            return "<h2>Invalid credentials</h2>", 401
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(port=9000, debug=True, threaded=True)
