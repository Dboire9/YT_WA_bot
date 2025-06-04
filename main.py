from langchain_together import ChatTogether
from youtube_transcript_api import YouTubeTranscriptApi
import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel




load_dotenv()
api_key = os.getenv("API_KEY")
llm = ChatTogether(api_key=api_key, temperature=0.0, 
                   model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo")

app = FastAPI()

class SummarizeRequest(BaseModel):
    video_id: str

@app.post("/summarize")
def summarize(request: SummarizeRequest):
    try:
        # Try normal fetch first
        transcript = YouTubeTranscriptApi.get_transcript(request.video_id, languages=['fr'])
        text = " ".join([t['text'] for t in transcript])
    except Exception:
        # Try fetching auto-generated transcript
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(request.video_id)
            transcript = transcript_list.find_generated_transcript(['fr']).fetch()
            text = " ".join([t.text for t in transcript])
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Transcript not found: {e}")

    product_description_template = PromptTemplate(
        input_variables=["text"],
        template="""
            Read through the entire transcript carefully.
            Then, write a concise description in French based on the transcript.
            It should capture the main points and key details.
            Do not include any personal opinions or additional information.
            The description should be clear, informative, and relevant to the content of the video.
            Make sure to use proper grammar and punctuation.
            Do not use more than 1000 characters.
            Video transcript: {text}
            """
    )

    chain = LLMChain(llm=llm, prompt=product_description_template)
    summary = chain.invoke({"text": text})
    return {"summary": summary['text']}

from fastapi import Request
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse

@app.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    form = await request.form()
    incoming_msg = form.get("Body", "")
    sender = form.get("From", "")

    video_id = extract_video_id(incoming_msg)
    if not video_id:
        resp = MessagingResponse()
        resp.message("Veuillez envoyer un lien ou un ID de vidéo YouTube.")
        return PlainTextResponse(str(resp))

    try:
        summary = summarize(SummarizeRequest(video_id=video_id))
        resp = MessagingResponse()
        resp.message(summary["summary"])
    except Exception as e:
        resp = MessagingResponse()
        resp.message(f"Erreur: {e}")
    return PlainTextResponse(str(resp))

def extract_video_id(msg):
    import re
    match = re.search(r"(?:v=|youtu\.be/)([\w-]{11})", msg)
    if match:
        return match.group(1)
    elif len(msg.strip()) == 11:
        return msg.strip()
    return None