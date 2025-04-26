import requests
from bs4 import BeautifulSoup
import urllib.parse

def get_webpage_content(url):
    """
    Загружает содержимое веб-страницы.
    
    Args:
        url (str): URL страницы.
    
    Returns:
        str: HTML-содержимое страницы.
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        raise RuntimeError(f"Ошибка загрузки страницы: {e}")

def extract_text_from_html(html_content):
    """
    Извлекает текстовое содержимое из HTML.
    
    Args:
        html_content (str): HTML-код страницы.
    
    Returns:
        str: Очищенный текст.
    """
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        for element in soup(['script', 'style', 'meta', 'link', 'noscript']):
            element.decompose()
        return soup.get_text(separator='\n', strip=True)
    except Exception as e:
        raise RuntimeError(f"Ошибка извлечения текста: {e}")
