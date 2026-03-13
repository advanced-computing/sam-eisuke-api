import requests

user1 = {"username": "Alice", "age": 25, "country": "USA"}
res1 = requests.post("http://127.0.0.1:5000/users", json=user1)
print(res1.json())

user2 = {"username": "Bob", "age": 30, "country": "UK"}
res2 = requests.post("http://127.0.0.1:5000/users", json=user2)
print(res2.json())

user3 = {"username": "Lee", "age": 35, "country": "China"}
res3 = requests.post("http://127.0.0.1:5000/users", json=user3)
print(res3.json())