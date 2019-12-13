from flask import Flask, escape, request, render_template
from decouple import config
import requests

app = Flask(__name__)

api_url = 'https://api.telegram.org/bot'
token = config('TELEGRAM_BOT_TOKEN')

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/write')
def write():
    return render_template('write.html')

@app.route('/send')
def send():
    get_user_api = f"{api_url}{token}/getUpdates"

    res = requests.get(get_user_api).json()

    user_id = res["result"][0]["message"]["from"]["id"]

    #user_input=input("보낼메세지를 입력해주세요 : ")
    user_input=request.args.get('user_input')

    send_url = f'https://api.telegram.org/bot{token}/sendMessage?text={user_input}&chat_id={user_id}'

    requests.get(send_url)
    return render_template('send.html')

@app.route(f'/telegram', methods=['POST'])
def telegram():
    return 'ok', 200



if __name__ == '__main__':
    app.run(debug=True)