from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mangum import Mangum
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os

# Load local .env
load_dotenv()

app = FastAPI(title="Intelligent API", version="1.0")

class InputText(BaseModel):
    text: str
    target_lang: str = "French"

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/process")
def process_text(payload: InputText):
    try:
        llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))

        # Step 1: Summarization
        summarize_prompt = PromptTemplate(
            input_variables=["text"],
            template="Summarize the following text in 2-3 concise sentences:\n\n{text}"
        )
        summary = (summarize_prompt | llm).invoke({"text": payload.text})

        # Step 2: Translation
        translate_prompt = PromptTemplate(
            input_variables=["summary", "target_lang"],
            template="Translate this summary into {target_lang}. Only output the translation:\n\n{summary}"
        )
        translation = (translate_prompt | llm).invoke(
            {"summary": summary, "target_lang": payload.target_lang}
        )

        return {
            "summary": summary,
            "translation": translation
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# AWS Lambda handler
handler = Mangum(app)
