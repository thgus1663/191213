from decouple import config #토큰 가져오는

#웹훅설정 위한 경로
token = config('TELEGRAM_BOT_TOKEN')
url=f'https://api.telegram.org/bot{token}/setWebhook'

#내가 연결하려는 주소
ngrok_url = 'https://1426b9dd.ngrok.io/telegram'
#실행주소
setwebhook_url = f"{url}?url={ngrok_url}"

print(setwebhook_url)