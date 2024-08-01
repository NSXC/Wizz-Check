import requests
import time
import threading
import json
access_token = None
refresh_token = "<FIRST RESET TOKEN>"  # Replace with your initial refresh token

def refresh_access_token(refresh_token):
    url = "https://wizz.chat/auth/refresh"
    response = requests.post(url, json={"refreshToken": refresh_token})
    if response.status_code == 200:
        data = response.json()
        return data["accessToken"], data["refreshToken"]
    else:
        raise Exception(f"Failed to refresh tokens: {response.status_code}, {response.text}")

def update_tokens():
    global access_token, refresh_token

    while True:
        try:
            new_access_token, new_refresh_token = refresh_access_token(refresh_token)
            access_token = new_access_token
            refresh_token = new_refresh_token
            print(f"Updated Refresh Token: {refresh_token}")
        except Exception as e:
            print(f"Error refreshing tokens: {e}")
            break
        time.sleep(300)  

token_thread = threading.Thread(target=update_tokens)
token_thread.daemon = True
token_thread.start()
def send_discord_message(webhook_url, message):
    payload = {
        "content": message
    }

    response = requests.post(
        webhook_url,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload)
    )

    # Print the response status and body
    if response.status_code == 204:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message: {response.status_code}")
        print(response.text)
def use_access_token():
    global access_token
    url = "https://wizz.chat/users/<USERID>?projection=default"

    headers = {
        "Accept-Encoding": "gzip",
        "appconfiguration": "playStore",
        "appVersion": "5.7.1",
        "Authorization": "Bearer " + str(access_token),
        "Connection": "Keep-Alive",
        "device_model": "SM-S908E",
        "Host": "wizz.chat",
        "keychain_udid": "<CHAINUUID>",
        "location": "US",
        "mixpanelUserID": "<ID>",
        "os_name": "Android",
        "os_version": "28",
        "preferredlanguage": "en-US",
        "timezone": "America/New_York",
        "User-Agent": "Wizz/5.7.1 (info.wizzapp; build:539; Android 28) okhttp/4.11.0",
        "Cache-Control": "no-cache"
    }

    response = requests.get(url, headers=headers)

    print(response.status_code)
    data = response.json()  
    liveness_info = data.get('liveness', {})
    name = data.get('name', 'Unknown')
    is_online = liveness_info.get('isOnline', False)
    last_online_date = liveness_info.get('lastOnlineDate', 'Unknown')
    if is_online == True:
        send_discord_message("<WEBHOOK>", f"{name} is Online")
if __name__ == "__main__":
    try:
        while True:
            use_access_token()
            time.sleep(30)  
    except KeyboardInterrupt:
        print("Program terminated.")
