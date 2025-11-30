from googletrans import Translator

translator = Translator()

def translate_text(text, target_lang):
    if target_lang is None:
        return text
    result = translator.translate(text, dest=target_lang)
    return result.text
