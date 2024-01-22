import requests
import hashlib
import time
import certifi
from selenium import webdriver
from selenium.webdriver.chromium.options import ChromiumOptions
import subprocess
import json

MLX_BASE = "https://api.multilogin.com"
MLX_LAUNCHER = "https://launcher.mlx.yt:45001/api/v1"
LOCALHOST = "http://127.0.0.1"
HEADERS = {
 'Accept': 'application/json',
 'Content-Type': 'application/json',
 'User-Agent': 'curl/8.4.0'
 }

#TODO: Insert your account information in both variables below.
USERNAME = ""
PASSWORD = ""

#TODO: Insert the Folder ID and the Profile ID below 
FOLDER_ID = ""
PROFILE_ID = ""

def signin() -> str:

    payload = {
    'email': USERNAME,
    'password': hashlib.md5(PASSWORD.encode()).hexdigest()
    }

    r = requests.post(f'{MLX_BASE}/user/signin', json=payload, verify=certifi.where())

    if(r.status_code != 200):
        print(f'\nError during login: {r.text}\n')

    response = r.json()['data']

    token = response['token']
    print(token)

    return token

def start_profile() -> webdriver:

    """
    
    bc = requests.get(f"{MLX_LAUNCHER}/load_browser_core?browser_type=mimic&version=120", headers=HEADERS, verify=certifi.where())
    print(f"Loading browser core, please wait 120 seconds. Status: {bc.status_code}, message: {bc.text}")
    time.sleep(120)

    curl_command = [
    'curl',
    '--http1.1',
    '--location',
    f'{MLX_LAUNCHER}/profile/f/{FOLDER_ID}/p/{PROFILE_ID}/start?automation_type=selenium&headless_mode=true',
    '--header', f'Authorization: {HEADERS["Authorization"]}',
    '--header', f'Content-Type: {HEADERS["Content-Type"]}',
    '--header', f'Accept: {HEADERS["Accept"]}'
    ]
    
    try:
        result = subprocess.run(curl_command, capture_output=True, text=True, check=True)
        response_json = json.loads(result.stdout)

        if response_json.get('status', {}).get('message'):
            selenium_port = response_json['status']['message']
            print(f'\nProfile {PROFILE_ID} started. Selenium Port: {selenium_port}\n')
        else:
            print(f'\nError while starting profile: {result.stderr}\n')
    except subprocess.CalledProcessError as e:
        print(f"Command failed with return code {e.returncode}")
        print(e.stderr)
    """

    bc = requests.get(f"{MLX_LAUNCHER}/load_browser_core?browser_type=mimic&version=120", headers=HEADERS, verify=False)
    print(f"Loading browser core, please wait 120 seconds. Status: {bc.status_code}, message: {bc.text}")
    time.sleep(120)
    r = requests.get(f'{MLX_LAUNCHER}/profile/f/{FOLDER_ID}/p/{PROFILE_ID}/start?automation_type=selenium&headless_mode=true', headers=HEADERS, verify=False)

    response = r.json()

    if(r.status_code != 200):
       print(f'\nError while starting profile: {r.text}\n')
    else:
       print(f'\nProfile {PROFILE_ID} started.\n')
    
    selenium_port = response.get('status').get('message')
    driver = webdriver.Remote(command_executor=f'{LOCALHOST}:{selenium_port}', options=ChromiumOptions())

    return driver
 
def stop_profile() -> None:

    """
    curl_command = [
    'curl',
    '--http1.1',
    '--location',
    f'{MLX_LAUNCHER}/profile/stop/p/{PROFILE_ID}',
    '--header', f'Authorization: {HEADERS["Authorization"]}',
    '--header', f'Content-Type: {HEADERS["Content-Type"]}',
    '--header', f'Accept: {HEADERS["Accept"]}'
    ]

    try:
        result = subprocess.run(curl_command, capture_output=True, text=True, check=True)
        
        if result.returncode == 0:
            print(f'\nProfile {PROFILE_ID} stopped.\n')
        else:
            print(f'\nError while stopping profile: {result.stderr}\n')

    except subprocess.CalledProcessError as e:
        print(f"Command failed with return code {e.returncode}")
        print(e.stderr)

    """

    r = requests.get(f'{MLX_LAUNCHER}/profile/stop/p/{PROFILE_ID}', headers=HEADERS, verify=False)

    if(r.status_code != 200):
        print(f'\nError while stopping profile: {r.text}\n')
    else:
        print(f'\nProfile {PROFILE_ID} stopped.\n')


token = signin()
HEADERS.update({"Authorization": f'Bearer {token}'})
driver = start_profile()
driver.get('https://multilogin.com/')
time.sleep(5)
stop_profile()
