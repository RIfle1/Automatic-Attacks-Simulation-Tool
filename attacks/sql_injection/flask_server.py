from flask import Flask, request

app = Flask(__name__)

@app.route('/login', methods=['GET'])
def login():
    username = request.args.get('username', '')
    password = request.args.get('password', '')

    # Simulate SQL Injection vulnerability
    if "'" in username or "'" in password:
        return "SQL Injection Detected", 500
    return "Login Successful", 200

def run_server():
    """Run the Flask server."""
    app.run(port=8080)
