from flask import Flask


app = Flask(__name__)

@app.route('/')
def home():
    return "Server is running."

if __name__ == '__main__':
    app.run(port=5000)  # Run the server on localhost:5000
