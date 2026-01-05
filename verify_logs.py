import urllib.request
import urllib.parse
import json
import sys
import time

BASE_URL = "http://localhost:8000/api/v1"

def make_request(url, data=None, headers=None, method='POST'):
    if headers is None:
        headers = {}
    try:
        if data:
            data = json.dumps(data).encode('utf-8')
            headers['Content-Type'] = 'application/json'
            req = urllib.request.Request(url, data=data, headers=headers, method=method)
        else:
            req = urllib.request.Request(url, headers=headers, method=method)
        
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

def test_logs_flow():
    print("Testing Logs Flow...")
    
    # 1. Login to get token
    login_payload = {
        "username": "test@example.com",
        "password": "strongpassword"
    }
    status, response = make_form_request(f"{BASE_URL}/login", login_payload)
    if status != 200:
        # Try signup if login fails
        signup_payload = {"email": "test@example.com", "password": "strongpassword"}
        make_request(f"{BASE_URL}/signup", signup_payload)
        status, response = make_form_request(f"{BASE_URL}/login", login_payload)
        
    if status != 200:
        print(f"Login failed: {status}")
        return False
        
    token_data = json.loads(response)
    token = token_data['access_token']
    auth_headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Create Project to get API Key
    project_payload = {"name": f"Log Project {int(time.time())}"}
    status, response = make_request(f"{BASE_URL}/projects/", data=project_payload, headers=auth_headers, method='POST')
    
    if status != 200:
        print(f"Failed to create project: {status} - {response}")
        return False
        
    project_data = json.loads(response)
    api_key = project_data['api_key']
    project_id = project_data['id']
    print(f"Project Created. API Key: {api_key[:10]}...")
    
    # 3. Ingest Log
    print("Ingesting Log...")
    log_payload = {
        "level": "INFO",
        "message": "User logged in",
        "service_name": "auth-service",
        "extra": {"user_id": 123}
    }
    ingest_headers = {"X-API-Key": api_key}
    status, response = make_request(f"{BASE_URL}/logs/ingest", data=log_payload, headers=ingest_headers, method='POST')
    
    if status != 200:
        print(f"Failed to ingest log: {status} - {response}")
        return False
    
    log_data = json.loads(response)
    print(f"Log Ingested. ID: {log_data['id']}")
    
    # 4. Retrieve Logs
    print("Retrieving Logs...")
    status, response = make_request(f"{BASE_URL}/logs/?project_id={project_id}", headers=auth_headers, method='GET')
    
    if status == 200:
        logs_list = json.loads(response)
        print(f"Logs retrieved: {len(logs_list)}")
        if len(logs_list) >= 1 and logs_list[0]['message'] == "User logged in":
            return True
        else:
            print("Log list empty or mismatch")
            return False
    else:
        print(f"Failed to retrieve logs: {status} - {response}")
        return False

if __name__ == "__main__":
    if test_logs_flow():
        print("VERIFICATION SUCCESSFUL")
    else:
        print("VERIFICATION FAILED")
        sys.exit(1)
