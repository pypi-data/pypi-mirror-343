from googletrans import Translator

def translate_text(text, target_lang='ru'):
    """
    Переводит текст на указанный язык.
    
    Args:
        text (str): Текст для перевода.
        target_lang (str): Целевой язык (по умолчанию 'ru').
    
    Returns:
        str: Переведенный текст.
    """
    try:
        translator = Translator()
        chunks = [text[i:i+5000] for i in range(0, len(text), 5000)]
        translated = [translator.translate(chunk, dest=target_lang).text for chunk in chunks]
        return '\n'.join(translated)
    except Exception as e:
        raise RuntimeError(f"Ошибка перевода: {e}")
