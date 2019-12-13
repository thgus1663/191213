from flask import Flask, escape, request, render_template
from decouple import config
import requests

app = Flask(__name__)

api_url = 'https://api.telegram.org/bot'
token = config('TELEGRAM_BOT_TOKEN')
google_key=config('GOOGLE_KEY')

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
    req=request.get_json()
    #print(req)
    user_id = req["message"]["from"]["id"]
    user_input= req["message"]["text"]

    if user_input=="로또":
        return_data="로또를 입력하셨습니다."
    elif user_input[0:3]=="번역 ":
        google_api_url = "https://translation.googleapis.com/language/translate/v2"
        before_text=user_input[3:]
        data={
            'q':before_text,
            'source':'ko',
            'target':'en'
        }
        requests_url=f'{google_api_url}?key={google_key}'
        res=requests.post(requests_url, data).json()
        #print(res)
        return_data=res["data"]["translations"][0]["translatedText"]
    else:
        return_data="지금 사용 가능하는 명령어는 로또입니다."
    send_url = f'https://api.telegram.org/bot{token}/sendMessage?text={return_data}&chat_id={user_id}'
    requests.get(send_url)
    #print(user_id)
    #print(user_input)
    return 'ok', 200



if __name__ == '__main__':
    app.run(debug=True)