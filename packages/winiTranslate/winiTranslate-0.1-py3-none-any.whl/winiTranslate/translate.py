from googletrans import Translator

def translate(text, target_language='en'):
    translator = Translator()
    result = translator.translate(text, dest=target_language)
    return result.text