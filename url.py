import requests

response = requests.post(
    "http://127.0.0.1:8000/summarize",
    json={"video_id": "3PK2Wm7_HSI"}
)
print(response.json())