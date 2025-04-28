from googletrans import Translator

def detect(text):
    translator = Translator()
    result = translator.detect(text)
    return result.lang