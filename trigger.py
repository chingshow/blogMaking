from flask import Flask, request
import subprocess

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        print("Received webhook")
        subprocess.run(["python", "main.py"])
        return "OK", 200
    return "Webhook receiver is running", 200


if __name__ == '__main__':
    app.run(port=5000)


