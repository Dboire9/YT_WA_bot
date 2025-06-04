# YouTube WhatsApp Summarizer API

This project provides an API with FastAPI to summarize YouTube videos in French using LLMs (via LangChain and Together AI), and lets users interact with it via WhatsApp using Twilio.

---

## Features

- **/summarize**: FastAPI endpoint to get a French summary of a YouTube video by ID.
- **/whatsapp**: WhatsApp webhook endpoint for Twilio, allowing users to request summaries by sending YouTube links or IDs via WhatsApp.

---

## Requirements

- Python 3.8+
- [Together AI API key](https://www.together.ai/)
- [Twilio account](https://www.twilio.com/) with WhatsApp Sandbox enabled

---

## Usage

### Run the FastAPI server

```bash
python3 -m uvicorn main:app --reload
```

### Expose your server to the internet (for Twilio)

```bash
ngrok http 8000
```
Copy the HTTPS URL provided by ngrok.

---

### Test the API

#### 1. Summarize endpoint in url.py


response = requests.post(
    "http://127.0.0.1:8000/summarize",
    json={"video_id": "YOUR_VIDEO_ID"}
)


#### 2. WhatsApp integration

- Set your Twilio Sandbox webhook to `https://<ngrok-url>/whatsapp`
- Send a YouTube link or video ID to your Twilio sandbox WhatsApp number.
- Receive a summary in reply!

---

## File Structure

- `main.py` — FastAPI app, summarization logic, and Twilio webhook
- `url.py` — Example client for the API

---

## Notes

- Only French transcripts are supported.
- If a manual transcript is not available, the auto-generated one is used.
- Make sure your server is accessible from the internet for Twilio to work (use ngrok or similar).

---

## License

Dorian Boiré
MIT
