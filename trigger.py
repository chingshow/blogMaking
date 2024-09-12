from flask import Flask, request
import subprocess
import json

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        print("Received webhook")

        # 打印接收到的全部數據
        print("request data:")
        print(json.dumps(request.json, indent=2))

        # 打印請求頭
        #print("Request headers:")
        #print(request.headers)

        # 打印表單數據（如果有）
        #print("Form data:")
        #print(request.form)

        # 執行 main.py
        subprocess.run(["python", "main.py"])

        return "OK", 200
    return "Webhook receiver is running", 200


if __name__ == '__main__':
    app.run(port=5001)