import urllib.request
import urllib.parse
import json
import sys

BASE_URL = "http://localhost:8000/api/v1"

def make_request(url, data=None, method='POST'):
    try:
        if data:
            data = json.dumps(data).encode('utf-8')
            headers = {'Content-Type': 'application/json'}
            req = urllib.request.Request(url, data=data, headers=headers, method=method)
        else:
            req = urllib.request.Request(url, method=method)
        
        with urllib.request.urlopen(req) as response:
            return response.status, response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8')
    except Exception as e:
        return 0, str(e)

def make_form_request(url, data):
    try:
        data = urllib.parse.urlencode(data).encode('utf-8')
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        
        with urllib.request.urlopen(req) as response:
            return response.status, response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8')
    except Exception as e:
        return 0, str(e)

def test_signup():
    print("Testing Signup...")
    payload = {
        "email": "test@example.com",
        "password": "strongpassword"
    }
    status, response = make_request(f"{BASE_URL}/signup", payload)
    
    if status == 200:
        print("Signup Successful")
        return True
    elif status == 400 and "already exists" in response:
        print("User already exists (Signup OK)")
        return True
    else:
        print(f"Signup Failed: {status} - {response}")
        return False

def test_login():
    print("Testing Login...")
    payload = {
        "username": "test@example.com",
        "password": "strongpassword"
    }
    # Login expects form data, not JSON
    status, response = make_form_request(f"{BASE_URL}/login", payload)
    
    if status == 200:
        print("Login Successful")
        token = json.loads(response)
        print(f"Token received: {token['access_token'][:10]}...")
        return True
    else:
        print(f"Login Failed: {status} - {response}")
        return False

if __name__ == "__main__":
    if test_signup() and test_login():
        print("VERIFICATION SUCCESSFUL")
    else:
        print("VERIFICATION FAILED")
        sys.exit(1)
