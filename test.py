import requests

url = "http://localhost:8000/users/update"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiZXhwIjoxNzUyNTE2NTM3fQ.H9ry_-JNjFkLTN-7NU74CwJWNemViZw8nIyiI2AUeiU",
    "Content-Type": "application/json"
}
data = {
    "phone": "new_name",
    "email": "new@email.com"
}

response = requests.put(url, json=data, headers=headers)
print(response.status_code)
print(response)
    