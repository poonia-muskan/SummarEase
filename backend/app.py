import os
os.environ["TRANSFORMERS_NO_TF"] = "1"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from fastapi import FastAPI, File, UploadFile, Query
from fastapi.middleware.cors import CORSMiddleware
from utils.extract_text import extract_text
from utils.summarize import generate_summary
from utils.keywords import extract_keywords
from utils.translate import translate_text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/summarize")
async def summarize(
    file: UploadFile = File(...),
    words: int | None = Query(default=None),
    target_lang: str | None = Query(default=None)
):
    text = extract_text(file)

    if words == "" or words is None:
        words = None

    if not target_lang or target_lang.strip() == "" or target_lang == "Auto":
        target_lang = None

    summary, engine = generate_summary(text, words)

    if target_lang is not None:
        summary = translate_text(summary, target_lang)
        engine = engine + " + Translation"

    return {"summary": summary, "engine": engine or "Auto"}

@app.post("/keywords")
async def keywords(file: UploadFile = File(...), num: int = Query(default=10)):
    text = extract_text(file)
    kw = extract_keywords(text, num)
    return {"keywords": kw}
