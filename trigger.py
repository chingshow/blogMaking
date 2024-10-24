from flask import Flask, request
import subprocess
import json

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        print("Received webhook")

        data = json.dumps(request.json, indent=2)
        # 打印接收到的全部數據
        print("request data:")
        print(data)
        data = json.loads(data)
        print(data['sheetIndex'])

        if data['sheetIndex'] == 6:
            print(data["data"][0]["_ragicId"])
            subprocess.run(["python", "main.py", str(data["data"][0]["_ragicId"])])
        else:
            # 執行 main.py
            subprocess.run(["python", "main_5.py"])

        return "OK", 200
    return "Webhook receiver is running", 200


if __name__ == '__main__':
    app.run(port=5001)