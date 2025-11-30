import yake

extractor = yake.KeywordExtractor(lan="en", n=1, top=20)

def extract_keywords(text, num=10):
    kw = extractor.extract_keywords(text)
    return [k[0] for k in kw[:num]]
