import requests


headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzY5NjA4NjYxfQ.iNQxEXnNkdN3A5iBRa7c_vZTXO_3-aRtG7Ni8a8XYjU"
}


url = "http://localhost:8000/auth/refresh"

requisicao = requests.get(url, headers=headers)

print(f"Status: {requisicao.status_code}")
print(requisicao.json())