Intelligent API
A FastAPI-based API that summarizes and translates text using LangChain and OpenAI.

Features
/ — Health check endpoint.
/process — Summarizes input text and translates the summary to a target language.
Setup
Clone the repository and navigate to the project folder.
Create a virtual environment (Python 3.11 recommended):

Install dependencies:

Set your OpenAI API key
Usage
Health Check
GET / 
Response:
{ "status": "ok" }
Summarize and Translate
