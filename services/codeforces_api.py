import requests

def get_user_info(handle):
    api_url = f"https://codeforces.com/api/user.info?handles={handle}"
    response = requests.get(api_url)
    if response.status_code == 200 and response.json().get("status") == "OK":
        return response.json()["result"][0]
    return None
