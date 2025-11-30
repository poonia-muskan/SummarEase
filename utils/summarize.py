from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from langdetect import detect

def detect_language(text: str) -> str:
    try:
        return detect(text)
    except Exception:
        return "en"

def summarize_textrank(text: str, word_limit: int, lang: str) -> str:
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

def generate_summary(text: str, word_limit: int | None = None):
    text = text.strip()

    if not text:
        return ("No readable text found.", "None")

    lang = detect_language(text)

    if not word_limit:
        word_limit = 180

    summary = summarize_textrank(text, word_limit, lang)
    return (summary, "TextRank")
