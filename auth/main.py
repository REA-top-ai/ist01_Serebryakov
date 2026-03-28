import requests as req

def basic_authenticate_user(username, password):
    url = f"https://httpbin.org/basic-auth/{username}/{password}"
    response = req.get(url, auth=(username, password), timeout=2)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Authentication failed"}

def brear_authenticate_user(token):
    url = "https://httpbin.org/bearer"
    jwt_token = f"Bearer {token}"
    headers = {"Authorization": jwt_token}
    response = req.get(url, headers=headers, timeout=2)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Authentication failed"}
    
def digest_authenticate_user(username, password, qop="auth"):
    url = f"https://httpbin.org/digest-auth/auth/{username}/{password}"
    response = req.get(url, auth=req.auth.HTTPDigestAuth(username, password), timeout=2)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Authentication failed"}

print(basic_authenticate_user("admin", "admin"))
print(brear_authenticate_user("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IlNlcmVicnlha292VnNldm9sb2QiLCJhZG1pbiI6dHJ1ZSwiaWF0IjoxNTE2MjM5MDIyfQ.GqSUssuqfOfWeBe15UIIiKZmloeJHBnuyoB6vUMITCA"))
print(digest_authenticate_user("seva", "admin"))