from transformers import pipeline
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from langdetect import detect

transformer = pipeline(
    "summarization",
    model="t5-small",
    tokenizer="t5-small"
)

def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"

def summarize_transformer(text, max_len):
    text = "summarize: " + text
    result = transformer(
        text,
        max_length=max_len,
        min_length=max_len // 2,
        do_sample=False
    )[0]["summary_text"]
    return result

def summarize_textrank(text, word_limit, lang):
    parser = PlaintextParser.from_string(text, Tokenizer(lang))
    summarizer = TextRankSummarizer()

    sentences = list(parser.document.sentences)
    total = len(sentences)

    if total == 0:
        return ""

    avg_words = 18
    needed = max(1, word_limit // avg_words)
    needed = min(needed, total)

    summary_sentences = summarizer(parser.document, needed)
    summary = " ".join(str(s) for s in summary_sentences)

    while len(summary.split()) < word_limit and needed < total:
        needed += 1
        summary_sentences = summarizer(parser.document, needed)
        summary = " ".join(str(s) for s in summary_sentences)

    return summary

def generate_summary(text, word_limit=None):
    text = text.strip()

    if not text:
        return ("No readable text found.", "None")

    lang = detect_language(text)

    if word_limit:
        summary = summarize_textrank(text, word_limit, lang)
        return (summary, "TextRank")

    if len(text) <= 2000:
        summary = summarize_transformer(text, 150)
        return (summary, "Transformer")

    summary = summarize_textrank(text, 180, lang)
    return (summary, "TextRank")
