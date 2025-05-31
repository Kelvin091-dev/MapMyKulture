from googletrans import Translator  # Free, no API key needed

translator = Translator()

def translate_text(text, target_lang='hi'):
    try:
        translated = translator.translate(text, dest=target_lang)
        return translated.text
    except:
        return text  # Fallback to original text if translation fails
