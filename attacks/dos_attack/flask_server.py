from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    result = 0
    for i in range(1, 10**6):  # Inefficient computation
        result += i ** 0.5
    return "Welcome to the DoS Testing Server!", 200


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True, threaded=False)
